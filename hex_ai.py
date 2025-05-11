"""
main_hex.py: Launch and play a game of Hex using various AI or human strategies.
"""

import argparse
import logging
from datetime import datetime
import os

from hexai.hexgame import Hex
from hexai.players.humanplayer import HumanPlayer
from hexai.players.alphabetaplayer import AlphaBetaPlayer
from hexai.players.mctsplayer import MctsPlayer

def configure_logging():
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"hex_game_{timestamp}.log")

    logging.basicConfig(
        filename=log_file,
        format="%(asctime)s [%(levelname)s]: %(message)s",
        level=logging.CRITICAL
    )

def create_player(player_type: str, use_tt: bool):
    if player_type == "human":
        return HumanPlayer()
    elif player_type == "alphabeta":
        return AlphaBetaPlayer(
            evaluation="dijkstra",
            use_id=True,
            use_tt=use_tt,
            max_time=2
        )
    elif player_type == "mcts":
        return MctsPlayer(max_time=2)
    else:
        raise ValueError(f"Unknown player type: {player_type}")

def setup_game(p1_type, p2_type, size, use_tt, starter):
    player1 = create_player(p1_type, use_tt)
    player2 = create_player(p2_type, use_tt)
    game = Hex(board_size=size, players=[player1, player2])
    game.play(starter - 1, verbose=2)

def main():
    parser = argparse.ArgumentParser(description="Start a Hex game with AI or human players.")
    parser.add_argument("-p1", type=str, default="human", choices=["human", "alphabeta", "mcts"],
                        help="Type of Player 1")
    parser.add_argument("-p2", type=str, default="alphabeta", choices=["human", "alphabeta", "mcts"],
                        help="Type of Player 2")
    parser.add_argument("-s", "--size", type=int, default=5,
                        help="Board size")
    parser.add_argument("-t", "--use_tt", action="store_true",
                        help="Enable transposition table for AlphaBeta player")
    parser.add_argument("-b", "--begin", type=int, default=1,
                        help="Which player starts (1 or 2)")

    args = parser.parse_args()

    configure_logging()
    setup_game(args.p1, args.p2, args.size, args.use_tt, args.begin)

if __name__ == "__main__":
    main()
