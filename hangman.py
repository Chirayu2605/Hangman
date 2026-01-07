import random
from os import system, name
import pandas as pd


def decorator(f):
    def wrapper(self,*args):
        print('--------------------------------------------')
        res=f(self,args[0])
        print('--------------------------------------------')
        return res
    return wrapper
class Game():
    df =  pd.read_excel('hangman.xlsx')
    df.dropna(inplace=True)
    # test = {'Easy':'APPLE', 'Medium':'BANANA', 'Hard':'POMEGRANATE'}
    words = {'Easy':df['Easy'].tolist(), 'Medium':df['Medium'].tolist(), 'Hard':df['Hard'].tolist()}
    hangman = {0:('     ',
                 '     ',
                 '     '),
               1:('  O  ',
                 '     ',
                 '     '),
               2:('  O  ',
                  '  |  ',
                  '     '),
                3:('  O  ',
                   ' /|  ',
                  '     '),
                4:('  O  ',
                   ' /|\\ ',
                   '     '),
                5:('  O  ',
                   ' /|\\ ',
                   ' /   '),
                6:('  O  ',
                   ' /|\\ ',
                   ' / \\ ')}
    def __init__(self):
        self.guessed = []
        self.attempts=0
        print("------------ Welcome to Hangman -----------")
        self.rules()
        self.level = str(input("Choose difficulty level (Easy/Medium/Hard): ")).capitalize()
        # self.word = Game.test[self.level] 
        self.word = random.choice(Game.words[self.level])
        self.word_completion = ' _ ' * len(self.word)
        print(f"The word has {len(self.word)} letters.")
        over = False
        tries = 0 
        while not over:
            over,tries=self.game_loop(over,tries)
        self.display("-------Thank you for playing Hangman!-------")
    @decorator
    def display(self,n):
        widhth = 44
        print(n.center(widhth))
    def game_loop(self,over,tries):
        print('\n'.join(Game.hangman[tries]))
        self.display(self.word_completion)
        guess = input('Your guess:').upper()
        if guess.isnumeric() or guess.isspace() or len(guess)!=1:
            self.display(f'Invalid input. Please enter a letter. Only {3-self.attempts+1} wrong attempts more will be allowed.')
            self.attempts += 1
            if self.attempts == 5:
                print(f'You lost! The word was: {self.word}')
                return True,tries
            return self.game_loop(over,tries)
        elif guess in self.guessed:
            self.display('Already guessed, retry!')
            return self.game_loop(over,tries)
        else:
            return self.check_the_guess(guess,tries)
            
    def check_the_guess(self,guess,tries):
        if guess in self.word:
            self.guessed.append(guess)
            print(f'Good job! {guess} is in the word.')
            word_as_list = list(self.word_completion)
            indices = [i for i, letter in enumerate(self.word) if letter == guess]
            for index in indices:
                word_as_list[(index*3)+1] = guess
            self.word_completion = ''.join(word_as_list)
            if ' _ ' not in self.word_completion:
                print('\n'.join(Game.hangman[tries]))
                self.display(f'Congratulations! You guessed the word: {self.word}')
                return True,tries
            return False,tries
        else:
            self.guessed.append(guess)
            print(f'Sorry, {guess} is not in the word.')
            tries += 1
            if tries == 6:
                print('\n'.join(Game.hangman[tries]))
                self.display(f'You lost! The word was: {self.word}')
                return True,tries
            return False,tries
    def rules(self):
        self.display("""------------------ Rules  -----------------
1. You have 6 attempts to guess the word.
2. You can guess one letter at a time.
3. If you guess a letter correctly, it will be revealed in the word.
4. If you guess incorrectly, a part of the hangman will be drawn.
5. The game ends when you either guess the word or the hangman is fully drawn.""")
# if __name__ == "__main__":
#     game = Game()