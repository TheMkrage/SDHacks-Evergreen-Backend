from profiler_parser import Line

tokens = set()
tokens.add("if")
tokens.add("len(")
tokens.add(")")
tokens.add("==")
tokens.add("0:")
tokens.add(":")
tokens.add("for")
tokens.add("in")
tokens.add("+=")
tokens.add("''.join(")
tokens.add("''.jjoin(")
tokens.add("=")

rules = {}
rules["if len( var_0 ) == var_1 :"] = ['if', 0, ":"]
rules["for var_0 in var_1 : var_2 += var_3"] = [2, "=", "''.join(", 1, ")"]

def fix_pattern(line, fix):

	var_list =[]
	for token in line:
		if token not in tokens:
			var_list.append(token)

	result = []
	for token in fix:
		if token not in tokens:
			result.append(var_list[int(token)])
		else:
			result.append(token)

	return result

def space_parens(code_str):
	spaced = ""
	for char in code_str:
		if char == "(":
			spaced += char
			spaced += " "
		elif char == ")" or char == ":":
			spaced += " "
			spaced += char
		else:
			spaced += char
	spaced.replace("  ", " ")
	print(spaced)
	return spaced

def tokenize(token_list):
	var_count = 0
	tokenized_line = []

	for token in token_list:
		if token in tokens:
			tokenized_line.append(token)
		else:
			toke = "var_" + str(var_count)
			var_count += 1
			tokenized_line.append(toke)

	tokenized_line = " ".join(tokenized_line)
	return tokenized_line

def grammar_on_line(code_str, first_line, last_line):
	code_str = space_parens(code_str)
	token_list = code_str.split()

	tokenized_str = tokenize(token_list)

	if(tokenized_str in rules.keys()):
		token_list = fix_pattern(token_list, rules[tokenized_str])
	print(tokenized_str)
	return(token_list)

# print(grammar_on_line("if len(A) == 0:"))

def add_indents(sugg, indents):
	sugg_split = sugg.split("\n")
	new_sugg = [sugg_split[0]]
	for i in range(1, len(sugg_split)):
		if(sugg_split[i] == ""):
			new_sugg.append('\n')
		elif(sugg_split[i-1] == ""):
			new_sugg.append('\n'*indents)
			new_sugg.append(sugg_split[i])
		else:
			new_sugg.append(sugg_split[i])
	sugg = "".join(new_sugg)
	sugg = "\t"*indents + sugg

	# pass
	# new_string = ""
	# last_char = ''
	# train_length = 0
	# for c in new_string:
	# 	new_string += c
	# 	# When last_char does not match current, check if need to append j, reset vars
	# 	if c != last_char:
	# 		if last_char == 'j' and train_length >= 2:
	# 			new_string += 'j'
	# 		train_length = 1
	# 	else:
	# 		train_length += 1
	# 	last_char = c

	# # Handle if last character is j
	# if last_char == "j" and train_length >= 2:
	# 	new_string += "j"

	# sugg = new_string
	return sugg

def extract_values(krager_line):
	line_num = krager_line.line_num
	hits = krager_line.hits
	time = krager_line.time
	time_per_hit = krager_line.time_per_hit
	time_percent = krager_line.time_percent
	content = krager_line.content
	indents = krager_line.indent_level

	return((line_num, hits, time, time_per_hit, time_percent, content, indents))

def improve_suggestion(sugg):
	sugg = sugg.replace("( ","(")
	sugg = sugg.replace(" )",")")
	sugg = sugg.replace(" :",":")
	sugg = sugg.replace("\t","    ")

	return sugg
def from_profile(list_of_lines):
	suggestions = []

	for i, line in enumerate(list_of_lines):
		if line is None:
			continue
		line_num, hits, time, time_per_hit, time_percent, content, indents = extract_values(line)

		if "for" in content:
			first_line = line_num
			multiline = []

			multiline.append(content)

			j = i + 1
			while( indents < list_of_lines[j].indent_level):
				# print(j)
				# print(list_of_lines[j][6])
				multiline.append(list_of_lines[j].content)
				j += 1
				last_line = j
			full_line = " ".join(multiline)

			print(full_line)
			sugg = grammar_on_line(full_line, first_line, last_line)
			if(content != " ".join(sugg)):
				sugg = " ".join(sugg)
				sugg = add_indents(sugg, indents)
				sugg = improve_suggestion(sugg)
				suggestions.append((sugg, first_line, last_line))


			pass
		else:
			# single line case
			sugg = grammar_on_line(content, line_num, line_num)
			sugg = " ".join(sugg)
			if(content.replace(" ", "") != sugg.replace(" ", "")):
				sugg = "\t"*indents + sugg
				sugg = improve_suggestion(sugg)
				suggestions.append((sugg, line_num, line_num))


	return suggestions

# test = [
# Line(1, 2, 3, 4, 5, "if len(A) == 0:", 2),
# Line(2, 2, 3, 4, 5, "s = ''", 2),
# Line(3, 2, 3, 4, 5, "for substring in list:", 2),
# Line(4, 2, 3, 4, 5, "s += substring", 3),
# Line(5, 2, 3, 4, 5, "if len(A) == 0:", 2),
# Line(6, 2, 3, 4, 5, "def run()", 2)
# ]

# print(from_profile(test))
