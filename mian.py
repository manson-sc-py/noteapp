import tkinter as tk
from tkinter import ttk, messagebox
import os

# 全局变量，用于跟踪当前打开的文件名和内容
current_filename = None
current_content = ""

def list_files(directory):
    return os.listdir(directory)

def populate_listbox(listbox, directory, search_text=""):
    listbox.delete(0, tk.END)
    files = list_files(directory)
    for file in files:
        if search_text in file.lower():
            listbox.insert(tk.END, file)

def display_file_content(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return None

def save_file(filename, content):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
        return True
    except Exception as e:
        messagebox.showerror("保存失败", f"保存文件时出现错误：{str(e)}")
        return False

def delete_file(filename):
    try:
        os.remove(filename)
        return True
    except Exception as e:
        messagebox.showerror("删除失败", f"删除文件时出现错误：{str(e)}")
        return False

def file_selected(event):
    global current_filename, current_content
    
    # 如果当前有打开的文件且文本框内容和实际文件内容不一致，弹出提示框
    if current_filename and current_content != content_text.get('1.0', tk.END):
        response = messagebox.askquestion("未保存的更改", "当前文件有未保存的更改，是否保存？")
        if response == 'yes':
            save_success = save_file(current_filename, content_text.get('1.0', tk.END))
            if not save_success:
                return  # 如果保存失败，则不切换文件
        # 重置当前内容为文本框中的内容
        current_content = content_text.get('1.0', tk.END)

    selection = file_listbox.curselection()
    if selection:
        filename = file_listbox.get(selection[0])
        if filename.endswith('.nt'):
            current_filename = os.path.join(directory, filename)
            content_text.config(state=tk.NORMAL)
            content_text.delete('1.0', tk.END)
            content = display_file_content(current_filename)
            if content:
                content_text.insert(tk.END, content)
            current_content = content_text.get('1.0', tk.END)  # 更新当前内容
            delete_button.config(state=tk.NORMAL)  # 启用删除笔记按钮
            content_text.config(state=tk.NORMAL)   # 显示文本框
        else:
            content_text.config(state=tk.DISABLED)
            content_text.delete('1.0', tk.END)
            content_text.insert(tk.END, "文件必须是nt格式的")
            delete_button.config(state=tk.DISABLED)  # 禁用删除笔记按钮
            content_text.config(state=tk.DISABLED)   # 隐藏文本框
    else:
        content_text.config(state=tk.DISABLED)
        content_text.delete('1.0', tk.END)
        current_filename = None
        current_content = ""
        delete_button.config(state=tk.DISABLED)  # 禁用删除笔记按钮
        content_text.config(state=tk.DISABLED)   # 隐藏文本框

def save_file_handler(event):
    if event.state == 12 and event.keysym == 's':  # 12 corresponds to Control key
        if current_filename and current_filename.endswith('.nt'):
            content = content_text.get('1.0', tk.END)
            if save_file(current_filename, content):
                messagebox.showinfo("保存成功", "文件保存成功！")
                content_text.edit_modified(False)

def delete_note():
    global current_filename, current_content

    if current_filename:
        response = messagebox.askquestion("确认删除", f"是否删除笔记 '{current_filename}'？")
        if response == 'yes':
            if delete_file(current_filename):
                current_filename = None
                current_content = ""
                populate_listbox(file_listbox, directory)  # 刷新列表
                messagebox.showinfo("删除成功", f"笔记 '{current_filename}' 删除成功！")
                content_text.config(state=tk.DISABLED)   # 隐藏文本框
                delete_button.config(state=tk.DISABLED)  # 禁用删除笔记按钮

def create_note_window():
    def create_note():
        filename = entry.get().strip() + ".nt"
        file_path = os.path.join(directory, filename)
        if not os.path.exists(file_path):
            open(file_path, 'w').close()  # 创建空文件
            populate_listbox(file_listbox, directory)
            note_window.destroy()
            messagebox.showinfo("创建成功", f"笔记 '{filename}' 创建成功！")
        else:
            messagebox.showerror("创建失败", "文件已存在，请使用不同的名称")

    note_window = tk.Toplevel(root)
    note_window.title("新建笔记")
    note_window.geometry("300x100")

    frame = ttk.Frame(note_window, padding="10")
    frame.pack(fill=tk.BOTH, expand=True)

    entry = ttk.Entry(frame)
    entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

    label = ttk.Label(frame, text=".nt")
    label.pack(side=tk.LEFT)

    create_button = ttk.Button(frame, text="确定", command=create_note)
    create_button.pack(side=tk.LEFT, padx=(5, 0))

root = tk.Tk()

V = 0.3
Vb = "内测版"
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.title("笔记 - V%.1f %s" % (V, Vb))
root.iconbitmap(r"w.ico")


width = screen_width // 2
height = screen_height // 2
x = (screen_width - width) // 2
y = (screen_height - height) // 2
root.geometry(f"{width}x{height}+{x}+{y}")

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=2)
root.grid_rowconfigure(0, weight=1)

# 创建导航栏框架
nav_frame = ttk.Frame(root, width=width // 3, height=height, padding=(10, 10))
nav_frame.grid(row=0, column=0, sticky="nsew")

# 创建新建笔记按钮
create_button = ttk.Button(nav_frame, text="新建笔记", command=create_note_window)
create_button.pack(pady=(0, 10))

# 创建删除笔记按钮
delete_button = ttk.Button(nav_frame, text="删除笔记", command=delete_note, state=tk.DISABLED)
delete_button.pack(pady=(0, 10))

# 创建目录列表框
file_listbox = tk.Listbox(nav_frame)
file_listbox.pack(fill=tk.BOTH, expand=True)
file_listbox.bind('<<ListboxSelect>>', file_selected)

# 填充目录列表框
directory = "note"
populate_listbox(file_listbox, directory)

# 创建主内容框架
content_frame = ttk.Frame(root, width=width * 2 // 3, height=height, padding=(10, 10))
content_frame.grid(row=0, column=1, sticky="nsew")

# 创建内容文本框
content_text = tk.Text(content_frame, wrap=tk.WORD)
content_text.pack(fill=tk.BOTH, expand=True)
content_text.config(state=tk.DISABLED) # 默认不可编辑

# 绑定保存文件的事件
content_text.bind('<Control-s>', save_file_handler)

root.mainloop()