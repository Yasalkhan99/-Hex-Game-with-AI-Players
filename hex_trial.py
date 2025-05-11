import argparse
import logging
from datetime import datetime
import os

def setup_logging():
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_filename = os.path.join(
        log_dir, f"hex_game_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    )
    
    logging.basicConfig(
        filename=log_filename,
        format="%(asctime)s [%(levelname)s] %(message)s",
        level=logging.CRITICAL
    )

def run_experiment(test_type, config, board_size, match_count, fixed_start):
    if test_type == "comp":
        from tests.exp_competition import test as run_test
        run_test(config, board_size, match_count, fixed_start)
    elif test_type == "comp_old":
        from tests.exp_competition_old import test as run_test
        run_test(config, board_size, match_count, fixed_start)
    elif test_type == "mcts":
        from tests.exp_mcts import test as run_test
        run_test(board_size, match_count)

def main():
    parser = argparse.ArgumentParser(description="Run Hex AI experiments")
    parser.add_argument("mode", type=str, choices=["comp", "comp_old", "mcts"],
                        help="Experiment type to execute")
    parser.add_argument("-c", "--config", type=str, default="base",
                        choices=["base", "idtt", "mcts"],
                        help="Configuration preset for competition")
    parser.add_argument("-b", "--board", type=int, default=5,
                        help="Size of the hex board")
    parser.add_argument("-r", "--rounds", type=int, default=None,
                        help="Number of matches to simulate")
    parser.add_argument("-f", "--fixed", action="store_true",
                        help="Use fixed starting moves")
    args = parser.parse_args()

    setup_logging()
    run_experiment(args.mode, args.config, args.board, args.rounds, args.fixed)

if __name__ == "__main__":
    main()
