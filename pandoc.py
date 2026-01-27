import re
def get_problems_from_pandoc_tex(text):
  problems = []
  empty_chars = [' ', '\n']
  matches = re.finditer(r'\\item\[\w{1,5}\]', text)
  problems_positions = []
  titles = []
  for i, match in enumerate(matches):
    title = re.search(r'(?<=\[)\w{1,}', match.group())
    titles.append(title.group())
    # Adding the ending index of the prev problem
    if(i > 0):
      problems_positions[i-1]["end"] = match.start()

    index = match.end() + 1
    problems_positions.append({"st": index, "end": -1})

  end_of_file_match = re.search(r'\\end\{itemize\}',text)
  problems_positions[-1]["end"] = end_of_file_match.start()
  
  for index,positions in enumerate(problems_positions):
    problem = {
      "name": titles[index],
      "description_latex":text[positions['st']:positions['end']].strip(),
    }
    problems.append(problem) 
  
  # for i,problem in enumerate(problems):
  #   print(f'******problem{i+1}*********')
  #   print(problem)
  #   print('\n\n')
  return problems