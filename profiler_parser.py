import subprocess
import string

class Line:
    def __init__(self, line_num, hits, time, time_per_hit, time_percent, content, indent_level):
        self.line_num = line_num
        self.hits = hits
        self.time = time
        self.time_per_hit = time_per_hit
        self.time_percent = time_percent
        self.content = content
        self.indent_level = indent_level


    def __repr__(self):
        return str([self.line_num, self.hits, self.time, self.time_per_hit, self.time_percent, self.content, self.indent_level])


class ProfilerOutput:
    def __init__(self, total_time, lines):
        self.total_time = total_time
        self.lines = lines


    def __str__(self):
        toReturn = ""
        toReturn = toReturn + "Total Time: " + str(self.total_time) + "\n"
        for elem in self.lines:
            if elem is not None:
                toReturn = toReturn + str(elem) + "\n"
        return toReturn


def does_line_contain_profile_info(tokens):
    """Return True if tokens contains all profile info"""
    if len(tokens) < 6:
        return False

    for i, tok in enumerate(tokens):
        if i < 5:
            try:
                float(tok)
            except ValueError:
                return False

    return True


def profile_and_parse(code) -> ProfilerOutput:
    code_lines = code.split("\n")

    # Remove old temp.py and write code to the file again
    subprocess.call(["rm", "temp.py"])
    echo_cmd = "echo \"" + code + "\" > temp.py"
    subprocess.Popen(echo_cmd, shell=True, stdout=subprocess.PIPE)

    # profile temp.py
    profile_cmd = "python profiler.py"
    p = subprocess.Popen(profile_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    raw_profile_encoded, _ = p.communicate()
    raw_profile = raw_profile_encoded.decode()

    lines_raw = raw_profile.split("\n")
    total_time = 0
    found_lines = False
    lines = []

    for line in lines_raw:
        # mark when following lines are going to be profile info for lines
        if "====" in line:
            found_lines = True
            continue

        if found_lines:
            tokens = line.split()

            # if this line has profile information for it (time, etc)
            if does_line_contain_profile_info(tokens):
                line_num, hits = map(int, tokens[:2])
                time, time_per_hit, time_percent = map(float, tokens[2:5])
                content = " ".join(tokens[5:])
            # else assume default info
            elif len(tokens) > 0:
                line_num = int(tokens[0])
                hits, time, time_per_hit, time_percent = [0] * 4
                content = " ".join(tokens[1:])
            else:
                continue # continue if junk line
            indents = code_lines[line_num - 1].count('\t')

            # Add more space till we have a list where index i can be the line info for i = line_num
            while len(lines) < line_num + 1:
                lines.append(None)
            lines[line_num] = Line(line_num, hits, time, time_per_hit, time_percent, content, indents) # TODO: implement indent level
            continue

        if "Total time: " in line:
            total_time = float(line.split()[2])
            continue

    output = ProfilerOutput(total_time, lines)
    return output

# Test!
# print(profile_and_parse("""
# import math
#
# def beans():
# 	krager = 1 + 4
#
# def run():
# 	a = 1
# 	for i in range(int(math.pow(100,2))):
# 		a=i
# 		a = a**2
#
# 	a = 1
# 	for i in range(int(math.pow(100,2))):
# 		a=i
#
# 	a = 1
# 	for i in range(int(math.pow(100,2))):
# 		a=i
#
# 	a = 1
# 	for i in range(int(math.pow(100,2))):
# 		a=i
# 	beans()
# # return a
# """))
