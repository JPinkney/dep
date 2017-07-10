import platform
import json
import os
import sys
import subprocess

MAC_OS = "OSX"
LINUX_OS = "Linux"
WINDOWS_OS = "Windows"
OTHER_OS = "Other"

COMMAND_LIST = [MAC_OS, LINUX_OS, WINDOWS_OS, OTHER_OS]
json_output = {}

def setup_file():
	setup_file_if_not_exists()

	#This is currently running to the end
	with open('dependency.dep', 'r') as f:
		#File is open and we are reading it
		lines = f.readlines()

		last_cmd = ""
		for line in lines:
			#Check for the the OS at that location
			input_token = line.strip()
			if check_for_header(input_token):
				last_cmd = input_token
				json_output[last_cmd] = []
			else:
				if not (last_cmd == "" or input_token == ""):
					split_line = line.split(" ")
					package_manager = split_line[0].strip()
					dependency = split_line[1].strip()
					json_output[last_cmd].append({
						"packagemanager": package_manager,
						"dependency": dependency,
						"install": input_token
					})
		return json_output
		

def check_for_header(input_str):
	for command in COMMAND_LIST:
		if input_str.lower() == command.lower():
			return True
	return False

def install_dependencies(depencencies_for_os):
	for install_item in depencencies_for_os:
		if is_package_manager_found(install_item["packagemanager"]):
			install_dependency(install_item["install"])

def is_package_manager_found(package_manager):
	try:
		p = subprocess.Popen(package_manager, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	except:
		print("Could not find dependency manager: " + package_manager)
		return False
	return True

def install_dependency(depencency):
	try:
		print("Installing dependency: " + depencency)
		p = subprocess.Popen(depencency, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		out, err = p.communicate()
		print(out)
		print(err)
		print("Installed dependency: " + depencency)
	except:
		print("Installing dependency: " + depencency + " failed")

def setup_file_if_not_exists():
	if not os.path.isfile('dependency.dep'):
		setup_file_even_if_exists()

def setup_file_even_if_exists():
	with open('dependency.dep', "w+") as f:
		f.write("OSX\n\n")
		f.write("Linux\n\n")
		f.write("Windows\n\n")
		f.write("Other\n")

def setup(sys_input):
	if len(sys_input) != 2:
		print("Installing depencies failed")
		exit(0)
	
	first_cmd = sys_input[0]
	second_cmd = sys_input[1]

	if second_cmd == "init":
		setup_file_if_not_exists()
	elif second_cmd == "run":
		setup_run()
	elif second_cmd == "reset":
		setup_file_even_if_exists()
	else:
		print("Blah blah I do not remember")

def setup_run():
	current_os = platform.system()
	if current_os == "Darwin":
		current_os = "OSX"
	depencencies_json = setup_file()
	depencencies_for_os = depencencies_json[current_os]
	print("Installing depencies for " + current_os)
	install_dependencies(depencencies_for_os)

if __name__ == '__main__':
	setup(sys.argv)