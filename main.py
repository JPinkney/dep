import platform
import json
import os
import sys
import subprocess

MAC_OS = "OSX"
LINUX_OS = "Linux"
WINDOWS_OS = "Windows"
OTHER_OS = "Other"

OS_LIST = [MAC_OS, LINUX_OS, WINDOWS_OS, OTHER_OS]
file_info_dict = {}

def file_to_dict():
	"""Turn dependency.dep file into python dictionary

    Returns:
        dependency.dep in a python dictionary
    """

	setup_file_if_not_exists()

	with open('dependency.dep', 'r') as f:
		lines = f.readlines()

		last_cmd = ""
		for line in lines:

			input_token = line.strip()

			if check_for_os_header(input_token):
				last_command = input_token
				file_info_dict[last_command] = []

			else:

				if not (last_command  == "" or input_token == ""):
					split_line = line.split(" ")
					package_manager = split_line[0].strip()
					dependency = split_line[1].strip()
					file_info_dict[last_command].append({
						"packagemanager": package_manager,
						"dependency": dependency,
						"install": input_token
					})

		return file_info_dict
		

def check_for_os_header(input_str):
	"""Check if input_str is a valid supported OS

    Args:
        input_str: the name of an os.
    Returns:
        True if input_str is a valid supported OS otherwise False
    """

	for command in OS_LIST:
		if input_str.lower() == command.lower():
			return True
	return False

def install_dependencies(depencencies_for_os):
	"""Install all depencies listed in depencencies_for_os

    Args:
        depencencies_for_os: a python dictionary of dependencies to install
    """

	for install_item in depencencies_for_os:
		if is_package_manager_found(install_item["packagemanager"]):
			install_dependency(install_item["install"])

def is_package_manager_found(package_manager):
	"""Check if package_manager is found on the system

    Args:
        package_manager: the name of the package manager to check for
    Returns:
        True if the package manager is one the system otherwise False
    """

	try:
		p = subprocess.Popen(package_manager, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	except:
		print("Could not find dependency manager: " + package_manager)
		return False
	return True

def install_dependency(depencency):
	"""Install the specific dependency

    Args:
        depencency: the dependency you want to install.
    """

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
	"""Setup the file if it does not exist"""

	if not os.path.isfile('dependency.dep'):
		setup_file_even_if_exists()

def setup_file_even_if_exists():
	"""Setup the file with correct OS headers"""

	with open('dependency.dep', "w+") as f:
		f.write("OSX\n\n")
		f.write("Linux\n\n")
		f.write("Windows\n\n")
		f.write("Other\n")

def check_inputs(sys_input):
	"""Run the program based off of sys_input"""

	if len(sys_input) != 2:
		print("Invalid number of parameters")
		exit(0)
	
	first_cmd = sys_input[0]
	second_cmd = sys_input[1]

	if second_cmd == "init":
		setup_file_if_not_exists()
	elif second_cmd == "run":
		main_dependency_installer()
	elif second_cmd == "reset":
		setup_file_even_if_exists()
	else:
		print("Invalid command. Available commands are init, run, and reset")

def main_dependency_installer():
	"""Calcuates and installs all the depencies from dependecy.dep"""

	current_os = platform.system()
	if current_os == "Darwin":
		current_os = "OSX"
	depencencies_json = file_to_dict()
	depencencies_for_os = depencencies_json[current_os]
	print("Installing depencies for " + current_os)
	install_dependencies(depencencies_for_os)

if __name__ == '__main__':
	check_inputs(sys.argv)