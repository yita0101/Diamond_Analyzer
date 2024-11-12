import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import pyperclip
from config import LANGUAGES, DEFAULT_SETTINGS
import json
import os
import csv
import sys

# Add project root to Python path
def setup_path():
    if getattr(sys, 'frozen', False):
        # If running in PyInstaller bundle
        base_path = sys._MEIPASS
    else:
        # If running in development
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Add base path to system path if not already there
    if base_path not in sys.path:
        sys.path.insert(0, base_path)

# Setup path before imports
setup_path()

from lib.DiamondManager import DiamondManager



class DiamondAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.load_settings()
        self.texts = LANGUAGES[self.current_language]
        
        self.root.title(self.texts["title"])
        self.diamond_manager = DiamondManager(self.settings.get('fullnode_url'))
        self.results = []
        
        # 创建主框架
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 创建菜单栏
        self.create_menu()
        
        # 创建输入区域
        self.create_input_area()
        
        # 筛选和统计区域
        self.create_filter_area()
        
        # 结果显示区域
        self.create_result_area()
        
        # 进度条
        self.progress_var = tk.StringVar()
        self.progress_label = ttk.Label(self.main_frame, textvariable=self.progress_var)
        self.progress_label.grid(row=4, column=0, columnspan=5)

    def load_settings(self):
        try:
            # 获取应用程序的数据目录
            if getattr(sys, 'frozen', False):
                # 如果是打包后的环境
                app_data_dir = os.path.dirname(sys.executable)
            else:
                # 如果是开发环境
                app_data_dir = os.path.dirname(os.path.abspath(__file__))
                
            self.settings_path = os.path.join(app_data_dir, 'settings.json')
            
            if os.path.exists(self.settings_path):
                with open(self.settings_path, 'r', encoding='utf-8') as f:
                    self.settings = json.load(f)
                    self.current_language = self.settings.get('language', DEFAULT_SETTINGS['language'])
                    if 'fullnode_url' not in self.settings:
                        self.settings['fullnode_url'] = DEFAULT_SETTINGS['fullnode_url']
            else:
                # 如果设置文件不存在，创建默认设置
                self.current_language = DEFAULT_SETTINGS['language']
                self.settings = DEFAULT_SETTINGS.copy()
                # 保存默认设置
                self.save_settings()
                
        except Exception as e:
            self.current_language = DEFAULT_SETTINGS['language']
            self.settings = DEFAULT_SETTINGS.copy()
            messagebox.showerror(
                "Error",
                f"Failed to load settings: {str(e)}\nUsing default settings."
            )

    def save_settings(self):
        try:
            # 获取应用程序的数据目录
            if getattr(sys, 'frozen', False):
                # 如果是打包后的环境
                app_data_dir = os.path.dirname(sys.executable)
            else:
                # 如果是开发环境
                app_data_dir = os.path.dirname(os.path.abspath(__file__))
                
            settings_path = os.path.join(app_data_dir, 'settings.json')
            
            with open(settings_path, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=4)
                
            # 同步更新 load_settings 使用的路径
            self.settings_path = settings_path
                
        except Exception as e:
            messagebox.showerror(
                self.texts['messages']['error'],
                f"{self.texts['messages']['settings_save_error']}: {str(e)}"
            )

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 设置菜单
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.texts["settings"], menu=settings_menu)
        settings_menu.add_command(label=self.texts["settings"], 
                                command=self.open_settings)

    def open_settings(self):
        SettingsWindow(self)

    def create_input_area(self):
        # 输入框架
        input_frame = ttk.LabelFrame(self.main_frame, text=self.texts["input_group"], padding="5")
        input_frame.grid(row=0, column=0, columnspan=5, sticky=(tk.W, tk.E), pady=5)
        
        # 地址输入
        address_frame = ttk.Frame(input_frame)
        address_frame.pack(fill=tk.X, pady=2)
        ttk.Label(address_frame, text=self.texts["address_label"]).pack(side=tk.LEFT)
        self.address_var = tk.StringVar()
        self.address_entry = ttk.Entry(address_frame, textvariable=self.address_var, width=50)
        self.address_entry.pack(side=tk.LEFT, padx=5)
        self.analyze_address_button = ttk.Button(address_frame, 
                                               text=self.texts["analyze_address"], 
                                               command=self.start_address_analysis)
        self.analyze_address_button.pack(side=tk.LEFT, padx=5)
        
        # 名称输入
        name_frame = ttk.Frame(input_frame)
        name_frame.pack(fill=tk.X, pady=2)
        ttk.Label(name_frame, text=self.texts["name_label"]).pack(side=tk.LEFT)
        self.names_var = tk.StringVar()
        self.names_entry = ttk.Entry(name_frame, textvariable=self.names_var, width=50)
        self.names_entry.pack(side=tk.LEFT, padx=5)
        self.analyze_names_button = ttk.Button(name_frame, 
                                             text=self.texts["analyze_names"], 
                                             command=self.start_names_analysis)
        self.analyze_names_button.pack(side=tk.LEFT, padx=5)
        
        # 导出按钮
        self.export_button = ttk.Button(input_frame, text=self.texts["export_csv"], 
                                      command=self.export_csv)
        self.export_button.pack(side=tk.RIGHT, padx=5)
        self.export_button.state(['disabled'])

    def create_filter_area(self):
        filter_frame = ttk.LabelFrame(self.main_frame, text=self.texts["filter_group"], 
                                    padding="5")
        filter_frame.grid(row=1, column=0, columnspan=5, sticky=(tk.W, tk.E), pady=5)
        
        # HACDS筛选选项
        hacds_frame = ttk.Frame(filter_frame)
        hacds_frame.pack(fill=tk.X, pady=2)
        
        self.filter_var = tk.StringVar(value="all")
        ttk.Radiobutton(hacds_frame, text=self.texts["show_all"], 
                       variable=self.filter_var, value="all", 
                       command=self.apply_filter).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(hacds_frame, text=self.texts["show_hacds"], 
                       variable=self.filter_var, value="has_hacds", 
                       command=self.apply_filter).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(hacds_frame, text=self.texts["show_no_hacds"], 
                       variable=self.filter_var, value="no_hacds", 
                       command=self.apply_filter).pack(side=tk.LEFT, padx=5)
        
        # 分数筛选
        score_frame = ttk.Frame(filter_frame)
        score_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(score_frame, text=self.texts["score_condition"]).pack(side=tk.LEFT)
        self.score_condition = ttk.Combobox(score_frame, values=['>', '>=', '=', '<=', '<'], 
                                          width=5)
        self.score_condition.set('>')
        self.score_condition.pack(side=tk.LEFT, padx=5)
        
        self.score_value = ttk.Entry(score_frame, width=10)
        self.score_value.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(score_frame, text=self.texts["apply_filter"], 
                  command=self.apply_filter).pack(side=tk.LEFT, padx=5)
        
        # 统计标签
        self.stats_label = ttk.Label(filter_frame, text="")
        self.stats_label.pack(side=tk.LEFT, padx=20)
        
        # 复制按钮
        self.copy_hacds_button = ttk.Button(filter_frame, 
                                          text=self.texts["copy_hacds"], 
                                          command=lambda: self.copy_filtered_diamonds(True))
        self.copy_hacds_button.pack(side=tk.LEFT, padx=5)
        
        self.copy_no_hacds_button = ttk.Button(filter_frame, 
                                             text=self.texts["copy_no_hacds"], 
                                             command=lambda: self.copy_filtered_diamonds(False))
        self.copy_no_hacds_button.pack(side=tk.LEFT, padx=5)

    def apply_filter(self):
        self.result_tree.delete(*self.result_tree.get_children())
        hacds_filter = self.filter_var.get()
        
        try:
            score_value = float(self.score_value.get()) if self.score_value.get() else None
        except ValueError:
            score_value = None
        
        score_condition = self.score_condition.get() if score_value is not None else None
        
        filtered_results = []
        for result in self.results:
            # HACDS筛选
            if hacds_filter == "has_hacds" and not result['has_hacds']:
                continue
            elif hacds_filter == "no_hacds" and result['has_hacds']:
                continue
                
            # 分数筛选
            if score_value is not None:
                score = float(result['score'])
                if score_condition == '>' and not score > score_value:
                    continue
                elif score_condition == '>=' and not score >= score_value:
                    continue
                elif score_condition == '=' and not score == score_value:
                    continue
                elif score_condition == '<=' and not score <= score_value:
                    continue
                elif score_condition == '<' and not score < score_value:
                    continue
            
            filtered_results.append(result)
        
        for result in filtered_results:
            yes_text = 'Yes' if self.current_language == 'English' else '是'
            no_text = 'No' if self.current_language == 'English' else '否'
            self.result_tree.insert('', 'end', values=(
                result['name'],
                result['score'],
                yes_text if result['has_hacds'] else no_text
            ))
        
        self.update_statistics(filtered_results)

    def change_language(self, language):
        self.current_language = language
        self.settings['language'] = language
        self.texts = LANGUAGES[language]  # 更新texts引用
        self.save_settings()
        
        # 更新界面文本
        self.root.title(self.texts["title"])
        
        # 更新输入区域
        self.main_frame.children['!labelframe'].configure(text=self.texts["input_group"])
        self.analyze_address_button.configure(text=self.texts["analyze_address"])
        self.analyze_names_button.configure(text=self.texts["analyze_names"])
        self.export_button.configure(text=self.texts["export_csv"])
        
        # 更新筛选区域
        self.main_frame.children['!labelframe2'].configure(text=self.texts["filter_group"])
        
        # 更新表格头部
        self.result_tree.heading('name', text=self.texts['columns']['name'])
        self.result_tree.heading('score', text=self.texts['columns']['score'])
        self.result_tree.heading('hacds', text=self.texts['columns']['hacds'])
        
        # 重新应用筛选以更新是/否的显示
        self.apply_filter()
        
        messagebox.showinfo("Info", self.texts["settings_window"]["restart_required"])

    def export_csv(self):
        if not self.results:
            messagebox.showwarning(self.texts["messages"]["warning"], 
                                 self.texts["messages"]["no_data"])
            return
            
        # 让用户选择保存位置
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"diamond_analysis_{self.address_var.get().strip() or 'custom_list'}.csv"
        )
        
        if filename:
            success = self.diamond_manager.export_to_csv(self.results, filename)
            if success:
                messagebox.showinfo(self.texts["messages"]["success"], 
                                  self.texts["messages"]["export_success"].format(filename))
            else:
                messagebox.showerror(self.texts["messages"]["error"], 
                                   self.texts["messages"]["export_error"])

    def create_result_area(self):
        # 结果显示区域
        self.result_tree = ttk.Treeview(self.main_frame, columns=('name', 'score', 'hacds'), 
                                      show='headings', height=20)
        self.result_tree.grid(row=2, column=0, columnspan=5, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.result_tree.yview)
        scrollbar.grid(row=2, column=5, sticky=(tk.N, tk.S))
        self.result_tree.configure(yscrollcommand=scrollbar.set)
        
        # 设置列标题
        self.result_tree.heading('name', text=self.texts['columns']['name'])
        self.result_tree.heading('score', text=self.texts['columns']['score'])
        self.result_tree.heading('hacds', text=self.texts['columns']['hacds'])
        
        # 设置列宽
        self.result_tree.column('name', width=150)
        self.result_tree.column('score', width=100)
        self.result_tree.column('hacds', width=100)

    def start_address_analysis(self):
        address = self.address_var.get().strip()
        if not address:
            messagebox.showerror(self.texts['messages']['error'], 
                               self.texts['messages']['no_address'])
            return
            
        self.start_analysis(self.analyze_address)

    def start_names_analysis(self):
        names = self.names_var.get().strip()
        if not names:
            messagebox.showerror(self.texts['messages']['error'], 
                               self.texts['messages']['no_name'])
            return
        self.start_analysis(lambda: self.analyze_names(names))

    def start_analysis(self, analysis_func):
        self.analyze_address_button.state(['disabled'])
        self.analyze_names_button.state(['disabled'])
        self.export_button.state(['disabled'])
        self.result_tree.delete(*self.result_tree.get_children())
        self.progress_var.set(self.texts['messages']['analysis_progress'])
        
        thread = threading.Thread(target=self.run_analysis, args=(analysis_func,))
        thread.daemon = True
        thread.start()

    def analyze_address(self):
        return self.diamond_manager.analyse_address_diamonds(self.address_var.get().strip())

    def analyze_names(self, names):
        results = []
        for name in names.split(','):
            name = name.strip()
            if name:
                score, has_hacds = self.diamond_manager.analyse_diamond(name)
                results.append({
                    "name": name,
                    "score": score,
                    "has_hacds": has_hacds
                })
        return results

    def run_analysis(self, analysis_func):
        try:
            self.results = analysis_func()
            self.root.after(0, self.update_results)
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror(
                self.texts['messages']['error'], 
                f"{self.texts['messages']['error']}: {str(e)}"
            ))
        finally:
            self.root.after(0, self.analysis_completed)

    def update_results(self):
        self.apply_filter()

    def update_statistics(self, filtered_results=None):
        results = filtered_results if filtered_results is not None else self.results
        hacds_count = sum(1 for r in results if r['has_hacds'])
        no_hacds_count = len(results) - hacds_count
        
        self.stats_label.config(text=self.texts['messages']['stats'].format(
            len(results), hacds_count, no_hacds_count
        ))

    def analysis_completed(self):
        self.analyze_address_button.state(['!disabled'])
        self.analyze_names_button.state(['!disabled'])
        self.export_button.state(['!disabled'])
        self.progress_var.set(self.texts['messages']['analysis_complete'].format(len(self.results)))
        self.update_statistics()

    def copy_filtered_diamonds(self, has_hacds):
        filtered_names = []
        for item in self.result_tree.get_children():
            values = self.result_tree.item(item)['values']
            if (values[2] == 'Yes') == has_hacds:
                filtered_names.append(values[0])
        
        if filtered_names:
            names_text = ','.join(filtered_names)
            pyperclip.copy(names_text)
            messagebox.showinfo(
                self.texts['messages']['success'],
                self.texts['messages']['copy_success'].format(len(filtered_names))
            )
        else:
            messagebox.showinfo(
                self.texts['messages']['warning'],
                self.texts['messages']['no_diamonds']
            )

    def export_csv(self):
        if not self.results:
            messagebox.showwarning(
                self.texts['messages']['warning'],
                self.texts['messages']['no_data']
            )
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"diamond_analysis_{self.address_var.get().strip() or 'custom_list'}.csv"
        )
        
        if filename:
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        self.texts['columns']['name'],
                        self.texts['columns']['score'],
                        self.texts['columns']['hacds']
                    ])
                    for result in self.results:
                        writer.writerow([
                            result['name'],
                            result['score'],
                            'Yes' if result['has_hacds'] else 'No'
                        ])
                messagebox.showinfo(
                    self.texts['messages']['success'],
                    self.texts['messages']['export_success'].format(filename)
                )
            except Exception as e:
                messagebox.showerror(
                    self.texts['messages']['error'],
                    f"{self.texts['messages']['export_error']}: {str(e)}"
                )

class SettingsWindow:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent.root)
        self.window.title(parent.texts["settings"])
        self.window.geometry("500x400")
        self.window.resizable(False, False)
        
        # 使窗口模态
        self.window.transient(parent.root)
        self.window.grab_set()
        
        # 创建设置界面
        self.create_settings_ui()
        
        # 居中显示
        self.center_window()

    def create_settings_ui(self):
        # 主框架
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 语言设置
        lang_frame = ttk.LabelFrame(main_frame, text=self.parent.texts["language"], padding="10")
        lang_frame.pack(fill=tk.X, pady=10)
        
        self.lang_var = tk.StringVar(value=self.parent.current_language)
        for lang in LANGUAGES.keys():
            radio_frame = ttk.Frame(lang_frame)
            radio_frame.pack(fill=tk.X, pady=5)
            ttk.Radiobutton(radio_frame, text=lang, variable=self.lang_var, 
                          value=lang).pack(side=tk.LEFT, padx=10)
        
        # URL设置
        url_frame = ttk.LabelFrame(main_frame, text=self.parent.texts["settings_window"]["fullnode_url"], 
                                 padding="10")
        url_frame.pack(fill=tk.X, pady=10)
        
        # URL输入框和默认按钮的框架
        url_input_frame = ttk.Frame(url_frame)
        url_input_frame.pack(fill=tk.X, pady=5)
        
        self.url_var = tk.StringVar(value=self.parent.settings.get('fullnode_url'))
        url_entry = ttk.Entry(url_input_frame, textvariable=self.url_var, width=50)
        url_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        # 默认URL按钮
        default_url_btn = ttk.Button(url_input_frame, 
                                   text=self.parent.texts["settings_window"]["default_url"],
                                   command=self.set_default_url)
        default_url_btn.pack(side=tk.LEFT)
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        # 保存按钮
        save_button = ttk.Button(button_frame, 
                               text=self.parent.texts["settings_window"]["save"], 
                               command=self.save_settings,
                               width=15)
        save_button.pack(side=tk.RIGHT, padx=10)
        
        # 取消按钮
        cancel_button = ttk.Button(button_frame, 
                                 text=self.parent.texts["settings_window"]["cancel"], 
                                 command=self.window.destroy,
                                 width=15)
        cancel_button.pack(side=tk.RIGHT, padx=10)

    def set_default_url(self):
        self.url_var.set(DEFAULT_SETTINGS['fullnode_url'])

    def save_settings(self):
        # 检查是否改变了语言
        new_language = self.lang_var.get()
        language_changed = new_language != self.parent.current_language
        
        # 检查是否改变了URL
        new_url = self.url_var.get().strip()
        url_changed = new_url != self.parent.settings.get('fullnode_url')
        
        # 保存设置
        if language_changed:
            self.parent.current_language = new_language
            self.parent.settings['language'] = new_language
            
        if url_changed and new_url:
            self.parent.settings['fullnode_url'] = new_url
            self.parent.diamond_manager = DiamondManager(new_url)
            
        # 保存到文件
        self.parent.save_settings()
        
        # 如果改变了语言，提示重启
        if language_changed:
            messagebox.showinfo("", self.parent.texts["settings_window"]["restart_required"])
        
        self.window.destroy()

    def center_window(self):
        # 获取父窗口位置和大小
        parent_x = self.parent.root.winfo_x()
        parent_y = self.parent.root.winfo_y()
        parent_width = self.parent.root.winfo_width()
        parent_height = self.parent.root.winfo_height()
        
        # 计算居中位置
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = parent_x + (parent_width - width) // 2
        y = parent_y + (parent_height - height) // 2
        
        # 设置窗口位置
        self.window.geometry(f"+{x}+{y}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DiamondAnalyzerGUI(root)
    root.mainloop()