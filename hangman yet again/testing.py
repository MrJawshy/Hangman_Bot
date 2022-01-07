from main import *
from functools import cache

words_list = load_words()
d_words = dict.fromkeys(words_list, [])
bad_letters = ['a', 'b', 'c']
for w in words_list:
    d_words[w] = [letter for letter in w]



def prune_by_bad(dw, words, bad):
    for letter in bad:
        for word in words:
            if letter in word:
                del dw[word]
                continue
            else:
                continue
    return dw


print(len(d_words))
d_words = prune_by_bad(d_words, words_list, bad_letters)
print(len(d_words))
