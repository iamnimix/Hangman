import json
from random import choice
import re
import requests


class Bank:
    colours = ['red', 'blue']
    animals = ['dog', 'cat']
    topic_names = ['Colours', 'Animals']
    topics = {'Colours': colours, 'Animals': animals}
    api = 'https://api.api-ninjas.com/v1/randomword'
    api_key = 'FRkfTIwrgLLk+4TIMd+NMA==m6isKOfXzCLPgdGz'

    def __init__(self):
        self.current_topic = ''
        self.current_word = ''
        self.current_word_display = []
        self.letters_guessed_counter = 0
        self.not_solved = True
        self.letters_already_guessed = []

    def pick_topic(self):
        self.current_topic = choice(self.topic_names)
        return f'Topic: {self.current_topic}'

    def get_word(self):
        try:
            response = requests.get(f"{self.api}", headers={'X-Api-Key': f"{self.api_key}"}, params={type: 'noun'})
            if response.status_code == 200:
                word = json.loads(response.text)
                self.api_response_status = True
                self.current_word = word['word']
                return self.current_word
        except requests.exceptions.ConnectionError:
            self.api_response_status = False
            return self.api_response_status

    def pick_word(self):
        self.current_word = choice(self.topics[self.current_topic])
        return self.current_word

    def display(self):
        for i in self.current_word:
            self.current_word_display.append('_')
        return self.current_word_display

    def check_solve(self):
        self.not_solved = "_" in self.current_word_display
        return self.not_solved


class Player:
    def __init__(self):
        self.lives = 0
        self.answer = ''
        self.guess_validation_incomplete = True

    def guess(self, answer):
        self.answer = answer
        return self.answer


class Processes:
    def __init__(self):
        pass

    def validate_user_input(self, player):
        self.expression = re.match('(?i)[a-z]', player.answer)
        if self.expression is None or len(player.answer) > 1:
            return False
        else:
            player.guess_validation_incomplete = False
            return True

    def check_answer_update_lives(self, bank, player):
        if player.answer in bank.letters_already_guessed:
            return '\nLetter already guessed.'

        elif player.answer not in bank.current_word:
            if self.expression is not None and len(player.answer) == 1:
                player.lives -= 1
            bank.letters_already_guessed.append(player.answer)
            return '\nNoop! \nLives remaining: {}'.format(player.lives)

        else:
            for i in range(len(bank.current_word)):
                if player.answer == bank.current_word[i]:
                    bank.current_word_display[i] = player.answer
                    bank.letters_guessed_counter += 1
                    bank.letters_already_guessed.append(player.answer)
            return '\nNice!'


# class Main:
#     def __init__(self):
#         pass
#
#     while True:
#         word_bank = Bank()
#         word_bank.get_word()
#
#         if not word_bank.api_response_status:
#             print(word_bank.pick_topic())
#             word_bank.pick_word()
#             word_bank.display()
#             print(word_bank.current_word_display)
#             print(f'Word is {len(word_bank.current_word)} letters long.')
#         else:
#             word_bank.display()
#             print(word_bank.current_word_display)
#             print(f'Word is {len(word_bank.current_word)} letters long.')
#
#         player1 = Player()
#         player1.lives = 3 * len(word_bank.current_word)
#         game = Processes()
#
#         while word_bank.not_solved and player1.lives > 0:
#             while player1.guess_validation_incomplete:
#                 answer = input('Guess a letter: ')
#                 player1.guess(answer)
#                 check_input = game.validate_user_input(player1)
#                 if not check_input:
#                     print('\nPlease guess a single alphabet')
#                 result = game.check_answer_update_lives(word_bank, player1)
#                 print(result)
#             print(word_bank.current_word_display)
#             player1.guess_validation_incomplete = True
#             word_bank.check_solve()
#
#         if not word_bank.not_solved:
#             print('\nYou win!')
#
#         else:
#             print('\nYou lose')
#             print('Word was {}'.format(word_bank.current_word))
#
#         replay = input('Press any key to play again, x to quit: ')
#         print('\n')
#         if replay.upper() == 'X':
#             break
#
#
# Play = Main()
