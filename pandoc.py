import re
def get_problems_from_pandoc_tex(text):
  problems = []
  empty_chars = [' ', '\n']
  matches = re.finditer(r'\\item\[\w{1,5}\]', text)
  problems_positions = []
  for i, match in enumerate(matches):
    # Adding the ending index of the prev problem
    if(i > 0):
      problems_positions[i-1]["end"] = match.start()

    index = match.end() + 1
    problems_positions.append({"st": index, "end": -1})

  end_of_file_match = re.search(r'\\end\{itemize\}',text)
  problems_positions[-1]["end"] = end_of_file_match.start()
  
  for index in problems_positions:
    problems.append(text[index['st']:index['end']].strip()) 
  
  for i,problem in enumerate(problems):
    print(f'******problem{i+1}*********')
    print(problem)
    print('\n\n')
  return problems