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
import io
from pathlib import Path


def get_filehandle(path: str, mode: str) -> io.FileIO:
    """ """


def get_input_lines(in_fh: io.FileIO) -> list[str]:
    """ """


def get_translation_info(path_fh: io.FileIO) -> list[dict]:
    """ """


def make_csv_header(translation_info: list[dict]) -> str:
    """ """


def translate_lines(lines: list[str], translation_info: list[dict]) -> str:
    """ """


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

    # handle args
    if not args.OUTFILE:
        # build output path if needed
        p = Path(args.INFILE)
        args.OUTFILE = str(p.parents[0] / p.stem) + ".csv"

    print(f"IN: {args.INFILE}")
    print(f"OUT: {args.OUTFILE}")

    # get filehandles
    in_fh = get_filehandle(args.INFILE, "r")
    out_fh = get_filehandle(args.OUTFILE, "w")
    trans_fh = get_filehandle("translation.json", "r")

    # get translation and close fh
    translation_info = get_translation_info(trans_fh)
    trans_fh.close()

    # get data lines and close fh
    data_lines = get_input_lines(in_fh)
    in_fh.close()

    # get csv header
    header = make_csv_header(translation_info)

    # get csv lines
    csv_lines = translate_lines(data_lines, translation_info)

    # write to output file
    out_fh.write(header + "\n")
    out_fh.writelines(csv_lines)  # TODO check that this correctly puts newlines

    # close out_fh
    out_fh.close()

if __name__ == "__main__":
    main()
