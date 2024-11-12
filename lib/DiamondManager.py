import requests
import csv
from datetime import datetime
from lib.DiamondAnalyser import DiamondAnalyser

class DiamondManager:
    def __init__(self, fullnode_url="http://127.0.0.1:8081"):
        self.fullnode_url = fullnode_url
        
    def get_diamond_info(self, name):
        """获取单个钻石信息"""
        url = f"{self.fullnode_url}/query/diamond?name={name}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None

    def get_address_diamonds(self, address):
        """获取地址下的所有钻石"""
        url = f"{self.fullnode_url}/query/balance?address={address}&diamonds=true"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get('ret') == 0 and data.get('list'):
                for item in data['list']:
                    diamonds_str = item.get('diamonds', '')
                    return [diamonds_str[i:i+6] for i in range(0, len(diamonds_str), 6)]
        return []

    def analyse_diamond(self, name):
        """分析单个钻石"""
        diamond_data = self.get_diamond_info(name)
        
        if not diamond_data or diamond_data.get('ret') != 0:
            print(f"无法获取钻石 {name} 的信息")
            return 0, False
        
        analyser = DiamondAnalyser(
            visual_gene=diamond_data['visual_gene'],
            name=diamond_data['name'],
            number=str(diamond_data['number'])
        )
        
        analyser.analyse()
        
        has_hacds = False
        inscriptions = diamond_data.get('inscriptions', [])
        if inscriptions:
            has_hacds = any('hacds' in insc.lower() for insc in inscriptions)
        
        return analyser.score, has_hacds

    def analyse_address_diamonds(self, address):
        """分析地址下的所有钻石"""
        results = []
        diamonds = self.get_address_diamonds(address)
        
        for diamond_name in diamonds:
            score, has_hacds = self.analyse_diamond(diamond_name)
            result = {
                "name": diamond_name,
                "score": max(1,score),
                "has_hacds": has_hacds
            }
            results.append(result)
        
        return results

    def export_to_csv(self, results, address):
        """将分析结果导出到CSV文件"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"diamond_analysis_{address}_{timestamp}.csv"
        
        headers = ['钻石名称', '分数', '包含hacds']
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                for result in results:
                    writer.writerow([
                        result['name'],
                        result['score'],
                        result['has_hacds']
                    ])
            return filename
        except Exception as e:
            print(f"导出CSV时发生错误: {str(e)}")
            return None
