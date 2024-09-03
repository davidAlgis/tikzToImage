import argparse
import subprocess
import os
import fitz  # PyMuPDF
from PIL import Image

def create_latex_file(tikz_file_path, output_latex_file):
    latex_content = r"""
    \documentclass[tikz]{standalone}
    \begin{document}
    \input{%s}
    \end{document}
    """ % tikz_file_path
    with open(output_latex_file, 'w') as file:
        file.write(latex_content)

def compile_latex_to_pdf(latex_file, output_dir):
    command = ["pdflatex", "-output-directory", output_dir, latex_file]
    subprocess.run(command, check=True)

def convert_pdf_to_png(pdf_file, output_png_file, dpi=300):
    doc = fitz.open(pdf_file)
    page = doc.load_page(0)  # Get the first page
    pix = page.get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72))
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    img.save(output_png_file)

def tikz_to_png(tikz_file_path, output_png_file, dpi=300):
    base_name = os.path.splitext(os.path.basename(tikz_file_path))[0]
    output_dir = os.path.dirname(tikz_file_path)
    latex_file = os.path.join(output_dir, f"{base_name}.tex")
    pdf_file = os.path.join(output_dir, f"{base_name}.pdf")
    
    # Create LaTeX file
    create_latex_file(tikz_file_path, latex_file)
    
    # Compile LaTeX to PDF
    compile_latex_to_pdf(latex_file, output_dir)
    
    # Convert PDF to PNG
    convert_pdf_to_png(pdf_file, output_png_file, dpi)
    
    print(f"Generated PNG: {output_png_file}")

def main():
    parser = argparse.ArgumentParser(description="Convert TikZ picture to a high-resolution PNG.")
    parser.add_argument('-i', '--input', type=str, default='input.tikz', help="Path to the input TikZ file (default: input.tikz)")
    parser.add_argument('-o', '--output', type=str, default='output.png', help="Path to the output PNG file (default: output.png)")
    parser.add_argument('-d', '--dpi', type=int, default=300, help="DPI for the output PNG (default: 300)")

    args = parser.parse_args()

    tikz_to_png(args.input, args.output, args.dpi)

if __name__ == "__main__":
    main()
