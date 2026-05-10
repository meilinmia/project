# angr 符号执行实验

## 1. 项目目的

这个实验项目用于演示如何使用 `angr` 对一个简单的 C 程序进行符号执行，并自动生成能够触发目标分支的输入。  
实验目标很明确：

- 让程序从标准输入读取字符串；
- 当输入前 6 个字符是 `secret` 时输出 `Good`；
- 否则输出 `Bad`；
- 使用 `angr + claripy` 自动求出能够进入 `Good` 分支的输入。

这个案例足够简单，适合初学者理解 `angr` 的基本流程，也适合写进课程报告。

## 2. 文件说明

- `check.c`：待分析的 C 程序。
- `solve.py`：使用 `angr` 进行符号执行并自动生成输入的脚本。
- `README.md`：实验说明、运行命令和报告写法参考。

## 3. 环境准备

### Windows + conda

建议先创建一个单独环境：

```bash
conda create -n angrlab python=3.10 -y
conda activate angrlab
pip install angr
```

检查 angr 是否安装成功：

```bash
python -c "import angr; print(angr.__version__)"
```

如果能输出版本号，例如：

```text
9.x.x
```

说明安装成功。

### Linux / WSL

```bash
python3 -m venv venv
source venv/bin/activate
pip install angr
```

检查安装：

```bash
python -c "import angr; print(angr.__version__)"
```

## 4. 编译 C 程序

### Linux / WSL

优先使用：

```bash
gcc check.c -o check -no-pie
```

如果 `-no-pie` 报错，则使用：

```bash
gcc check.c -o check
```

### Windows MinGW

```bash
gcc check.c -o check.exe
```

## 5. 手动测试程序

### Linux / WSL

运行：

```bash
./check
```

输入：

```text
aaa
```

预期输出：

```text
Input: Bad
```

再次运行：

```bash
./check
```

输入：

```text
secret
```

预期输出：

```text
Input: Good
```

### Windows

运行：

```powershell
.\check.exe
```

输入 `aaa` 应输出 `Bad`，输入 `secret` 应输出 `Good`。

## 6. 运行 angr 脚本

`solve.py` 会自动判断当前系统应加载 `./check` 还是 `./check.exe`，因此 Windows 用户不需要手动修改脚本。

### Linux / WSL

```bash
python solve.py
```

### Windows

```powershell
python solve.py
```

## 7. 预期输出

运行后通常会看到类似结果：

```text
[+] 找到了能够触发 Good 分支的输入
[+] 求解结果（原始字节）: b'secret  '
[+] 求解结果（去掉末尾空格后显示）: b'secret'
[+] 只要前 6 个字符是 secret，就可以进入 Good 分支
```

注意：

- 输出不一定每次完全一样；
- 只要前 6 个字符是 `secret` 就是正确答案；
- 后面的字符可能是空格，也可能是其他可打印字符。

## 8. 关于 unicornlib.dll warning

在 Windows 上运行 angr 时，可能看到类似 `unicornlib.dll` 加载失败的 warning。  
这通常表示 `Unicorn` 加速模块没有启用。

对于本实验来说，这个 warning 一般**不影响实验完成**，因为即使没有启用 Unicorn，加速功能缺失也不妨碍 angr 正常进行符号执行。

## 9. 完整运行步骤

第一步：检查 angr 是否安装成功

```bash
python -c "import angr; print(angr.__version__)"
```

第二步：编译 C 程序

Linux / WSL:

```bash
gcc check.c -o check -no-pie
```

如果 `-no-pie` 报错，则使用：

```bash
gcc check.c -o check
```

Windows MinGW:

```bash
gcc check.c -o check.exe
```

第三步：手动测试程序

Linux / WSL:

```bash
./check
```

Windows:

```powershell
.\check.exe
```

输入 `aaa` 应输出 `Bad`。  
输入 `secret` 应输出 `Good`。

第四步：运行 angr 脚本

Linux / WSL:

```bash
python solve.py
```

Windows:

```powershell
python solve.py
```

## 10. 如何写进课程报告

你可以把本实验写成一个“从手工测试到自动求解”的小型案例，结构建议如下：

1. 实验目的  
   使用 angr 对简单分支程序进行符号执行，并自动生成满足条件的输入。

2. 实验程序设计  
   编写一个 C 程序，从标准输入读取字符串，若前 6 个字符为 `secret`，则输出 `Good`，否则输出 `Bad`。

3. 符号执行思路  
   使用 `claripy.BVS` 创建符号化标准输入，并约束每个字节都属于可打印 ASCII 范围，再通过 `simulation_manager.explore()` 搜索输出 `Good` 的路径，同时避开输出 `Bad` 的路径。

4. 实验结果  
   angr 成功生成了满足条件的输入，例如 `secret` 或 `secret  `，说明工具能够自动构造进入目标分支的测试数据。

## 11. 可直接放进报告的文字

下面这段文字可以直接作为实验报告中的“实验过程与结果分析”部分：

```text
本实验选择 angr 作为符号执行工具，主要原因是 angr 使用方便、资料较多，并且能够直接对二进制程序进行路径探索，适合初学者学习符号执行的基本过程。与只做静态阅读代码相比，angr 可以自动分析程序中的分支条件，并求出满足条件的具体输入，这对于理解符号执行思想非常直观。

在实验中，我首先编写了一个简单的 C 程序作为分析对象。该程序从标准输入读取一个字符串，当输入的前 6 个字符为 secret 时输出 Good，否则输出 Bad。这个程序结构简单，但包含了明确的条件分支，适合用于 angr 的入门实验。

随后，我在 Python 脚本中使用 claripy 创建了符号输入。具体来说，我通过 claripy.BVS 构造了一个符号化字节串，并将其作为程序的标准输入。为了让求解结果更容易理解，我还约束了每个字节都必须属于可打印 ASCII 字符范围，这样 angr 求出的结果就可以直接作为正常字符串使用。

在路径搜索阶段，我使用了 angr 的 simulation_manager，并设置 find 条件为程序输出包含 Good，avoid 条件为程序输出包含 Bad。这样，angr 会自动搜索所有可能路径，并优先寻找能够到达目标分支的输入，同时避免进入错误分支。

实验结果表明，angr 成功生成了可以触发 Good 分支的输入。例如，求解结果可能为 secret 或者以 secret 开头的其他可打印字符串。这说明 angr 已经正确分析出程序的关键约束条件，即输入前 6 个字符必须为 secret，从而验证了符号执行在自动测试输入生成方面的有效性。
```
