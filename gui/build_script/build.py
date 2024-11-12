import PyInstaller.__main__
import os

# 确保在正确的目录下
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 运行PyInstaller
PyInstaller.__main__.run([
    'diamond_analyzer.spec',
    '--clean',  # 清理临时文件
    '--noconfirm'  # 不询问确认
]) 