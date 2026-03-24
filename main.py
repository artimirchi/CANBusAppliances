from subsystems.translation import DtCleaner, SerialNumber, PartNumber, DtCleanerfml, DataClassifier, UsageTime, HealthMonitor, SelectChannel, allApps
from canlib import Frame, canlib
from subsystems.channels import GetChannelsConnected

bitRatesCnst = {1: canlib.Bitrate.BITRATE_10K,2: canlib.Bitrate.BITRATE_50K,3: canlib.Bitrate.BITRATE_62K,4: canlib.Bitrate.BITRATE_83K,5: canlib.Bitrate.BITRATE_100K,6: canlib.Bitrate.BITRATE_125K,7: canlib.Bitrate.BITRATE_250K,8: canlib.Bitrate.BITRATE_500K,9: canlib.Bitrate.BITRATE_1M}
channelStatus = {1:"Error passive", 2: "Bus Off",4:"Error warning",8: "Error active",10:"Some msgs are pending transmission",40:"Works",20:"There are some msgs in the receive buffer",80:"Theres at least one TX error",100:"Theres at least one RX error",200:"Theres one HW buffer overflow",400:"Theres one SW buffer overflow"}
bitRates = {1: "10kbps",2: "50kbps",3: "62kbps",4: "83kbps",5: "100kbps",6: "125kbps",7: "250kbps",8: "500kbps",9: "1Mbps"}


# def DtCleaner1(frame, withX = False):
#     cleanDt = ""
#     dt = frame.data
#     dDt = (frame.data)[12:]
#     if ("\\x" in dt): #could not work, try \\x otherwise
#         dt = dt.split("\\x") #need to handle corner case of those chars being together in ascii too...... fml
    
#     for i in range (len(dt)):
#         currDt = dt[i]
#         if (len(currDt) == 2): #then its ok
#             if (withX):
#                 cleanDt = cleanDt + str("\\x"+ currDt)
#             else:
#                 cleanDt = cleanDt + str(currDt)
        
#         else:
#             if (i == 0 and dDt[0] != 'x'): #so its the first set of chars, and we start with ascii... so all of them are ascii
#                 for j in range (len(currDt)):
#                     hexV = hex(ord(currDt[j])) #converts to hex
#                     if (withX):
#                         cleanDt = cleanDt + str("\\x"+ hexV)
#                     else:
#                         cleanDt = cleanDt + str(hexV)
            
#             else: #so we start with hex, then have the ascii
#                 for j in range (len(currDt)):
#                     if (j == 0):
#                         v = currDt[:2]
#                         cleanDt = cleanDt + v
#                     else:
#                         hexV = hex(ord(currDt[j])) #converts to hex
#                         if (withX):
#                             cleanDt = cleanDt + str("\\x"+ hexV)
#                         else:
#                             cleanDt = cleanDt + str(hexV)
#     return cleanDt


def main():
    a = Frame(8847360, data=bytearray(b'aaaaaaaa'), dlc=8, flags=0x4, timestamp=49)
    #DtCleaner1(a)

# def DTCleaner(frame, withX = True):
#     cleanDt = ""
#     dt = frame.data
#     dDt = (frame.data)[10:]
#     if ("\\x" in str(dt)): #could not work, try \\x otherwise
#         dt = str(dt).split("\\x") #need to handle corner case of those chars being together in ascii too...... fml
#     print(dt)

#     i = 0

#     while (i < len(dt)):
#         currDt = dt[i]
#         if (i == 0): #then itll include the bytearray shit
#             currDt = currDt[12:]
#             if (len(currDt) == 0): #so dt[0] was only the byte array stuff, so its already in hex
#                 i += 1
#                 currDt = dt[i]

#         if (len(currDt) == 4 and currDt[-1] == ')' and i == len(dt) - 1): #then tis the ' inserted by the sender
#             currDt = currDt[:2]
#             print(currDt)

#         if (len(currDt) == 2): #then its ok
#             #print(i)
#             if (withX):
#                 cleanDt = cleanDt + str("\\x"+ currDt)
#             else:
#                 cleanDt = cleanDt + str(currDt)

#         else: #so the length isnt 2...
#             if (i != 0): #dont deal with if its the first element... so there has to be a hex in front of it
#                 c = currDt[:2] #just the hex
#                 if (withX): #add just the hex into the string
#                     cleanDt = cleanDt + str("\\x"+ c)
#                 else:
#                     cleanDt = cleanDt + str(c)
                
#                 a = 0
#                 if (i == len(dt) - 1): #if its the last one, will exclude the ')
#                     a = 2
                
#                 for j in range(2, len(currDt) - a):
#                     print((currDt[j]))
#                     c = ord(currDt[j]) #get the associated hex
#                     c = str(hex(c))[2:]

#                     if (withX):
#                         cleanDt = cleanDt + str("\\x"+ c)
#                     else:
#                         cleanDt = cleanDt + str(c)

#             if (i == 0):
#                 for j in range(0, len(currDt)):
#                     print((currDt[j]))
#                     c = ord(currDt[j]) #get the associated hex
#                     c = str(hex(c))[2:]

#                     if (withX):
#                         cleanDt = cleanDt + str("\\x"+ c)
#                     else:
#                         cleanDt = cleanDt + str(c)
#         i += 1
#     return cleanDt

    #print(dDt)

def test1():
    b = Frame(8847360, data=bytearray(b'\x0E\x05\x01\x86\x9f'), dlc=2, flags=0x4, timestamp=49)
    print(DtCleanerfml(b))

def test2(): #ok
    b = Frame(8847360, data=bytearray(b'aaaaaaaaa'), dlc=2, flags=0x4, timestamp=49)
    print(DtCleanerfml(b))

def test3(): #ok
    b = Frame(8847360, data=bytearray(b'\x0a\x0d09'), dlc=2, flags=0x4, timestamp=49)
    print(DtCleanerfml(b))

def test4(): #ok
    b = Frame(8847360, data=bytearray(b'\x0E\x05\x01\x86\x9f'), dlc=2, flags=0x4, timestamp=49)
    print(DtCleanerfml(b))

def test5(): #ok
    b = Frame(8847360, data=bytearray(b'\x0E\x05ad65)'), dlc=2, flags=0x4, timestamp=49)
    print(DtCleanerfml(b))

def test6(): #ok
    b = Frame(8847360, data=bytearray(b'\x0E\x05zxsofkegppl'), dlc=2, flags=0x4, timestamp=49)
    print(DtCleanerfml(b))

def test7(): #ok
    b = Frame(8847360, data=bytearray(b'\xAA\\XFDa'), dlc=2, flags=0x4, timestamp=49)
    print(DtCleanerfml(b))

def test8(): #ok
    b = Frame(8847360, data=bytearray(b'\xAA\xFDA'), dlc=2, flags=0x4, timestamp=49)
    print(DtCleanerfml(b))

def test9():
    b = Frame(8847360, data=bytearray(b'\x10\x0F\x0e\x05\x01\x86b'), dlc=2, flags=0x4, timestamp=49)
    arr = [5, "first"]

    print(DataClassifier(b, arr))

def test10():
    b = Frame(8847360, data=bytearray(b'\x21\x2F\xb0\xea\x09\x7e\xf4\x02'), dlc=2, flags=0x4, timestamp=49)
    print(UsageTime(b))

def test11():
    b = Frame(8847360, data=bytearray(b'\x21\x2F\xb0\xea\x09\x7e\xf4\x02'), dlc=2, flags=0x4, timestamp=49)
    print(PartNumber(b))

def test12():
    b = Frame(8847360, data=bytearray(b'\x21\x2F\xb0\xea\x09\x7e\xf4\x02'), dlc=2, flags=0x4, timestamp=49)
    print(HealthMonitor(b))


def main1():
    a = GetChannelsConnected()
    for i in range (canlib.getNumberOfChannels()):
        print(str(a[i].channel_number) + ". " + a[i].channel_name)

    ch = int(input("Select the channel number you wish to use:"))

    #select the bitrate to use (for the WS, use 83.33 kbps)
    print("Select the bitrate you wish to use")
    bR = int(input(bitRates))

    sBR = bitRatesCnst[bR]
    sCh = SelectChannel(ch, sBR)

    for i in range(len(allApps)):
        print("\n" + i + ". " + allApps[i])

    c = input("Select the appliance you wish to monitor. You can select multiple, but include commas between their assigned numbers.")

    if (',' in c): #so multiple included
        c = list(c.split(','))

    else:
        c = [c]

def getMsgs(sCh):
    try:
        frame = sCh.read()
    except canlib.canNoMsg:
        pass
    except canlib.canError as ex:
        print(ex)
    

    



        

if (__name__ == "__main__"):
    # test1()
    # test2()
    # test3()
    # test4()
    #test9()
    #test10()
    #test11()
    #test12()
    #test6()
    #test7()
    #b = Frame(460288, data=bytearray(b'\x00\x19'), dlc=3, flags=4, timestamp=1930)
    main1()
    #print(DtCleaner(b))
    
    #print(DtCleanerfml(b))
    #print(dt)
    #main()

