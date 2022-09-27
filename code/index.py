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
    
def getHeader(cSocket, messageId):
    cmd = 'TOP ' + messageId + ' 1\r\n'
    cSocket.send(cmd.encode('utf-8'))
    reply = cSocket.recv(BUFF_SIZE).decode('utf-8')
    if reply[0] == '+':
        return True, reply
    else:
        return False, ""

def preview(cSocket, messageId):
    isSuccess, header = getHeader(cSocket, messageId)
    return hp.parsestr(header)
    
def open_mailDetail(cSocket, subject):
    window = tk.MailWindow("ttttest")

def start(serverIP, account, password):
    cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Connecting to %s port %s' % (serverIP, PORT))
    cSocket.connect((serverIP, PORT))
    window = tk.createToplevel(account)
    tk.mailboxInit(window, lambda: sendQuit(cSocket))
    pop3_init(cSocket)
    try:
        sendUser(cSocket,account)
        sendPassword(cSocket,password)
        isSuccess, numberOfMails = sendList(cSocket)
        for i in range(numberOfMails):
            headers, body = preview(cSocket, str(i+1))
            li = tk.createFrame(window)
            tk.maillistInit(li, headers['From'].split('@')[0], headers['Subject'], body, open_mailDetail, cSocket)
#        deleteMail(cSocket,str(1))
    except socket.error as e:
        print('Socket error: %s' % str(e))
    except Exception as e:
        print('Other exception: %s' % str(e))
        
def main():
#    if(len(sys.argv) < 2):
#        print("Usage: python3 pop3client.py ServerIP")
#        return
    baseLoginWindow = tk.LoginWindow(start)
    #window = tk.createToplevel()
    baseLoginWindow.mainloop()
    return 
	# Get server IP
    serverIP = socket.gethostbyname(sys.argv[1])
	
	# Get username & password
    name = input('Username: ')
    password = getpass('Password: ')
		
	# Create a TCP client socket
    cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Connecting to %s port %s' % (serverIP, PORT))
    cSocket.connect((serverIP, PORT))
    
    pop3_init(cSocket)
    try:
        sendUser(cSocket,name)
        sendPassword(cSocket,password)
        method1(cSocket)
#        method2(cSocket)
        getHeader(cSocket,str(1))
#        deleteMail(cSocket,str(1))
        sendQuit(cSocket)
    except socket.error as e:
        print('Socket error: %s' % str(e))
    except Exception as e:
        print('Other exception: %s' % str(e))

    print('Closing connection.')
    cSocket.close()
# end of main


if __name__ == '__main__':
	main()