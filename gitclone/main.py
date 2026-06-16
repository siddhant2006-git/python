# argparse- it is libary which are used to handle the input .
import argparse


def main():
    parser = argparse.ArgumentParser(description="A simple git clone")

    # add_subparsers- multiple command add karni hoti hai cli .(command line interface )
    subparse = parser.add_subparsers(dest="command", help="Available commands")

    # init command
    init_parse = subparse.add_parser("init", help="Initialize a new repository")

    # parse_args reads terminal arguments and stores them in args
    args = parser.parse_args()

    print(args)

    if not args.command:
        parser.print_help()
        return 


main()
