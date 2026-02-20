from canlib import canlib
from translation import FrameTypeClassifier

coffeeMaker = {0x7E8:"first", 0x7E9: "second", 0x7CA: "requested first", 0x7CB: "requested second"}
combiOven = {0x7D8:"first", 0x7D9:"second",0x7BA:"requested first",0x7BB:"requested second"}
steamOven = {0x7C8:"first",0x7C9:"second",0x7AA:"requested first",0x7A8:"requested second"}
espressoMaker = {0x7B8:"first",0x7B9:"second",0x79A:"requested first",0x79B:"requested second"}
airChiller = {0x7A8:"first",0x7A9:"second",0x78A:"requested first",0x78B:"requested second"}

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
        print(ch.readStatus())
        return ch
    
    else:
        print("\nThe channel selected does not exist")
        return None
    ##can create an exception class to handle this when making the GUI

def GetChannelMsgs(ch, sCh):
    while (True):
        allFrames = []
        allClass = []
        try:
            frame = sCh.read()
            type = FrameTypeClassifier(frame)

            

        except canlib.canNoMsg:
            pass
        except canlib.canError as ex:
            print(ex)