"""Sample test file for the Texas Hold'em AI system."""

import pytest
from src.core.game_state import GameState  # 根据实际模块名调整
from src.core.card import Card, Suit, Rank


class TestCard:
    """Test card creation and comparison."""
    
    def test_card_creation(self):
        card = Card(Suit.HEARTS, Rank.ACE)
        assert card.suit == Suit.HEARTS
        assert card.rank == Rank.ACE
    
    def test_card_string(self):
        card = Card(Suit.SPADES, Rank.KING)
        assert str(card) == "K♠"
    
    def test_card_comparison(self):
        ace_hearts = Card(Suit.HEARTS, Rank.ACE)
        king_spades = Card(Suit.SPADES, Rank.KING)
        assert ace_hearts > king_spades


class TestGameState:
    """Test game state initialization and updates."""
    
    def test_initial_state(self):
        state = GameState()
        assert state.players == []
        assert state.pot == 0
        assert state.stage == "preflop"
    
    def test_add_player(self):
        state = GameState()
        state.add_player("player1", 1000)
        assert len(state.players) == 1
        assert state.players[0].stack == 1000


class TestHandEvaluator:
    """Test hand evaluation logic."""
    
    def test_high_card(self):
        # TODO: 实现手牌评估测试
        pass
    
    def test_pair(self):
        # TODO: 实现手牌评估测试
        pass
    
    def test_flush(self):
        # TODO: 实现手牌评估测试
        pass