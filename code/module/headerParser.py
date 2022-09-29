def parseHeaderFromStr(reply):
    line = reply.split("\r\n")
    lastKey = ''
    response = {}
    body = ''
    isInHeader = True
    bodyLine = 0
    bodyStartIndex = 0
    for i in range(1, len(line)):
        if isInHeader:
            if line[i] == "":
                isInHeader = False
                bodyStartIndex = i + 1
            elif line[i][0] != '\t':
                key = line[i].split(': ')[0]
                value = line[i].split(key+': ')[1]
                response[key] = value
                lastKey = key
            else:
                response[lastKey] += line[i]
        else:
            body += line[i]
            bodyLine += 1
            if i != len(line)-3:
                body += '\n'
    return response, body, bodyLine


class Mail():
    def __init__(self, receiveFunc):
        self.receiveFunc = receiveFunc
        self.headers = {}
        self.body = ''
        self.bodyLine = 0
        self.isEnd = False

        reply = self.receiveFunc()
        self.handleHeader(reply)
        #self.headers['Lines'] = int(self.headers['Lines'])


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