#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verilog 快速项目生成工具
自动生成Module、Testbench、Makefile和仿真脚本
"""

import os
import sys
import argparse
from pathlib import Path


class VerilogProjectGenerator:
    """Verilog项目生成器"""
    
    def __init__(self, project_name, signals):
        """
        初始化生成器
        Args:
            project_name: 项目名称
            signals: 信号列表，格式: "input1 input2 / output1 output2"
        """
        self.project_name = project_name
        self.parse_signals(signals)
        self.project_dir = Path(project_name)
        
    def parse_signals(self, signals):
        """
        解析信号字符串，支持Verilog类型修饰符
        格式: [type] sig_name [, [type] sig_name, ...]
        例如: "signed input1, input2" 或 "[7:0] data, clk"
        """
        parts = signals.split('/')
        
        # 解析输入信号
        self.inputs = []
        if len(parts) > 0:
            self.inputs = self._parse_signal_list(parts[0].strip())
        
        # 解析输出信号
        self.outputs = []
        if len(parts) > 1:
            self.outputs = self._parse_signal_list(parts[1].strip())
    
    def _parse_signal_list(self, signal_str):
        """
        解析逗号分隔的信号列表，支持类型修饰符
        例如: "signed a, [7:0] b, c" -> ["signed a", "[7:0] b", "c"]
        """
        if not signal_str:
            return []
        
        signals = []
        # 首先按逗号分割
        tokens = signal_str.split(',')
        
        for token in tokens:
            token = token.strip()
            if token:
                # 每个token可能是: "signed name", "[7:0] name", "signed [7:0] name", 或 "name"
                sig_with_type = self._extract_signal_with_type(token)
                if sig_with_type:
                    signals.append(sig_with_type)
        
        return signals
    
    def _extract_signal_with_type(self, token_str):
        """
        从token中提取信号及其类型修饰符
        例如:
        - "signed data" -> "signed data"
        - "[7:0] data" -> "[7:0] data"  
        - "data" -> "data"
        - "signed [7:0] data" -> "signed [7:0] data"
        """
        token_str = token_str.strip()
        
        if not token_str:
            return None
        
        # 将token按空格分割成parts
        parts = token_str.split()
        
        if len(parts) == 0:
            return None
        elif len(parts) == 1:
            # 只有一个token，检查是否是有效的标识符
            if self._is_valid_identifier(parts[0]):
                return parts[0]
            return None
        
        # 多个parts的情况: 最后一个必须是有效的标识符（信号名），前面的是修饰符
        signal_name = parts[-1]
        
        if not self._is_valid_identifier(signal_name):
            return None
        
        # 验证前面的parts是否都是有效的修饰符
        type_modifiers = parts[:-1]
        valid_modifiers = {'signed', 'unsigned'}
        
        for mod in type_modifiers:
            # 检查是否是有效的修饰符或者宽度指示符 [7:0]
            if not (mod in valid_modifiers or (mod.startswith('[') and mod.endswith(']'))):
                # 如果不是已知修饰符，可能是包含宽度的，需要特殊处理
                if not self._is_width_spec(mod):
                    return None
        
        # 重新组合：类型修饰符 + 信号名
        return ' '.join(parts)
    
    def _is_width_spec(self, s):
        """检查是否是宽度指示符，如 [7:0] 或 [3]"""
        if not (s.startswith('[') and s.endswith(']')):
            return False
        # 简单检查：内部应该只有数字、冒号和空格
        inner = s[1:-1]
        return all(c.isdigit() or c in ':,[] ' for c in inner)
    
    def _is_valid_identifier(self, s):
        """检查是否是有效的Verilog标识符"""
        if not s or s[0].isdigit():
            return False
        
        # 排除已知的关键字和修饰符
        if s.startswith('[') and s.endswith(']'):
            return False  # 宽度指示符
        
        # 必须是字母开头，后面只能是字母、数字或下划线
        return all(c.isalnum() or c == '_' for c in s) and (s[0].isalpha() or s[0] == '_')
    
    def create_project_structure(self):
        """创建项目目录结构"""
        self.project_dir.mkdir(exist_ok=True)
        (self.project_dir / 'sim').mkdir(exist_ok=True)
        (self.project_dir / 'rtl').mkdir(exist_ok=True)
        print(f"✓ 创建项目目录: {self.project_dir}")
    
    def generate_module(self):
        """生成RTL模块文件"""
        module_content = self._generate_module_code()
        module_file = self.project_dir / 'rtl' / f'{self.project_name}.v'
        
        with open(module_file, 'w', encoding='utf-8') as f:
            f.write(module_content)
        
        print(f"✓ 生成模块文件: {module_file}")
        return module_file
    
    def _generate_module_code(self):
        """生成Module代码"""
        # 生成端口声明
        all_ports = self.inputs + self.outputs
        port_decl = []
        
        for i, sig in enumerate(self.inputs):
            if i < len(self.inputs) - 1 or len(self.outputs) > 0:
                port_decl.append(f"    input {sig},")
            else:
                port_decl.append(f"    input {sig}")
        
        for i, sig in enumerate(self.outputs):
            if i < len(self.outputs) - 1:
                port_decl.append(f"    output {sig},")
            else:
                port_decl.append(f"    output {sig}")
        
        ports = '\n'.join(port_decl) if port_decl else ""
        
        # 生成输出声明 - 如果信号已经在port中声明了类型，这里就不需要重复声明
        output_decl = '\n'.join([f"    // output {sig};" for sig in self.outputs]) if self.outputs else "    // 无输出端口"
        
        code = f'''`timescale 1ns/1ps

module {self.project_name} (
{ports}
);

    // ============================================
    // 内部信号声明 (需要时添加)
    // ============================================
    // wire/reg 声明在此

    // ============================================
    // 组合逻辑/时序逻辑实现
    // ============================================
    // 在此添加你的逻辑实现
    // 例如: assign output1 = input1 & input2;

endmodule
'''
        return code
    
    def generate_testbench(self):
        """生成Testbench文件"""
        tb_content = self._generate_testbench_code()
        tb_file = self.project_dir / 'sim' / f'{self.project_name}_tb.v'
        
        with open(tb_file, 'w', encoding='utf-8') as f:
            f.write(tb_content)
        
        print(f"✓ 生成测试文件: {tb_file}")
        return tb_file
    
    def _get_signal_name(self, signal_def):
        """
        从信号定义中提取信号名称
        例如: "signed data" -> "data", "[7:0] addr" -> "addr"
        """
        parts = signal_def.split()
        # 最后一个token是信号名
        return parts[-1] if parts else signal_def
    
    def _generate_testbench_code(self):
        """生成Testbench代码"""
        # 生成信号声明
        signal_decl = []
        signal_decl.extend([f"    reg {sig};" for sig in self.inputs])
        signal_decl.extend([f"    wire {sig};" for sig in self.outputs])
        signal_decl.append("    integer i;  // 循环计数器")
        
        # 生成module实例化 - 使用信号名称
        port_connections = []
        for sig in self.inputs:
            sig_name = self._get_signal_name(sig)
            port_connections.append(f"        .{sig_name}({sig_name})")
        for sig in self.outputs:
            sig_name = self._get_signal_name(sig)
            port_connections.append(f"        .{sig_name}({sig_name})")
        
        port_conn_str = ',\n'.join(port_connections)
        
        # 生成监控显示 - 使用信号名称
        input_names = [self._get_signal_name(sig) for sig in self.inputs]
        output_names = [self._get_signal_name(sig) for sig in self.outputs]
        all_names = input_names + output_names
        monitor_signals = ', '.join(all_names)
        monitor_values = ', ' + ', '.join(all_names) if all_names else ""
        
        code = f'''`timescale 1ns/1ps

module {self.project_name}_tb;
    // ============================================
    // 信号声明
    // ============================================
{chr(10).join(signal_decl)}

    // ============================================
    // Module实例化
    // ============================================
    {self.project_name} uut (
{port_conn_str}
    );

    // ============================================
    // 初始化
    // ============================================
    initial begin
        // 初始化所有输入信号
{self._generate_initialization()}
        
        // 生成波形文件用于gtkwave查看
        $dumpfile("{self.project_name}.vcd");
        $dumpvars(0, {self.project_name}_tb);
        
        // 监控器：显示信号变化
        $monitor("@%4d ns : {monitor_signals}", $time{monitor_values});
        
        // ============================================
        // 测试用例
        // ============================================
{self._generate_test_cases()}
        
        #100 $finish;  // 仿真结束
    end

endmodule
'''
        return code
    
    def _generate_initialization(self):
        """生成初始化代码"""
        init_lines = []
        for sig in self.inputs:
            sig_name = self._get_signal_name(sig)
            init_lines.append(f"        {sig_name} = 1'b0;")
        return '\n'.join(init_lines) if init_lines else "        // 初始化代码（按需添加）"
    
    def _generate_test_cases(self):
        """生成测试用例模板"""
        test_cases = []
        test_cases.append("        // 测试用例1: 基本功能测试")
        test_cases.append("        #10;  // 等待10ns")
        
        # 最多修改前2个输入信号
        for sig in self.inputs[:min(2, len(self.inputs))]:
            sig_name = self._get_signal_name(sig)
            test_cases.append(f"        {sig_name} = ~{sig_name};  // 翻转信号")
        
        test_cases.append("        #10;  // 观察输出")
        test_cases.append("")
        test_cases.append("        // 添加更多测试用例...")
        
        return '\n'.join(test_cases) if test_cases else "        // 添加测试用例"
    
    def generate_makefile(self):
        """生成Makefile"""
        makefile_content = f'''# Verilog Simulation Makefile
# Using Icarus Verilog and VVP

VERILOG_FILES = rtl/{self.project_name}.v sim/{self.project_name}_tb.v
MODULE_NAME = {self.project_name}_tb
OUTPUT_NAME = {self.project_name}

.PHONY: all compile simulate view clean

all: compile simulate view

compile:
\tiverilog -o $(OUTPUT_NAME).vvp $(VERILOG_FILES)
\t@echo "[OK] Compilation done: $(OUTPUT_NAME).vvp"

simulate: compile
\tvvp $(OUTPUT_NAME).vvp
\t@echo "[OK] Simulation done: $(OUTPUT_NAME).vcd"

view: simulate
\tgtkwave $(OUTPUT_NAME).vcd &
\t@echo "[OK] Waveform viewer opened"

clean:
\trm -f $(OUTPUT_NAME).vvp $(OUTPUT_NAME).vcd
\t@echo "[OK] Clean done"

help:
\t@echo "Available commands:"
\t@echo "  make         - Compile + Simulate + View (full flow)"
\t@echo "  make compile - Compile only"
\t@echo "  make simulate- Compile and simulate"
\t@echo "  make view    - View waveform"
\t@echo "  make clean   - Clean generated files"
'''
        makefile_file = self.project_dir / 'Makefile'
        
        with open(makefile_file, 'w', encoding='utf-8') as f:
            f.write(makefile_content)
        
        print(f"✓ 生成Makefile: {makefile_file}")
        return makefile_file
    
    def generate_readme(self):
        """生成README文档"""
        readme_content = f'''# {self.project_name} Verilog项目

## 项目结构

```
{self.project_name}/
├── rtl/
│   └── {self.project_name}.v       # RTL模块文件（待填充）
├── sim/
│   └── {self.project_name}_tb.v    # Testbench文件
├── Makefile                         # 仿真流程自动化
└── README.md                        # 本文件
```

## 模块接口

### 输入信号 ({len(self.inputs)} 个)
{self._format_signal_list(self.inputs) if self.inputs else "- 无"}

### 输出信号 ({len(self.outputs)} 个)
{self._format_signal_list(self.outputs) if self.outputs else "- 无"}

## 快速开始

### 1. 编辑模块代码
打开 `rtl/{self.project_name}.v`，在 `// 组合逻辑/时序逻辑实现` 部分填入你的逻辑

### 2. 编辑测试代码
打开 `sim/{self.project_name}_tb.v`，在 `// 测试用例` 部分添加你的测试向量

### 3. 运行仿真

**完整流程（编译+仿真+查看波形）：**
```bash
cd {self.project_name}
make
```

**仅编译：**
```bash
make compile
```

**仅仿真：**
```bash
make simulate
```

**查看波形文件：**
```bash
make view
```

**清理生成文件：**
```bash
make clean
```

## 工具版本

- Icarus Verilog (iverilog)
- VVP (verilog virtual processor)
- GTKWave (波形查看工具)

## 常见问题

### Q: 如何添加更多测试用例？
在 `sim/{self.project_name}_tb.v` 的测试用例部分添加：
```verilog
#10;                    // 延迟
input_signal = value;   // 改变输入
#10;                    // 延迟观察
```

### Q: 如何查看仿真波形？
运行 `make view` 或手动运行 `gtkwave {self.project_name}.vcd`

### Q: 编译出错怎么办？
检查：
1. 文件是否保存
2. Verilog语法是否正确
3. 输入/输出信号名称是否匹配

## 学习资源

- Verilog基础教程
- Icarus Verilog官方文档: http://iverilog.icarus.com/
- GTKWave使用指南

---
生成时间: {self.get_timestamp()}
'''
        readme_file = self.project_dir / 'README.md'
        
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"✓ 生成README: {readme_file}")
        return readme_file
    
    def _format_signal_list(self, signals):
        """格式化信号列表"""
        return '\n'.join([f"- `{sig}`" for sig in signals])
    
    def get_timestamp(self):
        """获取当前时间戳"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def generate_all(self):
        """生成所有文件"""
        print(f"\n{'='*60}")
        print(f"开始生成 Verilog 项目: {self.project_name}")
        print(f"{'='*60}\n")
        
        self.create_project_structure()
        self.generate_module()
        self.generate_testbench()
        self.generate_makefile()
        self.generate_readme()
        
        print(f"\n{'='*60}")
        print("✓ 项目生成完成！")
        print(f"{'='*60}\n")
        print(f"后续步骤:")
        print(f"  1. cd {self.project_name}")
        print(f"  2. 编辑 rtl/{self.project_name}.v 添加你的逻辑")
        print(f"  3. 编辑 sim/{self.project_name}_tb.v 添加测试向量")
        print(f"  4. 运行 'make' 进行仿真\n")


def main():
    parser = argparse.ArgumentParser(
        description='Verilog项目快速生成工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  # 创建一个有2个输入、1个输出的模块
  python create_verilog_project.py my_module "clk rst / out"
  
  # 创建只有输出的模块（如时钟生成器）
  python create_verilog_project.py clk_gen "/ clk"
  
  # 创建只有输入的模块（如监视器）
  python create_verilog_project.py monitor "sig1 sig2 sig3 /"
        '''
    )
    
    parser.add_argument('project_name', help='项目名称 (同时是Module名称)')
    parser.add_argument(
        'signals',
        help='信号定义: "input1 input2 ... / output1 output2 ..." (用 / 分隔输入和输出)',
        nargs='?',
        default='/'
    )
    
    args = parser.parse_args()
    
    # 验证项目名称
    if not args.project_name.isidentifier():
        print(f"✗ 错误: 项目名称 '{args.project_name}' 无效（必须是有效的Verilog标识符）")
        sys.exit(1)
    
    # 检查项目是否已存在
    if Path(args.project_name).exists():
        response = input(f"项目 '{args.project_name}' 已存在，是否覆盖? (y/n): ").strip().lower()
        if response != 'y':
            print("操作已取消")
            sys.exit(0)
    
    # 创建项目
    generator = VerilogProjectGenerator(args.project_name, args.signals)
    generator.generate_all()


if __name__ == '__main__':
    main()
