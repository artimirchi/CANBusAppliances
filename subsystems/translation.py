from canlib import canlib, Frame
import re

coffeeMaker = {0x7E8:"first", 0x7E9: "second", 0x7CA: "requested first", 0x7CB: "requested second"}
combiOven = {0x7D8:"first", 0x7D9:"second",0x7BA:"requested first",0x7BB:"requested second"}
steamOven = {0x7C8:"first",0x7C9:"second",0x7AA:"requested first",0x7A8:"requested second"}
espressoMaker = {0x7B8:"first",0x7B9:"second",0x79A:"requested first",0x79B:"requested second"}
airChiller = {0x7A8:"first",0x7A9:"second",0x78A:"requested first",0x78B:"requested second"}

vals = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F"]

def FrameTypeClassifier(frame):
    currID = frame.id
    if (currID in coffeeMaker.keys()):
        frameType = coffeeMaker[currID]
        return ["coffeeMaker", frameType]

    elif (currID in combiOven.keys()):
        frameType = combiOven[currID]
        return ["combiOven", frameType]

    elif (currID in steamOven.keys()):
        frameType = steamOven[currID]
        return ["steamOven", frameType]
    
    elif (currID in espressoMaker.keys()):
        frameType = espressoMaker[currID]
        return ["espressoMaker", frameType]
    
    elif (currID in airChiller.keys()):
        frameType = airChiller[currID]
        return ["airChiller", frameType]

    else:
        print("\nError: Frame type not recognized")

##only for first frames
def SerialNumber(frame):
    cleanDt = DtCleaner(frame, True)

    #sep the dt
    p1 = cleanDt[:2]
    p2 = cleanDt[2:4]
    p3 = cleanDt[5:]

    #convert to decimal
    dP1 = int(p1, 16)
    dP2 = int(p2, 16)
    dP3 = int(p3, 16)

    return str(dP1) + '-' + str(dP2) + '-' + str(dP3)

def PartNumber(frame):
    cleanDt = DtCleaner(frame, False) #gives full hex
    d = str(int(cleanDt, 16))

    return (d[:3] + '-' + d[3:7] + '-' + d[7:])

def DtCleaner(frame, withX = True):
    cleanDt = ""
    dt = frame.data
    dDt = (frame.data)[10:]
    if ("\\x" in str(dt)): #could not work, try \\x otherwise
        dt = str(dt).split("\\x") #need to handle corner case of those chars being together in ascii too...... fml
    print(dt)

    i = 0

    while (i < len(dt)):
        currDt = dt[i]
        print(dt[i])
        if (i == 0): #then itll include the bytearray shit
            currDt = (currDt[12:])
            if (len(currDt) == 0): #so dt[0] was only the byte array stuff, so its already in hex
                i += 1
                currDt = dt[i]

        if (len(currDt) == 4 and currDt[-1] == ')' and i == len(dt) - 1): #then tis the ' inserted by the sender
            currDt = currDt[:2]
            print(currDt)

        if (len(currDt) == 2 and currDt[0] in vals and currDt[1] in vals): #then its ok
            #print(i)
            if (withX):
                cleanDt = cleanDt + str("\\x"+ currDt)
            else:
                cleanDt = cleanDt + str(currDt)
        
        elif (len(currDt) == 2): #so correct len, but not hex
            for j in range(0, len(currDt)):
                print((currDt[j]))
                c = ord(currDt[j]) #get the associated hex
                c = str(hex(c))[2:]

                if (withX):
                    cleanDt = cleanDt + str("\\x"+ c)
                else:
                    cleanDt = cleanDt + str(c)

        else: #so the length isnt 2...
            if (i != 0): #dont deal with if its the first element... so there has to be a hex in front of it
                c = currDt[:2] #just the hex
                if (withX): #add just the hex into the string
                    cleanDt = cleanDt + str("\\x"+ c)
                else:
                    cleanDt = cleanDt + str(c)
                
                a = 0
                if (i == len(dt) - 1): #if its the last one, will exclude the ')
                    a = 2
                
                for j in range(2, len(currDt) - a):
                    print((currDt[j]))
                    c = ord(currDt[j]) #get the associated hex
                    c = str(hex(c))[2:]

                    if (withX):
                        cleanDt = cleanDt + str("\\x"+ c)
                    else:
                        cleanDt = cleanDt + str(c)

            if (i == 0):
                for j in range(0, len(currDt)):
                    print((currDt[j]))
                    c = ord(currDt[j]) #get the associated hex
                    c = str(hex(c))[2:]

                    if (withX):
                        cleanDt = cleanDt + str("\\x"+ c)
                    else:
                        cleanDt = cleanDt + str(c)
        i += 1
    return cleanDt


def UsageTime(frame):
    cleanDt = DtCleaner(frame, False)
    t = str(int(cleanDt, 16))

    return t

def HealthMonitor(frame):
    dt = frame.data
    cleanDt = DtCleaner(frame, False)

    h = str(bin(int(cleanDt, 16)))

    if (h[-1] == 1):
        print("issue 1")

    if (h[-2] == 1):
        print("issue 2")
    
    if (h[-3] == 1):
        print("issue 3")

    return [h[-1] == 1, h[-2] == 1, h[-3] == 1]


def PCIClassifier(frame):
    dt = frame.data
    dt = dt.split("'") #could be an issue later if there are ascii of '

    if ('\\' in dt):
        dt = dt.split('\\')
        print(dt)

    pci = dt[0] #gets the first char
    if (pci[0] == 'x'): #then it uses hex...
        pci = pci[1:]
        if (pci[0] == '1'):
            return "FstF" #first frame

        if (pci[0] == '0'):
            return "SF" #single frame

    else: #uses ascii, just one char, should be the first then
        pci = pci[0]
        hexV = str(hex(ord(pci))) #get the corresponding hex

        if (hexV[:3] == '0x2'):
            return "CF" #consec frame
        
        elif (hexV[:3] == '0x3'):
            return "FloF" #flow frame