USER MANUAL FOR THE SHELL:

To run the shell, go to the location of the shell by typing 'cd <pathname>', once in the same directory of myshell.py, type
'python3 myshell.py' to run the shell.

OPERATION AND COMMANDS OF THE SHELL:

This shell can do many things. It supports a variety of commands and background execution of programs. This manual will outline
how to use every component of this shell. 

cd command: This command allows you change your current working directory. 'cd <pathname>' will change your current working 
directory to <pathname>. Typing 'cd' will print your current working directory.'cd ..' will move your up or 'back' on directory.  
So, if you are /usr/bin/tmp, 'cd ..' moves you to /usr/bin. This command supports i/o redirection.

clr command: This command clears the screen.

dir command: Typing 'dir' will list all files in your current working directory. Typing 'dir <pathname>' will list all files
in <pathname>. This command supports i/o redirection. 

environ command: This command displays all the environment strings. This command supports i/o redirection. 

echo command: This command prints to the terminal. Typing 'echo <string>' will print <string> to the terminal. This command 
supports i/o redirection.

help command: Typing 'help <command>' will display help on <command>.

pause command: This command pauses the terminal until the Enter key is pressed. 

quit command: This command terminates the shell. 
helpmore command: This command prints this manual. NOTE: This command will not work unless 'readme.txt' and 'myshell.py' must 
be in the same folder.

ENVIRONMENT CONCEPTS:

When a program is invoked it is given an array of strings called the environment. This is a list of name-value pairs, of 
the form 'name=value'. Typing 'environ' will list all environment strings. When Bash invokes an external command, the variable 
'$_' is set to the full pathname of the command and passed to that command in its environment.

I/O REDIRECTION:

Input output redirection is an extremely useful feature. It allows you to take input from a batch file and also allows you to 
put the output of different commands into batch files. 
The '>' symbol is used for output (STDOUT) redirection. For example, 
typing 'dir > output.txt' will put the output of 'dir' into output.txt. > will override everything in output.txt. If you do
not wish for the contents of output.txt to be overwritten, using '>>' instead of '>' will append to output.txt rather than
overwritting it.
The '<' symbol is used for input(STDIN) redirection. Rather than taking input for commands from inside the shell we can
take input from batch files. For example, input.txt contains a pathname. Let's call it <pathname> for simplicity. If we
type 'dir < input.txt' the shell will list the files in <pathname>. 'dir < input.txt' is the exact same as doing 
'dir <pathname>' in this case.

BACKGROUND EXECUTION:

The shell also supports background execution of programs. A background process executes independently of the shell, leaving the 
terminal free for other work. To run a process in the background, include an & (an ampersand) at the end of the command you use 
to run the job. For example, writing 'python3 test.py &' will mean that that program runs as a subprocess. 
