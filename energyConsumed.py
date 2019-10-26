import subprocess

def calculate_power(total_time):
	sum_of_avg_pow = 10

	power = total_time*1.58*sum_of_avg_pow
	return power

def get_time(num_req, cmd):
	time = 0

	# begin profiling
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	stdout = []
	while True:
		line = p.stdout.readline()
		stdout.append(line)
		# print line,
		if line == '' and p.poll() != None:
			break
	# var = ''.join(stdout)
	summary_line = stdout[0].split()
	time = float(summary_line[4])
	# end profiling

	time = time*num_req
	time = time / 60
	time = time / 60
	return time

def CO2e(num_req, cmd):
	total_time = get_time(num_req, cmd) # profiling to find total time to run code
	total_power  = calculate_power(total_time)
	carbon_emit = 0.954 * total_power
	return carbon_emit


def main():
	number_of_requests = 10000
	filename = "prof_test.py"
	cmd = "python -m cProfile -s cumtime"
	cmd = cmd + " " + filename
	print(CO2e(number_of_requests, cmd))
	

if __name__ == '__main__':
	main()
