# run.py

import os
import argparse
import subprocess
import shutil
import warnings
from pathlib import Path

from pdf2image import convert_from_path
from PIL import Image

# Path for latex compiler
LATEX_COMPILER_PATH = "pdflatex"

# Input and output file names
INPUT_FILE = "equation.eqs"
OUTPUT_FILE = "equation"

# Image resolution and width
DPI = 250
WIDTH = 800

# Verbosity setting
VERBOSITY = 1


def generate_pdf(equation, template_file="standalone", output_file=None, index=None, compiler=LATEX_COMPILER_PATH):
    """
    Generate pdf document for given equation string

    Args:
        equation (str): The latex equation string.
        template_file (str, optional): The name of the LaTeX template file 
            without .tex extension.
        output_file (str, optional): The name of the output PDF file.
        index (int, optional): An optional index when generating multiple 
            equations.
        compiler (str): path of latex compiler.

    Returns:
        None
    """

    # --- Get latex template ---
    template_file_path = Path(os.getcwd(), "templates", f"{template_file}.tex")
    if not os.path.exists(template_file_path):
        raise FileExistsError(f"Template file {template_file_path} does not exist")

    with open(template_file_path) as file_handle:
        template = file_handle.read()

    # --- Create output file name ---
    file_name = output_file
    if file_name is None:
        file_name = "output"

    if index is not None:
        file_name += f"_{index}"

    # --- Generate tex file ---
    template = template.replace("EQUATION", equation)

    with open(Path(os.getcwd(), "temp", f"{file_name}.tex"), "w+") as file_handle:
        file_handle.write(template)

    # --- Compile pdf ---
    try:
      res = subprocess.run(
          [
              compiler,
              Path(f"{file_name}.tex"),
          ],
          cwd="temp/",
          stdout=subprocess.DEVNULL,
          stderr=subprocess.STDOUT,
          timeout=10
      )
    except subprocess.TimeoutExpired as e:
        warnings.warn(f"Compiler timed out on equation {file_name}, check log files")

    # --- Copy results to output directories ---
    if os.path.exists(Path("temp", f"{file_name}.pdf")):
        shutil.copyfile(
            Path(os.getcwd(), "temp", f"{file_name}.pdf"),
            Path(os.getcwd(), "pdf", f"{file_name}.pdf"),
        )
    else:
        warnings.warn(f"{file_name}.pdf was not created.")

    if os.path.exists(Path("temp", f"{file_name}.log")):
        shutil.copyfile(
            Path(os.getcwd(), "temp", f"{file_name}.log"),
            Path(os.getcwd(), "logs", f"{file_name}.log"),
        )

    return


def generate_png(output_file=None, index=None, dpi=DPI, width=WIDTH):
    """
    Convert a PDF file to a PNG image.

    Args:
        output_file (str, optional): The name of the output PNG file.
        index (int, optional): An optional index when generating multiple 
            equations.
        dpi (int, optional): The resolution (dots per inch) of the output image.
        width (int, optional): The desired width of the output image in pixels.
        
    Returns:
        None

    """

    # --- Create output file name ---
    file_name = f"{output_file}"
    if file_name is None:
        file_name = "output"

    if index is not None:
        file_name += f"_{index}"

    # --- Convert pdf to png using pdf2image library ---
    image = convert_from_path(
        Path(os.getcwd(), "pdf", f"{file_name}.pdf"),
        dpi=dpi,
        single_file=True,
    )

    image[0].save(Path(os.getcwd(), "png", f"{file_name}@2x.png"), "PNG")

    # --- Resize png to requested width ---
    image = Image.open(Path(os.getcwd(), "png", f"{file_name}@2x.png"))

    image_width, image_height = image.size

    # Update width and height
    new_height = image_height
    new_width = image_width
    if image_width < width:
        new_width = width

    # Create new image
    result = Image.new(image.mode, (new_width, new_height), (255, 255, 255))

    # Paste equation into new image
    left = 0
    if image_width < width:
        left = int((width - image_width) / 2)
    top = 0
    result.paste(image, (left, top))

    result.save(Path(os.getcwd(), "png", f"{file_name}@2x.png"))

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
        "--dpi",
        help=f"Output dpi setting default {DPI}",
        required=False,
        default=DPI,
        type=int
    )

    parser.add_argument(
        "-w",
        "--width",
        help=f"Image width default {WIDTH}",
        required=False,
        default=WIDTH,
        type=int
    )

    parser.add_argument(
        "-v",
        "--verbose",
        required=False,
        help=f"Verbosity integer; default -> {VERBOSITY}",
        default=VERBOSITY,
    )

    # --- Parse command line arguments ---
    args = vars(parser.parse_args())

    latex_compiler = args["latex"]

    input_file = args["input"]
    output_file = args["output"]

    dpi = args["dpi"]
    width = args["width"]
    verbose = args["verbose"]

    # --- Create output folder ---
    os.makedirs("logs", exist_ok=True)  # Log files
    os.makedirs("pdf", exist_ok=True)  # Pdf files
    os.makedirs("png", exist_ok=True)  # Png files
    os.makedirs("temp", exist_ok=True)  # Temp build files

    # --- Loop over equation in input files ---
    # Open file
    input_file_path = Path(os.getcwd(), input_file)
    if not os.path.exists(input_file_path):
        raise FileExistsError(f"Input file {input_file_path} does not exist")

    with open(input_file_path) as file_handle:
        # Read equations
        equations = file_handle.readlines()
        n = len(equations)

        # Print number of equations in file
        if verbose > 0:
            print(f"Found {n} equations in {input_file}")

        for i, equation in enumerate(equations):
            # Create pdf
            generate_pdf(equation, output_file=output_file, index=i, compiler=latex_compiler)

            # Create png
            generate_png(output_file=output_file, index=i, dpi=dpi, width=width)

    # --- Remove temp build files ---
    shutil.rmtree(Path(os.getcwd(), "temp"))

    return


if __name__ == "__main__":
    main()
