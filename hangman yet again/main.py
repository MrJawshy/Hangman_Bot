import string


def load_words():  # good
    with open('wordlistlowercase.txt') as word_file:
        valid_words = word_file.read().split()
    return valid_words


def prune_length(bank, target):
    pruned_bank = [word for word in bank if len(word) == len(target)]
    return pruned_bank


def get_legal_letters(bank, legal=None, bad=None):  # good
    if bad is None:
        bad = []
    if legal is None:
        legal = []
    if not legal:
        for word in bank:
            for letter in word:
                legal.extend(letter)
        return legal
    elif legal:
        if not bad:
            return legal
        else:
            legal = [letter for letter in legal if letter not in bad]
            return legal


def guess_letter_freq(legal):  # appears to work!
    guess = ''
    guess_count = 0
    for letter in string.ascii_lowercase:
        current = legal.count(letter)
        if current > guess_count:
            guess = letter
            guess_count = current
            continue
        else:
            continue
    return guess


def prune_by_bad(bank, bad):
    bye = []
    new = []
    for letter in string.ascii_lowercase:
        for word in bank:
            if word in bye or new:
                continue
            elif letter in word and bad:
                bye.extend(word)
            else:
                new.extend(word)
    print(bye)
    return new



def prune_by_not_good(bank, target):
    pass


if __name__ == '__main__':
    word_bank = load_words()
