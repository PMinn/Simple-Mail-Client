####################################################
#  D1014636 潘子珉                                                									
####################################################
import sys
import socket
import module.tk as tk
import module.headerParser as hp

PORT = 110
BUFF_SIZE = 1024

cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def pop3_init():
    reply = cSocket.recv(BUFF_SIZE).decode('utf-8')
    print('Receive message: %s' % reply)
    if reply[0] != '+':
        raise Exception(reply)
    
def sendUser(name):
    cmd = f'USER {name}\r\n'
    cSocket.send(cmd.encode('utf-8'))
    reply = cSocket.recv(BUFF_SIZE).decode('utf-8')
    print('Receive message: %s' % reply)
    if reply[0] != '+':
        raise Exception(reply)

def sendPassword(password):
    cmd = f'PASS {password}\r\n'	# don't forget "\r\n"\
    cSocket.send(cmd.encode('utf-8'))
    reply = cSocket.recv(BUFF_SIZE).decode('utf-8')
    print('Receive message: %s' % reply)
    if reply[0] != '+':
        raise Exception(reply)

def sendList():
    cmd = 'LIST\r\n'	
    cSocket.send(cmd.encode('utf-8'))
    reply = cSocket.recv(BUFF_SIZE).decode('utf-8')
    print('Receive message: %s' % reply)
    if reply[0] != '+':
        raise Exception(reply)
    else:
        # Count mails
        lines = reply.split('\r\n')
        count = int(lines[0].split(' ')[1])
        print('Mailbox has %d mails' % count)
        info = []
        for i in range(1, len(lines) - 2):
            info.append(tuple(lines[i].split(' ')))
        return count, tuple(info)
    
def sendQuit():
    global cSocket
    try:
        cmd = 'QUIT\r\n'
        cSocket.send(cmd.encode('utf-8'))
        cSocket.close()
        cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('send quit')
    except socket.error as e:
        print('Socket error: %s' % str(e))
    except Exception as e:
        print('Other exception: %s' % str(e))

def sendRset():
    cmd = 'RSET\r\n'
    cSocket.send(cmd.encode('utf-8'))
    reply = cSocket.recv(BUFF_SIZE).decode('utf-8')
    print('Receive message: %s' % reply)
    if reply[0] != '+':
        raise Exception(reply)
            

def deleteMail(messageId):
    cmd = f'DELE {str(messageId)}\r\n'
    cSocket.send(cmd.encode('utf-8'))
    reply = cSocket.recv(BUFF_SIZE).decode('utf-8')
    print('Receive message: %s' % reply)
    if reply[0] != '+':
        raise Exception(reply)
    
def getHeader(messageId, preline):
    cmd = f"TOP {str(messageId)} {str(preline)}\r\n"
    cSocket.send(cmd.encode('utf-8'))

def receiveFunc():
    return cSocket.recv(BUFF_SIZE).decode('utf-8')

def preview(messageId):
    getHeader(messageId, 1)
    return hp.Mail(receiveFunc)


def sendRetr(cSocket, messageId):
    cmd = f"RETR {str(messageId)}\r\n"
    cSocket.send(cmd.encode('utf-8'))

def open_mailDetail(listWindow, messageId):
    try:
        sendRetr(cSocket, messageId)
        mail = hp.Mail(receiveFunc)
        mailWindow = tk.MailWindow(mail.headers, mail.body)
        print(mail.headers)
        print(mail.body)
    except socket.error as e:
        print('Socket error: %s' % str(e))
        listWindow.error('Socket error: %s' % str(e))
    except Exception as e:
        print('Other exception: %s' % str(e))
        listWindow.error('Other exception: %s' % str(e))

def mailList_render(listWindow):
    try:
        numberOfMails, infoOfMails = sendList()
        for i in range(numberOfMails):
            messageID = int(infoOfMails[i][0])
            mailPreview = preview(messageID)
            listWindow.append(messageID, mailPreview.headers, mailPreview.body, open_mailDetail, deleteMail)
    except socket.error as e:
        print('Socket error: %s' % str(e))
        listWindow.error('Socket error: %s' % str(e))
    except Exception as e:
        print('Other exception: %s' % str(e))
        listWindow.error('Other exception: %s' % str(e))


def start(loginWindow, serverIP, account, password):
    print('Connecting to %s port %s' % (serverIP, PORT))
    cSocket.connect((serverIP, PORT))
    
    pop3_init()
    try:
        sendUser(account)
        sendPassword(password)
        listWindow = tk.ListWindow(account, mailList_render, sendQuit, sendRset)
        mailList_render(listWindow)

    except socket.error as e:
        print('Socket error: %s' % str(e))
        tk.Dialog(loginWindow, str(e))
        sendQuit()
    except Exception as e:
        print('Other exception: %s' % str(e))
        tk.Dialog(loginWindow, str(e))
        sendQuit()
        
def main():
    loginWindow = tk.LoginWindow(start)
    loginWindow.mainloop()
    
if __name__ == '__main__':
    main()