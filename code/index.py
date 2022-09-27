####################################################
#  Network Programming - Unit 3 Application based on TCP         
#  Program Name: pop3client.py                                      			
#  The program is a simple POP3 client.            		
#  2021.08.03                                                   									
####################################################
import sys
import socket
from getpass import getpass
import module.tk as tk
import module.headerParser as hp


PORT = 110
BUFF_SIZE = 1024			# Receive buffer size

def pop3_init(cSocket):
    reply = cSocket.recv(BUFF_SIZE).decode('utf-8')
    print('Receive message: %s' % reply)
    if reply[0] == '+':
        return True
    else:
        return False
    
def sendUser(cSocket,name):
    cmd = 'USER ' + name + '\r\n'			# don't forget "\r\n"
    cSocket.send(cmd.encode('utf-8'))
    reply = cSocket.recv(BUFF_SIZE).decode('utf-8')
    print('Receive message: %s' % reply)
    if reply[0] == '+':
        return True
    else:
        return False

def sendPassword(cSocket,password):
    cmd = 'PASS ' + password + '\r\n'	# don't forget "\r\n"\
    cSocket.send(cmd.encode('utf-8'))
    reply = cSocket.recv(BUFF_SIZE).decode('utf-8')
    print('Receive message: %s' % reply)
    if reply[0] == '+':
        return True
    else:
        return False

def sendList(cSocket):
    cmd = 'LIST\r\n'	
    cSocket.send(cmd.encode('utf-8'))
    reply = cSocket.recv(BUFF_SIZE).decode('utf-8')
    print('Receive message: %s' % reply)
    if reply[0] == '+':
        # Count mails
        tokens = reply.split(' ')
        print('Mailbox has %d mails' % int(tokens[1]))
        return True, int(tokens[1])
    else:
        return False, 0
    
def sendQuit(cSocket):
    cmd = 'QUIT\r\n'
    cSocket.send(cmd.encode('utf-8'))
    print('send quit')
    
def deleteMail(cSocket, messageId):
    cmd = 'DELE '+messageId+'\r\n'
    cSocket.send(cmd.encode('utf-8'))
    reply = cSocket.recv(BUFF_SIZE).decode('utf-8')
    print('Receive message: %s' % reply)
    if reply[0] == '+':
        return True
    else:
        return False
    
def getHeader(cSocket, messageId, preline):
    cmd = f"TOP {str(messageId)} {str(preline)}\r\n"
    cSocket.send(cmd.encode('utf-8'))
    reply = cSocket.recv(BUFF_SIZE).decode('utf-8')
    if reply[0] == '+':
        return True, reply
    else:
        return False, ""

def preview(cSocket, messageId):
    isSuccess, header = getHeader(cSocket, messageId, 1)
    return hp.parsestr(header)

def fullMail(cSocket, messageId):
    cmd = f"RETR {str(messageId)}\r\n"
    cSocket.send(cmd.encode('utf-8'))
    reply = cSocket.recv(BUFF_SIZE).decode('utf-8')
    if reply[0] == '+':
        return True, reply
    else:
        return False, ""

def open_mailDetail(cSocket, messageId):
    isSuccess, mailData = fullMail(cSocket, messageId)
    headers, body = hp.parsestr(mailData)
    window = tk.MailWindow(headers, body)
    print(headers)
    print(body)

def start(serverIP, account, password):
    cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Connecting to %s port %s' % (serverIP, PORT))
    cSocket.connect((serverIP, PORT))
    listWindow = tk.ListWindow(account, lambda: sendQuit(cSocket))
    
    pop3_init(cSocket)
    try:
        sendUser(cSocket,account)
        sendPassword(cSocket,password)
        isSuccess, numberOfMails = sendList(cSocket)
        for i in range(numberOfMails):
            headers, body = preview(cSocket, i+1)
            listWindow.append(cSocket, i+1, headers, body, open_mailDetail)

#        deleteMail(cSocket,str(1))
    except socket.error as e:
        print('Socket error: %s' % str(e))
    except Exception as e:
        print('Other exception: %s' % str(e))
        
def main():
    loginWindow = tk.LoginWindow(start)
    loginWindow.mainloop()

if __name__ == '__main__':
	main()