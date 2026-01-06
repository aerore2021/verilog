#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verilog 项目管理工具
用于批量操作、测试和管理多个 Verilog 项目
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
import json
from datetime import datetime


class VerilogProjectManager:
    """Verilog项目管理器"""
    
    def __init__(self):
        self.projects = {}
        self.load_projects()
    
    def load_projects(self):
        """扫描当前目录下的所有 Verilog 项目"""
        current_dir = Path('.')
        
        for item in current_dir.iterdir():
            if item.is_dir() and (item / 'Makefile').exists():
                if (item / 'rtl').exists() and (item / 'sim').exists():
                    self.projects[item.name] = {
                        'path': item,
                        'has_makefile': True,
                        'verilog_files': list(item.glob('**/*.v'))
                    }
    
    def list_projects(self):
        """列出所有项目"""
        if not self.projects:
            print("没有找到任何 Verilog 项目")
            return
        
        print("\n" + "="*70)
        print(f"{'项目名':<20} {'RTL文件':<15} {'TB文件':<15} {'状态':<15}")
        print("="*70)
        
        for name, info in self.projects.items():
            rtl_files = list(info['path'].glob('rtl/*.v'))
            tb_files = list(info['path'].glob('sim/*_tb.v'))
            
            status = "✓ 完整" if rtl_files and tb_files else "⚠ 不完整"
            
            print(f"{name:<20} {len(rtl_files):<15} {len(tb_files):<15} {status:<15}")
        
        print("="*70 + "\n")
    
    def compile_all(self):
        """编译所有项目"""
        print("\n开始编译所有项目...\n")
        
        success = []
        failed = []
        
        for name, info in self.projects.items():
            print(f"编译 {name}...", end=" ")
            try:
                result = subprocess.run(
                    ['make', 'compile'],
                    cwd=info['path'],
                    capture_output=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    print("✓ 成功")
                    success.append(name)
                else:
                    print("✗ 失败")
                    failed.append(name)
                    print(f"  错误: {result.stderr.decode('utf-8', errors='ignore')}")
            
            except subprocess.TimeoutExpired:
                print("✗ 超时")
                failed.append(name)
            except Exception as e:
                print(f"✗ 异常: {e}")
                failed.append(name)
        
        print(f"\n编译完成: {len(success)} 个成功, {len(failed)} 个失败\n")
        
        return len(failed) == 0
    
    def simulate_all(self):
        """仿真所有项目"""
        print("\n开始仿真所有项目...\n")
        
        success = []
        failed = []
        
        for name, info in self.projects.items():
            print(f"仿真 {name}...", end=" ")
            try:
                result = subprocess.run(
                    ['make', 'simulate'],
                    cwd=info['path'],
                    capture_output=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    print("✓ 成功")
                    success.append(name)
                else:
                    print("✗ 失败")
                    failed.append(name)
            
            except subprocess.TimeoutExpired:
                print("✗ 超时")
                failed.append(name)
            except Exception as e:
                print(f"✗ 异常: {e}")
                failed.append(name)
        
        print(f"\n仿真完成: {len(success)} 个成功, {len(failed)} 个失败\n")
        
        return len(failed) == 0
    
    def clean_all(self):
        """清理所有项目"""
        print("\n开始清理所有项目...\n")
        
        for name, info in self.projects.items():
            print(f"清理 {name}...", end=" ")
            try:
                result = subprocess.run(
                    ['make', 'clean'],
                    cwd=info['path'],
                    capture_output=True,
                    timeout=10
                )
                
                if result.returncode == 0:
                    print("✓")
                else:
                    print("✗")
            
            except Exception as e:
                print(f"✗ ({e})")
        
        print("\n清理完成\n")
    
    def generate_report(self):
        """生成项目报告"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_projects': len(self.projects),
            'projects': {}
        }
        
        for name, info in self.projects.items():
            rtl_files = list(info['path'].glob('rtl/*.v'))
            tb_files = list(info['path'].glob('sim/*_tb.v'))
            
            # 统计代码行数
            rtl_lines = sum(len(open(f, encoding='utf-8', errors='ignore').readlines()) 
                          for f in rtl_files)
            tb_lines = sum(len(open(f, encoding='utf-8', errors='ignore').readlines()) 
                         for f in tb_files)
            
            report['projects'][name] = {
                'rtl_files': len(rtl_files),
                'tb_files': len(tb_files),
                'rtl_lines': rtl_lines,
                'tb_lines': tb_lines,
                'vcd_file': (info['path'] / f"{name}.vcd").exists()
            }
        
        # 保存报告
        report_file = Path('project_report.json')
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"✓ 报告已保存到 {report_file}\n")
        print(json.dumps(report, indent=2, ensure_ascii=False))
    
    def show_project_details(self, project_name):
        """显示项目详细信息"""
        if project_name not in self.projects:
            print(f"✗ 项目 '{project_name}' 不存在")
            return
        
        info = self.projects[project_name]
        
        print(f"\n{'='*70}")
        print(f"项目: {project_name}")
        print(f"{'='*70}\n")
        
        print(f"路径: {info['path']}\n")
        
        # RTL 文件
        rtl_files = list(info['path'].glob('rtl/*.v'))
        if rtl_files:
            print("RTL 文件:")
            for f in rtl_files:
                lines = len(open(f, encoding='utf-8', errors='ignore').readlines())
                print(f"  - {f.name} ({lines} 行)")
        
        # Testbench 文件
        tb_files = list(info['path'].glob('sim/*_tb.v'))
        if tb_files:
            print("\nTestbench 文件:")
            for f in tb_files:
                lines = len(open(f, encoding='utf-8', errors='ignore').readlines())
                print(f"  - {f.name} ({lines} 行)")
        
        # VCD 文件
        vcd_file = info['path'] / f"{project_name}.vcd"
        if vcd_file.exists():
            size_kb = vcd_file.stat().st_size / 1024
            print(f"\n波形文件: {vcd_file.name} ({size_kb:.1f} KB)")
        
        print(f"\n{'='*70}\n")


def main():
    parser = argparse.ArgumentParser(
        description='Verilog 项目管理工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  python manage_verilog_projects.py list       # 列出所有项目
  python manage_verilog_projects.py compile    # 编译所有项目
  python manage_verilog_projects.py simulate   # 仿真所有项目
  python manage_verilog_projects.py clean      # 清理所有项目
  python manage_verilog_projects.py report     # 生成项目报告
  python manage_verilog_projects.py show <name> # 显示项目详情
        '''
    )
    
    parser.add_argument('command', choices=['list', 'compile', 'simulate', 'clean', 'report', 'show'],
                       help='执行的命令')
    parser.add_argument('project_name', nargs='?', help='项目名称（仅用于 show 命令）')
    
    args = parser.parse_args()
    
    manager = VerilogProjectManager()
    
    if args.command == 'list':
        manager.list_projects()
    
    elif args.command == 'compile':
        manager.compile_all()
    
    elif args.command == 'simulate':
        manager.simulate_all()
    
    elif args.command == 'clean':
        manager.clean_all()
    
    elif args.command == 'report':
        manager.generate_report()
    
    elif args.command == 'show':
        if not args.project_name:
            print("✗ show 命令需要指定项目名称")
            sys.exit(1)
        manager.show_project_details(args.project_name)


if __name__ == '__main__':
    main()
