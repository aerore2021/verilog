

# 目录
- [系统概述](#系统概述)
- [快速开始](#快速开始)
- [核心工具](#核心工具)
- [完整工作流](#完整工作流)
- [参数说明与示例](#参数说明与示例)
- [Makefile 命令](#makefile-命令)

---

# 系统概述

这套工具可以帮助你快速搭建 Verilog 仿真环境。你无需手动创建项目结构，只需运行一个 Python 脚本即可自动生成：

- 项目文件夹结构（rtl/ sim/）
- RTL 模块文件（带清晰的填充指导）
- Testbench 文件（带自动化测试框架）
- Makefile（自动化编译和仿真）
- README 文档（项目说明）

## 你现在拥有的完整组件

| 脚本                           | 功能    | 用途          |
| ---------------------------- | ----- | ----------- |
| `create_verilog_project.py`  | 项目生成器 | 一键生成完整的项目框架 |
| `manage_verilog_projects.py` | 项目管理器 | 批量管理多个项目    |
| `create_templates.py`        | 模板生成器 | 快速生成常用电路模块  |
| `demo.sh`                    | 演示脚本  | 展示系统的使用方法   |

---

# 快速开始


```bash
# 1. 生成项目
python create_verilog_project.py my_module "a b / y"

# 2. 进入项目目录
cd my_module

# 3. 编辑 RTL 模块（rtl/my_module.v）
# 在 "组合逻辑/时序逻辑实现" 部分添加：assign y = a & b;

# 4. 编辑 Testbench（sim/my_module_tb.v）（可选）
# 在 "测试用例" 部分添加测试向量

# 5. 运行仿真
make
```

## 项目结构

```
my_module/
├── rtl/
│   └── my_module.v           # <- 编辑这个（加入你的逻辑）
├── sim/
│   └── my_module_tb.v        # <- 编辑这个（加入测试向量）
├── Makefile                  # <- 运行 make 命令
└── README.md                 # <- 项目说明
```

---

# 核心工具

## 项目生成器：`create_verilog_project.py`

**最常用！** 用于一键生成完整的项目框架。

**使用语法**：
```bash
python create_verilog_project.py <项目名> "<输入信号> / <输出信号>"
```

**参数说明**：

| 参数       | 说明                           | 示例                                  |
| -------- | ---------------------------- | ----------------------------------- |
| `<项目名>`  | Module 名称，必须是有效的 Verilog 标识符 | `and_gate`, `counter`, `adder_4bit` |
| `<输入信号>` | 逗号分隔的输入信号名列表                 | `clk rst`, `a b cin`                |
| `<输出信号>` | 逗号分隔的输出信号名列表                 | `y`, `sum cout`                     |

**注意**：用 `/` 分隔输入和输出，支持 Verilog 类型修饰符（signed, unsigned, 位宽指示符等）。

---

## 项目管理器：`manage_verilog_projects.py`

用于批量管理和操作多个项目。

**常用命令**：
```bash
python manage_verilog_projects.py list       # 列出所有项目
python manage_verilog_projects.py compile    # 编译全部
python manage_verilog_projects.py simulate   # 仿真全部
python manage_verilog_projects.py clean      # 清理全部
python manage_verilog_projects.py report     # 生成报告
python manage_verilog_projects.py show <name># 项目详情
```

---

## 模板生成器：`create_templates.py`

快速生成常用数字电路模块的模板。

**可用模板**：
```bash
python create_templates.py list              # 列出所有模板
python create_templates.py mux2to1           # 2选1多路选择器
python create_templates.py demux1to2         # 1分2解多路器
python create_templates.py counter           # 4位计数器
python create_templates.py shift_register    # 4位移位寄存器
python create_templates.py fsm               # 状态机
```

---

# 完整工作流

## Step 1: 创建项目框架

```bash
python create_verilog_project.py and_gate "a b / y"
```

**生成内容**：
```
and_gate/
├── rtl/and_gate.v
├── sim/and_gate_tb.v
├── Makefile
└── README.md
```

---

## Step 2: 编辑 RTL 模块

打开 `rtl/and_gate.v`，在以下部分添加逻辑：

```verilog
module and_gate (
    input a,
    input b,
    output y
);
    // ============================================
    // 组合逻辑/时序逻辑实现
    // ============================================
    assign y = a & b;  // <- 在这里添加你的实现

endmodule
```

---

## Step 3: 编辑 Testbench

打开 `sim/and_gate_tb.v`，在测试用例部分添加测试向量：

```verilog
initial begin
    // ...
    
    // ============================================
    // 测试用例
    // ============================================
    #10 a = 0; b = 0;
    #10 a = 0; b = 1;
    #10 a = 1; b = 0;
    #10 a = 1; b = 1;
    
    #100 $finish;
end
```

---

## Step 4: 运行仿真

```bash
cd and_gate

# 完整流程（推荐）
make

# 或分步执行
make compile    # 仅编译
make simulate   # 仅仿真
make view       # 查看波形（需要GTKWave）
make clean      # 清理生成的文件
```

---

# 参数说明与示例

## 支持的信号定义格式

脚本支持 Verilog 类型修饰符（signed, unsigned, 位宽指示符等）：

#### 示例 1：与门（最简单）
```bash
python create_verilog_project.py and_gate "a b / y"
```

#### 示例 2：加法器（带位宽）
```bash
python create_verilog_project.py adder "a[3:0] b[3:0] cin / sum[3:0] cout"
```

#### 示例 3：计数器（时序逻辑）
```bash
python create_verilog_project.py counter "clk rst load / count[7:0]"
```

#### 示例 4：时钟生成器（仅输出）
```bash
python create_verilog_project.py clk_gen "/ clk"
```

#### 示例 5：监视器（仅输入）
```bash
python create_verilog_project.py monitor "sig1 sig2 sig3 /"
```

#### 示例 6：有符号数（支持修饰符）
```bash
python create_verilog_project.py signed_adder "signed a, signed b / signed result"
```

#### 示例 7：混合修饰符
```bash
python create_verilog_project.py processor "unsigned [7:0] data, signed en / [15:0] result, valid"
```

---

# Makefile 命令

在项目目录中运行：

```bash
make              # 完整流程：编译 + 仿真 + 查看波形
make compile      # 仅编译
make simulate     # 编译并仿真
make view         # 查看波形文件（需要 GTKWave）
make clean        # 清理生成文件
make help         # 显示帮助信息
```
