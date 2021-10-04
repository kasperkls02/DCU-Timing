import socket
s = socket.socket()
port = 5403

s.connect(('192.168.1.200', port))


def handleMylapsInput(message):
    if not(message == ''):
        val = decodeMsg(message)
        decoder = val[1]
        if not(decoder == ''):
            print(val[4])
            timee = ''
            if val[4] != '':
                timee = int(val[4]) / 1000000 #Convert to seconds
            chip = val[0]
            strength = val[2]
            flags = val[3]
            if not(chip == ''):
                if flags == '':
                    return
                if type(flags) is str:
                    if not(flags == ''):
                        flags = int(flags)
                    else:
                        flags = 0
                print(flags)
                battery = repr(flags % 2)
                print(chip)


rest = ''

while 1:
    print("Ny passing her! rest = " + str(len(rest)))
    message = rest + s.recv(4096)
    parts = message.split("\x8f")
    partsLen = len(parts)
    for i in range(0,partsLen):
        if i == partsLen - 1:
            rest = parts[i]
            break
        handleMylapsInput(parts[i] + "\x8f")
