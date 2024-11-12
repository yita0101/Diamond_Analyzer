import os
import sys

from dotenv import load_dotenv

# 获取环境变量文件的路径
def get_env_file():
    if getattr(sys, 'frozen', False):
        # 如果是打包后的环境，从可执行文件所在目录读取
        base_path = os.path.dirname(sys.executable)
    else:
        # 如果是开发环境，从当前文件所在目录读取
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(base_path, '.env')

# 加载环境变量
load_dotenv(get_env_file())

# 配置类
class Config:
    # 默认配置
    DEFAULT_FULLNODE_URL = "http://127.0.0.1:8081"
    
    @staticmethod
    def get_fullnode_url():
        return os.getenv('FULLNODE_URL', Config.DEFAULT_FULLNODE_URL)
    
    @staticmethod
    def is_development():
        return os.getenv('FLASK_ENV', 'production') == 'development' 