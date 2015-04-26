myList = ['04', '08', '12', '19', '59']

myList2 = ['10', '20', '30', '45', '55']

myDifference = ['', '', '', '', '']

myChangr = ['+6', '+12', '+18', '+26', '00']

myLists = [myList, myList2]


def compareNumbers(x, y):
    if x > y:
        return '-' + str(abs(x - y))
    elif x < y:
        return '+' + str(abs(y - x))
    else:
        return '00'

def makeNewNumbers(chgr, number):
    if chgr[0] == '+':
        return int(number) + int(chgr[1:])
    elif chgr[0] == '-':
        return int(number) - int(chgr[1:])
    else:
        return int(number)

def makeNewNumbersInRange(chgr, number, yRange):
    results = makeNewNumbers(chgr, number)
    if results > yRange:
        return abs(results - yRange)
    if results < 0:
        return abs(abs(results) - yRange)
    else:
        return results

print(myList)
print(myChangr)

for (i, item) in enumerate(myList):
    print(makeNewNumbersInRange(myChangr[i], item, 59))

# print(makeNewNumbersInRange('-4', '1'))


# for (i, item) in enumerate(myList):
#     myDifference[i] = compareNumbers(int(item), int(myList2[i]))

# print(myList[0], myList[1], myList[2], myList[3], myList[4])
# print(myDifference[0], myDifference[1], myDifference[2], myDifference[3], myDifference[4])