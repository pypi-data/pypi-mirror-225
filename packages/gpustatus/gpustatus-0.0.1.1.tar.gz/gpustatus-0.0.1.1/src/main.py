import os
import argparse
from src.gpu_info import GPU_Monitor


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--show-all",
        action="store_true",
        default=False,
        help="Show all GPU usage",
    )
    parser.add_argument(
        "--show-by-gpu",
        action="store_true",
        default=False,
        help="Show GPU usage by no. gpu",
    )
    parser.add_argument(
        "--show-by-user",
        action="store_true",
        default=False,
        help="Show GPU usage by user",
    )
    parser.add_argument(
        "--gpu",
        nargs='+',
        type=int,
        default=None,
        help="number of GPU",
    )
    parser.add_argument(
        "--user",
        nargs='+',
        default=None,
        help="user name",
    )
    return parser.parse_args()

def main():
    args = parse_arguments()
    assert (args.show_all or args.show_by_gpu or args.show_by_user), "Please choose one to show"
    gm = GPU_Monitor()
    if args.show_all:
        gm.show_all_info()
    if args.show_by_gpu:
        gm.show_by_gpu(args.gpu)
    if args.show_by_user:
        gm.show_by_user(args.user)

if __name__ == "__main__":
    main()