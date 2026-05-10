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


