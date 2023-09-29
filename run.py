# run.py

import argparse

# Paths for latex generator and pdf to png tool
LATEX_COMPILER_PATH = "pdflatex"
PNG_COMPILER_PATH = "pdftoppm"

INPUT_FILE = "equation.eqs"
OUTPUT_FILE = "equation"

DPI = 150

VERBOSITY = 1


def generate_pdf():
    file_handle = open("templates/standalone.tex")

    return


def main():
    # --- Initialize command line parser ---
    parser = argparse.ArgumentParser()

    # Add parser arguments
    parser.add_argument(
        "-l",
        "--latex",
        help="Latex pdf compiler path",
        required=False,
        default=LATEX_COMPILER_PATH,
    )

    parser.add_argument(
        "-p",
        "--png",
        help="PDF to PNG compiler path",
        required=False,
        default=PNG_COMPILER_PATH,
    )

    parser.add_argument(
        "-i",
        "--input",
        help="Input file with latex equation code",
        required=False,
        default=INPUT_FILE,
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Output name for pdf and png files",
        required=False,
        default=OUTPUT_FILE,
    )

    parser.add_argument(
        "-r",
        "--resolution",
        help=f"Output dpi setting default {DPI}",
        required=False,
        default=DPI,
    )

    parser.add_argument(
        "-v",
        "--verbose",
        required=False,
        help=f"Verbosity integer; default -> {VERBOSITY}",
    )

    # --- Parse command line arguments ---
    args = vars(parser.parse_args())

    latex_compiler = args["latex"]
    png_compiler = args["png"]

    input_file = args["input"]
    output_file = args["output"]

    resolution = args["resolution"]
    verbose = args["verbose"]

    # --- Loop over equation in input files ---

    return


if __name__ == "__main__":
    main()
