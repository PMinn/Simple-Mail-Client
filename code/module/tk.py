import tkinter as tk

def createTk():
    window = tk.Tk()
    window.title('Login')
    window.geometry("400x300")
    return window

def loginInit(window, start):
    window.grid_columnconfigure(0, weight = 1)
    window.grid_columnconfigure(1, weight = 2)

    ipLabel = tk.Label(window ,text = "server IP")
    ipLabel.grid(row = 0, column = 0)
    ipEntry = tk.Entry(window)
    ipEntry.grid(row = 0, column = 1)
    ipEntry.insert(0, '140.134.135.41')

    accountLabel = tk.Label(window ,text = "帳號")
    accountLabel.grid(row = 1, column = 0)
    accountEntry = tk.Entry(window)
    accountEntry.grid(row = 1, column = 1)
    accountEntry.insert(0, 'iecs01')

    passLabel = tk.Label(window ,text = "密碼")
    passLabel.grid(row = 2, column = 0)
    passEntry = tk.Entry(window)
    passEntry.insert(0, 'K4ZrAHDB')
    passEntry.grid(row = 2, column = 1)

    start_btn = tk.Button(window, text='連線', command = lambda: start(ipEntry.get(), accountEntry.get(), passEntry.get()))
    start_btn.grid(row = 3, column = 0,columnspan = 2, pady = 20, sticky = "WENS")

def closeMailbox(window, stopFunc):
    stopFunc()
    window.destroy()

def mailboxInit(window, stopFunc):
    window.protocol("WM_DELETE_WINDOW", lambda: closeMailbox(window, stopFunc))

def createToplevel(title):
    window = tk.Toplevel()
    window.title(title)
    window.geometry("400x300")
    return window

def maillistInit(frame, fromMail, subject, inner, open_mailDetail, cSocket):
    fromLabel = tk.Label(frame, text = fromMail, bg = "#f2f6fc", font = 'bold')
    fromLabel.pack(side = 'left')
    fromLabel.bind("<Button-1>",lambda e: open_mailDetail(cSocket, subject))

    subjectLabel = tk.Label(frame, text = subject, bg = "#f2f6fc", font = 'bold')
    subjectLabel.pack(side = 'left')
    subjectLabel.bind("<Button-1>", lambda e: open_mailDetail(cSocket, subject))
    
    if inner != '':
        innerLabel = tk.Label(frame, text = f" - {inner}", fg='#5f6368', bg = "#f2f6fc")
        innerLabel.pack(side = 'left')
        innerLabel.bind("<Button-1>", lambda e: open_mailDetail(cSocket, subject))
    
def createFrame(window):
    frame = tk.Frame(window, bg = "#f2f6fc")
    frame.pack(fill = 'x')
    return frame

class loginWindow(tk.Tk):
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

class mailWindow(tk.Toplevel):
    def __init__(self,headers):
        super().__init__()
        self.headers = headers
        self.title(headers)   	 
        self.geometry("400x300")