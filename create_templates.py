#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
常用数字电路模板生成器
提供快速生成常用芯片模块的功能
"""

import os
import sys
from pathlib import Path


def create_template_project(name, inputs, outputs, template_type):
    """生成模板项目"""
    from create_verilog_project import VerilogProjectGenerator
    
    # 构建信号字符串
    if inputs and outputs:
        signals = f"{' '.join(inputs)} / {' '.join(outputs)}"
    elif inputs:
        signals = f"{' '.join(inputs)} /"
    else:
        signals = f"/ {' '.join(outputs)}"
    
    # 生成基础项目
    generator = VerilogProjectGenerator(name, signals)
    generator.create_project_structure()
    
    # 生成模板特定的内容
    if template_type == "mux2to1":
        generate_mux2to1(generator)
    elif template_type == "demux1to2":
        generate_demux1to2(generator)
    elif template_type == "counter":
        generate_counter(generator)
    elif template_type == "shift_register":
        generate_shift_register(generator)
    elif template_type == "fsm":
        generate_fsm(generator)
    
    # 生成其他文件
    generator.generate_makefile()
    generator.generate_readme()
    
    print(f"✓ 模板项目 '{name}' ({template_type}) 生成完成")
    return generator.project_dir


def generate_mux2to1(gen):
    """2选1多路选择器"""
    rtl_code = """`timescale 1ns/1ps

module mux2to1 (
    input i0, i1, sel,
    output y
);
    // 2选1多路选择器
    // sel=0时，y=i0; sel=1时，y=i1
    
    assign y = sel ? i1 : i0;

endmodule
"""
    
    tb_code = """`timescale 1ns/1ps

module mux2to1_tb;
    reg i0, i1, sel;
    wire y;
    
    mux2to1 uut (.i0(i0), .i1(i1), .sel(sel), .y(y));
    
    initial begin
        $dumpfile("mux2to1.vcd");
        $dumpvars(0, mux2to1_tb);
        $monitor("@%t: i0=%b i1=%b sel=%b => y=%b", $time, i0, i1, sel, y);
        
        // 测试所有8种组合
        #10 i0=0; i1=0; sel=0;
        #10 i0=0; i1=0; sel=1;
        #10 i0=0; i1=1; sel=0;
        #10 i0=0; i1=1; sel=1;
        #10 i0=1; i1=0; sel=0;
        #10 i0=1; i1=0; sel=1;
        #10 i0=1; i1=1; sel=0;
        #10 i0=1; i1=1; sel=1;
        
        #20 $finish;
    end
endmodule
"""
    
    gen.project_dir.joinpath('rtl', 'mux2to1.v').write_text(rtl_code)
    gen.project_dir.joinpath('sim', 'mux2to1_tb.v').write_text(tb_code)
    print("  - 生成 mux2to1 模板")


def generate_demux1to2(gen):
    """1分2解多路器"""
    rtl_code = """`timescale 1ns/1ps

module demux1to2 (
    input i, sel,
    output o0, o1
);
    // 1分2解多路器
    // sel=0时，o0=i, o1=0; sel=1时，o0=0, o1=i
    
    assign o0 = sel ? 1'b0 : i;
    assign o1 = sel ? i : 1'b0;

endmodule
"""
    
    tb_code = """`timescale 1ns/1ps

module demux1to2_tb;
    reg i, sel;
    wire o0, o1;
    
    demux1to2 uut (.i(i), .sel(sel), .o0(o0), .o1(o1));
    
    initial begin
        $dumpfile("demux1to2.vcd");
        $dumpvars(0, demux1to2_tb);
        $monitor("@%t: i=%b sel=%b => o0=%b o1=%b", $time, i, sel, o0, o1);
        
        // 测试所有4种组合
        #10 i=0; sel=0;
        #10 i=1; sel=0;
        #10 i=0; sel=1;
        #10 i=1; sel=1;
        
        #20 $finish;
    end
endmodule
"""
    
    gen.project_dir.joinpath('rtl', 'demux1to2.v').write_text(rtl_code)
    gen.project_dir.joinpath('sim', 'demux1to2_tb.v').write_text(tb_code)
    print("  - 生成 demux1to2 模板")


def generate_counter(gen):
    """4位计数器"""
    rtl_code = """`timescale 1ns/1ps

module counter (
    input clk, rst, enable,
    output [3:0] count
);
    // 4位二进制计数器
    // enable=1时计数，rst=1时复位
    
    reg [3:0] count_reg;
    
    always @(posedge clk) begin
        if (rst)
            count_reg <= 4'b0000;
        else if (enable)
            count_reg <= count_reg + 1;
    end
    
    assign count = count_reg;

endmodule
"""
    
    tb_code = """`timescale 1ns/1ps

module counter_tb;
    reg clk, rst, enable;
    wire [3:0] count;
    integer i;
    
    counter uut (.clk(clk), .rst(rst), .enable(enable), .count(count));
    
    // 时钟生成
    always #5 clk = ~clk;
    
    initial begin
        clk = 0;
        $dumpfile("counter.vcd");
        $dumpvars(0, counter_tb);
        $monitor("@%t: count=%4b rst=%b enable=%b", $time, count, rst, enable);
        
        // 测试1: 复位
        #10 rst = 1; enable = 0;
        #20 rst = 0; enable = 0;
        #10 $display("Test 1: 复位完成");
        
        // 测试2: 计数（0到15）
        #10 enable = 1;
        for (i = 0; i < 16; i = i + 1) begin
            #10;
        end
        #10 $display("Test 2: 计数完成");
        
        // 测试3: 禁用计数
        #10 enable = 0;
        #20 $display("Test 3: 计数禁用");
        
        // 测试4: 重新复位
        #10 rst = 1;
        #10 rst = 0;
        #10 $display("Test 4: 重新复位完成");
        
        #20 $finish;
    end
endmodule
"""
    
    gen.project_dir.joinpath('rtl', 'counter.v').write_text(rtl_code)
    gen.project_dir.joinpath('sim', 'counter_tb.v').write_text(tb_code)
    print("  - 生成 counter 模板")


def generate_shift_register(gen):
    """4位移位寄存器"""
    rtl_code = """`timescale 1ns/1ps

module shift_register (
    input clk, rst, shift_in,
    output [3:0] data_out
);
    // 4位串入并出的移位寄存器
    
    reg [3:0] sr;
    
    always @(posedge clk) begin
        if (rst)
            sr <= 4'b0000;
        else
            sr <= {sr[2:0], shift_in};
    end
    
    assign data_out = sr;

endmodule
"""
    
    tb_code = """`timescale 1ns/1ps

module shift_register_tb;
    reg clk, rst, shift_in;
    wire [3:0] data_out;
    integer i;
    
    shift_register uut (.clk(clk), .rst(rst), .shift_in(shift_in), .data_out(data_out));
    
    // 时钟生成
    always #5 clk = ~clk;
    
    initial begin
        clk = 0;
        $dumpfile("shift_register.vcd");
        $dumpvars(0, shift_register_tb);
        $monitor("@%t: data_out=%4b shift_in=%b", $time, data_out, shift_in);
        
        // 测试1: 复位
        #10 rst = 1; shift_in = 0;
        #20 rst = 0;
        #10 $display("Test 1: 复位完成");
        
        // 测试2: 移入序列 1010
        #10 shift_in = 1;
        #10 shift_in = 0;
        #10 shift_in = 1;
        #10 shift_in = 0;
        #10 $display("Test 2: 移入序列 1010");
        
        // 测试3: 再次复位后移入 1111
        #10 rst = 1;
        #10 rst = 0;
        #10 shift_in = 1;
        #40;
        #10 $display("Test 3: 移入序列 1111");
        
        #20 $finish;
    end
endmodule
"""
    
    gen.project_dir.joinpath('rtl', 'shift_register.v').write_text(rtl_code)
    gen.project_dir.joinpath('sim', 'shift_register_tb.v').write_text(tb_code)
    print("  - 生成 shift_register 模板")


def generate_fsm(gen):
    """简单状态机（红绿灯控制器）"""
    rtl_code = """`timescale 1ns/1ps

module fsm (
    input clk, rst,
    output reg [1:0] light  // 00=红，01=绿，10=黄
);
    // 简单状态机：红->绿->黄->红
    
    localparam RED = 2'b00, GREEN = 2'b01, YELLOW = 2'b10;
    
    reg [1:0] current_state, next_state;
    
    // 次态逻辑
    always @(*) begin
        case (current_state)
            RED:    next_state = GREEN;
            GREEN:  next_state = YELLOW;
            YELLOW: next_state = RED;
            default: next_state = RED;
        endcase
    end
    
    // 状态转移
    always @(posedge clk) begin
        if (rst)
            current_state <= RED;
        else
            current_state <= next_state;
    end
    
    // 输出逻辑
    assign light = current_state;

endmodule
"""
    
    tb_code = """`timescale 1ns/1ps

module fsm_tb;
    reg clk, rst;
    wire [1:0] light;
    integer i;
    
    fsm uut (.clk(clk), .rst(rst), .light(light));
    
    // 时钟生成
    always #5 clk = ~clk;
    
    initial begin
        clk = 0;
        $dumpfile("fsm.vcd");
        $dumpvars(0, fsm_tb);
        
        // 显示状态名称
        always @(light) begin
            case (light)
                2'b00: $write("RED");
                2'b01: $write("GREEN");
                2'b10: $write("YELLOW");
                default: $write("UNKNOWN");
            endcase
        end
        
        $monitor("@%t: light=%b (%s)", $time, light, 
                 light==2'b00 ? "RED" : light==2'b01 ? "GREEN" : "YELLOW");
        
        // 测试: 状态机循环
        #10 rst = 1;
        #20 rst = 0;
        #10 $display("开始状态机循环：RED -> GREEN -> YELLOW -> RED");
        
        for (i = 0; i < 6; i = i + 1) begin
            #10;
        end
        
        #10 $finish;
    end
endmodule
"""
    
    gen.project_dir.joinpath('rtl', 'fsm.v').write_text(rtl_code)
    gen.project_dir.joinpath('sim', 'fsm_tb.v').write_text(tb_code)
    print("  - 生成 fsm 模板")


def show_templates():
    """显示所有可用的模板"""
    templates = {
        'mux2to1': '2选1多路选择器',
        'demux1to2': '1分2解多路器',
        'counter': '4位计数器',
        'shift_register': '4位移位寄存器',
        'fsm': '状态机（红绿灯控制器）'
    }
    
    print("\n可用的模板:\n")
    for key, desc in templates.items():
        print(f"  + {key:<20} - {desc}")
    print()


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='常用数字电路模板生成器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  # 生成2选1多路选择器
  python create_templates.py mux2to1
  
  # 生成计数器
  python create_templates.py counter
  
  # 列出所有可用模板
  python create_templates.py list
        '''
    )
    
    parser.add_argument('template', nargs='?', default='list',
                       help='模板类型或"list"显示所有模板')
    
    args = parser.parse_args()
    
    if args.template == 'list':
        show_templates()
        return
    
    # 模板定义
    templates = {
        'mux2to1': {
            'name': 'mux2to1',
            'inputs': ['i0', 'i1', 'sel'],
            'outputs': ['y'],
            'func': generate_mux2to1
        },
        'demux1to2': {
            'name': 'demux1to2',
            'inputs': ['i', 'sel'],
            'outputs': ['o0', 'o1'],
            'func': generate_demux1to2
        },
        'counter': {
            'name': 'counter',
            'inputs': ['clk', 'rst', 'enable'],
            'outputs': ['count[3:0]'],
            'func': generate_counter
        },
        'shift_register': {
            'name': 'shift_register',
            'inputs': ['clk', 'rst', 'shift_in'],
            'outputs': ['data_out[3:0]'],
            'func': generate_shift_register
        },
        'fsm': {
            'name': 'fsm',
            'inputs': ['clk', 'rst'],
            'outputs': ['light[1:0]'],
            'func': generate_fsm
        }
    }
    
    if args.template not in templates:
        print(f"❌ 错误：未知的模板 '{args.template}'")
        print("\n运行 'python create_templates.py list' 查看所有可用模板")
        sys.exit(1)
    
    template = templates[args.template]
    
    print(f"\n生成模板: {template['name']}")
    print(f"{'='*60}\n")
    
    create_template_project(
        template['name'],
        template['inputs'],
        template['outputs'],
        args.template
    )
    
    print(f"\n✓ 完成！")
    print(f"\n后续步骤:")
    print(f"  cd {template['name']}")
    print(f"  make")


if __name__ == '__main__':
    main()
