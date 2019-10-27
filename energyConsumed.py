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


def CO2e(time_per_request, num_req, inst_name):
	total_time = time_per_request * num_req
	total_power  = calculate_power(total_time, inst_name)
	carbon_emit = 0.954 * total_power
	return carbon_emit


def metric(CO2):
	american_life_year = 36156/365
	NY_SF = 1984
	car_lifetime = 9200/365

	num_life = round(CO2 / american_life_year, 1)
	num_flight = round(CO2 / NY_SF, 1)
	num_car = round(CO2 / car_lifetime, 1)

	return [num_life, num_flight, num_car]
