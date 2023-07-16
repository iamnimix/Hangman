import unittest
from random import choice
from hangman import Bank, Player, Processes


class TestHangman(unittest.TestCase):
    def setUp(self) -> None:
        self.word_bank = Bank()
        self.player = Player()
        self.game = Processes()
        self.word_bank.pick_topic()

    def test_pick_topic(self):
        self.assertIn(self.word_bank.current_topic, self.word_bank.topic_names)
        self.assertNotEqual(self.word_bank.current_topic, '')

    def test_manual_topic(self):
        self.word_bank.current_topic = 'Colours'
        self.assertEqual(self.word_bank.current_topic, 'Colours')

    def test_get_word_api(self):
        result = self.word_bank.get_word()
        if result is not False:
            self.assertNotEqual(self.word_bank.current_word, '')
        else:
            self.assertEqual(self.word_bank.current_word, '')
            self.assertFalse(result)

    def test_pick_word(self):
        self.word_bank.pick_word()
        if self.word_bank.current_topic == 'Colours':
            self.assertIn(self.word_bank.current_word, self.word_bank.colours)
        else:
            self.assertIn(self.word_bank.current_word, self.word_bank.animals)

    def test_current_word_display_no_guess(self):
        self.word_bank.pick_word()
        self.word_bank.display()
        self.assertIn('_', self.word_bank.current_word_display)
        self.assertEqual(len(self.word_bank.current_word), len(self.word_bank.current_word_display))

    def test_letter_guessed_solved(self):
        self.assertEqual(self.word_bank.letters_guessed_counter, 0)
        self.assertEqual(self.word_bank.letters_already_guessed, [])

    def test_check_solve(self):
        self.assertTrue(self.word_bank.not_solved)
        self.word_bank.pick_word()
        self.word_bank.display()
        self.assertTrue(self.word_bank.check_solve())

    def test_basic_player_info(self):
        self.assertEqual(self.player.lives, 0)
        self.assertTrue(self.player.guess_validation_incomplete)

    def test_guess(self):
        answer = 'a'
        self.player.guess(answer)
        self.assertEqual(self.player.answer, answer)

    def test_player_lives(self):
        self.word_bank.pick_word()
        self.player.lives = 3 * len(self.word_bank.current_word)
        self.assertEqual(self.player.lives, 3 * len(self.word_bank.current_word))  # !!!!!!

    def test_validate_correct_user_input(self):
        answer = 'a'
        self.player.guess(answer)
        self.assertTrue(self.game.validate_user_input(self.player))
        self.assertFalse(self.player.guess_validation_incomplete)

    def test_validate_incorrect_user_input(self):
        answer = 'as'
        self.player.guess(answer)
        self.assertFalse(self.game.validate_user_input(self.player))
        self.assertTrue(self.player.guess_validation_incomplete)

    def test_check_correct_answer(self):
        self.word_bank.current_word = 'hello'
        self.word_bank.display()
        self.assertEqual(self.word_bank.current_word_display, ['_', '_', '_', '_', '_'])
        self.player.guess('l')
        self.assertEqual(self.game.check_answer_update_lives(self.word_bank, self.player), '\nNice!')
        self.assertEqual(self.word_bank.current_word_display, ['_', '_', 'l', 'l', '_'])
        self.assertEqual(self.word_bank.letters_guessed_counter, 2)
        self.assertEqual(self.word_bank.letters_already_guessed, ['l', 'l'])

    def test_check_incorrect_answer(self):
        self.word_bank.current_word = 'python'
        self.word_bank.display()
        self.assertEqual(self.word_bank.current_word_display, ['_', '_', '_', '_', '_', '_'])
        self.player.guess('z')
        self.game.validate_user_input(self.player)
        self.assertEqual(self.game.check_answer_update_lives(self.word_bank, self.player), '\nNoop! \nLives '
                                                                                           'remaining: {}'.format(
            self.player.lives))
        self.assertEqual(self.word_bank.current_word_display, ['_', '_', '_', '_', '_', '_'])
        self.assertEqual(self.word_bank.letters_guessed_counter, 0)
        self.assertEqual(self.word_bank.letters_already_guessed, ['z'])

    def test_check_already_guessed_answer(self):
        self.word_bank.current_word = 'python'
        self.word_bank.display()
        self.player.guess('z')
        self.game.validate_user_input(self.player)
        self.assertEqual(self.game.check_answer_update_lives(self.word_bank, self.player), '\nNoop! \nLives '
                                                                                           'remaining: {}'.format(
            self.player.lives))
        self.player.guess('z')
        self.assertEqual(self.game.check_answer_update_lives(self.word_bank, self.player), '\nLetter already guessed.')


if __name__ == "__main__":
    unittest.main()
