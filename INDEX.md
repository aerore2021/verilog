# 🎯 Verilog 快速仿真系统 - 完整索引

## 📚 文档导航

### 🔴 必读文档（按推荐顺序）

1. **[README_CN.md](README_CN.md)** ⭐⭐⭐⭐⭐
   - 中文总结和快速开始
   - 包含完整的工作流演示
   - **新用户必读**
   - 阅读时间：15 分钟

2. **[VERILOG_QUICK_START.md](VERILOG_QUICK_START.md)** ⭐⭐⭐⭐
   - 详细的快速开始指南
   - 包含进阶技巧和常见问题
   - **想深入学习必读**
   - 阅读时间：30 分钟

3. **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** ⭐⭐⭐
   - 快速参考卡
   - 常用命令速查表
   - **日常使用参考**
   - 查阅时间：1-2 分钟

4. **[TOOLS_INVENTORY.md](TOOLS_INVENTORY.md)** ⭐⭐
   - 工具系统完整清单
   - 学习路径建议
   - 常见问题解答
   - 查阅时间：5-10 分钟

---

## 🛠️ 核心工具

### 一. 项目生成器 `create_verilog_project.py`

**最常用！** 用于一键生成完整的项目框架。

**快速使用：**
```bash
python create_verilog_project.py <项目名> "<输入信号> / <输出信号>"
```

**常见示例：**
```bash
python create_verilog_project.py and_gate "a b / y"
python create_verilog_project.py counter "clk rst / count[7:0]"
python create_verilog_project.py adder "a[3:0] b[3:0] cin / sum[3:0] cout"
```

**功能：**
- 自动创建项目目录结构
- 生成 RTL 模块文件（带编辑指导）
- 生成 Testbench 文件（带测试框架）
- 生成 Makefile（自动化编译仿真）
- 生成 README（项目说明）

**文档：** [VERILOG_QUICK_START.md](VERILOG_QUICK_START.md#%E4%BA%8C%E6%AD%A5%E7%BC%96%E8%BE%91-rtl-%E6%A8%A1%E5%9D%97)

---

### 二. 项目管理器 `manage_verilog_projects.py`

用于批量管理和操作多个项目。

**常用命令：**
```bash
python manage_verilog_projects.py list       # 列出所有项目
python manage_verilog_projects.py compile    # 编译全部
python manage_verilog_projects.py simulate   # 仿真全部
python manage_verilog_projects.py clean      # 清理全部
python manage_verilog_projects.py report     # 生成报告
python manage_verilog_projects.py show <name># 项目详情
```

**适用场景：**
- 管理多个项目
- 批量编译和仿真
- 生成项目统计报告

---

### 三. 模板生成器 `create_templates.py`

快速生成常用数字电路模块的模板。

**可用模板：**
```bash
python create_templates.py list              # 列出所有模板
python create_templates.py mux2to1           # 2选1多路选择器
python create_templates.py demux1to2         # 1分2解多路器
python create_templates.py counter           # 4位计数器
python create_templates.py shift_register    # 4位移位寄存器
python create_templates.py fsm               # 状态机
```

**优点：**
- 节省编码时间
- 提供最佳实践示例
- 包含完整的测试用例

---

### 四. 演示脚本 `demo.sh`

展示系统功能和使用方法。

```bash
bash demo.sh
```

**显示内容：**
- 系统环境检查
- 已有项目列表
- 快速命令参考
- 使用示例

---

## 📋 项目工作流

### 3 步完成一个项目

```bash
# 第1步：生成项目框架
python create_verilog_project.py my_module "a b / y"

# 第2步：编辑代码
cd my_module
# - 编辑 rtl/my_module.v（添加你的逻辑）
# - 编辑 sim/my_module_tb.v（添加测试向量）

# 第3步：运行仿真
make
```

### 完整的 Makefile 命令

在项目目录中运行：

```bash
make              # 完整流程（编译+仿真+查看波形）
make compile      # 仅编译
make simulate     # 仅仿真
make view         # 查看波形文件
make clean        # 清理生成的文件
make help         # 显示帮助
```

---

## 🎓 学习建议

### 初学者（第1周）
- [ ] 阅读 [README_CN.md](README_CN.md)
- [ ] 运行 `bash demo.sh` 了解系统
- [ ] 查看示例项目 `and_gate`
- [ ] 创建第一个简单项目
- [ ] 修改项目的 RTL 和 testbench

**预期成果**：掌握基本工作流

### 进阶（第2-3周）
- [ ] 学习 [VERILOG_QUICK_START.md](VERILOG_QUICK_START.md)
- [ ] 运行示例项目 `adder_4bit`
- [ ] 使用 `create_templates.py` 生成模板
- [ ] 创建 5-10 个不同类型的项目
- [ ] 学习时序逻辑和状态机

**预期成果**：能独立设计简单电路

### 高级（第4周+）
- [ ] 学习参数化设计
- [ ] 创建多模块项目
- [ ] 学习 SystemVerilog（可选）
- [ ] 深入学习验证技术

**预期成果**：能设计中等复杂度模块

---

## 📊 示例项目

### 1. AND 门 (`and_gate`)

**位置**：`/d/iverilog/and_gate/`

**内容**：
- 简单的 2 输入 AND 门
- 4 个测试用例
- 完整的仿真演示

**查看**：
```bash
cd and_gate
cat rtl/and_gate.v      # 查看 RTL 实现
cat sim/and_gate_tb.v   # 查看测试代码
make                    # 运行仿真
```

### 2. 4 位加法器 (`adder_4bit`)

**位置**：`/d/iverilog/adder_4bit/`

**内容**：
- 4 位二进制加法器
- 进位处理
- 随机测试用例

**查看**：
```bash
cd adder_4bit
cat rtl/adder_4bit.v      # 查看 RTL 实现
cat sim/adder_4bit_tb.v   # 查看测试代码
make                      # 运行仿真
```

---

## 🔍 快速查找

### "我想..."

| 需求 | 解决方案 | 文件 |
|------|---------|------|
| 创建一个新项目 | `python create_verilog_project.py name "inputs / outputs"` | [QUICK_REFERENCE.md](QUICK_REFERENCE.md) |
| 查看所有命令 | `bash demo.sh` | [QUICK_REFERENCE.md](QUICK_REFERENCE.md) |
| 快速生成计数器 | `python create_templates.py counter` | [TOOLS_INVENTORY.md](TOOLS_INVENTORY.md) |
| 批量编译项目 | `python manage_verilog_projects.py compile` | [TOOLS_INVENTORY.md](TOOLS_INVENTORY.md) |
| 学习 Verilog | 阅读 [VERILOG_QUICK_START.md](VERILOG_QUICK_START.md) | [VERILOG_QUICK_START.md](VERILOG_QUICK_START.md) |
| 查看波形文件 | `make view` （或 `gtkwave project.vcd`） | [QUICK_REFERENCE.md](QUICK_REFERENCE.md) |
| 了解系统架构 | 阅读 [README_CN.md](README_CN.md) | [README_CN.md](README_CN.md) |
| 获取帮助 | `python script.py --help` | [TOOLS_INVENTORY.md](TOOLS_INVENTORY.md) |

---

## 💡 常见问题速查

### 安装和环境
- **Q：需要安装什么？**  
  A：[VERILOG_QUICK_START.md#环境要求](VERILOG_QUICK_START.md#环境要求)

- **Q：如何检查环境？**  
  A：`bash demo.sh` 会自动检查

### 创建项目
- **Q：如何创建项目？**  
  A：[QUICK_REFERENCE.md#脚本命令](QUICK_REFERENCE.md#脚本命令)

- **Q：支持哪些信号格式？**  
  A：[VERILOG_QUICK_START.md#参数说明](VERILOG_QUICK_START.md#参数说明)

### 编辑和测试
- **Q：编辑哪些文件？**  
  A：[README_CN.md#工作流程](README_CN.md#工作流程)

- **Q：如何添加测试？**  
  A：[VERILOG_QUICK_START.md#第四步编辑-testbench](VERILOG_QUICK_START.md#第四步编辑-testbench)

### 运行仿真
- **Q：如何运行仿真？**  
  A：[QUICK_REFERENCE.md#makefile-常用命令](QUICK_REFERENCE.md#makefile-常用命令)

- **Q：波形文件在哪里？**  
  A：项目根目录中的 `.vcd` 文件

### 高级功能
- **Q：如何批量操作项目？**  
  A：[TOOLS_INVENTORY.md#项目管理](TOOLS_INVENTORY.md#项目管理)

- **Q：如何快速生成模板？**  
  A：[TOOLS_INVENTORY.md#模板生成](TOOLS_INVENTORY.md#模板生成)

---

## 📁 文件目录一览

```
/d/iverilog/
│
├─ 脚本工具 (核心)
│  ├── create_verilog_project.py    ← 最常用！创建项目
│  ├── manage_verilog_projects.py   ← 管理多个项目
│  ├── create_templates.py          ← 生成电路模板
│  └── demo.sh                      ← 运行演示
│
├─ 文档 (必读)
│  ├── README_CN.md                 ← ⭐ 从这里开始
│  ├── VERILOG_QUICK_START.md       ← ⭐ 详细指南
│  ├── QUICK_REFERENCE.md           ← ⭐ 速查表
│  ├── TOOLS_INVENTORY.md           ← 系统清单
│  └── INDEX.md                     ← 本文件
│
├─ 示例项目 (学习)
│  ├── and_gate/                    ← 简单示例
│  │   ├── rtl/and_gate.v
│  │   ├── sim/and_gate_tb.v
│  │   └── Makefile
│  │
│  └── adder_4bit/                  ← 中等示例
│      ├── rtl/adder_4bit.v
│      ├── sim/adder_4bit_tb.v
│      └── Makefile
│
└─ [你的项目]/                      ← 你创建的项目
    ├── rtl/
    ├── sim/
    ├── Makefile
    └── README.md
```

---

## 🎯 30 秒快速开始

```bash
# 1. 生成项目
python create_verilog_project.py my_and "a b / y"

# 2. 进入项目
cd my_and

# 3. 编辑 RTL（vim/nano/vscode 任选）
# 打开 rtl/my_and.v，在注释位置添加：
# assign y = a & b;

# 4. 编辑测试（可选）
# 打开 sim/my_and_tb.v，测试框架已生成

# 5. 运行仿真
make

# ✅ 完成！
```

---

## 🌟 系统特色

✅ **一键生成**：项目框架秒速生成  
✅ **完全自动**：无需手动配置  
✅ **开箱即用**：生成后直接可用  
✅ **中文友好**：完整的中文文档  
✅ **示例丰富**：多个完整示例  
✅ **易于扩展**：支持自定义模板  

---

## 🚀 立即开始

### 方案 A：第一次使用（推荐）

1. **阅读** `README_CN.md`（15分钟）
2. **运行** `bash demo.sh`（查看指南）
3. **创建** 第一个简单项目
4. **参考** `QUICK_REFERENCE.md`（日常查阅）

### 方案 B：急着开始

```bash
python create_verilog_project.py hello_world "a b / y"
cd hello_world
# 编辑 rtl/hello_world.v：assign y = a & b;
make
```

### 方案 C：查看示例

```bash
cd and_gate && make
cd ../adder_4bit && make
```

---

## 📞 获取帮助

| 需要 | 查看 |
|------|------|
| 中文入门 | [README_CN.md](README_CN.md) |
| 详细指南 | [VERILOG_QUICK_START.md](VERILOG_QUICK_START.md) |
| 快速查阅 | [QUICK_REFERENCE.md](QUICK_REFERENCE.md) |
| 系统信息 | [TOOLS_INVENTORY.md](TOOLS_INVENTORY.md) |
| 脚本帮助 | `python script.py --help` |
| 系统演示 | `bash demo.sh` |

---

## ✨ 你现在可以...

✅ 一键创建完整的 Verilog 项目  
✅ 快速编辑和测试代码  
✅ 自动编译和仿真  
✅ 生成波形文件进行调试  
✅ 批量管理多个项目  
✅ 使用模板快速开发  
✅ 完全专注于设计，无需配置环节  

---

## 🎉 祝你学习顺利！

**推荐阅读顺序：**
1. 本文件（2 分钟）
2. [README_CN.md](README_CN.md)（15 分钟）
3. [VERILOG_QUICK_START.md](VERILOG_QUICK_START.md)（30 分钟）
4. 创建第一个项目（5 分钟）
5. [QUICK_REFERENCE.md](QUICK_REFERENCE.md)（收藏以备日常查阅）

**总时间**：约 50 分钟掌握整个系统

---

**开始你的第一个项目吧！** 🚀

```bash
python create_verilog_project.py hello_world "a b / y"
cd hello_world && make
```

---

*生成时间：2026-01-06*  
*版本：1.0*  
*祝你设计愉快！* ✨
