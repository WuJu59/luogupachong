import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import re
import urllib.request, urllib.error
import bs4
import os
import sys

baseUrl = "https://www.luogu.com.cn/problem/P"
savePath = ""
minn = 1000
maxn = 1049

def crawl_selected_problems():
    selected_tag = tags_var.get()
    input_label = input_label_var.get()

    if not selected_tag:
        messagebox.showerror("Error", "请选择一个标签")
        return

    save_path = filedialog.askdirectory(title="选择保存路径")
    if not save_path:
        return

    # 获取最小题号和最大题号的值
    minn = minn_var.get()
    maxn = maxn_var.get()

    if minn < 1000:
        messagebox.showerror("Error", "最小题号不能小于1000")
        return
    if maxn < minn:
        messagebox.showerror("Error", "最大题号不能小于最小题号")
        return

    progress_bar["maximum"] = maxn - minn + 1  # 设置进度条的最大值

    for i in range(minn, maxn + 1):
        progress_bar["value"] = i - minn + 1  # 更新进度条的值
        window.update()  # 更新GUI界面

        print("正在爬取P{}...".format(i), end="")
        html = getHTML(baseUrl + str(i))
        if html == "error":
            print("爬取失败，可能是不存在该题或无权查看")
        else:
            problemMD = getMD(html)
            print("爬取成功！正在保存...", end="")
            saveData(problemMD, save_path, input_label, "P" + str(i) + ".md")
            print("保存成功!")

    print("爬取完毕")
    progress_bar["value"] = 0  # 完成爬取后，将进度条归零


def getHTML(url):
    headers = {
        "user-agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 85.0.4183.121 Safari / 537.36"
    }
    request = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(request)
    html = response.read().decode('utf-8')
    if str(html).find("Exception") == -1:  # 洛谷中没找到该题目或无权查看的提示网页中会有该字样
        return html
    else:
        return "error"

def getMD(html):
    bs = bs4.BeautifulSoup(html, "html.parser")
    core = bs.select("article")[0]
    md = str(core)
    md = re.sub("<h1>", "# ", md)
    md = re.sub("<h2>", "## ", md)
    md = re.sub("<h3>", "#### ", md)
    md = re.sub("</?[a-zA-Z]+[^<>]*>", "", md)
    return md

def saveData(data, path, input_label, filename):
    # 提取 MD 文件名，用作文件夹名
    dirname = os.path.splitext(filename)[0]

    # 创建文件夹
    dirpath = os.path.join(path, dirname)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    # 完整的输出文件路径
    output_filepath = os.path.join(dirpath, filename)

    with open(output_filepath, 'w', encoding="utf-8") as f:
        f.write("标签: {}\n\n".format(input_label))  # 将用户输入的标签写入文件
        f.write(data)



# 创建主窗口
window = tk.Tk()
window.title("洛谷爬虫")
window.geometry("400x350")

# 标签选择框
tags_frame = tk.Frame(window)
tags_label = tk.Label(tags_frame, text="选择难度:")
tags_label.pack(side=tk.LEFT)

tags_var = tk.StringVar()
tag_options = ['全部','入门','普及-','普及/提高-','普及+/提高','提高+/省选-','省选/NOI-','NOI/NOI+/CTSC']  # 替换为实际的标签列表
tags_combobox = ttk.Combobox(tags_frame, textvariable=tags_var, values=tag_options)
tags_combobox.current(0)
tags_combobox.pack()
tags_frame.pack()

# 输入关键词框
input_label_frame = tk.Frame(window)
input_label_label = tk.Label(input_label_frame, text="输入关键词:")
input_label_label.pack(side=tk.LEFT)
input_label_var = tk.StringVar()
input_label_entry = tk.Entry(input_label_frame, textvariable=input_label_var)
input_label_entry.pack(side=tk.LEFT)
input_label_frame.pack()


# 输入标签框
input_label_frame = tk.Frame(window)
input_label_label = tk.Label(input_label_frame, text="输入标签:")
input_label_label.pack(side=tk.LEFT)

input_label_var = tk.StringVar()
input_label_entry = tk.Entry(input_label_frame, textvariable=input_label_var)
input_label_entry.pack(side=tk.LEFT)
input_label_frame.pack()

# 最小题号输入框
minn_frame = tk.Frame(window)
minn_label = tk.Label(minn_frame, text="最小题号:")
minn_label.pack(side=tk.LEFT)

minn_var = tk.IntVar(value= 1000)
minn_entry = tk.Entry(minn_frame, textvariable=minn_var)
minn_entry.pack(side=tk.LEFT)
minn_frame.pack()

# 最大题号输入框
maxn_frame = tk.Frame(window)
maxn_label = tk.Label(maxn_frame, text="最大题号:")
maxn_label.pack(side=tk.LEFT)

maxn_var = tk.IntVar(value= 1049)
maxn_entry = tk.Entry(maxn_frame, textvariable=maxn_var)
maxn_entry.pack(side=tk.LEFT)
maxn_frame.pack()

# 文本框
text_frame = tk.Frame(window)
text_label = tk.Label(text_frame, text="输出日志：")
text_label.pack(side=tk.LEFT)

text_box = tk.Text(text_frame, height=10, width=40)
text_box.pack(fill=tk.BOTH, expand=True)
text_frame.pack(fill=tk.BOTH, pady=10, padx=10)

# 进度条
progress_frame = tk.Frame(window)
progress_label = tk.Label(progress_frame, text="进度：")
progress_label.pack(side=tk.LEFT)

progress_bar = ttk.Progressbar(progress_frame, mode="determinate")
progress_bar.pack(fill=tk.BOTH, expand=True)
progress_frame.pack(fill=tk.BOTH, pady=10, padx=10)

# 启动爬虫按钮
start_button = tk.Button(window, text="开始爬取", command=crawl_selected_problems)
start_button.pack()

# 重定向print输出到文本框
class PrintRedirector:
    def __init__(self, text_box):
        self.text_box = text_box

    def write(self, s):
        self.text_box.insert(tk.END, s)
        self.text_box.see(tk.END)

    def flush(self):
        pass

print_redirector = PrintRedirector(text_box)
sys.stdout = print_redirector

# 运行主窗口
window.mainloop()
