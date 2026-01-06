# Verilog 仿真快速参考

## 一分钟快速开始

```bash
# 1. 生成项目
python create_verilog_project.py my_module "a b / y"

# 2. 进入项目目录
cd my_module

# 3. 编辑 rtl/my_module.v，添加你的逻辑
# 4. 编辑 sim/my_module_tb.v，添加测试用例

# 5. 运行仿真
make
```

## 脚本命令

### 创建新项目

| 示例 | 描述 |
|------|------|
| `python create_verilog_project.py and_gate "a b / y"` | 创建与门模块 |
| `python create_verilog_project.py adder "a[3:0] b[3:0] cin / sum[3:0] cout"` | 创建加法器 |
| `python create_verilog_project.py counter "clk rst / count[7:0]"` | 创建计数器 |
| `python create_verilog_project.py clk_gen "/ clk"` | 创建时钟生成器（仅输出） |
| `python create_verilog_project.py monitor "sig1 sig2 /"` | 创建监视器（仅输入） |

### 项目管理

```bash
# 列出所有项目
python manage_verilog_projects.py list

# 编译所有项目
python manage_verilog_projects.py compile

# 仿真所有项目
python manage_verilog_projects.py simulate

# 清理所有项目的生成文件
python manage_verilog_projects.py clean

# 生成项目报告
python manage_verilog_projects.py report

# 显示特定项目详情
python manage_verilog_projects.py show my_module
```

## Makefile 常用命令

在项目目录中运行：

```bash
make              # 完整流程：编译 + 仿真 + 查看波形
make compile      # 仅编译
make simulate     # 编译并仿真
make view         # 查看波形文件（需要 GTKWave）
make clean        # 清理生成文件
make help         # 显示帮助信息
```

## 文件结构

```
my_module/
├── rtl/
│   └── my_module.v       # ← 编辑这个（RTL实现）
├── sim/
│   └── my_module_tb.v    # ← 编辑这个（测试代码）
├── Makefile              # ← 运行 make 命令
└── README.md             # ← 项目说明
```

## 关键代码片段

### RTL 模块编辑位置

```verilog
module my_module (
    input a, b,
    output y
);
    // ============================================
    // 组合逻辑/时序逻辑实现
    // ============================================
    assign y = a & b;  // ← 在这里添加你的逻辑

endmodule
```

### Testbench 测试用例编辑位置

```verilog
initial begin
    // ...
    
    // ============================================
    // 测试用例
    // ============================================
    // ← 在这里添加测试向量
    
    #10 a = 0; b = 0;
    #10 a = 0; b = 1;
    #10 a = 1; b = 0;
    #10 a = 1; b = 1;
    
    #100 $finish;
end
```

## 常用 Verilog 语法速查

| 操作 | 示例 |
|------|------|
| 赋值 | `a = 1'b0;` |
| 延迟 | `#10;` （等待10个时间单位） |
| 显示信息 | `$display("y = %b", y);` |
| 监控信号 | `$monitor("@%t: y=%b", $time, y);` |
| 条件分支 | `if (a) ... else ...` |
| 循环 | `for (i=0; i<10; i++)` |
| 时钟生成 | `always #5 clk = ~clk;` |
| 终止仿真 | `$finish;` 或 `$stop;` |

## 信号位宽写法

```verilog
reg a;              // 1 位
reg [3:0] b;        // 4 位
reg [7:0] data;     // 8 位（byte）
reg [31:0] word;    // 32 位

// 赋值
a = 1'b0;          // 1 位
b = 4'hF;          // 16进制
data = 8'd255;     // 10进制
word = 32'b1010;   // 2进制
```

## 调试技巧

### 查看仿真输出
```bash
# 仅查看编译输出（不仿真）
make compile

# 运行仿真并查看输出
make simulate

# 查看已生成的波形
make view
```

### 波形文件查看（GTKWave）
```bash
gtkwave and_gate.vcd &
```

### 修改延迟时间
在 testbench 中调整 `#` 数值：
```verilog
#5        # 短延迟
#100      # 长延迟
```

## 错误排查

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| `make: command not found` | 未安装 make | 在项目目录运行，检查 Makefile 存在 |
| `iverilog: command not found` | 未安装 Icarus Verilog | 检查安装，或使用完整路径 |
| 编译失败 | Verilog 语法错误 | 检查 RTL 或 testbench 的括号、分号 |
| 无波形文件生成 | 仿真异常退出 | 检查 testbench 的 `$finish` 位置 |

## 更多资源

- 完整指南：查看 `VERILOG_QUICK_START.md`
- 官方文档：[Icarus Verilog](http://iverilog.icarus.com/)
- 学习资料：网络搜索 "Verilog教程"

---

**提示：** 把这个文件保存成书签，快速参考！
