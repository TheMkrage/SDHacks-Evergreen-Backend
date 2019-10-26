tokens = set()
tokens.add("if")
tokens.add("len(")
tokens.add(")")
tokens.add("==")
tokens.add("0:")
tokens.add(":")


rules = {}
rules[" ".join(['if', 'len(', 'var_0', ')', '==', '0:'])] = ['if', 0, ":"]

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
		elif char == ")":
			spaced += " "
			spaced += char
		else:
			spaced += char

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

def from_profile(list_of_lines):
	suggestions = []

	for i, line in enumerate(list_of_lines):
		line_num, hits, time, time_per_hit, time_percent, content, indents = line

		if "for" in content:
			pass

		else:
			# single line case
			sugg = grammar_on_line(content, line_num, line_num)
			if(content != " ".join(sugg)):
				suggestions.append((sugg, line_num, line_num))
	return suggestions

test = [
[1, 2, 3, 4, 5, "if len(A) == 0:", 0],
[2, 2, 3, 4, 5, "s = ''", 0],
[3, 2, 3, 4, 5, "for substring in list:", 0],
[4, 2, 3, 4, 5, "s += substring", 1],
[5, 2, 3, 4, 5, "if len(A) == 0:", 0]
]

print(from_profile(test))	
