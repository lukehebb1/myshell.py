#Name: Luke Hebblethwaite
#Python version used: 3.7.1

import cmd, sys, os, getpass, subprocess

class MyShell(cmd.Cmd):

	intro = "Welcome to my shell. \nType 'help' to access specific information on the available commands."
	prompt = os.getcwd() + "> "
	#change environment variable for 'SHELL'
	os.environ['SHELL'] = os.getcwd()+'/MyShell'

	def default(self, arg):
		#this method is run if a non built in command is inputed.
		args = tokenise(arg)
		try:
			if args[-1] == '&':
				#runs program as a backgroud process
				for i in range(0, len(args[:-1])):
					#if outputting to file and overwriting it
					if args[i] == '>':
						try:
							overwrite_file(subprocess.Popen(args[:i]), args[i+1:])
						except IndexError:
							print("Error: No filename given.")
					#if outputing to file and apppend to it
					elif args[i] == '>>':
						try:
							append_file(subprocess.Popen(args[:i], args[i+1]))
						except IndexError:
							print("Error: No filename given.")
					else:
						#if not using i/o redirection
						try:
							subprocess.Popen(args[:-1])
						except FileNotFoundError:
							print("Error: That command does not exist.")
			else:
				#if not running program as a background process
				try:
					subprocess.run(args)
				except FileNotFoundError:
					#if the command doesn't exist
					print('Error: That command does not exist.')
		except IndexError:
			#if command with no arguments given
			try:
				subprocess.run(args)
			except FileNotFoundError:
				#if the command doesn't exist
				print('Error: That command does not exist')

	def do_cd(self, arg):
		"""Displays the name of or changes the current directory. 
cd <pathname> will change your current working directory to <pathname>."""
		try:
			#if no arg is given
			if arg == '':
				print("The current directory is " + os.getcwd())
			else:
				#if an arg is given
				os.chdir(arg)
				#change environment variable for 'PWD'
				os.environ['PWD'] = os.getcwd()
				#update prompt
				prompt = os.getcwd() + "> "
		except FileNotFoundError:
			print("That path does not exist.")

	def do_clr(self, arg):
		"""Clears the screen."""
		print("\033c")

	def do_dir(self, arg):
		'''\nlists the contents of a directory, \
or prints the current directory if no arguemts are given\n'''
		#gets list of command line arguments
		args = tokenise(arg)
		try:
			#if using standard input
			if args[0] == '<':
				try:
					#use contents of input file as directory
					data = from_file(args[1])
					try:
						#if using output to append data
						if args[2] == '>>':
							try:
								#append contents to the file
								append_file(dir_to_str(data[0]), args[3:])
							except IndexError:
								#if no filename specified
								print('Error: No filename given')
								string = 'Usage: dir < {} >> <filename>'
								string = string.format(data[0])
								print(string)
						#if using output to overwrite data
						elif args[2] == '>':
							try:
								#overwrite the data in the file
								overwrite_file(dir_to_str(data[0]), args[3:])
							except IndexError:
								#if no filename specified
								print('Error: No filename given')
								string = 'Usage: dir < {} >> <filename>'
								string = string.format(data[0])
								print(string)
						else:
							#if standard output not being used
							#prints content
							print(dir_to_str(data[0]))
					except IndexError:
						#if standard output not being used
						#prints content
						print(dir_to_str(data[0]))
				except IndexError:
					#shows this error message if no filename was specified
					print('Error: No filename given')
					print('Usage: dir < <filename>')
			elif args[1] == '>>':
				#if using append output with a specific directory
				try:
					#appends to the filename specified
					append_file(dir_to_str(args[0]), args[2:])
				except IndexError:
					#shows this error if no filename is specified
					print('Error: No filename given')
					print('Usage: dir {} >> <filename>'.format(args[0]))
			elif args[1] == '>':
				#if using overwrite output with a specific directory
				try:
					#overwrites the contents of the listed directory
					overwrite_file(dir_to_str(args[0]), args[2:])
				except IndexError:
					#shows this error if no filename is specified
					print('Error: No filename given')
					print('Usage: dir {} > <filename>'.format(args[0]))
				#if using append output without a specified directory
			elif args[0] == '>>':
				try:
					#append to the specified file
					append_file([dir_to_str()], args[1:])
				except IndexError:
					#if no filename is specified
					print('Error: No filename given')
					print('Usage: dir >> <filename>')
			elif args[0] == '>':
				#if using overwrite without a specified directory
				try:
					#overwrites file's contents
					overwrite_file([dir_to_str()], args[1:])
				except IndexError:
					#if no filename is specified
					print('Error: No filename given')
					print('Usage: dir > <filename>')
			else:
				#prints the content of the specified directory
				print(dir_to_str(args[0]))
		except IndexError:
			#prints the content of the current directory
			print(dir_to_str())

	def do_environ(self, arg):
		"""Lists all the environment strings."""
		#converts arg to a list
		args = tokenise(arg)
		try:
			#if using overwrite
			if args[0] == '>':
				try:
					#output environment strings to the specified file
					overwrite_file(get_environ(), args[1:])
				except IndexError:
					#print this Error message if no filename is given
					print('Error: No filename given')
					print('Usage: environ > <filename>')
			#if using append
			elif args[0] == '>>':
				try:
					#appends output to the given file
					append_file(get_environ(), args[1:])
				except IndexError:
					#print this Error message if no filename is given
					print('Error: No filename given')
					print('Usage: environ >> <filename>')
		except IndexError:
			print("\n".join(get_environ()))

	def do_echo(self, arg):
		"""Displays messages."""
		args = tokenise(arg)
		comment = []
		count = 0
		for i in range(0, len(args)):
			#if using overwrite
			if args[i] == '>':
				#concatenate preceding arguments to a string
				echoed = get_echo(comment)
				try:
					#outputs the string to the given file
					overwrite_file([echoed], args[i+1:])
					break
				except IndexError:
					#prints this error message if no filename is given
					print('Error: No filename given')
					print('Usage: echo <comment> > <filename>')
					break
			#if using append
			elif args[i] == '>>':
				#concatenate preceding arguments to a string
				echoed = get_echo(comment)
				try:
					#outputs the string to the given file
					append_file([echoed], args[i+1:])
					break
				except IndexError:
					#shows this error if no filename is given
					print('Error: No filename given')
					print('Usage: echo <comment> >> <filename>')
					break
			else:
				#appends arguments that are not output commands to a list
				comment.append(args[i])
				count += 1
		#if the loop did not break early
		if count == len(args):
			#print the concatenated list of arguments as a string
			print(get_echo(comment))

	def do_help(self, arg):
		"""Displays the manual"""
		os.system("more readme.txt")

	def do_pause(self, arg):
		"""Pauses the shell until 'Enter' is pressed."""
		getpass.getpass("Press 'Enter' to continue...")

	def do_quit(self, arg):
		"""Exits the shell."""
		print("Quitting...\nThank you for using my shell.")
		exit()

def get_echo(comment):
	'''\nConcatenates a list to a single string\n'''
	return " ".join(comment)

def get_environ():
	'''\nreturns a list containing all the environment \
variables and their values as strings\n'''
	env_list = []
	for x in os.environ:
		env_list.append('{} : {}'.format(x, os.environ[x]))
	return env_list

def dir_to_str(directory=None):

	'''\nReturns the contents of a directory as a string\n'''
	try:
		#if a directory is specified
		if directory is not None:
			# Return a string containing all the contents
			return "\n".join([f for f in os.listdir(directory)])
		#if no directory is specified
		else:
			#return a string containing the contents of the current directory
			return '\n'.join([f for f in os.listdir()])
	except FileNotFoundError:
		#shows this error message if the directory does not exist
		print('Error: Directory "{}" not found'.format(directory))

def from_file(file):
	#method that returns a list of all the lines contained in the file
	try:
		with open(file, 'r') as f:
			#returns a list of all the lines contained in the file
			return [args.strip() for args in f.readlines()]
	except FileNotFoundError:
		#shows this error message if the file does not exist
		print('Error: File "{}" not found'.format(filename))

def overwrite_file(data, args):
	#method to overwrite data to file
	try:
		with open(args[0], 'w+') as f:
			for a in data:
				f.write(a)
				f.write('\n')
	except IndexError:
		print("Usage: <command> > <filename>")

def append_file(data, args):
	#method to append data to file
	try:
		with open(args[0], 'a+') as f:
			for a in data:
				f.write(a)
				f.write('\n')
	except IndexError:
		print("Usage: <command> > <filename>")

def tokenise(args):
	#tokenises the args given
	return args.split()

if __name__ == '__main__':
	try:
		#if using file as input
		with open(sys.argv[1], 'r') as f:
			shell = MyShell()
			cmds = f.readlines()
			cmds.append("quit")
			shell.cmdqueue = cmds
			shell.cmdloop()
	except IndexError:
		#if not using file as input
		MyShell().cmdloop()
