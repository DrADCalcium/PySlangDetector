# import os
import tkinter as tk
from tkinter import messagebox as msg
from tkinter import ttk
from tkinter.ttk import Combobox as combo
from tkinter import font as tkFont
import sv_ttk


window = tk.Tk()
window.title('PySlangDetector')

font = tkFont.Font(family='Corbel', size=10, weight='bold')

max_res = window.maxsize()
width, height = max_res

window.geometry(f'{int(width*0.4)}x{int(height*0.3)}')
window.resizable(False, False)
window.iconbitmap('')
window.attributes('-alpha', 1)

hint = tk.Label(window, text='请选择检测的平台后在输入框输入检测的投稿链接', font=font, fg = 'black')
hint.place(x=int(width*0.01), y=int(height*0.01))

list_hint = tk.Label(window, text='请选择检测的平台：', font=font, fg = 'black')
list_hint.place(x=int(width*0.01), y=int(height*0.05))

platform = tk.StringVar()
combo(window, values=('bilibili', 'xhs', 'weibo'), font=font, state='readonly').place(x=int(width*0.12), y=int(height*0.05), width=int(width*0.05))


def url_get():
    print(url.get)

url = tk.StringVar()
tk.Entry(window, show=None, font = ('Arial', 14, 'underline'), textvariable=url).place(x=int(width*0.01), y=int(height*0.1), width=int(width*0.3))





sv_ttk.set_theme("dark")
def del_window():
    q = msg.askokcancel('提示', '确定要退出吗？')
    if q:
        window.destroy()

window.protocol('WM_DELETE_WINDOW', del_window)
window.mainloop()