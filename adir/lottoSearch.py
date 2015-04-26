x = 0

with open("winnums-text.txt", "r") as f:
       searchlines = f.readlines()
for i, line in enumerate(searchlines):
    if "40  12  15  05  27  14" in line:
        x += 1
        for l in searchlines[i:i+1]: print(l, x)