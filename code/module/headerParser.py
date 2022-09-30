####################################################
#  D1014636 潘子珉                                                									
####################################################
from email.header import decode_header
class Mail():
    def __init__(self, receiveFunc):
        self.receiveFunc = receiveFunc
        self.headers = {}
        self.body = ''
        self.bodyLine = 0
        self.isEnd = False

        reply = self.receiveFunc()
        self.handleHeader(reply)
        headersDecode = decode_header(self.headers['Subject'])[0]
        if headersDecode[1] != None:
            self.headers['Subject'] = headersDecode[0].decode(headersDecode[1], 'ignore')

    def handleHeader(self, reply):
        lines = reply.split("\r\n")
        lastKey = ''
        if lines[len(lines) - 2] == ".":
            self.isEnd = True
        for i in range(1, len(lines)):
            if lines[i] == "":
                if self.isEnd:
                    self.handleBodyWithEnd(lines, i + 1)
                else:
                    self.handleBody(lines, i + 1)
                break
            elif lines[i][0] != '\t':
                key = lines[i].split(': ')[0]
                value = lines[i].split(key+': ')[1]
                self.headers[key] = value
                lastKey = key
            else:
                self.headers[lastKey] += lines[i]

    def handleBody(self, lines, lineIndex):
        for i in range(lineIndex, len(lines)):
            self.body += lines[i] + '\n'
            self.bodyLine += 1
        reply = self.receiveFunc()
        lines = reply.split("\r\n")
        if lines[len(lines) - 2] == ".":
            self.isEnd = True
            self.handleBodyWithEnd(lines, 0)
        else:
            self.handleBody(lines, 0)

    def handleBodyWithEnd(self, lines, lineIndex):
        for i in range(lineIndex, len(lines) - 2):
            self.bodyLine += 1
            if i != len(lines) - 3:
                self.body += lines[i] + '\n'
            else:
                self.body += lines[i]