import tkinter as tk

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
        super().pack(fill = 'x', side = 'top')
        self.cSocket = cSocket
        self.clickFunc = clickFunc
        self.subject = headers['Subject']
        fromLabel = tk.Label(self, text = headers['From'].split('@')[0], bg = "#f2f6fc", font = 'bold')
        fromLabel.pack(side = 'left')
        fromLabel.bind("<Button-1>", lambda e: clickFunc(cSocket, headers['Subject']))

        subjectLabel = tk.Label(self, text = headers['Subject'], bg = "#f2f6fc", font = 'bold')
        subjectLabel.pack(side = 'left')
        subjectLabel.bind("<Button-1>", lambda e: clickFunc(cSocket, headers['Subject']))
        
        if body != '':
            innerLabel = tk.Label(self, text = f" - {body}", fg='#5f6368', bg = "#f2f6fc")
            innerLabel.pack(side = 'left')
            innerLabel.bind("<Button-1>", lambda e: clickFunc(cSocket, headers['Subject']))


class ListWindow(tk.Toplevel):
    def __init__(self, account, stopFunc):
        super().__init__()
        self.title(account)
        self.geometry("400x300")
        self.protocol("WM_DELETE_WINDOW", lambda: self.exit(stopFunc))

    def append(self, cSocket, indexMail, headers, body, clickFunc):
        li = MailList(indexMail, self, cSocket, headers, body, clickFunc)

    def exit(self, stopFunc):
        stopFunc()
        self.destroy()


class MailWindow(tk.Toplevel):
    def __init__(self,headers):
        super().__init__()
        self.headers = headers
        self.title(headers)   	 
        self.geometry("400x300")
