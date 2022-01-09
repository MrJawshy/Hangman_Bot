import string


def load_words():  # good
    with open('wordlistlowercase.txt') as word_file:
        valid_words = word_file.read().split()
    return valid_words


def prune_length(bank, target):
    pruned_bank = [word for word in bank if len(word) == len(target)]
    return pruned_bank


def get_legal_letters(bank, legal, bad, used):
    if not legal:
        for word in bank:
            for letter in word:
                legal.extend(letter)
        return legal
    elif legal: 
        print(bad)
        if not used:
            return legal
        else:
            if bad:
                legal = [letter for letter in legal if letter not in bad]
            if used:
                legal = [letter for letter in legal if letter not in used]
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


def prune_by_bad(bank, bad):  # works!!
    for i in range(len(bank)):
        for letter in bad:
            if letter in bank[i]:
                bank[i] = '_'
                break
    while '_' in bank:  # this has the same effect as the commented out code below, but is way cleaner
        bank.remove('_')
        if '_' not in bank:
            break
    # j = 1
    # len_bank = len(bank)
    # while j <= len_bank:
    #     if j >= len_bank:
    #         break
    #     elif bank[j] == '_':
    #         bank.remove(bank[j])
    #         len_bank -= 1
    #         print(f'{j}  {bank[j-1]}')
    #     else:
    #         j += 1
    return bank


def prune_by_not_good(bank, target):  # works!
    for letter in target:
        if letter == '_':
            continue
        else:
            for i in range(len(bank)):
                if letter not in bank[i]:
                    bank[i] = '_'
    while '_' in bank:
        bank.remove('_')
        if '_' not in bank:
            break
    return bank


def print_board(target, bad, lives):
    print('--------------------------------------------------------')
    print(f'Computer\'s Lives: {lives}')
    print(f"Incorrect Guesses: {' '.join(bad)}")
    print(' '.join(target))
    print('')
    print('--------------------------------------------------------')


def count_target_letters(target):
    # get a list of integers, starting with one, an integer for each blank
    fbi = [i + 1 for i in range(len(target))]
    return fbi


def hangman_bot_game():
    # initialize variables needed for game
    num_lives = 6
    word_bank = load_words()
    bad_letters = []
    legal_letters = []
    used_letters = list()
    print('Welcome to a game of hangman! In this game, you will think of a word and the computer will try to guess it.')
    print('When you have thought of a word, please enter an _ for each letter of the word, with spaces in between.')
    print('For example: for "word" you would enter _ _ _ _')
    target_word = input('Enter your blanks here, then press Enter: ').split()

    # catch empty inputs
    while len(target_word) < 1:
        target_word = input('please enter at least one underscore.').split()
        if len(target_word) >= 1:
            break

    print(f'Thank you! Your word is {len(target_word)} letters long.')
    word_bank = prune_length(word_bank, target_word)
    feedback_integers = count_target_letters(target_word)

    # main loop
    while num_lives > 0 and '_' in target_word:
        print_board(target_word, bad_letters, num_lives)

        # adjust legal_letters, present guess to player and get feedback
        print(f'used: {used_letters}')
        
        legal_letters = get_legal_letters(word_bank, legal_letters, bad_letters, used_letters)
        
        guess = guess_letter_freq(legal_letters)
        if not used_letters:
            used_letters = [guess]
        else:
            used_letters.extend(guess)
        print(f'The computer guessed the letter: {guess}.')
        feedback = input(f'Is {guess} in your word? y/n: ').lower()

        # lose a life and note the incorrect guess, then prune by bad
        if feedback == 'n':
            bad_letters.extend(guess)
            num_lives -= 1
            word_bank = prune_by_bad(word_bank, guess)

        # loop for getting feedback on the guess, and changing target_word to reflect new letters
        elif feedback == 'y' or 'yes':
            cont = True
            while cont:
                print(' '.join(target_word))
                print(f"In which of the blanks does {guess} belong? {feedback_integers}?")
                feedback = input('Please input one numeral at a time: ')
                if int(feedback) in feedback_integers:
                    target_word[int(feedback) - 1] = guess
                feedback = input(f"Does {guess} appear again in your word {''.join(target_word)}? y/n: ")
                if feedback == 'n':
                    cont = False
                    feedback = 0
                    break

        if '_' not in target_word:
            print(f"The computer has guessed your word, {''.join(target_word)}!")
            print('Thank you for playing!')
            break
        if num_lives == 0:
            print('The computer has run out of lives and failed to guess your word! Congratulations!')
            break


if __name__ == '__main__':
    hangman_bot_game()
