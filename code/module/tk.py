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

    start_btn = tk.Button(window, text='連線', font = ("Times", 11, ""), command = lambda: start(ipEntry.get(), accountEntry.get(), passEntry.get()))
    start_btn.grid(row = 3, column = 0,columnspan = 2, pady = 20, sticky = "WENS")

def createToplevel():
    window = tk.Toplevel()
    window.title('Login')
    window.geometry("400x300")
    return window