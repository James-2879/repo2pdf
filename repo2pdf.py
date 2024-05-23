import argparse
import os

from scripts.repo2md import repo_to_markdown
from scripts.md2pdf import markdown_to_pdf


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Convert GitHub repository to PDF with a styled header.")
    parser.add_argument("--repo_path",
                        type=str,
                        help="path to repo",
                        required=True)
    parser.add_argument("--pdf_file_path",
                        type=str,
                        help="path to save the output PDF file",
                        default="output.pdf",
                        nargs="?")
    parser.add_argument("--style",
                        type=str,
                        choices=["blue", "red", "green", "orange", "purple", "blank"],
                        help="header style to use",
                        default="blank",
                        nargs="?")
    args = parser.parse_args()

    repo_to_markdown(args.repo_path, md_file_path = "output.md")
    markdown_to_pdf("output.md", pdf_file_path = args.pdf_file_path, style = args.style)
    os.remove("output.md")
