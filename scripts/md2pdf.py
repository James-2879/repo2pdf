import markdown
import pdfkit
import os
import argparse

def markdown_to_pdf(md_file_path, pdf_file_path = "output.pdf", style = "blank"):
    # Read the markdown file
    with open(md_file_path, "r") as f:
        md_content = f.read()

    # Convert markdown to HTML with fenced code extension
    html_content = markdown.markdown(md_content, extensions=["fenced_code"])

    # Read the CSS file
    with open("styles.css", "r") as f:
        css_content = f.read()

    # Set header style class to use
    if style == "blue":
        header_class = "header blue"
    elif style == "red":
        header_class = "header red"
    elif style == "green":
        header_class = "header green"
    elif style == "orange":
        header_class = "header orange"
    elif style == "purple":
        header_class = "header purple"
    else:
        header_class = "header blank"

    # Embed the CSS in the HTML and add a header
    full_html_content = f"""
    <html>
    <head>
    <style>
    {css_content}
    </style>
    </head>
    <body>
    <div class="{header_class}"></div>
    {html_content}
    </body>
    </html>
    """

    # Write the full HTML content to a temporary file
    temp_html_file = "temp.html"
    with open(temp_html_file, 'w') as f:
        f.write(full_html_content)

    # Convert HTML to PDF
    pdfkit.from_file(temp_html_file, pdf_file_path)

    # Clean up the temporary HTML file
    os.remove(temp_html_file)

    print(f"PDF saved as {pdf_file_path}")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Convert Markdown file to PDF with a styled header.")
    parser.add_argument("--md_file_path",
                        type=str,
                        help="path to the markdown file",
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

    markdown_to_pdf(md_file_path = args.md_file_path,
                    pdf_file_path = args.pdf_file_path,
                    style = args.style)
