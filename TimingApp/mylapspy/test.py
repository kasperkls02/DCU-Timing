import os
import socket

def decodeMsg(data):
    returnval = ['','','','','']
    tortof2namtyp = {
        "1_1": "dPassing Number",
        "1_4": "qRTC Time",
        "1_5": "wStrength",
        "1_6": "wHits",
        "1_8": "wFlags",
        "1_10": "sTran Code",
        "1_16": "qUTC Time",
        "1_17": "bCounter??",
        "1_19": "dPip??",
        "1_20": "bSport",

        "2_1": "wNoise",
        "2_6": "bGPS",
        "2_7": "wTemperature",
        "2_10": "bSatInUse",
        "2_12": "bInput Voltage",

        "69_2": "sID",
        "77_1": "dCounter??",
        "78_1": "dID??",
        "78_2": "sTran Code??",
        "78_3": "qRTC Time??",
        "78_4": "qUTC Time??",
}

    tor = 0
    tof = 0
    tofdat = []

    def tortof2txt():
        if tof == 0x81:
            decoder = str(tofdat[0] | (tofdat[1] << 8) | (tofdat[2] << 16) | (tofdat[3] << 34))
            returnval[1] = decoder
            #print("Decoder ID=" + str(tofdat[0] | (tofdat[1] << 8) | (tofdat[2] << 16) | (tofdat[3] << 34)))
            pass
        elif tof == 0x83:
            #print("Controller ID=" + str(tofdat[0] | (tofdat[1] << 8) | (tofdat[2] << 16) | (tofdat[3] << 34)))
            pass
        elif tof == 0x85:
            #print("Request ID=...") # + str(tofdat[0] | (tofdat[1] << 8) | (tofdat[2] << 16) | (tofdat[3] << 34))
            pass
        else:
            tt = str(tor) + "_" + str(tof)
            if tt in tortof2namtyp:
                nam = tortof2namtyp[tt]
                typ = nam[0]
                nam = nam[1:]
                val = "..."
                if typ == 'b': val = str(tofdat[0])
                elif typ == 'w': val = str(tofdat[0] | (tofdat[1] << 8))
                elif typ == 'd': val = str(tofdat[0] | (tofdat[1] << 8) | (tofdat[2] << 16) | (tofdat[3] << 24))
                elif typ == 'q': val = str(tofdat[0] | (tofdat[1] << 8) | (tofdat[2] << 16) | (tofdat[3] << 24) | (tofdat[4] << 32) | (tofdat[5] << 40) | (tofdat[6] << 48) | (tofdat[7] << 56))
                elif typ == 's':
                    val = ""
                    for byt in tofdat:
                        val += chr(byt)
                if tt == "1_5":
                    print("tt=" + tt + " typ=" + typ + nam + " len=" + str(len(tofdat)) + " val=" + str(val))
                    returnval[2] = str(val)
                elif tt == "1_8":
                    returnval[3] = val
                elif tt == "78_2" or tt == "1_10": #tt == "69_2" or
                    returnval[0] = val.replace("-","")

            else:
                print("Unknown: tt=" + tt + " len=" + str(len(tofdat)))

    state = -1
    esc = 0
    for byt in data: # print "state=" + str(state) + " b=" + str(b)
        b = ord(byt)
        # print("state=" + str(state) + " b=" + str(b))
        if b == 0x8d:
            esc = 1
            continue
        elif esc == 1:
            b -= 0x20
            esc = 0
        if state == -1:
            if b == 0x8e:
                state = 0
                #print("SOR:")
            else: print("Syntax Error...")
        elif state == 0:
            version = b
            state = 1
        elif state == 1:
            state = 101
        elif state == 101:
            state = 2
        elif state == 2:
            crc = b
            state = 102
        elif state == 102:
            crc |= b << 8
            state = 4
        elif state == 4:
            flags = b
            state = 104
        elif state == 104:
            flags |= b << 8
            state = 6
        elif state == 6:
            tor = b
            state = 106
        elif state == 106:
            tor |= b << 8
            state = 7
            #print("TOR:" + str(tor) + "\t" + str(version) + "\t" + str(crc) + "\t" + str(flags))
        elif state == 7:
            if b == 0x8f:
                state = -1
                # evt check crc
                #print("EOR")
            else:
                tofdat = []
                tof = b
                state = 8
        elif state == 8:
            dlen = fieldlen = b
            if (flags & 1) == 1: state = 108
            else: state = 12
        elif state == 108:
            fieldlen |= b << 9
            state = 208
        elif state == 208:
            fieldlen |= b << 16
            state = 308
        elif state == 308:
            fieldlen |= b << 24
            dlen = fieldlen
            state = 12
        elif state == 12:
            dlen -= 1
            tofdat.append(b)
            if dlen == 0:
                tortof2txt()
                state = 7
        else:
            #print("Syntax Error...")
            pass
    return returnval



#print("Connecting to AMB with IP: %s Port: %s" % (ip, port))
#s.connect((ip, port))




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
            print("val[0]")
            print(val[0])
            print("val[1]")
            print(val[1])
            print("val[2]")
            print(val[2])
            print("val[3]")
            print(val[3])
            print("val[4]")
            print(val[4])
            if not(chip == ''):
                if flags == '':
                    return
                if type(flags) is str:
                    if not(flags == ''):
                        flags = int(flags)
                    else:
                        flags = 0
                print(flags)
                battery = repr(flags)
                print("Chip: " + chip + "; Battery: " + battery)

notConnected = True
timeout = 10 # seconds

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('192.168.1.200', 5403))

rest = ""
print("Starting main loop")
while 1:
    print("Ny passing her! rest = " + str(len(rest)))
    message = rest + clientsocket.recv(4096)
    print(message)
    parts = message.split(b'\x8f')
    partsLen = len(parts)
    for i in range(0,partsLen):
        if i == partsLen - 1:
            rest = parts[i]
            break
        handleMylapsInput(parts[i] + b'\x8f')
