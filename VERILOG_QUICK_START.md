# Verilog 快速仿真搭建指南

## 概述

这套工具可以帮助你快速搭建 Verilog 仿真环境。你无需手动创建项目结构，只需运行一个 Python 脚本即可自动生成：
- ✅ 项目文件夹结构
- ✅ RTL 模块文件（带清晰的填充指导）
- ✅ Testbench 文件（带自动化测试框架）
- ✅ Makefile（自动化编译和仿真）
- ✅ README 文档

## 环境要求

- Python 3.6+
- Icarus Verilog (iverilog)
- VVP (verilog virtual processor)
- GTKWave (波形查看工具，可选)

**验证环境：**
```bash
iverilog --version
vvp --version
gtkwave --version  # 可选
```

## 核心工具：create_verilog_project.py

这个 Python 脚本是整个工作流的核心。它可以根据你指定的信号名自动生成完整的项目框架。

### 使用语法

```bash
python create_verilog_project.py <项目名> "<输入信号> / <输出信号>"
```

### 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| `<项目名>` | Module 名称，必须是有效的 Verilog 标识符 | `and_gate`, `adder_4bit`, `counter` |
| `<输入信号>` | 空格分隔的输入信号名列表 | `clk rst`, `a b cin` |
| `<输出信号>` | 空格分隔的输出信号名列表 | `y`, `sum cout` |

**注意：** 用 `/` 分隔输入和输出，如果只有输入或只有输出，相应位置留空。

### 使用示例

#### 示例 1：创建与门（AND Gate）
```bash
python create_verilog_project.py and_gate "a b / y"
```

生成：
- Module 有 2 个输入（a, b）和 1 个输出（y）

#### 示例 2：创建加法器
```bash
python create_verilog_project.py adder_4bit "a[3:0] b[3:0] cin / sum[3:0] cout"
```

#### 示例 3：创建计数器
```bash
python create_verilog_project.py counter "clk rst load / count[7:0]"
```

#### 示例 4：创建时钟生成器（仅输出）
```bash
python create_verilog_project.py clk_gen "/ clk"
```

#### 示例 5：创建监视器（仅输入）
```bash
python create_verilog_project.py monitor "sig1 sig2 sig3 /"
```

## 工作流程

### 第一步：生成项目框架

```bash
cd /d/iverilog
python create_verilog_project.py my_module "a b / y"
```

输出：
```
============================================================
开始生成 Verilog 项目: my_module
============================================================

✓ 创建项目目录: my_module
✓ 生成模块文件: my_module\rtl\my_module.v
✓ 生成测试文件: my_module\sim\my_module_tb.v
✓ 生成Makefile: my_module\Makefile
✓ 生成README: my_module\README.md

✓ 项目生成完成！

后续步骤:
  1. cd my_module
  2. 编辑 rtl/my_module.v 添加你的逻辑
  3. 编辑 sim/my_module_tb.v 添加测试向量
  4. 运行 'make' 进行仿真
```

### 第二步：查看生成的项目结构

```
my_module/
├── rtl/
│   └── my_module.v           # RTL 实现文件（待填充）
├── sim/
│   └── my_module_tb.v        # Testbench 文件（待填充）
├── Makefile                  # 自动化脚本
└── README.md                 # 项目说明
```

### 第三步：编辑 RTL 模块

打开 `rtl/my_module.v`，你会看到：

```verilog
`timescale 1ns/1ps

module my_module (
    input a,
    input b,
    output y
);
    // ============================================
    // 输出端口声明
    // ============================================
    // output y; // 已在port list中声明

    // ============================================
    // 内部信号声明 (需要时添加)
    // ============================================
    // wire/reg 声明在此

    // ============================================
    // 组合逻辑/时序逻辑实现
    // ============================================
    // 在此添加你的逻辑实现
    // 例如: assign y = a & b;

endmodule
```

**请在 "组合逻辑/时序逻辑实现" 部分添加你的代码。**

例如，实现与门逻辑：
```verilog
assign y = a & b;
```

### 第四步：编辑 Testbench

打开 `sim/my_module_tb.v`，你会看到一个包含以下部分的测试框架：

- **信号声明**：自动生成了所有输入和输出信号
- **Module 实例化**：自动生成了 DUT（Design Under Test）实例
- **初始化块**：包含信号初始化、波形文件设置、监控器
- **测试用例**：预留了测试用例位置

**编辑要点：**
1. 修改 `$monitor` 的格式字符串（可选）
2. 添加/修改测试用例
3. 修改延迟时间（`#10` 等）

示例测试框架：
```verilog
// 测试用例1: a=0, b=0 (期望: y=0)
#10 a = 1'b0; b = 1'b0;
#10 $display("Test 1 passed: (0,0)->0");

// 测试用例2: a=0, b=1 (期望: y=0)
#10 a = 1'b0; b = 1'b1;
#10 $display("Test 2 passed: (0,1)->0");

// 更多测试用例...
```

### 第五步：运行仿真

进入项目目录，运行 make 命令：

```bash
cd my_module

# 完整流程：编译 + 仿真 + 查看波形
make

# 或者分步执行：
make compile   # 仅编译
make simulate  # 编译并仿真
make view      # 查看波形（需要GTKWave）
make clean     # 清理生成的文件
```

## 实际案例：AND 门完整演示

### 生成项目
```bash
python create_verilog_project.py and_gate "a b / y"
```

### 编辑 RTL 模块（rtl/and_gate.v）
```verilog
assign y = a & b;
```

### 编辑 Testbench（sim/and_gate_tb.v）
```verilog
// 测试用例：测试所有4种输入组合

// 测试用例1: a=0, b=0 (期望: y=0)
#10 a = 1'b0; b = 1'b0;
#10 $display("Test 1: (0,0)->%b", y);

// 测试用例2: a=0, b=1 (期望: y=0)
#10 a = 1'b0; b = 1'b1;
#10 $display("Test 2: (0,1)->%b", y);

// 测试用例3: a=1, b=0 (期望: y=0)
#10 a = 1'b1; b = 1'b0;
#10 $display("Test 3: (1,0)->%b", y);

// 测试用例4: a=1, b=1 (期望: y=1)
#10 a = 1'b1; b = 1'b1;
#10 $display("Test 4: (1,1)->%b", y);
```

### 运行仿真
```bash
cd and_gate
make
```

### 仿真输出
```
iverilog -o and_gate.vvp rtl/and_gate.v sim/and_gate_tb.v
✓ 编译完成: and_gate.vvp
vvp and_gate.vvp
VCD info: dumpfile and_gate.vcd opened for output.
@   0 ns : a=0, b=0, y=0
Test 1 passed: (0,0)->0
@  30 ns : a=0, b=1, y=0
Test 2 passed: (0,1)->0
@  50 ns : a=1, b=0, y=0
Test 3 passed: (1,0)->0
@  70 ns : a=1, b=1, y=1
Test 4 passed: (1,1)->1
✓ 仿真完成，生成波形文件: and_gate.vcd
```

✅ **所有测试通过！**

## 测试工作流优化建议

### 1. 使用 `$monitor` 自动显示信号变化

**好处：** 不需要 `$display` 就能看到信号变化

```verilog
$monitor("@%4d ns : a=%b, b=%b, y=%b", $time, a, b, y);
```

### 2. 使用 `$display` 打印调试信息

```verilog
if (y != expected) begin
    $display("ERROR: Expected %b, got %b", expected, y);
end else begin
    $display("PASS: Test case passed");
end
```

### 3. 组织测试用例

```verilog
// 分组测试用例
initial begin
    // =========== 边界值测试 ===========
    test_boundary_cases();
    
    // =========== 功能测试 ===========
    test_functionality();
    
    // =========== 时序测试 ===========
    test_timing();
    
    #100 $finish;
end
```

### 4. 使用任务（Task）组织测试代码

```verilog
task test_and_gate;
    input [1:0] test_a, test_b;
    input expected;
    begin
        a = test_a; b = test_b;
        #5;
        if (y == expected)
            $display("PASS");
        else
            $display("FAIL");
    end
endtask

initial begin
    test_and_gate(0, 0, 0);
    test_and_gate(0, 1, 0);
    test_and_gate(1, 0, 0);
    test_and_gate(1, 1, 1);
end
```

### 5. 查看波形文件

生成的 VCD 文件可以用 GTKWave 查看：
```bash
gtkwave and_gate.vcd &
```

GTKWave 中可以：
- 查看信号随时间的变化
- 放大/缩小波形
- 测量时间延迟
- 导出数据

## 常见问题

### Q1: 脚本生成的项目可以复用吗？
**A:** 可以。生成的框架设计为通用的，你可以通过修改端口和逻辑来实现不同的功能。

### Q2: 如何在 testbench 中添加时钟信号？
**A:** 可以在信号声明中手动添加时钟，或在 testbench 中生成：
```verilog
always #5 clk = ~clk;  // 10ns 周期的时钟
```

### Q3: 如何处理更复杂的输出验证？
**A:** 可以使用 Verilog 的 `$finish` 和 `$stop` 控制仿真流程，或使用 Assert：
```verilog
if (result !== expected_value) begin
    $error("Test failed!");
    $finish;
end
```

### Q4: Makefile 出错？
**A:** 确保：
1. 文件名正确（RTL 和 testbench 文件名必须与 Makefile 中定义的一致）
2. Icarus Verilog 已正确安装
3. 在项目根目录运行 `make`

### Q5: 能否添加更多 probe 点？
**A:** 可以。在 testbench 的 `$dumpvars` 中添加内部信号：
```verilog
$dumpvars(0, my_module_tb, my_module_tb.internal_signal);
```

## 进阶技巧

### 使用参数化 Testbench

```verilog
module adder_tb #(parameter WIDTH = 4);
    reg [WIDTH-1:0] a, b;
    wire [WIDTH:0] sum;
    
    adder #(.WIDTH(WIDTH)) uut (
        .a(a), .b(b), .sum(sum)
    );
```

### 集成多个模块测试

```verilog
// 在 testbench 中例化多个模块
and_gate and1 (.a(sig_a), .b(sig_b), .y(and_result));
or_gate or1 (.a(sig_a), .b(sig_b), .y(or_result));
```

### 自动化功能覆盖率

可以添加覆盖率统计（某些仿真工具支持）或手动计数：
```verilog
integer test_count = 0;
integer pass_count = 0;

always @(*) begin
    if (test_valid) begin
        test_count = test_count + 1;
        if (check_result()) pass_count = pass_count + 1;
    end
end
```

## 下一步学习

1. **学习 Verilog 语法**：掌握基本的 always, assign, generate 等结构
2. **仿真技巧**：学习 $monitor, $display, $finish 等系统函数
3. **调试技能**：使用 GTKWave 分析波形，定位问题
4. **高级特性**：参数化、层次化设计、SystemVerilog 等

## 参考资源

- [Icarus Verilog 官方](http://iverilog.icarus.com/)
- [Verilog LRM](https://en.wikipedia.org/wiki/Verilog)
- [GTKWave 文档](http://gtkwave.sourceforge.net/)

---

**祝你学习顺利！有任何问题欢迎反馈。**
