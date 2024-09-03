# TikZ to PNG Converter

This Python script converts TikZ pictures to high-resolution PNG images. It generates a LaTeX file from a TikZ input file, compiles it to PDF, and then converts the PDF to a PNG image. The script allows for specifying additional LaTeX packages and customizing the output DPI.

## Installation

To run this script, you'll need to ensure you have the required Python libraries. Install them using the `requirements.txt` file provided in this repository.

```bash
pip install -r requirements.txt
```


## Usage

Ensure you have Python 3.6 or newer installed on your system. Clone this repository or download the script and `requirements.txt` file. Then, install the required libraries as mentioned above.

Additionally, ensure that `pdflatex` is installed and available in your system's PATH.

To use the script, run it from the command line with the desired options:

```
python tikzToImage.py [options]
```


## Options

- `-i`, `--input` <input_file>: Specify the path to the input TikZ file. Default is `input.tikz`.

- `-o`, `--output` <output_file>: Specify the path to the output PNG file. Default is `output.png`.

- `-d`, `--dpi` <dpi>: Specify the DPI for the output PNG. Default is `300`.

- `-p`, `--packagesInput` <packages>: LaTeX packages or macros to include in the preamble of the LaTeX document. Default is an empty string (`""`).

## Example

To convert a TikZ file named `example.tikz` into a high-resolution PNG image, you can use the following command:

```bash
python tikzToImage.py -i example.tikz -o example.png

```


If you want to set the output DPI to 600, you would use:


```bash
python tikzToImage.py -i example.tikz -o example.png -d 600

```


If you need to include additional LaTeX packages, such as `\usepackage{amsmath}`, you can use:

```bash
python tikzToImage.py -i example.tikz -o example.png -p "\usepackage{amsmath}"
```

## Issues

If you encounter any issues or have suggestions for improvements, please submit them to the GitHub issue tracker for this project.