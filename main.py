import tkinter as tk
from tkinter import scrolledtext

class SensitiveDetectionApp:

    def __init__(self, root):
        import os
        import threading
        self.root = root
        self.root.title("敏感词检测工具")
        self.root.geometry("600x500")

        # 词库内存
        self.sensitive_words = set()
        self.json_lexicons = {}

        # 可编辑文本框
        self.input_text = scrolledtext.ScrolledText(root, height=10, width=70)
        self.input_text.pack(pady=10)

        # 按钮区域
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)
        self.analyze_btn = tk.Button(btn_frame, text="分析", width=10, command=self.analyze)
        self.analyze_btn.grid(row=0, column=0, padx=5)
        self.clear_btn = tk.Button(btn_frame, text="清空", width=10, command=self.clear)
        self.clear_btn.grid(row=0, column=1, padx=5)
        self.load_btn = tk.Button(btn_frame, text="加载", width=10, command=self.load)
        self.load_btn.grid(row=0, column=2, padx=5)
        self.unload_btn = tk.Button(btn_frame, text="卸载", width=10, command=self.unload)
        self.unload_btn.grid(row=0, column=3, padx=5)

        # 不可编辑文本框
        self.output_text = scrolledtext.ScrolledText(root, height=10, width=70, state='disabled')
        self.output_text.pack(pady=10)

        # 启动时自动加载词库
        self.load()



    def analyze(self):
        content = self.input_text.get("1.0", tk.END).strip()
        if not content:
            self._set_output("请输入要检测的文本！\n")
            return
        # 检测敏感词
        hit_words = set()
        for word in self.sensitive_words:
            if word and word in content:
                hit_words.add(word)
        if hit_words:
            result = "检测到敏感词：\n" + ", ".join(sorted(hit_words))
        else:
            result = "未检测到敏感词。"
        self._set_output(result)

    def _set_output(self, msg):
        self.output_text.config(state='normal')
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, msg)
        self.output_text.config(state='disabled')

    def clear(self):
        self.input_text.delete("1.0", tk.END)
        self.output_text.config(state='normal')
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state='disabled')

    def load(self):
        import os
        import json
        self.sensitive_words.clear()
        self.json_lexicons.clear()
        # 读取 Sensitive-lexicon 下所有 json 文件
        base_dir = os.path.join(os.path.dirname(__file__), 'Sensitive-lexicon')
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                if file.endswith('.json'):
                    path = os.path.join(root, file)
                    try:
                        with open(path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            self.json_lexicons[file] = data
                    except Exception as e:
                        self._append_output(f"加载JSON失败: {file} 错误: {e}\n")
                elif file.endswith('.txt'):
                    path = os.path.join(root, file)
                    try:
                        with open(path, 'r', encoding='utf-8') as f:
                            for line in f:
                                word = line.strip()
                                if word:
                                    self.sensitive_words.add(word)
                    except Exception as e:
                        self._append_output(f"加载词库失败: {file} 错误: {e}\n")
        self._append_output(f"已加载JSON词库{len(self.json_lexicons)}个，TXT词条{len(self.sensitive_words)}条\n")

    def _append_output(self, msg):
        self.output_text.config(state='normal')
        self.output_text.insert(tk.END, msg)
        self.output_text.config(state='disabled')

    def unload(self):
        # 示例卸载逻辑
        self.output_text.config(state='normal')
        self.output_text.insert(tk.END, "已卸载词库\n")
        self.output_text.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = SensitiveDetectionApp(root)
    root.mainloop()
