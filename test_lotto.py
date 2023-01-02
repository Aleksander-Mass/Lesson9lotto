import pytest
import builtins
from Lotto import Cart, PlayerComp, PlayerHuman, Game

class TestCart:
    def setup(self):
        self.cart = Cart()

    def teardown(self):
        del self.cart

    def test_init(self):
        assert len(self.cart.cart) == 3

        for item in self.cart.cart:
            assert len(item) == 10

    def test_create_cart(self):
        cart = self.cart.create_cart()
        assert len(cart) == 3

    def test_is_not_empty(self):
        assert self.cart.is_empty == False

    def test_is_empty(self):
        numbers = self.cart.get_cart_numbers()
        print(numbers)
        for number in numbers:
            self.cart.cross_out(number)
        assert self.cart.is_empty == True

    def test_get_cart_numbers(self):
        assert len(self.cart.get_cart_numbers()) == 15

    def test_contains(self):
        numbers = self.cart.get_cart_numbers()
        for number in numbers:
            assert (number in self.cart) == True

    def test_cross_out_success(self):
        numbers = self.cart.get_cart_numbers()
        assert self.cart.cross_out(numbers[5]) == True

    def test_cross_out_fail(self):
        assert self.cart.cross_out(1000) == False

    def test_str(self):
        assert str(self.cart) != ''

    def test_eq(self):
        cart1 = Cart()
        cart1.cart = [['#', '11', '#', '#', '44', '50', '65', '71', '80', '93'],
                      ['#', '15', '#', '#', '45', '51', '#', '#', '83', '94'],
                      ['#', '16', '#', '#', '49', '55', '#', '#', '#', '#']]
        cart2 = Cart()
        cart2.cart = [['#', '11', '#', '#', '44', '50', '65', '71', '80', '93'],
                      ['#', '15', '#', '#', '45', '51', '#', '#', '83', '94'],
                      ['#', '16', '#', '#', '49', '55', '#', '#', '#', '#']]

        assert cart1 == cart2

    def test_ne(self):
        cart1 = Cart()
        cart2 = Cart()
        assert cart1 != cart2

    def test_ne_other_type(self):
        assert self.cart != 5

class TestPlayerComp:
    def setup(self):
        self.playerComp = PlayerComp()

    def teardown(self):
        del self.playerComp

    def test_init(self):
        assert self.playerComp.cart.is_empty == False
        assert self.playerComp.name != ''

    def test_step(self):
        numbers = self.playerComp.cart.get_cart_numbers()
        assert self.playerComp.step(numbers[5]) == True

    def test_step_fail(self):
        assert self.playerComp.step(1000) == True

    def test_str(self):
        assert str(self.playerComp) != ''

    def test_eq(self):
        otherPlayerComp = PlayerComp()
        otherPlayerComp.name = self.playerComp.name
        otherPlayerComp.cart = self.playerComp.cart
        assert self.playerComp == otherPlayerComp

    def test_ne(self):
        otherPlayerComp = PlayerComp()
        assert self.playerComp != otherPlayerComp

    def test_ne_other_type(self):
        assert self.playerComp != 5

class TestPlayerHuman:
    def setup(self):
        builtins.input = lambda s: 'Max'
        self.playerHuman = PlayerHuman()

    def teardown(self):
        del self.playerHuman

    def test_init(self):
        assert self.playerHuman.cart.is_empty == False
        assert self.playerHuman.name == 'Max'

    def test_step_incorrect_input(self):
        inputs = ['Да', 'Д']
        builtins.input = lambda s: inputs.pop(0)
        numbers = self.playerHuman.cart.get_cart_numbers()
        assert self.playerHuman.step(numbers[5]) == True

    def test_step_success_yes(self):
        builtins.input = lambda s: 'Д'
        numbers = self.playerHuman.cart.get_cart_numbers()
        assert self.playerHuman.step(numbers[5]) == True

    def test_step_success_no(self):
        builtins.input = lambda s: 'Н'
        assert self.playerHuman.step(1000) == True

    def test_step_fail_yes(self):
        builtins.input = lambda s: 'Д'
        assert self.playerHuman.step(1000) == False

    def test_step_fail_no(self):
        builtins.input = lambda s: 'Н'
        numbers = self.playerHuman.cart.get_cart_numbers()
        assert self.playerHuman.step(numbers[5]) == False

    def test_str(self):
        assert str(self.playerHuman) != ''

    def test_eq(self):
        builtins.input = lambda s: 'Max'
        otherPlayerHuman = PlayerHuman()
        otherPlayerHuman.name = self.playerHuman.name
        otherPlayerHuman.cart = self.playerHuman.cart
        assert self.playerHuman == otherPlayerHuman

    def test_ne(self):
        builtins.input = lambda s: 'Alex'
        otherPlayerHuman = PlayerHuman()
        assert self.playerHuman != otherPlayerHuman

    def test_ne_other_type(self):
        assert self.playerHuman != 5

class TestGame:
    def setup(self):
        builtins.input = lambda s: ''
        self.game = Game()

    def teardown(self):
        del self.game

    def test_init(self):
        assert len(self.game.bag) == 99

    def test_menu(self):
        for num in '1234':
            builtins.input = lambda s: num
            assert self.game.menu() == int(num)
    
    def test_menu_incorrect_input(self):
        inputs = ['5', '1']
        builtins.input = lambda s: inputs.pop(0)
        assert self.game.menu() == 1

    def test_init_players_human_comp(self):
        self.game.init_players(1)
        assert isinstance(self.game.player1, PlayerHuman) == True
        assert isinstance(self.game.player2, PlayerComp) == True

    def test_init_players_human_human(self):
        self.game.init_players(2)
        assert isinstance(self.game.player1, PlayerHuman) == True
        assert isinstance(self.game.player2, PlayerHuman) == True

    def test_init_players_copm_comp(self):
        self.game.init_players(3)
        assert isinstance(self.game.player1, PlayerComp) == True
        assert isinstance(self.game.player2, PlayerComp) == True

    def test_step(self):
        assert self.game.step() > 0
        assert len(self.game.bag) == 99 - 1

    def test_start(self):
        builtins.input = lambda s: '3'
        assert self.game.start() == True

    def test_exit_game(self):
        builtins.input = lambda s: '4'
        assert self.game.start() == False

    def test_str(self):
        assert str(self.game) != ''

    def test_eq(self):
        otherGame = Game()
        assert self.game == otherGame

    def test_ne(self):
        otherGame = Game()
        self.game.init_players(3)
        otherGame.init_players(3)
        assert self.game != otherGame

    def test_ne_other_type(self):
        assert self.game != 5