import os
from subprocess import PIPE, run
import sys
from pandoc import get_problems_from_pandoc_tex
import argparse
from pathlib import Path
import re


def check_file_exists(path):
    if not os.path.exists(path):
        raise Exception("File doesn't exist")


def read_file(path):
    check_file_exists(path)
    with open(path, "r") as f:
        return f.read()


# Check path if file/dir exists if not creates them, optionally takes text to add into files
def check_and_create(path, replace, text=None):
    final_path = Path(path).resolve()
    if not replace:
        counter = 1
        while os.path.exists(final_path):
            if os.path.isfile(final_path):
                file_extension = re.search(r"\.\w{2,5}$", final_path)
                final_path = Path(f"temp{counter}{file_extension.group()}").resolve()
            elif os.path.isdir(final_path):
                final_path = Path(f"temp{counter}/").resolve()

    print("final_path:", final_path)
    print("exists:", os.path.exists(final_path))
    print("isdir:", os.path.isdir(final_path))
    if final_path.suffix:
        with open(final_path, "w") as f:
            if text:
                f.write(text)
    
    else:
        os.mkdir(final_path)
    return final_path

def get_html_from_tex(tex, output):
    if len(tex) == 0:
        return
    temp_file_path = check_and_create("temp.tex", True, tex)
    commands = [
        "pandoc",
        temp_file_path,
        "-f",
        "latex",
        "-t",
        "html",
        "-o",
        output,
        "--mathjax",
    ]
    run(commands, stdin=PIPE, stdout=PIPE)


def main():
    parser = argparse.ArgumentParser(
        description="convert Latex Contests into HTML problem"
    )

    # (required)
    parser.add_argument("input", help="Latex contest file (.tex) file type")
    parser.add_argument(
        "source",
        help="Source of .tex file (to know the nature of the algorithm to use)",
    )

    # (optional)
    parser.add_argument("-o", "--output", help="Set the output directory", default="/")
    parser.add_argument(
        "-t",
        "--type",
        help="Get the type problems of .tex file either single or multiple",
        choices=["single", "multiple"],
        default="multiple",
    )
    parser.add_argument(
        "-r", "--replace", help="replace the output directory if present", default=False
    )
    args = parser.parse_args()

    # Getting path
    # parsing all paths 
    args.input = Path(args.input).resolve()
    args.output = Path(args.output).resolve()
    if not os.path.exists(args.input):
        raise Exception("File Path doesn't exist")

    # Getting input 
    file_text = read_file(args.input)
    if not file_text or len(file_text) == 0:
        raise Exception("The file couldn't be read or it's empty")


    if args.type == "single":
        pass
    elif args.type == "multiple":
        problems = []
        match args.source:
            case "pandoc":
                problems = get_problems_from_pandoc_tex(file_text)
        if len(problems) == 0:
            print("Couldn't get problems or file doesn't contain any")

        
        output_dir = check_and_create(args.output, args.replace)
        for i, problem in enumerate(problems):
            # print(i, problem)
            get_html_from_tex(problem['latex'], os.path.join(output_dir, f"{problem['title']}.tex"))
    else:
        raise Exception("Argument type accepts only (single, multiple)")


if __name__ == "__main__":
    main()
