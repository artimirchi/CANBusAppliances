from canlib import canlib, Frame

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
def serialNumber(frame):
    sN = 