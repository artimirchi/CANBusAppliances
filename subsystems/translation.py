from canlib import canlib, Frame
import re
import time


CoffeeMaker = {0x7E8:"first", 0x7E9: "second", 0x7CA: "requested first", 0x7CB: "requested second"}
CombiOven = {0x7D8:"first", 0x7D9:"second",0x7BA:"requested first",0x7BB:"requested second"}
SteamOven = {0x7C8:"first",0x7C9:"second",0x7AA:"requested first",0x7AB:"requested second"}
EspressoMaker = {0x7B8:"first",0x7B9:"second",0x79A:"requested first",0x79B:"requested second"}
AirChiller = {0x7A8:"first",0x7A9:"second",0x78A:"requested first",0x78B:"requested second"}

vals = ["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]
spec = {"\n":"0a", "\r":"0d", "\b":"20", "\\n":"0a", "\\r":"0d", "\\t":"09", "\t":"09"}

apps = {0x7E8:"Coffee Maker",0x7D8:"Combi Oven",0x7C8:"Steam Oven",0x7B8:"Espresso Maker",0x7A8:"Air Chiller"}

first = {0x7E8:"Coffee Maker",0x7D8:"Combi Oven",0x7C8:"Steam Oven",0x7B8:"Espresso Maker",0x7A8:"Air Chiller"}
second = {0x7E9:"Coffee Maker",0x7D9:"Combi Oven",0x7C9:"Steam Oven",0x7B9:"Espresso Maker",0x7A9:"Air Chiller"}
rqf = {0x7CA:"Coffee Maker",0x7BA:"Combi Oven",0x7AA:"Steam Oven",0x79A:"Espresso Maker",0x78A:"Air Chiller"}
rqs = {0x7CB:"Coffee Maker",0x7BB:"Combi Oven",0x7AB:"Steam Oven",0x79B:"Espresso Maker",0x78B:"Air Chiller"}

cMI = {"Heating system issues": False, "Phase loss": False, "Magnetron issues": False, "Other": False, "Invalid Val": False}
cOI= {"Heating system issues": False, "Phase loss": False, "Magnetron issues": False, "Other": False, "Invalid Val": False}
sOI = {"Heating system issues": False, "Phase loss": False, "Magnetron issues": False, "Other": False, "Invalid Val": False}
eMI = {"Heating system issues": False, "Phase loss": False, "Magnetron issues": False, "Other": False, "Invalid Val": False}
aCI = {"Heating system issues": False, "Phase loss": False, "Magnetron issues": False, "Other": False, "Invalid Val": False}
appsStatus = [cMI,cOI,sOI,eMI,aCI]


#global
allApps = []

##get the frame type and the appliance its from
def FrameTypeClassifier(frame):
    currID = frame.id
    if (currID in CoffeeMaker.keys()):
        frameType = CoffeeMaker[currID]
        return ["Coffee Maker", frameType]

    elif (currID in CombiOven.keys()):
        frameType = CombiOven[currID]
        return ["Combi Oven", frameType]

    elif (currID in SteamOven.keys()):
        frameType = SteamOven[currID]
        return ["Steam Oven", frameType]
    
    elif (currID in EspressoMaker.keys()):
        frameType = EspressoMaker[currID]
        return ["Espresso Maker", frameType]
    
    elif (currID in AirChiller.keys()):
        frameType = AirChiller[currID]
        return ["Air Chiller", frameType]

    else:
        print("\nError: Frame type not recognized")

def SerialNumber(frame):
    cleanDt = DtCleanerfml(frame, False) #get the full thing
    sn = cleanDt[4:14]

    year = sn[0:2]
    month = sn[2:4]
    day = sn[4:]

    dP1 = int(year, 16)
    dP2 = int(month, 16)
    dP3 = int(day, 16)

    if (len(str(dP1)) != 2):
        dP1 = str('0' * (2 - (len(str(dP1))))) + str (dP1)
    
    if (len(str(dP2)) != 2):
        dP2 = str('0' * (2 - (len(str(dP2))))) + str(dP2)

    if (len(str(dP3)) != 5):
        print(len(str(dP3)))
        dP3 = str('0' * (5 - (len(str(dP3))))) + str(dP3)

    return str(dP1) + '-' + str(dP2) + '-' + str(dP3)


#unused
##only for first frames
def SerialNumber1(frame):
    cleanDt = DtCleanerfml(frame, True)
    print(cleanDt)

    #sep the dt
    p1 = cleanDt[2:4]
    p2 = cleanDt[6:8]
    p3 = cleanDt[10:12] + cleanDt[14:16] + cleanDt[18:20]


    #convert to decimal
    dP1 = int(p1, 16)
    dP2 = int(p2, 16)
    dP3 = int(p3, 16)

    if (len(str(dP1)) != 2):
        dP1 = str(0 * (2 - (len(str(dP1))))) + str (dP1)
    
    if (len(str(dP2)) != 2):
        dP2 = str(0 * (2 - (len(str(dP2))))) + str(dP2)

    if (len(str(dP3)) != 5):
        dP3 = str(0 * (2 - (len(str(dP3))))) + str(dP3)

    return str(dP1) + '-' + str(dP2) + '-' + str(dP3)

def PartNumber(frame):
    cleanDt = DtCleanerfml(frame, False) #gives full hex
    cleanDt = str(cleanDt)[2:10]
    d = str(int(cleanDt, 16))
    print(d)
    print(cleanDt)

    return (str((d[:3])) + '-' + str((d[3:7])) + '-' + str((d[7:])))

def DtCleaner(frame, withX = True):
    cleanDt = ""
    dt = str(frame.data)
    dDt = ((frame.data)[10:])
    print(type((dDt)))
    #if ("\\x" in str(dt)): #could not work, try \\x otherwise
    #    dt = str(dt).split("\\x") #need to handle corner case of those chars being together in ascii too...... fml
    print(dt)

    i = 0

    while (i < len(dt)):
        currDt = dt[i]
        print(dt[i])
        if (i == 0): #then itll include the bytearray shit
            currDt = (currDt[13:])
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

#not used
def DtCleaner1(frame, withX = True):
    cleanDt = ""
    dt = str(frame.data)
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
        i += 1

    #     if (len(currDt) == 4 and currDt[-1] == ')' and i == len(dt) - 1): #then tis the ' inserted by the sender
    #         currDt = currDt[:2]
    #         print(currDt)

    #     if (len(currDt) == 2 and currDt[0] in vals and currDt[1] in vals): #then its ok
    #         #print(i)
    #         if (withX):
    #             cleanDt = cleanDt + str("\\x"+ currDt)
    #         else:
    #             cleanDt = cleanDt + str(currDt)
        
    #     elif (len(currDt) == 2): #so correct len, but not hex
    #         for j in range(0, len(currDt)):
    #             print((currDt[j]))
    #             c = ord(currDt[j]) #get the associated hex
    #             c = str(hex(c))[2:]

    #             if (withX):
    #                 cleanDt = cleanDt + str("\\x"+ c)
    #             else:
    #                 cleanDt = cleanDt + str(c)

    #     else: #so the length isnt 2...
    #         if (i != 0): #dont deal with if its the first element... so there has to be a hex in front of it
    #             c = currDt[:2] #just the hex
    #             if (withX): #add just the hex into the string
    #                 cleanDt = cleanDt + str("\\x"+ c)
    #             else:
    #                 cleanDt = cleanDt + str(c)
                
    #             a = 0
    #             if (i == len(dt) - 1): #if its the last one, will exclude the ')
    #                 a = 2
                
    #             for j in range(2, len(currDt) - a):
    #                 print((currDt[j]))
    #                 c = ord(currDt[j]) #get the associated hex
    #                 c = str(hex(c))[2:]

    #                 if (withX):
    #                     cleanDt = cleanDt + str("\\x"+ c)
    #                 else:
    #                     cleanDt = cleanDt + str(c)

    #         if (i == 0):
    #             for j in range(0, len(currDt)):
    #                 print((currDt[j]))
    #                 c = ord(currDt[j]) #get the associated hex
    #                 c = str(hex(c))[2:]

    #                 if (withX):
    #                     cleanDt = cleanDt + str("\\x"+ c)
    #                 else:
    #                     cleanDt = cleanDt + str(c)
    #     i += 1
    # return cleanDt

#final ver (?)
def DtCleanerfml(frame, withX = True):
    cleanDt = ""
    dt = str(frame.data)[12:]
    dt = dt[:-2]
    print(len(dt))

    if (len(dt)/4 == frame.dlc): #if true: then we only have hex!
        if (withX):
            return dt
        else:
            for i in range (frame.dlc):
                dDt = dt[4 * i: (4*i) + 4]
                dDt = dDt[-2:]
                
                cleanDt = cleanDt + dDt

            return cleanDt
        
    else: #so theres not only hex
        i = 0
        currHex = ""
        while i < len(dt): #if its fully not hex will be fine
            if (i < len(dt) - 1 and dt[i:i+2] == '\\x'): #then the next two values are hex!!!!
                currHex = dt[i+2:i+4] #so thats only the hex
                if (withX):
                    cleanDt = cleanDt + "\\x" + str(currHex)
                
                else:
                    cleanDt = cleanDt + str(currHex)
                i += 4
                # print(dt)
                # print(dt[i])

            else: #the next value is NOT hex, but have to consider special chars (\n and \r)
                if (i < len(dt) - 1 and dt[i:i+2] not in spec.keys()): ##change cond, just placeholder, but will need to handle special chars
                    print(cleanDt)
                    print(dt)
                    print(dt[i:i+2])
                    print(dt[i:i+2] in spec.keys())
                    # if (dt[i: i + 2] == '\\'):
                    #     i += 1
                    #     continue
                    if (dt[i] == '\\'):
                        i += 1
                        continue
                    
                    currV = dt[i]
                    print(currV) #hex value of ascii
                    hexV = ord(currV)
                    hexV = hex(hexV)
                    hexV = str(hexV)
                    hexV = hexV[2:]

                    if (withX):
                        cleanDt = cleanDt + "\\x" + str(hexV)
                
                    else:
                        cleanDt = cleanDt + str(hexV)

                    i += 1
                
                elif (i < len(dt) - 1 and dt[i:i+2] in spec.keys()): #spec
                    currV = dt[i:i+2]
                    hexV = spec[currV]

                    if (withX):
                        cleanDt = cleanDt + "\\x" + str(hexV)
                
                    else:
                        cleanDt = cleanDt + str(hexV)
                    i += 2

                else: #so it is a special char
                    currV = dt[i]
                    hexV = ord(currV)
                    hexV = hex(hexV)
                    hexV = str(hexV)
                    hexV = hexV[2:]

                    if (withX):
                        cleanDt = cleanDt + "\\x" + str(hexV)
                
                    else:
                        cleanDt = cleanDt + str(hexV)
                    
                    i += 1
                

        return cleanDt

def DataClassifier(frame, arr): #arr is the array fromFrameTypeClassifier
    health = None
    if (arr[1] == "first"):
        sn = SerialNumber(frame)
        return sn


    elif (arr[1] == "second"):
        pn = PartNumber(frame)
        ut = UsageTime(frame)
        if (arr[0] in ["Coffee Maker","Steam Oven","Combi Oven", "Espresso Maker", "Air Chiller"]):
            health = HealthMonitor(frame)
        
        return pn, ut, health

def UsageTime(frame):
    cleanDt = DtCleanerfml(frame, False)
    cleanDt = str(cleanDt)[10:14]
    t = str(int(cleanDt, 16))
    return t

def HealthMonitor(frame, arr):
    app = arr[0]

    res = {"Heating system issues": False, "Phase loss": False, "Magnetron issues": False, "Other": False, "Invalid Val": False}
    cleanDt = DtCleanerfml(frame, False)
    cleanDt = str(cleanDt)[14:]
    t = str(int(cleanDt, 16))
    t = str(bin(int(t)))

    if (len(t) < 8):
        t = '0' * (8 - len(t)) + t

    if (t[-1] == '1'):
        if (app != "Combi Oven"):
            res["Invalid Val"] = True #the only one with this hould be the microwave. if not microwave thne die
        res["Magnetron issues"] = True

    if (t[-2] == '1'):
        res["Phase loss"] = True
    
    if (t[-3] == '1'):
        res["Heating system issues"] = True

    if ('1' in t[0:5]):
        res["Other"] = True
    
    return res

def PCIClassifier1(frame):
    dt = str(frame.data)
    dt = DtCleanerfml(frame, False)

    pci = dt[0]
    
    if (pci == '1'):
        return "FstF"
    elif (pci == '2'):
        return "CF"
    
    elif (pci == '3'):
        return "FloC"
    
    elif (pci == '0'):
        return "SF"






def PCIClassifier(frame):
    dt = str(frame.data)
    dt = dt.split("'") #could be an issue later if there are ascii of '

    if ('\\' in dt):
        dt = dt.split('\\')
        print(dt)

    pci = dt[1] #gets the first char
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
        
def getMsgs(sCh):
    try:
        frame = sCh.read()
    except canlib.canNoMsg:
        pass
    except canlib.canError as ex:
        print(ex)


def getAppsConnected(sCh):
    global allApps
    sT = time.time()

    while (time.time() - sT < 0.5):
        try:
            frame = sCh.read()
            if (frame.id in apps.keys()):
                if (apps[frame.id] not in allApps):
                    allApps.append(apps[frame.id])

        except canlib.canNoMsg:
            pass
        except canlib.canError as ex:
            print(ex)



    

