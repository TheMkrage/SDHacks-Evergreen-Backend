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
tokens.add("=")
tokens.add("while")
tokens.add("<")
tokens.add(">")
tokens.add("list_length")
tokens.add("\n")
tokens.add("while True:")
tokens.add("if not")

rules = {}
rules["if len( var_0 ) == var_1 :"] = ['if not', 0, ":"]
rules["for var_0 in var_1 : var_2 += var_3"] = [2, "=", "''.join(", 1, ")"]
rules["while var_0 < len( var_1 ) :"] = ["list_length", "=", "len(", 1,')','\n', 'while',0, "<", "list_length", ":"]
rules["while True:"] = "while 1:"

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
	# print(spaced)
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
	# print(tokenized_str)
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
	sugg = sugg.replace("\n ","\n")

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

			# print(full_line)
			sugg = grammar_on_line(full_line, first_line, last_line)

			a = full_line
			b =  " ".join(sugg)

			if([c for c in a if c.isalpha()] != [c for c in b if c.isalpha()]):
				# print([c for c in a if c.isalpha()], [c for c in b if c.isalpha()])
				sugg = " ".join(sugg)
				sugg = add_indents(sugg, indents)
				sugg = improve_suggestion(sugg)
				desc = "Using the .join function is a quicker way to concatenate a string."
				suggestions.append((sugg, first_line, last_line-1, desc)) # minus for quick fix

		elif(content in tokens):
			sugg = rules[content]
			sugg = "\t"*indents + sugg
			sugg = improve_suggestion(sugg)
			desc = "Even though 'while True' accomplishes the same thing, 'while 1' is a single jump operation."
			suggestions.append((sugg, line_num, line_num, desc))


		elif("while" in content):
			sugg = grammar_on_line(content, line_num, line_num)
			sugg = " ".join(sugg)
			# print(content)
			if(content.replace(" ", "") != sugg.replace(" ", "")):
				sugg = "\t"*indents + sugg
				next_line = '\n' + "\t"*indents
				sugg = sugg.replace('\n', next_line)
				sugg = improve_suggestion(sugg)
				desc = "Save some time by storing the length instead of recalculating each time."
				suggestions.append((sugg, line_num, line_num, desc))
		else:
			# single line case
			sugg = grammar_on_line(content, line_num, line_num)
			sugg = " ".join(sugg)
			if(content.replace(" ", "") != sugg.replace(" ", "")):
				sugg = "\t"*indents + sugg
				sugg = improve_suggestion(sugg)
				desc = "Treating a list as a boolean is quicker than trying to calculate it's length."
				suggestions.append((sugg, line_num, line_num, desc))


	return suggestions

# test = [
# Line(1, 2, 3, 4, 5, "if len(A) == 0:", 2),
# Line(2, 2, 3, 4, 5, "s = ''", 2),
# Line(3, 2, 3, 4, 5, "for substring in list:", 2),
# Line(4, 2, 3, 4, 5, "s += substring", 3),
# Line(5, 2, 3, 4, 5, "if len(A) == 0:", 2),
# Line(6, 2, 3, 4, 5, "def run()", 2),
# Line(7, 2, 3, 4, 5, "while A < len(B):", 2),
# Line(7, 2, 3, 4, 5, "while True:", 2)
# ]
#
# print(from_profile(test))
