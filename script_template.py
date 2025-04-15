#!/usr/bin/env python
"""Yes, this is over 100 lines just to get ready to write a script,
but this takes care of a lot of basic things that you will need with
any somewhat substantial script.  This shows how to parse command-line
arguments, how to handle signals, how to clean up before the program
exits (especially if it exits early), and a cool debugging trick

"""
import argparse
import atexit
import signal
import os
import traceback
import logging
import sys
import pdb


def configure_logging(level):
    logging.basicConfig(
        level=level,
        format="[%(asctime)s] [%(levelname)s] %(message)s",
        force=True,
    )


def signal_handler(signum, _):
    # ignore all signals while we clean up
    register_signals(signal.SIG_IGN)
    logging.debug("handling signal by just exiting")
    print(f"{os.getpid()} Received signal {signum}, exiting")
    # atexit will be called when the below is called
    sys.exit(-signum)


def register_signals(handler):
    signal_list = [
        signal.SIGINT,
        signal.SIGTERM,
    ]
    for sig in signal_list:
        signal.signal(sig, handler)


def cleanup_at_exit():
    """Put any cleanup that needs to happen if the program exits early
    here

    """
    logging.debug("cleaning up")


def idb_excepthook(exception_type, value, tb):
    """With this defined you cat do "sys.excepthook = idb_excepthook"
    when this is run in debug mode (see parse_args function below) and
    then an interactive debugger will be spawned if there's an
    unhandled exception

    """
    if hasattr(sys, "ps1") or not sys.stderr.isatty():
        sys.__excepthook__(exception_type, value, tb)
    else:
        traceback.print_exception(exception_type, value, tb)
        print()
        pdb.pm()


def parse_args():
    """Parse program arguments"""
    parser = argparse.ArgumentParser(
        description="Python command line script template"
    )
    parser.add_argument(
        "--debug",
        "-d",
        action="store_true",
        help="Launch a debugger on unhandled exception",
    )
    parsed = parser.parse_args()
    return parsed


def main(args):
    """This is the main function where you put your code"""
    configure_logging(logging.INFO)
    if args.debug:
        sys.excepthook = idb_excepthook
        configure_logging(logging.DEBUG)
    # replace stuff below with real code
    print("hello, world!")
    print("taking some time so you can try hitting ctrl-c")
    accum = 0
    for _ in range(100_000_000):
        accum += 4
    logging.debug("got to the end")
    return 0


if __name__ == "__main__":
    atexit.register(cleanup_at_exit)
    register_signals(signal_handler)
    sys.exit(main(parse_args()))
