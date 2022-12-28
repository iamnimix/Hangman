from random import choice
import re


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
        print(f'Topic: {self.current_topic}')

    def get_word(self):
        response = requests.get(f"{self.api}", headers={'X-Api-Key': f"{self.api_key}"}, params={type: 'noun'})
        if response.status_code == 200:
            word = json.loads(response.text)
            self.api_response_status = True
            self.current_word = word['word']
        else:
            self.current_word = choice(self.topics[self.current_topic])
            self.api_response_status = False

    def pick_word(self):
        self.current_word = choice(self.topics[self.current_topic])
        for i in self.current_word:
            self.current_word_display.append('_')
        print(f'Word is {self.current_word} letters long.')
        print(self.current_word_display)

    def check_solve(self):
        self.not_solved = self.letters_guessed_counter < len(self.current_word)


class Player:
    def __init__(self):
        self.lives = 10
        self.answer = ''
        self.guess_validation_incomplete = True

    def guess(self):
        self.answer = input('Guess a letter: ')


class Processes:
    def __init__(self):
        pass

    def validate_user_input(self, player):
        expression = re.match('[a-z]{1,1}$', player.answer)
        if expression == None or len(player.answer) > 1:
            print('\nPlease guess a single alphabet')
        else:
            player.guess_validation_incomplete = False

    def check_answer_update_lives(self, bank, player):
        if player.answer in bank.letters_already_guessed:
            print('\nLetter already guessed.')

        elif player.answer not in bank.current_word:
            player.lives -= 1
            print('\nNope!')
            print('Lives remaining: {}'.format(player.lives))
            bank.letters_already_guessed.append(player.answer)

        else:
            for i in range(len(bank.current_word)):
                if player.answer == bank.current_word[i]:
                    bank.current_word_display[i] = player.answer
                    bank.letters_guessed_counter += 1
                    bank.letters_already_guessed.append(player.answer)
                    print('\nNice!')


class Main:
    def __init__(self):
        pass

    while True:
        word_bank = Bank()
        player1 = Player()
        game = Processes()

        word_bank.pick_topic()
        word_bank.pick_word()

        while word_bank.not_solved and player1.lives > 0:
            while player1.guess_validation_incomplete:
                player1.guess()
                game.validate_user_input(player1)
                game.check_answer_update_lives(word_bank, player1)
            print(word_bank.current_word_display)
            player1.guess_validation_incomplete = True
            word_bank.check_solve()

        if not word_bank.not_solved:
            print('\nYou win!')

        else:
            print('\nYou lose')
            print('Word was {}'.format(word_bank.current_word))

        replay = input('Press any key to play again, x to quit: ')
        print('\n')
        if replay.upper() == 'X':
            break


Play = Main()
Play
del Play