#!/usr/bin/env python3
"""Training script for the Texas Hold'em AI system."""

import argparse
import logging
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(description="Train Texas Hold'em AI")
    parser.add_argument("--algo", type=str, default="cfr", choices=["cfr", "ppo", "dqn"],
                        help="Algorithm to use for training")
    parser.add_argument("--iterations", type=int, default=10000,
                        help="Number of training iterations")
    parser.add_argument("--save-path", type=str, default="models/",
                        help="Path to save trained models")
    parser.add_argument("--num-players", type=int, default=2,
                        help="Number of players in the game")
    return parser.parse_args()


def main():
    args = parse_args()
    logger.info(f"Starting training with {args.algo} algorithm")
    logger.info(f"Running for {args.iterations} iterations")
    
    # 根据算法选择训练器
    if args.algo == "cfr":
        from src.training.cfr_trainer import CFRTrainer
        trainer = CFRTrainer(num_players=args.num_players)
    elif args.algo in ["ppo", "dqn"]:
        from src.training.rl_trainer import RL_Trainer
        trainer = RL_Trainer(algo=args.algo, num_players=args.num_players)
    else:
        raise ValueError(f"Unknown algorithm: {args.algo}")
    
    # 执行训练
    trainer.train(iterations=args.iterations, save_path=args.save_path)
    logger.info(f"Training completed. Model saved to {args.save_path}")


if __name__ == "__main__":
    main()