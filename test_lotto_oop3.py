from lotto_oop import Player, Lototron, Card
import numpy as np
import pytest


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

    def test_is_empty(self):
        bag = Lototron()
        assert bag.is_empty()


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
        assert out == 'Игрок Alex ПРОИГРАЛ!!!\n***********************************\nИГРА ЗАКОНЧЕНА\n'
        print(out, err)


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

    def test_appearance(self, capsys):
        new_card = Card('Alex')
        new_card.card_cfg = 42
        new_card.card = np.array([43, 74, 78, 79, 82, 4, 46, 49, 65, 88, 17, 18, 40, 47, 72])
        new_card.update([5])
        assert new_card.appearance() == '-------------Alex--------------\n      43 74    78    79 82\n><             ' \
                                        '46 49 65 88\n   17 18 40    47       72\n-------------------------------'
