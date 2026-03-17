from subsystems.translation import DtCleaner
from canlib import Frame

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
    a = Frame(8847360, data=bytearray(b'\x00\x00\x00\xf0\x07\x00\x00\x00'), dlc=8, flags=0x4, timestamp=49)
    #DtCleaner1(a)

def DTCleaner(frame, withX = True):
    cleanDt = ""
    dt = frame.data
    dDt = (frame.data)[10:]
    if ("\\x" in str(dt)): #could not work, try \\x otherwise
        dt = str(dt).split("\\x") #need to handle corner case of those chars being together in ascii too...... fml
    print(dt)

    i = 0

    while (i < len(dt)):
        currDt = dt[i]
        if (i == 0): #then itll include the bytearray shit
            currDt = currDt[12:]
            if (len(currDt) == 0): #so dt[0] was only the byte array stuff, so its already in hex
                i += 1
                currDt = dt[i]

        if (len(currDt) == 4 and currDt[-1] == ')' and i == len(dt) - 1): #then tis the ' inserted by the sender
            currDt = currDt[:2]
            print(currDt)

        if (len(currDt) == 2): #then its ok
            #print(i)
            if (withX):
                cleanDt = cleanDt + str("\\x"+ currDt)
            else:
                cleanDt = cleanDt + str(currDt)

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

    #print(dDt)


if (__name__ == "__main__"):
    b = Frame(8847360, data=bytearray(b'a\x00\x00\xf0\x07\x1c\x00\x00'), dlc=8, flags=0x4, timestamp=49)
    #b = Frame(460288, data=bytearray(b'\x00\x19'), dlc=3, flags=4, timestamp=1930)

    print(a(b, True))
    #print(dt)
    #main()

