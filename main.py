import os
from subprocess import PIPE, run
import sys
from pandoc import get_problems_from_pandoc_tex
import argparse
from pathlib import Path

def check_file_exists(path):
  if(not os.path.exists(path)):
    raise Exception("File doesn't exist")
  
def read_file(path):
  check_file_exists(path)
  with open(path, 'r') as f:
    return f.read()


def main():
  parser = argparse.ArgumentParser(
    description="convert Latex Contests into HTML proble"
  )

  #(required)
  parser.add_argument(
    "input",
    help="Latex contest file (.tex) file type"
  )
  parser.add_argument(
    "source",
    help="Source of .tex file (to know the nature of the algorithm to use)"
  ) 

  # (optional)
  parser.add_argument(
    '-o','--output',
    help="Set the output directory",
    default='/'
  )
  parser.add_argument(
    '-t', '--type',
    help="Get the type problems of .tex file either single or multiple",
    choices=['single','multiple'],
    default='multiple'
  )
  args = parser.parse_args()
  
  
  # Getting path
  full_path = Path(args.input).resolve()
  if(not full_path.exists()):
    raise Exception("File Path doesn't exist")
  
  # Getting file
  file_text = read_file(full_path)
  if(not file_text or len(file_text) == 0):
    raise Exception("The file couldn't be read or it's empty")
  
  if(args.type == 'single'):
    pass
  elif(args.type == 'multiple'):
    problems = "" 
    match args.source:
      case "pandoc":
        problems = get_problems_from_pandoc_tex(file_text)
     
  else:
    raise Exception("Argument type accepts only (single, multiple)")

if __name__ == "__main__":
  main() 
