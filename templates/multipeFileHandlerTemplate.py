#!/usr/bin/env python
#

# import modules used here -- sys is a very standard one
import sys, argparse, logging


# Gather our code in a main() function
def main(args, loglevel):
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

    print(" I did something with:")
    for _arg in args.argument:
        print _arg


# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Does a thing to some stuff.",
        epilog="As an alternative to the commandline, params can be placed in"
               "a file, one per line, and specified on the commandline like "
               "'%(prog)s @params.conf'.",
        fromfile_prefix_chars='@',
    )
    # TODO Specify your real parameters here.
    parser.add_argument("argument",
                        help = "pass ARG to the program",
                        nargs="+",
                        )

    args = parser.parse_args()
    args.verbose = True

    # Setup logging
    if args.verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    main(args, loglevel)