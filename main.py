#!/usr/bin/env python

# Mark Apinis
# 31 March 2024
# main.py

"""
Converts an NBER-formatted file into a CSV via translations.csv
Takes paths for input and optionally specified output
Gibves warnings if a translation is not found and errors if no translation can be done
Format specified in README.md
"""

import argparse


def get_args():
    """
    Gets CLI args using argparse
    @return: Argparse arguments
    """

    parser = argparse.ArgumentParser(
        description="Provide an NBER .dat file and recieve a translated .csv \
                     based on translation.json"
    )

    parser.add_argument(
        "-i",
        "--infile",
        dest="INFILE",
        type=str,
        help="Path to NBER-formatted .dat",
        required=True,
    )

    parser.add_argument(
        "-o",
        "--outfile",
        dest="OUTFILE",
        type=str,
        help="Path to csv output. Overwritten if exists. Defaults to [INFILE].csv",
        default=None,
        required=False,
    )

    return parser.parse_args()


def main():
    """
    Main function
    """

    args = get_args()
    print(f"IN: {args.INFILE}")
    print(f"OUT: {args.OUTFILE}")


if __name__ == "__main__":
    main()
