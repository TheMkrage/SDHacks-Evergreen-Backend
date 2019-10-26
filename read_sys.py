import subprocess

def main(cmd):
    """from http://blog.kagesenshi.org/2008/02/teeing-python-subprocesspopen-output.html
    """
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout = []
    while True:
        line = p.stdout.readline()
        stdout.append(line)
        print line,
        if line == '' and p.poll() != None:
            break
    # var = ''.join(stdout)
    summary_line = stdout[0].split()
    time = summary_line[4]
    return time

if __name__ == '__main__':
    cmd = "python -m cProfile -s cumtime prof_test.py"
    print(main(cmd))