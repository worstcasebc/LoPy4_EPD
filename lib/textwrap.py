import re
import time

# create a pattern, that will match the line-break
pLF = re.compile('\n')

def wrap(data, columns, linebreak=True):
    mBlock = pLF.split(data)
    sElem = []

    for i in range(len(mBlock)):

        sPart = str(mBlock[i])
        while (len(sPart) > columns):
            end = sPart.rfind(' ', 0, columns)
            if end < 0:
                end = columns
            sElem.append(sPart[0:end])
            sPart = sPart[end+1:len(sPart)]

        if len(sPart) > 2:
            sElem.append(sPart)

        if linebreak and (not i == len(mBlock)):
            sElem.append('')
    
    return sElem

def wrapWidth(data, screenWidth, widthArray, tRow, linebreak=True):
    mBlock = pLF.split(data)
    line = ""
    sElem = []

    for i in range(len(mBlock)):
        sPart = str(mBlock[i])
        sPartEnd = 0
        line = ""
        lineLength = 0
        wordLength = 0
        wordStart = 0
        wordEnd = 0

        while (not sPartEnd) and (len(sElem) <= tRow):
            wordEnd = sPart.find(' ', wordStart)
            if (wordEnd < 0):
                sPartEnd = 1
                wordEnd = len(sPart) - 1
            word = sPart[wordStart:wordEnd + 1]

            for a in range(len(word)):
                oc = ord(word[a])
                if oc >= 32 and oc <=126:
                    wordLength += widthArray[oc-32]
                else:
                    #print("character unknown")
                    wordLength += widthArray[0]

            if (lineLength + wordLength) < screenWidth:
                line += word
                lineLength += wordLength
                wordLength = 0
                wordStart = wordEnd + 1
            else:
                sElem.append(line)
                line = word
                lineLength = wordLength
                wordLength = 0
                wordStart = wordEnd + 1
        
        sElem.append(line)
        
        wordStart = 0
        wordEnd = 0
    
    return sElem 