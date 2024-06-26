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
from io import FileIO
from pathlib import Path
import json


def get_filehandle(path: str, mode: str) -> FileIO:
    """
    Gets the filehandle for the provided path with the provided mode.
    If the path does not exist and the file is opened in read-only mode, OSError is raised
    If the mode is not valid, ValueError is raised
    @param path: The location of the file we want to open
    @param mode: The mode to open the file with
    @return: Filehandler with appropriate mode
    """

    try:
        filehandle = open(path, mode, encoding="utf-8")
    except FileNotFoundError as error:
        # incorrect file path for mode
        raise OSError(f"Incorrect mode {mode} for path {path}") from error
    except ValueError as error:
        # incorrect mode
        raise ValueError(f"Incorrect mode {mode}") from error

    return filehandle


def get_input_lines(in_fh: FileIO) -> list[str]:
    """
    Reads the input filehandle and returns the lines, stripped, in a list
    @param in_fh: Filehandle for input
    @return: List of lines from file
    """
    return [l.strip() for l in in_fh.readlines()]


class MissingFieldError(Exception):
    """
    Error to represent a missing field
    """


def _check_translation_item(tr: dict) -> None:
    """
    Checks that the translation item has the fields:
        * key
        * location with start and end
        * value_map
    Raises an exception if not
    @param tr: translation item
    """

    top_level_fields = {"key", "location", "value_map"}
    location_fields = {"start", "end"}

    try:
        if (top_level_fields & set(tr.keys()) != top_level_fields) or (
            location_fields & set(tr["location"].keys()) != location_fields
        ):
            raise MissingFieldError
    except Exception as e:
        raise MissingFieldError(
            "Bad translation file: Item(s) missing fields(s)"
        ) from e


def get_translation_info(trans_fh: FileIO) -> list[dict]:
    """
    Reads the translation from the json and returns the translations dict-list
    Checks that file includes all the necessary fields, raises exception if not
    @param trans_fh: Filehandle for the translation json
    @return: List of dictionaries of translation
    """
    input_json = json.load(trans_fh)
    if "translations" not in input_json:
        raise MissingFieldError("Bad translation file: Missing 'translations' field")

    translation_info = input_json["translations"]
    for tr in translation_info:
        _check_translation_item(tr)

    return translation_info


def make_csv_header(translation_info: list[dict]) -> str:
    """
    Extracts the keys from the translation file and makes the
    csv header line in the same order
    @param translation_info: List of translation dictionary items
    @return: csv header line of the keys
    """
    return ",".join([tr["key"] for tr in translation_info])


def translate_lines(lines: list[str], translation_info: list[dict]) -> list[str]:
    """
    Translates the info from the input lines according to the available translations
    Gives a warning if a value is not found in the value_map and copies it verbatim
    Raises an exception if the start/end locations do not properly exist
    O(n * m)
    @param lines: Input data lines
    @param translation_info: List of translation dictionary items
    @return: list of csv line strings
    """

    # holds final output strings
    out = []

    for i, line in enumerate(lines):

        # holds translated values for this line
        line_vals = []

        for tr in translation_info:
            loc = tr["location"]
            value_map = tr["value_map"]

            # get input value location
            input_value = line[loc["start"] - 1 : loc["end"]]

            # check that the location is valid
            if not input_value:
                # empty str, start/end locations do not exist
                raise ValueError(
                    f"Location for {tr['key']} does not exist for line {i}"
                )  # TODO: better exception

            # check that the value is in the value_map and convert
            if input_value in value_map:
                line_vals.append(value_map[input_value])
            else:
                # else append original value
                line_vals.append(input_value)
                # and warn if the value_map had anything at all
                if value_map:
                    print(
                        f"WARNING: Line {i} missing translation for {tr['key']}: {input_value}"
                    )

        # combine translated values
        out.append(",".join(line_vals) + "\n")

    return out


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
