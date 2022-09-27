def parsestr(reply):
    line = reply.split("\r\n")
    lastKey = ''
    response = {}
    isInHeader = True
    for i in range(1,len(line)-1):
        if line[i] == "":
            isInHeader = False
        elif line[i][0] != '\t':
            key = line[i].split(': ')[0]
            value = line[i].split(key+': ')[1]
            response[key] = value
            lastKey = key
        else:
            response[lastKey] += line[i]
    return response