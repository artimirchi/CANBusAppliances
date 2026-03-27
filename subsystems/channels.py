from canlib import canlib
from subsystems.translation import FrameTypeClassifier, PCIClassifier, PartNumber, SerialNumber, UsageTime, HealthMonitor, getAppsConnected, allApps

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
                pN = SerialNumber(frame)
            elif (pci == "CF"):
                pN = PartNumber(frame)
                uT = UsageTime(frame)
                hM = HealthMonitor(frame)

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
                

            
