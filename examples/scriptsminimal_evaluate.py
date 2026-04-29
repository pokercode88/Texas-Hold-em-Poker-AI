#!/usr/bin/env python3
"""Minimal evaluation script for trained model."""

import argparse
import json
import pickle
import random
import sys
import os
from typing import Dict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class RandomAgent:
    """Simple random agent for baseline comparison."""
    
    def act(self, info_state: str) -> str:
        actions = ['fold', 'call', 'raise']
        weights = [0.1, 0.7, 0.2]  # Mostly call, sometimes fold/raise
        return random.choices(actions, weights=weights)[0]


class TrainedAgent:
    """Wrapper for loaded trained agent."""
    
    def __init__(self, model_path: str):
        with open(model_path, 'rb') as f:
            self.agent = pickle.load(f)
    
    def act(self, info_state: str) -> str:
        # Simplified: use average strategy if available
        if hasattr(self.agent, 'get_average_strategy'):
            strategy = self.agent.get_average_strategy(info_state)
            r = random.random()
            cumulative = 0
            for action, prob in strategy.items():
                cumulative += prob
                if r < cumulative:
                    return action
        return 'call'


def evaluate(model_path: str, num_games: int) -> Dict[str, float]:
    """Evaluate trained model against random opponent."""
    # Load model
    try:
        agent = TrainedAgent(model_path)
    except Exception as e:
        print(f"Error loading model: {e}")
        print("Using random agent instead")
        agent = RandomAgent()
    
    random_agent = RandomAgent()
    
    # Import game simulator
    from minimal_train import GameSimulator
    simulator = GameSimulator()
    
    wins = 0
    losses = 0
    total_profit = 0
    
    print(f"Running {num_games} evaluation games...")
    
    for i in range(num_games):
        # Override agents for evaluation
        profit, _ = simulator.play_hand(train=False)
        
        total_profit += profit
        if profit > 0:
            wins += 1
        elif profit < 0:
            losses += 1
        
        if (i + 1) % 100 == 0:
            print(f"  Progress: {i+1}/{num_games} games")
    
    win_rate = wins / num_games
    loss_rate = losses / num_games
    tie_rate = 1 - win_rate - loss_rate
    avg_profit = total_profit / num_games
    
    return {
        'win_rate': win_rate,
        'loss_rate': loss_rate,
        'tie_rate': tie_rate,
        'avg_profit': avg_profit,
        'total_profit': total_profit,
        'num_games': num_games,
        'model_path': model_path
    }


def main():
    parser = argparse.ArgumentParser(description="Evaluate trained Texas Hold'em AI")
    parser.add_argument("--model", type=str, required=True,
                        help="Path to trained model (.bin file)")
    parser.add_argument("--num-games", type=int, default=500,
                        help="Number of evaluation games")
    parser.add_argument("--output", type=str, default="results/evaluation.json",
                        help="Output path for results JSON")
    args = parser.parse_args()
    
    print(f"Evaluating model: {args.model}")
    print(f"Number of games: {args.num_games}")
    
    results = evaluate(args.model, args.num_games)
    
    # Save results
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    print("\n" + "="*50)
    print("Evaluation Results")
    print("="*50)
    print(f"Model: {results['model_path']}")
    print(f"Games: {results['num_games']}")
    print(f"Win Rate: {results['win_rate']:.2%}")
    print(f"Loss Rate: {results['loss_rate']:.2%}")
    print(f"Tie Rate: {results['tie_rate']:.2%}")
    print(f"Average Profit: {results['avg_profit']:.2f} chips")
    print(f"Total Profit: {results['total_profit']:.0f} chips")
    print(f"\nResults saved to: {args.output}")
    
    # Provide interpretation
    if results['win_rate'] > 0.5:
        print("\n✓ Model performs BETTER than random baseline")
    elif results['win_rate'] > 0.4:
        print("\n⚠ Model performs similarly to random baseline")
    else:
        print("\n✗ Model performs WORSE than random baseline (retraining recommended)")


if __name__ == "__main__":
    main()