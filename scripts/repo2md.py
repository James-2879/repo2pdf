import argparse
import os

exclude = ["/.git", "/data", ".tsv", ".txt", ".md", ".lock", ".csv"]

def list_files_recursively(directory):
    # List all files in specified directory.
    paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)
            if not any(pattern in path for pattern in exclude) and not os.path.basename(path).startswith('.'):
                paths.append(path)
    return(paths)
            
def add_code_block(vector):
    # Surround strings in markdown code block syntax.
    start_block = "\n```\n"
    end_block = "\n```\n"
    output = start_block + "".join(vector) + end_block
    return(output)

def make_heading(text, level):
    # Add markdown heading syntax to string, based on levell.
    prefix = ""
    for i in range(1, level+1):
        prefix = prefix+"#"
    prefix = prefix+" "
    heading = prefix+text+"\n"
    return(heading)

def file_depth(file_path, reference_directory):
    # Check how many dirs deep file is compared to ref dir.
    relative_path = os.path.relpath(file_path, reference_directory)
    return relative_path.count(os.sep)

def repo_to_markdown(repo_directory, md_file_path = "output.md"):
    # Get all files in directory
    files = list_files_recursively(repo_directory)
    # Split off repo name
    repo = repo_directory.rsplit("/", 2)[1]

    # Open a new markdown file
    markdown_file = open(md_file_path, "w")
    markdown_file.write(make_heading(text = repo, level = 1))
    markdown_file.write("\nGenerated markdown file for GitHub repository.\n\n")

    # Open each found file sequentially and add to markdown
    for index, path in enumerate(files, start = 1):
        print("Processing file "+str(index)+" of "+str(len(files)), end = "\r")
        # Check file depth
        file_name = path.rsplit("/", 1)[1]
        depth = file_depth(file_path = path, reference_directory = repo_directory)
        try:
            # Read the file
            with open(path, "r") as file:
                contents = file.readlines()
                # Add code to markdown
                markdown_file.write(make_heading(text = file_name, level = depth + 2))
                markdown_file.write(add_code_block(vector = contents))
        # TODO Handle exceptions properly  
        except Exception as error:
            print(error)

    # Close the newly created markdown file
    markdown_file.close()
    print(" " * 50, end = "\n")
    print("> Done.")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Convert respository contents to markdown file.")
    parser.add_argument("--repo_path",
                        type=str,
                        help="path to repo",
                        required=True)
    parser.add_argument("--md_file_path",
                        type=str,
                        help="path to save the output MD file",
                        default="output.md",
                        nargs="?")
    args = parser.parse_args()

    repo_to_markdown(repo_directory = args.repo_path,
                     md_file_path = args.md_file_path)
    