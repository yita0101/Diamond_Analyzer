import PyInstaller.__main__
import os
import shutil
from pathlib import Path

def build_api():
    # 获取项目根目录的绝对路径
    root_dir = Path(__file__).parent.parent.absolute()
    
    # 创建输出目录
    if not os.path.exists('dist'):
        os.makedirs('dist')
    
    # PyInstaller打包参数
    params = [
        str(root_dir / 'api.py'),  # 主程序文件
        '--name=hacd_api',  # 输出文件名
        '--onefile',  # 打包成单个文件
        '--clean',  # 清理临时文件
        '--noconsole',  # 不显示控制台
        f'--add-data={str(root_dir / "DiamondManager.py")}:.',  # 添加依赖文件
        f'--add-data={str(root_dir / "lib/DiamondAnalyser.py")}:lib',  # 添加lib目录下的依赖
        '--hidden-import=flask',
        '--hidden-import=requests',
        '--hidden-import=gunicorn',
        '--distpath=./dist',  # 输出目录
        '--workpath=./build',  # 工作目录
        '--specpath=./build',  # spec文件目录
    ]
    
    # 执行打包
    PyInstaller.__main__.run(params)
    
    # 复制配置文件和说明文档
    shutil.copy(str(root_dir / 'api.txt'), './dist/')
    
    # 创建启动脚本
    create_start_script()
    
    print("Build completed! Output files are in the dist directory.")

def create_start_script():
    script_content = """#!/bin/bash
    
# 检查gunicorn是否已安装
if ! command -v gunicorn &> /dev/null; then
    echo "Installing gunicorn..."
    pip install gunicorn
fi

# 启动API服务
gunicorn -w 4 -b 0.0.0.0:5000 api:app
"""
    
    with open('dist/start.sh', 'w') as f:
        f.write(script_content)
    
    # 添加执行权限
    os.chmod('dist/start.sh', 0o755)

if __name__ == '__main__':
    build_api() 