#!/bin/bash
# Verilog 项目快速演示脚本

echo ""
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║        Verilog 仿真快速搭建系统 - 完整演示                         ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

# 显示脚本位置
echo "📁 当前工作目录: $(pwd)"
echo ""

# 检查必要的文件
echo "🔍 检查必要的文件..."
if [ ! -f "create_verilog_project.py" ]; then
    echo "❌ 错误: 未找到 create_verilog_project.py"
    exit 1
fi
echo "✓ 找到主脚本"

if [ ! -f "manage_verilog_projects.py" ]; then
    echo "❌ 错误: 未找到 manage_verilog_projects.py"
    exit 1
fi
echo "✓ 找到管理工具"

echo ""

# 检查 Icarus Verilog
echo "🔍 检查 Icarus Verilog 环境..."
if ! command -v iverilog &> /dev/null; then
    echo "⚠️  警告: iverilog 未安装或不在 PATH 中"
    echo "   请访问 http://iverilog.icarus.com/ 安装"
else
    IVERILOG_VERSION=$(iverilog -V 2>&1 | head -1)
    echo "✓ $IVERILOG_VERSION"
fi

if ! command -v vvp &> /dev/null; then
    echo "⚠️  警告: vvp 未安装或不在 PATH 中"
else
    echo "✓ vvp 已安装"
fi

echo ""

# 显示已有项目
echo "📊 已有项目列表:"
echo ""
python manage_verilog_projects.py list

echo ""

# 快速命令参考
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                          快速命令参考                              ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

echo "1️⃣  创建新项目:"
echo "   python create_verilog_project.py project_name \"inputs / outputs\""
echo ""

echo "   示例:"
echo "   • 与门:           and_gate \"a b / y\""
echo "   • 加法器:         adder \"a[3:0] b[3:0] cin / sum[3:0] cout\""
echo "   • 计数器:         counter \"clk rst load / count[7:0]\""
echo "   • 时钟生成器:     clk_gen \"/ clk\""
echo ""

echo "2️⃣  进行仿真 (在项目目录中):"
echo "   make              # 完整流程（编译+仿真+波形）"
echo "   make compile      # 仅编译"
echo "   make simulate     # 编译并仿真"
echo "   make view         # 查看波形"
echo "   make clean        # 清理"
echo ""

echo "3️⃣  管理项目:"
echo "   python manage_verilog_projects.py list       # 列出所有项目"
echo "   python manage_verilog_projects.py compile    # 编译全部"
echo "   python manage_verilog_projects.py simulate   # 仿真全部"
echo "   python manage_verilog_projects.py clean      # 清理全部"
echo "   python manage_verilog_projects.py report     # 生成报告"
echo "   python manage_verilog_projects.py show <name># 显示项目详情"
echo ""

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                          文档资源                                  ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

echo "📖 主要文档:"
echo "   • README_CN.md          - 中文总结和快速开始"
echo "   • VERILOG_QUICK_START.md - 详细使用指南（新手必读）"
echo "   • QUICK_REFERENCE.md     - 快速参考卡（速查）"
echo ""

echo "📁 项目内文档:"
echo "   • <project_name>/README.md - 每个项目的说明"
echo ""

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                          快速示例                                  ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

echo "已为你准备的完整示例:"
echo ""

# 显示已有项目的详情
if [ -d "and_gate" ]; then
    echo "✓ and_gate (与门)"
    echo "  - 完整的模块实现"
    echo "  - 完整的测试用例"
    echo "  - 运行: cd and_gate && make"
    echo ""
fi

if [ -d "adder_4bit" ]; then
    echo "✓ adder_4bit (4位加法器)"
    echo "  - 完整的模块实现"
    echo "  - 完整的测试用例（包括进位和随机测试）"
    echo "  - 运行: cd adder_4bit && make"
    echo ""
fi

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                       立即开始第一个项目                           ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

echo "方案 A: 创建一个简单的项目"
echo "--------"
echo "$ python create_verilog_project.py my_first_module \"a b / y\""
echo "$ cd my_first_module"
echo "$ nano rtl/my_first_module.v           # 编辑你的模块"
echo "$ nano sim/my_first_module_tb.v       # 编辑你的测试"
echo "$ make                                 # 运行仿真"
echo ""

echo "方案 B: 查看已有示例"
echo "--------"
echo "$ cd and_gate && make                 # 运行与门示例"
echo "$ cd ../adder_4bit && make            # 运行加法器示例"
echo ""

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                          需要帮助？                                ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

echo "查看详细文档:"
echo "  cat VERILOG_QUICK_START.md"
echo "  cat QUICK_REFERENCE.md"
echo "  cat README_CN.md"
echo ""

echo "查看脚本帮助:"
echo "  python create_verilog_project.py --help"
echo "  python manage_verilog_projects.py --help"
echo ""

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                       祝你学习顺利！🚀                             ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""
