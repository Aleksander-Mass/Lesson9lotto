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

    def test_is_num_to_cart(self):
        numbers = self.cart.get_cart_numbers()
        for number in numbers:
            assert self.cart.is_num_to_cart(number) == True

    def test_cross_out_success(self):
        numbers = self.cart.get_cart_numbers()
        assert self.cart.cross_out(numbers[5]) == True

    def test_cross_out_fail(self):
        assert self.cart.cross_out(1000) == False

    def test_out_print(self):
        assert self.cart.out_print() != ''

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