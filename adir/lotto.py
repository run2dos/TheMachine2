from colorloop import chgListColor
from colorloop import chgType
from colorloop import printColorList

file = open("winnums-text.txt", "r")
tempFile = open("lottoTemp.txt", "+w")

for line in file:
    newln = line.split()
    if len(newln) > 7:
        newln.pop()

    date = newln[0]
    newline2 = [newln[1], newln[2], newln[3], newln[4], newln[5]]

    newline2 = sorted(newline2)
    nonColorLine = str(newline2[0]) + ' ' + str(newline2[1]) + ' ' + str(newline2[2]) + ' ' + str(newline2[3]) + ' ' + str(newline2[4]) + '\n'


    chgType(newline2)
    chgListColor(newline2)
    finalLine ='\n' + 'Date:' + ' ' + date + ' ' + printColorList(newline2)
    if 'T1 T3 T4 T5 T6' in finalLine:
        tempFile.writelines(nonColorLine)
        print(finalLine)

    # print(newline2[0], newline2[1], newline2[2], newline2[3], newline2[4])
file.close()
tempFile.close()
