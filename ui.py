from tkinter import *
from tkinter.ttk import *

class WinGUI(Tk):
    def __init__(self):
        super().__init__()
        self.__win()
        self.tk_label_frame_url_frame = self.__tk_label_frame_url_frame(self)
        self.tk_label_url_hint = self.__tk_label_url_hint( self.tk_label_frame_url_frame) 
        self.tk_label_platform_select_hint = self.__tk_label_platform_select_hint( self.tk_label_frame_url_frame) 
        self.tk_select_box_platform = self.__tk_select_box_platform( self.tk_label_frame_url_frame) 
        self.tk_input_url = self.__tk_input_url( self.tk_label_frame_url_frame) 
        self.tk_button_start = self.__tk_button_start( self.tk_label_frame_url_frame) 
        self.tk_label_frame_func_frame = self.__tk_label_frame_func_frame(self)
        self.tk_check_button_show_result_checkbox = self.__tk_check_button_show_result_checkbox( self.tk_label_frame_func_frame) 
        self.tk_button_init_voca = self.__tk_button_init_voca( self.tk_label_frame_func_frame) 
        self.tk_button_login_bili = self.__tk_button_login_bili( self.tk_label_frame_func_frame) 
        self.tk_button_login_xhs = self.__tk_button_login_xhs( self.tk_label_frame_func_frame) 
        self.tk_button_login_wb = self.__tk_button_login_wb( self.tk_label_frame_func_frame) 
        self.tk_label_func_hint = self.__tk_label_func_hint( self.tk_label_frame_func_frame) 
        self.tk_label_frame_log_frame = self.__tk_label_frame_log_frame(self)

    def __win(self):
        self.title("PySlangDetector")
        # 设置窗口大小、居中
        width = 800
        height = 370
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)
        
        self.resizable(width=False, height=False)
        
    def scrollbar_autohide(self,vbar, hbar, widget):
        """自动隐藏滚动条"""
        def show():
            if vbar: vbar.lift(widget)
            if hbar: hbar.lift(widget)
        def hide():
            if vbar: vbar.lower(widget)
            if hbar: hbar.lower(widget)
        hide()
        widget.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Leave>", lambda e: hide())
        if hbar: hbar.bind("<Enter>", lambda e: show())
        if hbar: hbar.bind("<Leave>", lambda e: hide())
        widget.bind("<Leave>", lambda e: hide())
    
    def v_scrollbar(self,vbar, widget, x, y, w, h, pw, ph):
        widget.configure(yscrollcommand=vbar.set)
        vbar.config(command=widget.yview)
        vbar.place(relx=(w + x) / pw, rely=y / ph, relheight=h / ph, anchor='ne')
    def h_scrollbar(self,hbar, widget, x, y, w, h, pw, ph):
        widget.configure(xscrollcommand=hbar.set)
        hbar.config(command=widget.xview)
        hbar.place(relx=x / pw, rely=(y + h) / ph, relwidth=w / pw, anchor='sw')
    def create_bar(self,master, widget,is_vbar,is_hbar, x, y, w, h, pw, ph):
        vbar, hbar = None, None
        if is_vbar:
            vbar = Scrollbar(master)
            self.v_scrollbar(vbar, widget, x, y, w, h, pw, ph)
        if is_hbar:
            hbar = Scrollbar(master, orient="horizontal")
            self.h_scrollbar(hbar, widget, x, y, w, h, pw, ph)
        self.scrollbar_autohide(vbar, hbar, widget)
    def __tk_label_frame_url_frame(self,parent):
        frame = LabelFrame(parent,text="检测区",)
        frame.place(x=5, y=5, width=390, height=140)
        return frame
    def __tk_label_url_hint(self,parent):
        label = Label(parent,text="请选择对应平台后，输入网址开始检测",anchor="center", )
        label.place(x=10, y=10, width=260, height=30)
        return label
    def __tk_label_platform_select_hint(self,parent):
        label = Label(parent,text="请选择检测平台：",anchor="center", )
        label.place(x=10, y=45, width=120, height=30)
        return label
    def __tk_select_box_platform(self,parent):
        cb = Combobox(parent, state="readonly", )
        cb['values'] = ("bili","xhs","wb")
        cb.place(x=140, y=45, width=100, height=30)
        self.tk_select_box_platform = cb
        return cb
    def __tk_input_url(self,parent):
        ipt = Entry(parent)
        ipt.place(x=10, y=80, width=370, height=30)
        return ipt
    def __tk_button_start(self,parent):
        btn = Button(parent, text="启动检测", takefocus=False,)
        btn.place(x=250, y=45, width=130, height=30)
        return btn
    def __tk_label_frame_func_frame(self,parent):
        frame = LabelFrame(parent,text="功能区",)
        frame.place(x=5, y=150, width=390, height=210)
        return frame
    def __tk_check_button_show_result_checkbox(self,parent):
        cb = Checkbutton(parent,text="完成后展示检测结果",)
        cb.place(x=35, y=100, width=160, height=30)
        cb.state(['!selected'])
        return cb
    def __tk_button_init_voca(self,parent):
        btn = Button(parent, text="初始化词库", takefocus=False,)
        btn.place(x=30, y=10, width=150, height=30)
        return btn
    def __tk_button_login_bili(self,parent):
        btn = Button(parent, text="登录bilibili", takefocus=False,)
        btn.place(x=210, y=10, width=150, height=30)
        return btn
    def __tk_button_login_xhs(self,parent):
        btn = Button(parent, text="登录小红书", takefocus=False,)
        btn.place(x=30, y=60, width=150, height=30)
        return btn
    def __tk_button_login_wb(self,parent):
        btn = Button(parent, text="登录微博", takefocus=False,)
        btn.place(x=210, y=60, width=150, height=30)
        return btn
    def __tk_label_func_hint(self,parent):
        label = Label(parent,text="在使用本工具前请先使用上方按钮初始化词库，并登录对应平台",anchor="center")
        label.place(x=25, y=140, width=340, height=40)
        return label
    def __tk_label_frame_log_frame(self,parent):
        frame = LabelFrame(parent,text="日志",)
        frame.place(x=405, y=5, width=380, height=355)
        return frame


class Win(WinGUI):
    def __init__(self, controller):
        self.ctl = controller
        super().__init__()
        self.__event_bind()
        self.__style_config()
        self.ctl.init(self)
    def __event_bind(self):
        self.tk_button_start.bind('<Button>',self.ctl.start_main)
        self.tk_button_init_voca.bind('<Button>',self.ctl.init_trie)
        self.tk_button_login_bili.bind('<Button>',self.ctl.browser_login_bilibili)
        self.tk_button_login_xhs.bind('<Button>',self.ctl.browser_login_xhs)
        self.tk_button_login_wb.bind('<Button>',self.ctl.browser_login_wb)
        pass
    def __style_config(self):
        pass

    def get_input_url(self):
        return self.tk_input_url.get()

    def get_selected_platform(self):
        return self.tk_select_box_platform.get()

    def get_show_result_checkbox_state(self):
        return self.tk_check_button_show_result_checkbox.instate(['selected'])


if __name__ == "__main__":
    win = WinGUI()
    win.mainloop()