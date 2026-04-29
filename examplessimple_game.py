#!/usr/bin/env python3
"""Simple example of running a Texas Hold'em game with AI agents."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.env.poker_env import PokerEnv  # 根据实际模块调整
from src.ai.random_agent import RandomAgent
from src.ai.cfr_agent import CFRAgent


def main():
    """Run a simple 2-player game."""
    print("=" * 50)
    print("Texas Hold'em AI - Simple Example")
    print("=" * 50)
    
    # 创建环境
    env = PokerEnv(num_players=2, starting_stack=1000)
    
    # 创建AI智能体
    agent1 = RandomAgent("Agent_Random_1")
    agent2 = CFRAgent("Agent_CFR", model_path="models/cfr_v0.bin")
    
    # 运行一局
    print("\nStarting a new hand...\n")
    obs = env.reset()
    done = False
    
    while not done:
        current_player = env.get_current_player()
        if current_player == 0:
            action = agent1.act(obs)
        else:
            action = agent2.act(obs)
        
        obs, reward, done, info = env.step(action)
        print(f"Player {current_player}: {action}")
    
    print(f"\nGame finished! Winner: {info.get('winner', 'Unknown')}")
    print(f"Pot size: {info.get('pot', 0)}")
    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()