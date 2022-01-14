import string
import random

# Todo make sure to catch illegal inputs at every stage of the program


def load_words():  # good
    with open('wordlistlowercase.txt') as word_file:
        valid_words = word_file.read().split()
    return valid_words


def prune_length(bank, target):
    pruned_bank = [word for word in bank if len(word) == len(target)]
    return pruned_bank


def get_legal_letters(bank, used):
    legal = []
    for word in bank:
        for letter in word:
            if letter not in used:
                legal.extend(letter)
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


# todo is prune by bad redundant now?
def prune_by_bad(bank, bad):  # works!!
    for i in range(len(bank)):
        for letter in bad:
            if letter in bank[i]:
                bank[i] = '_'
                break
    while '_' in bank:
        bank.remove('_')
        if '_' not in bank:
            break
    return bank


def prune_by_location(bank, target):
    for i in range(len(bank)):
        word = bank[i]
        for j in range(len(target)):
            if bank[i] == '_':
                continue
            elif target[j] == word[j]:
                continue
            elif target[j] == '_':
                continue
            else:
                bank[i] = '_'
                break
    return [word for word in bank if word != '_']


def print_bot_board(target, bad, lives):
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

    # TODO: catch other bad inputs
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
        print_bot_board(target_word, bad_letters, num_lives)

        # adjust legal_letters, present guess to player and get feedback
        legal_letters = get_legal_letters(word_bank, used_letters)
        guess = guess_letter_freq(legal_letters)
        if not used_letters:
            used_letters = [guess]
        else:
            used_letters.extend(guess)
        print(f'The computer guessed the letter: {guess}.')

        # todo: catch bad inputs for every stage of the feedback section
        feedback = input(f'Is {guess} in your word? y/n: ').lower()

        # lose a life and note the incorrect guess, then prune by bad
        if feedback == 'n':
            bad_letters.extend(guess)
            num_lives -= 1
            word_bank = prune_by_bad(word_bank, guess)

        # If the letter is in the word, get feedback to put the guessed letter in the right place(s)
        elif feedback == 'y' or 'yes':
            cont = True
            while cont:
                print(' '.join(target_word))
                print(f"In which of the blanks does {guess} belong? {feedback_integers}?")
                feedback = input('Please input one numeral at a time: ')
                if int(feedback) in feedback_integers:
                    target_word[int(feedback) - 1] = guess
                # todo: clean up position feedback
                feedback = input(f"Does {guess} appear again in your word {''.join(target_word)}? y/n: ")
                if feedback == 'n':
                    break
            word_bank = prune_by_location(word_bank, target_word)

        if '_' not in target_word:
            print(f"The computer has guessed your word, {''.join(target_word)}!")
            print('Thank you for playing!')
            break
        if num_lives == 0:
            print('The computer has run out of lives and failed to guess your word! Congratulations!')
            break


def hangman_human_guesser():

    num_lives = 6
    legal_letters = [letter for letter in string.ascii_lowercase]
    used_letters = []
    winning_word = 'several'  # random.choice(load_words())
    target_word = [letter if letter in used_letters else '_' for letter in winning_word]

    """Main Loop"""
    while num_lives > 0 and '_' in target_word:
        target_word = [letter if letter in used_letters else '_' for letter in winning_word]

        """prints the board"""
        print('--------------------------------------------------------')
        print(f'Lives: {num_lives}')
        print(f"Incorrect Guesses: {' '.join([letter for letter in used_letters if letter not in target_word])}")
        print(' '.join(target_word))
        print('')
        print('--------------------------------------------------------')
        print(f'TEST Targetword = {target_word}')

        """end of game conditions: winning or losing"""
        if num_lives == 0:
            print(f'You have failed to guess the computer\'s word: {winning_word}. Better luck next time!')
            return
        if '_' not in target_word:
            print(f'Congratulations! You have guessed the word: {winning_word}!')
            return

        """Time for the player to guess a letter"""
        guess = input('Please input the letter you would like to guess: ').lower()

        """"Catch illegal guesses"""
        while guess not in legal_letters:
            guess = input('Please input the letter you would like to guess: ').lower()
            while guess in used_letters:
                guess = input('Please guess a letter that hasn\'t been guessed yet: ').lower()
        used_letters.extend(guess)
        legal_letters.remove(guess)

        """Computer gives feedback"""
        if guess in winning_word:
            print(f'{guess} is in the computer\'s word!')
        else:
            num_lives -= 1
            print(f'{guess} Is not in the computer\'s word. You have lost a life.')


def mode_select():
    print("")
    print("Please select a game mode by typing the corresponding numeral and pressing enter.")
    print('1) The computer will try to guess your word')
    print('2) You will try to guess the computer\'s word')
    need_input = True
    while need_input:
        m = input('Please make your selection: ')
        try:
            int(m)
            if int(m) == 1 or 2:
                need_input = False
                return int(m)
        except ValueError:
            print("I'm sorry, I am looking for an input of 1 or 2.")


if __name__ == '__main__':
    print("""Welcome to MrJawsh\'s hangman game!
            I hope you enjoy playing! :) """)

    # main loop starts here
    keep_playing = True
    while keep_playing:
        mode = mode_select()
        if mode == 1:
            hangman_bot_game()
        elif mode == 2:
            hangman_human_guesser()
        print('')
        print('Would you like to play another game of hangman?')
        again = input('y/n: ').lower()
        if again == 'y':
            continue
        else:
            keep_playing = False
