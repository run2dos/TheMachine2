import itertools
import random
from time import time


def randomLotto(n):
    lottoNumbers = []
    myNum = list(range(1, 60))
    for i in range(n):
        value = random.choice(myNum)
        myNum.remove(value)
        lottoNumbers.append(value)
    return tuple(sorted(lottoNumbers))


# mynumbers = list(range(1,60))

def permu(n, numbers):
    start = time()
    x = 0
    mylist = list(range(1, n + 1))
    for p in itertools.combinations(mylist, 5):
        # print(str(x)+':' ,p)
        x += 1
        if p == numbers:
            print("Found Winner!!! in", (time() - start) * 1000, 'sec...', 'Number:', x)
            break

x = 0
while x < 10:
    myLotto = randomLotto(5)
    print(x, myLotto)
    permu(59, myLotto)
    x += 1
