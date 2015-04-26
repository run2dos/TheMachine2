

myList = ['04', '08', '12', '19', '59']
myList2 = ['10', '20', '30', '45', '55']

myLists = [myList, myList2]

COLOR = ''
COLOR1 = '\033[90m'
COLOR2 = '\033[91m'
COLOR3 = '\033[92m'
COLOR4 = '\033[93m'
COLOR5 = '\033[94m'
COLOR6 = '\033[95m'
COLOR7 = '\033[96m'
ENDC = '\033[0m'

numTypes = ('N', 'T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7')
Type = [numTypes[0], numTypes[0], numTypes[0], numTypes[0], numTypes[0]]


def printWithColor(strToColor):
    if int(strToColor) <= 9:
        COLOR = COLOR1
    elif int(strToColor) > 9 and int(strToColor) <= 18:
        COLOR = COLOR2
    elif int(strToColor) > 18 and int(strToColor) <= 27:
        COLOR = COLOR3
    elif int(strToColor) > 27 and int(strToColor) <= 36:
        COLOR = COLOR4
    elif int(strToColor) > 36 and int(strToColor) <= 45:
        COLOR = COLOR5
    elif int(strToColor) > 45 and int(strToColor) <= 54:
        COLOR = COLOR6
    elif int(strToColor) > 54 and int(strToColor) <= 59:
        COLOR = COLOR7
    print(COLOR + strToColor + ENDC)


def chgStrColor(item):
    if int(item) <= 9:
        return COLOR1 + item + ENDC
    elif int(item) > 9 and int(item) <= 18:
        return COLOR2 + item + ENDC
    elif int(item) > 18 and int(item) <= 27:
        return COLOR3 + item + ENDC
    elif int(item) > 27 and int(item) <= 36:
        return COLOR4 + item + ENDC
    elif int(item) > 36 and int(item) <= 45:
        return COLOR5 + item + ENDC
    elif int(item) > 45 and int(item) <= 54:
        return COLOR6 + item + ENDC
    elif int(item) > 54 and int(item) <= 59:
        return COLOR7 + item + ENDC


def findType(item):
    if int(item) <= 9:
        return numTypes[1]
    elif int(item) > 9 and int(item) <= 18:
        return numTypes[2]
    elif int(item) > 18 and int(item) <= 27:
        return numTypes[3]
    elif int(item) > 27 and int(item) <= 36:
        return numTypes[4]
    elif int(item) > 36 and int(item) <= 45:
        return numTypes[5]
    elif int(item) > 45 and int(item) <= 54:
        return numTypes[6]
    elif int(item) > 54 and int(item) <= 59:
        return numTypes[7]


def chgListColor(list):
    for (i, item) in enumerate(list):
        list[i] = chgStrColor(item)


def chgType(list):
    for (i, item) in enumerate(list):
        Type[i] = findType(item)


def printColorList(list):
    return str(list[0]) + ' ' + str(list[1]) + ' ' + str(list[2]) + ' ' + str(list[3]) + ' ' + str(list[4]) + ' ' + str(Type[0]) + ' ' + str(Type[1]) + ' ' + str(Type[2]) + ' ' + str(Type[3]) + ' ' + str(Type[4])


def main():

    for x in myLists:
        chgType(x)
        chgListColor(x)
        printColorList(x)

    # chgType(myList2)
    # chgListColor(myList2)
    # printColorList(myList2)

    print(COLOR1 + '1 ~ 9  ' + ENDC, numTypes[1])
    print(COLOR2 + '10 ~ 18' + ENDC, numTypes[2])
    print(COLOR3 + '19 ~ 27' + ENDC, numTypes[3])
    print(COLOR4 + '28 ~ 36' + ENDC, numTypes[4])
    print(COLOR5 + '37 ~ 45' + ENDC, numTypes[5])
    print(COLOR6 + '46 ~ 54' + ENDC, numTypes[6])
    print(COLOR7 + '55 ~ 59' + ENDC, numTypes[7])

if __name__ == "__main__":
    main()
