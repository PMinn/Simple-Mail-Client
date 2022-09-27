def parsestr(reply):
    line = reply.split("\r\n")
    lastKey = ''
    response = {}
    body = ''
    isInHeader = True
    for i in range(1,len(line)-2):
        if isInHeader:
            if line[i] == "":
                isInHeader = False
            elif line[i][0] != '\t':
                key = line[i].split(': ')[0]
                value = line[i].split(key+': ')[1]
                response[key] = value
                lastKey = key
            else:
                response[lastKey] += line[i]
        else:
            body += line[i] + '\r\n'
    return response, body