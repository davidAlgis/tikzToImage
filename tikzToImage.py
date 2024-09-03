import argparse
import subprocess
import os
import fitz  # PyMuPDF
from PIL import Image
import shutil
import sys

def create_latex_file(tikz_file_path, output_latex_file, packages_input):
    print("Generating LaTeX file...")
    tikz_file_path_escaped = tikz_file_path.replace('\\', '/')
    
    latex_content = r"""
    \documentclass[tikz]{standalone}
    %s
    \begin{document}
    \input{%s}
    \end{document}
    """ % (packages_input, tikz_file_path_escaped)
    
    with open(output_latex_file, 'w') as file:
        file.write(latex_content)

def compile_latex_to_pdf(latex_file, output_dir):
    command = [
        "pdflatex",
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-output-directory", output_dir,
        latex_file
    ]
    try:
        print("Generating PDF from LaTeX...")
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print("Error during LaTeX compilation.")
        print(e.stdout.decode('utf-8', errors='replace'))
        print(e.stderr.decode('utf-8', errors='replace'))
        return False
    return True

def convert_pdf_to_png(pdf_file, output_png_file, dpi=300):
    print("Converting PDF to PNG...")
    doc = fitz.open(pdf_file)
    page = doc.load_page(0)  # Get the first page
    pix = page.get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72))
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    img.save(output_png_file)

def clean(files_to_remove):
    print("Cleaning up temporary files...")
    for file_path in files_to_remove:
        if os.path.exists(file_path):
            os.remove(file_path)

def tikz_to_png(tikz_file_path, output_png_file, dpi=300, packages_input=""):
    # Check if the input file exists
    if not os.path.exists(tikz_file_path):
        print(f"Error: The input file '{tikz_file_path}' does not exist.")
        sys.exit(1)
    
    # Copy the TikZ file to the current directory
    current_dir = os.getcwd()
    tikz_file_copy = os.path.join(current_dir, os.path.basename(tikz_file_path))
    shutil.copy(tikz_file_path, tikz_file_copy)
    print(f"Copied TikZ file to: {tikz_file_copy}")
    
    # Define file names for the LaTeX and PDF files
    base_name = os.path.splitext(os.path.basename(tikz_file_copy))[0]
    latex_file = os.path.join(current_dir, f"{base_name}.tex")
    pdf_file = os.path.join(current_dir, f"{base_name}.pdf")
    
    # Create LaTeX file
    create_latex_file(tikz_file_copy, latex_file, packages_input)
    
    # Compile LaTeX to PDF
    success = compile_latex_to_pdf(latex_file, current_dir)
    
    if not success:
        # Clean up if LaTeX compilation fails
        temp_files = [
            tikz_file_copy,
            latex_file,
            pdf_file,
            os.path.join(current_dir, f"{base_name}.aux"),
            os.path.join(current_dir, f"{base_name}.log"),
            os.path.join(current_dir, f"{base_name}.out")
        ]
        clean(temp_files)
        sys.exit(1)
    
    # Convert PDF to PNG
    convert_pdf_to_png(pdf_file, output_png_file, dpi)
    
    print(f"Generated PNG: {output_png_file}")
    
    # Clean up temporary files
    temp_files = [
        tikz_file_copy,
        latex_file,
        pdf_file,
        os.path.join(current_dir, f"{base_name}.aux"),
        os.path.join(current_dir, f"{base_name}.log"),
        os.path.join(current_dir, f"{base_name}.out")
    ]
    clean(temp_files)

def main():
    parser = argparse.ArgumentParser(description="Convert TikZ picture to a high-resolution PNG.")
    parser.add_argument('-i', '--input', type=str, default='input.tikz', help="Path to the input TikZ file (default: input.tikz)")
    parser.add_argument('-o', '--output', type=str, default='output.png', help="Path to the output PNG file (default: output.png)")
    parser.add_argument('-d', '--dpi', type=int, default=300, help="DPI for the output PNG (default: 300)")
    parser.add_argument('-p', '--packagesInput', type=str, default="", help="LaTeX packages or macros to include in the preamble (default: '')")

    args = parser.parse_args()

    tikz_to_png(args.input, args.output, args.dpi, args.packagesInput)

if __name__ == "__main__":
    main()
