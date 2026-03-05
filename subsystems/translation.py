from canlib import canlib, Frame
import re

coffeeMaker = {0x7E8:"first", 0x7E9: "second", 0x7CA: "requested first", 0x7CB: "requested second"}
combiOven = {0x7D8:"first", 0x7D9:"second",0x7BA:"requested first",0x7BB:"requested second"}
steamOven = {0x7C8:"first",0x7C9:"second",0x7AA:"requested first",0x7A8:"requested second"}
espressoMaker = {0x7B8:"first",0x7B9:"second",0x79A:"requested first",0x79B:"requested second"}
airChiller = {0x7A8:"first",0x7A9:"second",0x78A:"requested first",0x78B:"requested second"}

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

def DtCleaner(frame, withX):
    cleanDt = ""
    dt = frame.data
    dDt = (frame.data)[12:]
    if ("\x" in dt): #could not work, try \\x otherwise
        dt = dt.split("\x") #need to handle corner case of those chars being together in ascii too...... fml
    
    for i in range (len(dt)):
        currDt = dt[i]
        if (len(currDt) == 2): #then its ok
            if (withX):
                cleanDt = cleanDt + str("\x"+ currDt)
            else:
                cleanDt = cleanDt + str(currDt)
        
        else:
            if (i == 0 and dDt[0] != 'x'): #so its the first set of chars, and we start with ascii... so all of them are ascii
                for j in range (len(currDt)):
                    hexV = hex(ord(currDt[j])) #converts to hex
                    if (withX):
                        cleanDt = cleanDt + str("\x"+ hexV)
                    else:
                        cleanDt = cleanDt + str(hexV)
            
            else: #so we start with hex, then have the ascii
                for j in range (len(currDt)):
                    if (j == 0):
                        v = currDt[:2]
                        cleanDt = cleanDt + v
                    else:
                        hexV = hex(ord(currDt[j])) #converts to hex
                        if (withX):
                            cleanDt = cleanDt + str("\x"+ hexV)
                        else:
                            cleanDt = cleanDt + str(hexV)
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
        hexV = hex(ord(pci)) #get the corresponding hex

        if (hexV[:3] == '0x2'):
            return "CF" #control frame
        
        if (hexV[:3] == '0x3'):
            return "FloF" #flow frame
        
    




