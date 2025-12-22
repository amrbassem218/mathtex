import os
from subprocess import PIPE, run
import sys
import re

def check_file_exists(path):
  if(not os.path.exists(path)):
    raise Exception("File doesn't exist")
  
def read_file(path):
  check_file_exists(path)
  with open(path, 'r') as f:
    return f.read()

def get_full_path(path):
  cwd = os.getcwd()
  full_path = os.path.join(cwd, path)
  check_file_exists(full_path)
  return full_path

  
def main(path):
  full_path = get_full_path(path) 
  file_text = read_file(full_path)
  if(not file_text or len(file_text) == 0):
    raise Exception("The file couldn't be read")
  
  problems = get_problems(file_text)
if __name__ == "__main__":
  args = sys.argv
  if len(args) != 2:
    raise Exception("Enter 1 file only pls")
  elif not args[1].endswith('.tex'):
    raise Exception("Only accepts .tex files")
  
  path = args[1]
  main(path)
  
