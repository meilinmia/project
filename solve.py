import os
import logging
import warnings

# 关闭 Python warning
warnings.filterwarnings("ignore")

# 关闭 angr 相关日志输出
logging.getLogger("angr").setLevel(logging.CRITICAL)
logging.getLogger("cle").setLevel(logging.CRITICAL)
logging.getLogger("claripy").setLevel(logging.CRITICAL)
logging.getLogger("pyvex").setLevel(logging.CRITICAL)

import angr
import claripy


def main():
    # 自动选择 Windows 或 Linux 下的目标程序
    binary_path = "./check.exe" if os.path.exists("./check.exe") else "./check"

    print("[+] 正在分析目标程序:", binary_path)

    # 加载二进制程序
    project = angr.Project(binary_path, auto_load_libs=False)

    # 查找 check 函数符号
    check_symbol = project.loader.find_symbol("check")

    if check_symbol is None:
        print("[-] 没有找到 check 函数，请确认 check.c 中定义了 int check(char *input)")
        return

    check_addr = check_symbol.rebased_addr
    print("[+] check 函数地址:", hex(check_addr))

    # 创建 7 个符号字符
    # 程序只检查前 6 个字符，第 7 个字符无所谓
    chars = [claripy.BVS(f"c{i}", 8) for i in range(7)]

    # 在内存中放置符号字符串
    buffer_addr = 0x100000
    symbolic_input = claripy.Concat(*chars, claripy.BVV(0, 8))

    # 创建从 check 函数开始执行的状态
    state = project.factory.call_state(
        check_addr,
        buffer_addr,
        add_options={
            angr.options.ZERO_FILL_UNCONSTRAINED_MEMORY,
            angr.options.ZERO_FILL_UNCONSTRAINED_REGISTERS,
        },
    )

    # 把符号输入写入内存
    state.memory.store(buffer_addr, symbolic_input)

    # 限制字符为可打印 ASCII，避免结果是乱码
    for c in chars:
        state.solver.add(c >= 0x20)
        state.solver.add(c <= 0x7e)

    # 开始符号执行
    simgr = project.factory.simulation_manager(state)
    simgr.run()

    # 检查所有结束状态，寻找返回值为 1 的路径
    for deadended_state in simgr.deadended:
        condition = deadended_state.regs.eax == 1

        if deadended_state.solver.satisfiable(extra_constraints=[condition]):
            deadended_state.add_constraints(condition)

            solution = deadended_state.solver.eval(
                claripy.Concat(*chars),
                cast_to=bytes
            )

            print("[+] 找到满足条件的输入:", solution)
            print("[+] 有效输入前 6 个字符:", solution[:6].decode(errors="ignore"))
            return

    print("[-] 没有找到满足条件的输入")


if __name__ == "__main__":
    main()