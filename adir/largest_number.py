from functools import reduce

VOWELS = 'a e i o u'.split()
words = ['visions', 'of', 'infinity', 'python', 'squirrel']

def keep_values(character):
    return character[0].lower() in VOWELS

def concatenate(a, b): return a + b

concatenated_words = reduce(concatenate, words)
filtered_letters = list(filter(keep_values, concatenated_words))
print(len(filtered_letters))
print(list(map(keep_values, words)))