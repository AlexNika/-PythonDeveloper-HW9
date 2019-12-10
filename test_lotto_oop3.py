from lotto_oop import Player, Lototron, Card
import numpy as np
import pytest
import random


class TestLototron:

    def test_init(self):
        bag = Lototron()
        assert bag.kegs_count == 90
        assert len(bag.kegs) == 90
        assert bag.keg == 0

    def test_get_keg(self):
        bag = Lototron()
        new_keg = bag.get_keg()
        assert len(bag.kegs) == 89
        assert range(1, 91).count(new_keg) != 0
        bag.kegs.clear()
        new_keg = bag.get_keg()
        assert new_keg == 0

    def test_len(self):
        bag = Lototron()
        assert len(bag) == 90

    def test_eq(self):
        bag1 = Lototron()
        bag2 = Lototron()
        assert bag1 == bag2

    def test_ne(self):
        bag1 = Lototron()
        bag2 = Lototron()
        bag2.get_keg()
        assert bag1 != bag2

    def test_str(self):
        test_bag = 'Инициализация лототрона:\n 59 11 43 2 73 67 16 27 41 33\n 46 48 68 20 60 56 63 71 52 57\n 50 86 ' \
                   '80 64 34 9 38 72 31 44\n 62 42 40 89 47 78 13 37 24 19\n 66 69 53 8 35 74 3 17 39 51\n 23 79 25 6 ' \
                   '7 61 49 83 10 84\n 22 75 45 21 1 87 58 85 54 90\n 26 77 65 30 28 81 88 5 55 76\n 12 70 14 18 29 ' \
                   '32 36 4 15 82\n'
        rnd = random.getstate()
        random.seed(42)
        bag = Lototron()
        random.setstate(rnd)
        assert str(bag) == test_bag

    def test_getitem(self):
        rnd = random.getstate()
        random.seed(42)
        bag = Lototron()
        random.setstate(rnd)
        assert 11 == bag[1]


class TestPlayer:

    def test_init_name(self):
        human_player = Player('Alex', True, 0)
        computer_player = Player('Tianhe-2', False, 0)
        assert human_player.name == 'Alex'
        assert computer_player.name == 'Tianhe-2'

    def test_init_category(self):
        human_player = Player('Alex', True, 0)
        computer_player = Player('Tianhe-2', False, 0)
        assert human_player.category
        assert not computer_player.category

    def test_init_score(self):
        human_player = Player('Alex', True, 0)
        computer_player = Player('Tianhe-2', False, 0)
        assert human_player.score == 0
        assert computer_player.score == 0

    def test_failure(self, capsys):
        human_player = Player('Alex', True, 0)
        with pytest.raises(SystemExit):
            human_player.failure()
        out, err = capsys.readouterr()
        assert out == '***********************************\nИГРА ЗАКОНЧЕНА\n'
        print(out, err)

    def test_eq(self):
        human1_player = Player('Alex', True, 0)
        human2_player = Player('Alex', True, 0)
        assert human1_player == human2_player

    def test_str(self):
        human_player = Player('Alex', True, 0)
        human_player.score = 10
        assert 'Игрок Alex : набрано 10 очков' == str(human_player)


class TestCard:

    def test_init_name(self):
        new_card = Card('Alex')
        assert new_card.name == 'Alex'

    def test_init_position(self):
        new_card = Card('Alex')
        assert new_card.position == []

    def test_init_cfg(self):
        new_card = Card('Alex')
        assert range(1, 10000).count(new_card.card_cfg) != 0

    def test_card_valid(self):
        new_card = Card('Alex')
        assert new_card.card.size == 15
        assert isinstance(new_card.card, np.ndarray)
        assert new_card.card.ndim == 1

    def test_update(self):
        new_card = Card('Alex')
        new_card.update([5])
        assert new_card.card[5] == 0

    def test_check(self):
        new_card = Card('Alex')
        assert not new_card.check(91)
        assert new_card.position == []

    def test_show(self):
        new_card = Card('Alex')
        assert new_card.show() is None

    def test_str(self, capsys):
        new_card = Card('Alex')
        new_card.card_cfg = 42
        new_card.card = np.array([43, 74, 78, 79, 82, 4, 46, 49, 65, 88, 17, 18, 40, 47, 72])
        new_card.update([5])
        assert str(new_card) == '-------------Alex--------------\n      43 74    78    79 82\n><             ' \
                                        '46 49 65 88\n   17 18 40    47       72\n-------------------------------'

    def test_eq(self):
        new_card1 = Card('Alex')
        new_card2 = Card('Simone')
        new_card1.update([5])
        new_card2.update([10])
        assert new_card1 == new_card2

    def test_ne(self):
        new_card1 = Card('Alex')
        new_card2 = Card('Simone')
        new_card1.update([3])
        new_card1.update([6])
        new_card2.update([10])
        assert new_card1 != new_card2

