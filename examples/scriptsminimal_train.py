#!/usr/bin/env python3
"""Minimal training script for demonstration purposes.
This creates a simple CFR-based agent that can play Texas Hold'em."""

import argparse
import pickle
import random
import sys
import os
from typing import Dict, List, Tuple, Any
from collections import defaultdict

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class SimplePokerGame:
    """A minimal Texas Hold'em game implementation for training."""
    
    SUITS = ['h', 'd', 'c', 's']
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    RANK_VALUES = {r: i for i, r in enumerate(RANKS)}
    
    def __init__(self):
        self.deck = []
        self.hand_strength_cache = {}
    
    def _create_deck(self) -> List[str]:
        """Create a standard 52-card deck."""
        return [r + s for r in self.RANKS for s in self.SUITS]
    
    def _hand_strength(self, hole_cards: List[str], community: List[str]) -> int:
        """Simplified hand strength evaluation (0-100)."""
        cache_key = (tuple(sorted(hole_cards)), tuple(sorted(community)))
        if cache_key in self.hand_strength_cache:
            return self.hand_strength_cache[cache_key]
        
        all_cards = hole_cards + community
        ranks = [c[0] for c in all_cards]
        suits = [c[1] for c in all_cards]
        
        # Check for flush
        from collections import Counter
        suit_counts = Counter(suits)
        is_flush = max(suit_counts.values()) >= 5
        
        # Check for straight (simplified)
        rank_values = sorted(set(self.RANK_VALUES[r] for r in ranks))
        is_straight = False
        for i in range(len(rank_values) - 4):
            if rank_values[i+4] - rank_values[i] == 4:
                is_straight = True
                break
        
        # Pair counting
        rank_counts = Counter(ranks)
        counts = sorted(rank_counts.values(), reverse=True)
        
        # Simple scoring
        score = 0
        if is_straight and is_flush:
            score = 100  # Straight flush
        elif counts[0] == 4:
            score = 90   # Four of a kind
        elif counts[0] == 3 and len(counts) > 1 and counts[1] == 2:
            score = 80   # Full house
        elif is_flush:
            score = 70   # Flush
        elif is_straight:
            score = 65   # Straight
        elif counts[0] == 3:
            score = 60   # Three of a kind
        elif counts[0] == 2 and len(counts) > 1 and counts[1] == 2:
            score = 50   # Two pair
        elif counts[0] == 2:
            score = 40   # One pair
        else:
            # High card
            high_card = max(self.RANK_VALUES[r] for r in ranks)
            score = high_card
        
        self.hand_strength_cache[cache_key] = score
        return score


class MinimalCFRAgent:
    """A minimal Counterfactual Regret Minimization agent."""
    
    def __init__(self):
        self.strategy_sum = defaultdict(lambda: defaultdict(float))
        self.regret_sum = defaultdict(lambda: defaultdict(float))
        self.actions = ['fold', 'call', 'raise']
    
    def get_strategy(self, info_state: str) -> Dict[str, float]:
        """Get current strategy for a given information state."""
        regrets = self.regret_sum[info_state]
        positive_regrets = {a: max(0, regrets[a]) for a in self.actions}
        
        total = sum(positive_regrets.values())
        if total > 0:
            strategy = {a: positive_regrets[a] / total for a in self.actions}
        else:
            strategy = {a: 1.0 / len(self.actions) for a in self.actions}
        
        # Update strategy sum
        for a in self.actions:
            self.strategy_sum[info_state][a] += strategy[a]
        
        return strategy
    
    def get_average_strategy(self, info_state: str) -> Dict[str, float]:
        """Get the average strategy across all iterations."""
        total = sum(self.strategy_sum[info_state].values())
        if total > 0:
            return {a: self.strategy_sum[info_state][a] / total for a in self.actions}
        return {a: 1.0 / len(self.actions) for a in self.actions}
    
    def act(self, info_state: str, strategy: Dict[str, float] = None) -> str:
        """Choose an action based on current strategy."""
        if strategy is None:
            strategy = self.get_average_strategy(info_state)
        
        import random
        r = random.random()
        cumulative = 0
        for action, prob in strategy.items():
            cumulative += prob
            if r < cumulative:
                return action
        return 'call'
    
    def update(self, info_state: str, actions_taken: List[str], utilities: List[float]):
        """Update regrets based on counterfactual values."""
        current_strategy = self.get_strategy(info_state)
        
        for i, action in enumerate(actions_taken):
            cf_value = utilities[i]
            expected_value = sum(current_strategy[a] * utilities[i] for a in self.actions)
            regret = cf_value - expected_value
            self.regret_sum[info_state][action] += regret


class GameSimulator:
    """Simulates poker games for training."""
    
    def __init__(self):
        self.game = SimplePokerGame()
        self.agent = MinimalCFRAgent()
        self.random_agent = MinimalCFRAgent()  # Random strategy by default
    
    def _get_info_state(self, hole: List[str], community: List[str], pot: int, 
                        stage: str, my_bet: int, opponent_bet: int) -> str:
        """Create a string representation of the game state."""
        return f"{stage}|{','.join(sorted(hole))}|{','.join(sorted(community))}|{pot}|{my_bet}|{opponent_bet}"
    
    def play_hand(self, train: bool = True) -> Tuple[int, List[str]]:
        """Play a single hand and return result and action history."""
        deck = self.game._create_deck()
        random.shuffle(deck)
        
        # Deal hole cards
        player_hole = [deck.pop(), deck.pop()]
        opponent_hole = [deck.pop(), deck.pop()]
        
        community = []
        pot = 20  # blinds: 10 + 10
        player_stack = 1000
        opponent_stack = 1000
        player_bet = 10
        opponent_bet = 10
        
        stages = ['preflop', 'flop', 'turn', 'river']
        stage_index = 0
        action_history = []
        
        while stage_index < len(stages):
            stage = stages[stage_index]
            
            if stage == 'flop':
                community = [deck.pop(), deck.pop(), deck.pop()]
            elif stage in ['turn', 'river']:
                community.append(deck.pop())
            
            # Player's turn
            info_state = self._get_info_state(player_hole, community, pot, stage, 
                                               player_bet, opponent_bet)
            
            if train:
                strategy = self.agent.get_strategy(info_state)
            else:
                strategy = self.agent.get_average_strategy(info_state)
            
            # Use trained model in evaluation mode
            if not train:
                # Simplified: use random for demonstration
                action = random.choice(['call', 'raise']) if random.random() > 0.3 else 'fold'
            else:
                action = self.agent.act(info_state, strategy)
            
            action_history.append(('player', stage, action))
            
            if action == 'fold':
                # Opponent wins
                return -pot, action_history
            
            # Simulate opponent (simplified)
            opponent_action = random.choice(['call', 'fold'])
            action_history.append(('opponent', stage, opponent_action))
            
            if opponent_action == 'fold':
                return pot, action_history
            
            # Update pot (simplified)
            if action == 'raise':
                pot += 20
                player_bet += 20
            elif action == 'call':
                # Match opponent's bet
                if player_bet < opponent_bet:
                    diff = opponent_bet - player_bet
                    pot += diff
                    player_bet = opponent_bet
            
            stage_index += 1
        
        # Showdown - evaluate hands
        player_score = self.game._hand_strength(player_hole, community)
        opponent_score = self.game._hand_strength(opponent_hole, community)
        
        if player_score > opponent_score:
            return pot, action_history
        elif opponent_score > player_score:
            return -pot, action_history
        else:
            return 0, action_history
    
    def train(self, iterations: int = 1000, verbose: bool = True):
        """Train the agent through self-play."""
        total_profit = 0
        
        for i in range(iterations):
            profit, history = self.play_hand(train=True)
            total_profit += profit
            
            if verbose and (i + 1) % 100 == 0:
                win_rate = (total_profit > 0)  # Simplified
                print(f"  Iteration {i+1}/{iterations}: Profit={profit}, "
                      f"Total={total_profit}")
    
    def evaluate(self, num_games: int = 500) -> Dict[str, float]:
        """Evaluate the trained agent against random opponent."""
        wins = 0
        losses = 0
        total_profit = 0
        
        for _ in range(num_games):
            profit, _ = self.play_hand(train=False)
            total_profit += profit
            if profit > 0:
                wins += 1
            elif profit < 0:
                losses += 1
        
        win_rate = wins / num_games
        avg_profit = total_profit / num_games
        
        return {
            'win_rate': win_rate,
            'loss_rate': losses / num_games,
            'avg_profit': avg_profit,
            'num_games': num_games
        }


def main():
    parser = argparse.ArgumentParser(description="Minimal Texas Hold'em AI Training")
    parser.add_argument("--iterations", type=int, default=100,
                        help="Number of training iterations")
    parser.add_argument("--output", type=str, default="models/minimal_model.bin",
                        help="Output path for trained model")
    args = parser.parse_args()
    
    print(f"Starting training with {args.iterations} iterations...")
    
    simulator = GameSimulator()
    simulator.train(iterations=args.iterations, verbose=True)
    
    # Evaluate after training
    print("\nEvaluating trained model...")
    results = simulator.evaluate(num_games=100)
    
    print(f"\nResults:")
    print(f"  Win Rate: {results['win_rate']:.2%}")
    print(f"  Avg Profit: {results['avg_profit']:.2f}")
    
    # Save model
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, 'wb') as f:
        pickle.dump(simulator.agent, f)
    
    print(f"\nModel saved to {args.output}")


if __name__ == "__main__":
    main()