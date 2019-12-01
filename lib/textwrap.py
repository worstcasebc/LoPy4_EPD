import re

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