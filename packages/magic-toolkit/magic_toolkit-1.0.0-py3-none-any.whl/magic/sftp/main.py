import argparse
import sys
from .deploy import deploy_configure_parser
from .send import send_config_parser

def show_help_on_empty_command():
    if len(sys.argv) == 1:
        sys.argv.append("--help")  # sys.argv == ['/path/to/bin/conda-env']

def create_parser():
    p = argparse.ArgumentParser()
    sub_parsers = p.add_subparsers(
        metavar="command",
        dest="cmd",
        required=False,
    )
    deploy_configure_parser(sub_parsers)
    send_config_parser(sub_parsers)

    show_help_on_empty_command()
    return p

def main():
    parser = create_parser()
    args = parser.parse_args()
    args.func(args)
