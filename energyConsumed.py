import subprocess
import specs
def calculate_power(total_time, inst_name):

	local_ram = 16
	local_cores = 2
	local_speed = 1.3 
	local_power = 60 # found using RAPL

	if inst_name == "local":
		num_cores, clock_speed, ram_gig = (local_cores, local_speed, local_ram)
	else:
		num_cores, clock_speed, ram_gig = specs.spec_dic[inst_name]



	adj_time = float(total_time) / (clock_speed/local_speed)
	adj_time = adj_time / (float(ram_gig)/local_ram)
	adj_pow = local_power * (float(num_cores) / local_cores) 

	power = adj_time*1.58*adj_pow / 1000
	print(power)
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

def CO2e(num_req, cmd, inst_name):
	total_time = get_time(num_req, cmd) # profiling to find total time to run code
	total_power  = calculate_power(total_time, inst_name)
	carbon_emit = 0.954 * total_power
	return carbon_emit


def main():
	number_of_requests = 10000
	filename = "prof_test.py"
	cmd = "python -m cProfile -s cumtime"
	cmd = cmd + " " + filename
	print(CO2e(number_of_requests, cmd, "local"))
	

if __name__ == '__main__':
	main()
