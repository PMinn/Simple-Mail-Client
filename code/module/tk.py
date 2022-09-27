import tkinter as tk
from datetime import datetime

class LoginWindow(tk.Tk):
    def __init__(self, start):
        super().__init__()
        self.title('Login')
        self.geometry("400x300")

        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 2)

        ipLabel = tk.Label(self ,text = "server IP")
        ipLabel.grid(row = 0, column = 0)
        ipEntry = tk.Entry(self)
        ipEntry.grid(row = 0, column = 1)
        ipEntry.insert(0, '140.134.135.41')

        accountLabel = tk.Label(self ,text = "帳號")
        accountLabel.grid(row = 1, column = 0)
        accountEntry = tk.Entry(self)
        accountEntry.grid(row = 1, column = 1)
        accountEntry.insert(0, 'iecs01')

        passLabel = tk.Label(self ,text = "密碼")
        passLabel.grid(row = 2, column = 0)
        passEntry = tk.Entry(self)
        passEntry.insert(0, 'K4ZrAHDB')
        passEntry.grid(row = 2, column = 1)

        start_btn = tk.Button(self, text='連線', command = lambda: start(ipEntry.get(), accountEntry.get(), passEntry.get()))
        start_btn.grid(row = 3, column = 0,columnspan = 2, pady = 20, sticky = "WENS")


class MailList(tk.Frame):
    def __init__(self, indexMail, window, cSocket, headers, body, clickFunc):
        super().__init__(window, bg = "#f2f6fc")
        super().pack(fill = 'x', side = 'top', padx = 20, pady = 3)
        fromLabel = tk.Label(self, text = headers['From'].split('@')[0], bg = "#f2f6fc", font = 'bold')
        fromLabel.pack(side = 'left', padx = 3)
        fromLabel.bind("<Button-1>", lambda e: clickFunc(cSocket, indexMail))

        subjectLabel = tk.Label(self, text = headers['Subject'], bg = "#f2f6fc", font = 'bold')
        subjectLabel.pack(side = 'left', padx = 3)
        subjectLabel.bind("<Button-1>", lambda e: clickFunc(cSocket, indexMail))
        
        if body != '':
            innerLabel = tk.Label(self, text = f" - {body}", fg='#5f6368', bg = "#f2f6fc")
            innerLabel.pack(side = 'left')
            innerLabel.bind("<Button-1>", lambda e: clickFunc(cSocket, indexMail))
        
        dateLabel = tk.Label(self, text = datetime.strptime(headers['Date'], '%a, %d %b %Y %H:%M:%S +0800').strftime("%m月%d日 %H:%M"), bg = "#f2f6fc", font = 'bold')
        dateLabel.pack(side = 'right', padx = 3)
        dateLabel.bind("<Button-1>", lambda e: clickFunc(cSocket, indexMail))


class ListWindow(tk.Toplevel):
    def __init__(self, account, stopFunc):
        super().__init__()
        self.title(account)
        self.geometry("800x300")
        self.protocol("WM_DELETE_WINDOW", lambda: self.exit(stopFunc))

        vscrollbar = tk.Scrollbar(self, orient = 'vertical')
        vscrollbar.pack(fill = 'y', side = 'right', expand = False)
        canvas = tk.Canvas(self, bd = 0, highlightthickness = 0, yscrollcommand = vscrollbar.set)
        vscrollbar.config(command = canvas.yview)
        self.frame = tk.Frame(canvas, bg = "#f2f6fc")
        canvas.config(yscrollcommand = vscrollbar.set)
        self._frame_id = canvas.create_window(0, 0, window = self.frame, anchor = 'nw')
        canvas.pack(side = 'left', fill = 'both', expand = True)
        self.canvas = canvas
        canvas.bind("<Configure>", self.resize_frame)

        menubar = tk.Menu(self)
        menubar.add_cascade(label = "復原", command = self.reset)
        self.configure(menu = menubar)

    def reset(self):
        print('reset')

    def resize_frame(self, e):
        self.canvas.itemconfig(self._frame_id, height = e.height, width = e.width)

    def append(self, cSocket, indexMail, headers, body, clickFunc):
        MailList(indexMail, self.frame, cSocket, headers, body, clickFunc)

    def exit(self, stopFunc):
        stopFunc()
        self.destroy()


class MailWindow(tk.Toplevel):
    def __init__(self, headers, body):
        super().__init__()
        self.title(headers['Subject'])   	 
        self.geometry("400x300")
        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 1)
        self.grid_rowconfigure(6, weight = 1)

        fromKeyLabel = tk.Label(self, text = '寄件者：', justify = 'left')
        fromKeyLabel.grid(row = 0, column = 0, sticky = 'w', padx = (20, 0))

        fromValueLabel = tk.Label(self, text = headers['From'], justify = 'left')
        fromValueLabel.grid(row = 0, column = 1, sticky = 'w')

        reply_toKeyLabel = tk.Label(self, text = '回覆至：', justify = 'left')
        reply_toKeyLabel.grid(row = 1, column = 0, sticky = 'w', padx = (20, 0))

        if not ('Reply-To' in headers):
            headers['Reply-To'] = headers['From']
        reply_toValueLabel = tk.Label(self, text = headers['Reply-To'], justify = 'left')
        reply_toValueLabel.grid(row = 1, column = 1, sticky = 'w')
    
        toKeyLabel = tk.Label(self, text = '收件者：', justify = 'left')
        toKeyLabel.grid(row = 2, column = 0, sticky = 'w', padx = (20, 0))

        toValueLabel = tk.Label(self, text = headers['To'], justify = 'left')
        toValueLabel.grid(row = 2, column = 1, sticky = 'w')

        dateKeyLabel = tk.Label(self, text = '日期：', justify = 'left')
        dateKeyLabel.grid(row = 3, column = 0, sticky = 'w', padx = (20, 0))

        dateValueLabel = tk.Label(self, text = datetime.strptime(headers['Date'], '%a, %d %b %Y %H:%M:%S +0800').strftime("%Y年%m月%d日 %H:%M"), justify = 'left')
        dateValueLabel.grid(row = 3, column = 1, sticky = 'w')

        subjectKeyLabel = tk.Label(self, text = '主旨：', justify = 'left')
        subjectKeyLabel.grid(row = 4, column = 0, sticky = 'w', padx = (20, 0))

        subjectValueLabel = tk.Label(self, text = headers['Subject'], justify = 'left')
        subjectValueLabel.grid(row = 4, column = 1, sticky = 'w')

        return_pathKeyLabel = tk.Label(self, text = '寄件人：', justify = 'left')
        return_pathKeyLabel.grid(row = 5, column = 0, sticky = 'w', padx = (20, 0))

        return_pathValueLabel = tk.Label(self, text = headers['Return-Path'].split('@')[1].replace(">", ""), justify = 'left')
        return_pathValueLabel.grid(row = 5, column = 1, sticky = 'w')

        frame = tk.Frame(self)
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side = 'right', fill = 'y')
        text = tk.Text(frame, yscrollcommand = scrollbar.set)
        text.insert("insert", body)
        text.config(state = 'disabled')
        text.pack(side = 'bottom', fill = 'both', expand = True)
        scrollbar.config(command = text.yview)
        frame.grid(row = 6, column = 0, columnspan = 2, sticky = 'nsew', pady = (40, 5), padx = 20)
