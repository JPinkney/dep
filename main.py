import os
import json

MAC_OS = "OSX"
LINUX_OS = "Linux"
WINDOWS_OS = "Windows"

COMMAND_LIST = [MAC_OS, LINUX_OS, WINDOWS_OS]
json_output = {}

def setup_file():
	filepath = './file.txt'

	#This is currently running to the end
	with open(filepath, 'r') as f:
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
						"dependency": dependency
					})

		print(json.dumps(json_output, indent=4))

def check_for_header(input_str):
	for command in COMMAND_LIST:
		if input_str == command:
			return True
	return False

def install_dependencies():
	pass


if __name__ == '__main__':
	setup_file()