import os
from subprocess import PIPE, run
import sys
from pandoc import get_problems_from_pandoc_tex
import argparse
from pathlib import Path
import re
import json
from utils.database_action import Db_action
def read_file(path):
    if not os.path.exists(path):
        raise Exception("File doesn't exist")
    with open(path, "r") as f:
        return f.read()

# Check path if file/dir exists if not creates them, optionally takes text to add into files
def check_and_create(path, replace, text=None):
    final_path = Path(path).resolve()
    parent_path = final_path.parent
    if(not parent_path.exists()):
        os.makedirs(parent_path)
    if not replace:
        counter = 1
        while os.path.exists(final_path):
            if os.path.isfile(final_path):
                print("", final_path)
                file_extension = re.search(r"\.\w{2,5}$", str(final_path))
                final_path = Path(f"{Path(path).name}{counter}{file_extension.group()}").resolve()
            elif os.path.isdir(final_path):
                final_path = Path(f"{Path(path).name}{counter}/").resolve()
            counter += 1

    if final_path.suffix:
        with open(final_path, "w") as f:
            if text:
                f.write(text)
    elif not Path(final_path).exists():
        os.mkdir(final_path)
    return final_path

def get_html_from_tex(tex):
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
        "--mathjax",
    ]
    res = run(commands, stdin=PIPE, stdout=PIPE)
    return res.stdout

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
    parser.add_argument("-o", "--output", help="Set the output directory", default=None)
    parser.add_argument(
        "-t",
        "--type",
        help="Get the type problems of .tex file either single or multiple",
        choices=["single", "multiple"],
        default="multiple",
    )
    parser.add_argument(
        "-r", "--replace", help="replace the output directory if present", default=False, action='store_true'
    )
    parser.add_argument(
        "-p","--push",
        help="Push the problems to DB",
        default=False,
        action='store_true'
    )
    args = parser.parse_args()


    # Getting input 
    args.input = Path(args.input).resolve()
    if not os.path.exists(args.input):
        raise Exception("File Path doesn't exist")

    input_text = read_file(args.input)
    if not input_text or len(input_text) == 0:
        raise Exception("The file couldn't be read or it's empty")

    
    # Getting output
    if args.output == None: 
        args.output = args.input.name.split('.')[0] + '.json' 
    else:
        p_output = Path(args.output) 
        if len(p_output.suffix) == 0:
            args.output = args.input.name.split('.')[0] + '.json' 
            output_dir = check_and_create(p_output, args.replace)
            args.output = os.path.join(output_dir, args.output)

    args.output = Path(args.output)
    
    
    if args.type == "single":
        pass
    elif args.type == "multiple":
        problems = []
        match args.source:
            case "pandoc":
                problems = get_problems_from_pandoc_tex(input_text)
        if len(problems) == 0:
            print("Couldn't get problems or file doesn't contain any")

        
        output = check_and_create(args.output, args.replace)
        for i, problem in enumerate(problems):
            # print(i, problem)
            html = get_html_from_tex(problem['latex'])
            problems[i]["html"] = html.decode('utf-8') 
        
        with open(output, 'w') as f:
            json.dump(problems, f)
        
    else:
        raise Exception("Argument type accepts only (single, multiple)")
    
    if args.push:
        db = Db_action()
        db.create_problem(problems[0])
        


if __name__ == "__main__":
    main()
