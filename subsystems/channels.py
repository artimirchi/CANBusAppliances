from canlib import canlib, Frame
from subsystems.translation import FrameTypeClassifier, PCIClassifier, PartNumber, SerialNumber, UsageTime, HealthMonitor, getAppsConnected, allApps, PCIClassifier1
import keyboard

coffeeMaker = {0x7E8:"first", 0x7E9: "second", 0x7CA: "requested first", 0x7CB: "requested second"}
combiOven = {0x7D8:"first", 0x7D9:"second",0x7BA:"requested first",0x7BB:"requested second"}
steamOven = {0x7C8:"first",0x7C9:"second",0x7AA:"requested first",0x7A8:"requested second"}
espressoMaker = {0x7B8:"first",0x7B9:"second",0x79A:"requested first",0x79B:"requested second"}
airChiller = {0x7A8:"first",0x7A9:"second",0x78A:"requested first",0x78B:"requested second"}


#dicts
channelStatus = {1:"Error passive", 2: "Bus Off",4:"Error warning",8: "Error active",10:"Some msgs are pending transmission",40:"Works",20:"There are some msgs in the receive buffer",80:"Theres at least one TX error",100:"Theres at least one RX error",200:"Theres one HW buffer overflow",400:"Theres one SW buffer overflow"}


#helper function to obtain data on all the channels connected to the device
def GetChannelsConnected():
    allChData = []
    for ch in range (canlib.getNumberOfChannels()):
        chData = canlib.ChannelData(ch)
        allChData.append(chData)
	
    return allChData


#helper function to select and set up the channel to use
def SelectChannel(s, bitRate):
    if (s < canlib.getNumberOfChannels()):
        ##not sure if i need to flag anything......
        ch = canlib.openChannel(s, bitrate=bitRate)
        ch.busOn()
        print(bitRate)
        print("\nThe bus has been turned on.")
        print("\nCurrent status:" + str(channelStatus[ch.readStatus()]))
        return ch
    
    else:
        print("\nThe channel selected does not exist")
        return None
    ##can create an exception class to handle this when making the GUI

def GetChannelMsgs(ch, sCh, sel):
    pNS = {}
    sNS = {}
    uTS = {}
    hMS = {}

    while (True):
        allFrames = []
        allClass = []
        try:
            frame = sCh.read() #get da frame
            type = FrameTypeClassifier(frame) #who + type
            if (type[0] not in sel):
                continue
            pci = PCIClassifier(frame) #get the frame type

            if (pci == "FstF"):
                sN = SerialNumber(frame)
                
                if (type[0] not in sNS.keys() or sNS[type[0]] != sN):
                    sNS[type[0]] = sN
                    print("\nThe serial number of the " +type[0] + " is " + str(sN))

            elif (pci == "CF"):
                pN = PartNumber(frame)

                if (type[0] not in pNS.keys() or pNS[type[0]] != pN):
                    pNS[type[0]] = pN
                    print("\nThe part number of the " +type[0] + " is " + str(pN))
            
                uT = UsageTime(frame)
                if (type[0] not in uTS.keys() or uTS[type[0]] != uT):
                    uTS[type[0]] = uT
                    print("\nThe total usage time of the " + type[0]+"is " + str(uT) +" hours")

                hM = HealthMonitor(frame, type)
                if (type[0] not in hMS.keys() or hMS[type[0]] != hMS):
                    if (hM["Heating system issues"] == True):
                        print("The " + type[0] +" has heating system issues")
                    if (hM["Phase loss"] == True):
                        print("The " + type[0] +" has phase loss issues")
                    if (hM["Magnetron issues"] == True):
                        print("The " + type[0] +" has magnetron issues")
                    if (hM["Heating system issues"] == False and hM["Phase loss"] == False and hM["Magnetron issues"] == False):
                        print("\nNo issues found with "+type[0])
                    
        except canlib.canNoMsg:
            pass
        except canlib.canError as ex:
            print(ex)


def GetChannelMsgstest(ch = None, sCh = None, sel = None):
    pNS = {}
    sNS = {}
    uTS = {}
    hMS = {}

    while (True):
        allFrames = []
        allClass = []
        try:
            #frame = Frame(0x7e8, data=bytearray(b'\x10\x0F\x0E\x05\x01\x86\x9F'), dlc=5, flags=0x2, timestamp=49)
            #frame = Frame(0x7e9, data=bytearray(b'\x21\x2f\xb0\xea\x09\x7e\xf4\x02'), dlc=5, flags=0x2, timestamp=49)
            #frame = Frame(0x7e8, data=bytearray(b'\x10\x0F\x19\x06\x00\x01\x29'), dlc=5, flags=0x2, timestamp=49) #ok
            #frame = Frame(0x7e9, data=bytearray(b'\x21\x2f\xb0\xeB\x09\x7e\xf4\x02'), dlc=5, flags=0x2, timestamp=49)
            #frame = Frame(0x7e9, data=bytearray(b'\x21\x00\x00\x00\x04\xB0\xf4\x02'), dlc=5, flags=0x2, timestamp=49)
            frame = Frame(0x7e9, data=bytearray(b'\x21\x35\xf1\x35\x09\x7E\xf4\x02'), dlc=5, flags=0x2, timestamp=49)


            #frame = Frame(0x7e8, data=bytearray(b'\x10\x0F\x11\x0B\x00\x1B\x3B'), dlc=5, flags=0x2, timestamp=49)
            #frame = Frame(0x7e8, data=bytearray(b'\x10\x0F\x19\x06\x00\x01\x26'), dlc=5, flags=0x2, timestamp=49)
            #frame = Frame(0x7e8, data=bytearray(b'\x10\x0F\x19\x0A\x00\x9D\xAD'), dlc=5, flags=0x2, timestamp=49)
            #frame = Frame(0x7e8, data=bytearray(b'\x10\x0F\x19\x0B\x00\x9E\x3F'), dlc=5, flags=0x2, timestamp=49)
            #frame = Frame(0x7e8, data=bytearray(b'\x10\x0F\x19\x07\x00\x01\x29'), dlc=5, flags=0x2, timestamp=49)
            #frame = Frame(0x7e8, data=bytearray(b'\x10\x0F\x11\x0B\x00\x02\xB9'), dlc=5, flags=0x2, timestamp=49)

            type = FrameTypeClassifier(frame) #who + type
            # if (type[0] not in sel):
            #     continue
            pci = PCIClassifier1(frame) #get the frame type

            if (pci == "FstF"):
                sN = SerialNumber(frame)
                
                if (type[0] not in sNS.keys() or sNS[type[0]] != sN):
                    sNS[type[0]] = sN
                    print("\nThe serial number of the " +type[0] + " is " + str(sN))

            elif (pci == "CF"):
                pN = PartNumber(frame)

                if (type[0] not in pNS.keys() or pNS[type[0]] != pN):
                    pNS[type[0]] = pN
                    print("\nThe part number of the " +type[0] + " is " + str(pN))
            
                uT = UsageTime(frame)
                if (type[0] not in uTS.keys() or uTS[type[0]] != uT):
                    uTS[type[0]] = uT
                    print("\nThe total usage time of the " + type[0]+" is " + str(uT) +" hours")

                hM = HealthMonitor(frame, type)
                if (type[0] not in hMS.keys() or hMS[type[0]] != hMS):
                    if (hM["Heating system issues"] == True):
                        print("The " + type[0] +" has heating system issues")
                    if (hM["Phase loss"] == True):
                        print("The " + type[0] +" has phase loss issues")
                    if (hM["Magnetron issues"] == True):
                        print("The " + type[0] +" has magnetron issues")
                    if (hM["Heating system issues"] == False and hM["Phase loss"] == False and hM["Magnetron issues"] == False):
                        print("\nNo issues found with "+type[0])
                    
        except canlib.canNoMsg:
            pass
        except canlib.canError as ex:
            print(ex)

def getAppSelection():
    getAppsConnected()

    for i in range(len(allApps)):
        print("\n" + i + ". " + allApps[i])

    c = input("Select the appliance you wish to monitor. You can select multiple, but include commas between their assigned numbers.")
    c = c.split(',')

    a = []

    for i in range (len(c)):
        if (c[i] > len(allApps)):
            print("\nThe selected appliance no." +c[i]+ " does not exist. Its selection will be ignored.")
        else:
            a.append(c[i])

    if (len(a) == 0):
        return None
    
    else:
        return a
                

            
