git add - tells git what you want to stage
git commit - actually commits your changes to git
git init - initializes new empty repository
~ - home director
cd - change directory, used when you need to change paths

cat file - prints contents in files
sort file - prints out lines of file in sorted order
uniq file - eliminates consecutive duplicate lines from file
head file / tail file - print first and last few lines of file 

nano - edit .md files
git clone - clone git repository
rm -rf - remove/delete file
git status - can check if any commits and if branch is up-to-date
ls - lists files in folder that you are currently in

$ - represents that you are not the root user?
echo - prints out arguments
man - lets you look up more information about a command 
pwd - produces current working directory
. - "this directory"
.. - "the parent directory"

sed - has own prog language built for editing files
sed -i 's/pattern/replacement/g' file - replaces all instances of pattern with replacement in file; 
	-i - want substitutions to happen inline
	s/ - express in sed prog language that we want to do a substitution
	/g - indicates we want to replace all occurrences on each line rather than just first

find - lets you find files recursively that match certain conditions
	examples of how to use:
	* find ~/Downloads -type f -name "*.zip" -mtime +30
	- finds zip files in download directory that are older than 30 days
	* find ~ -type f - size +100M -exec ls -lh {} \;
	- finds files larger than 100M in home directory and lists them
	* find . -name "*.py" -exec grep -l "TODO" {} \;
	- finds any .py files with TODO items in them

awk - has own prog language like sed, but is built for parsing files
	awk '{print $2}' file
	- prints second whitespace-separated column of every line in file

pipes (|) - lets you string together output of one program with input of another
	takes "standard output" of program before | and makes it standard input of program after |

redirects (>file) - let you take standard output of program and write it to file instead of to terminal
	>>file - appends to file rather than overwrite it
	<file - tells shell to read from file instead of keyboard

CONDITIONALS:

if command1; then command2; command3; fi
	- executes command 1, if doesn't result in error, will run command2 and command3
	- can also use else branch

test command ([) - lets you evaluate conditions like "does a file exist" (test - f file / [-f file]) or "does a string equal another" ([ "$var" = "string"])
	- also [[ ]] which "safer" built-in version of test 

LOOPS: 
while - 
	while command1; do command2; command3; done
	- same as if statement but repeats until command1 starts error

for - 
	for varname in a b c d; do command; done
	- executes command 4 times, each time with $varname set to a, b, c, d
	may also be seen as:
	for i in $(seq 1 10); do
	- executes command seq 1 10 (prints numbers from 1 to 10) and replaces whole $() with command's output
	- basically 10-iteration for loop


COMMAND LINE ENVIRONMENT

ARGUMENTS:
$1 - first argument
$2 - second argument
...
$@ - access all arguments
$# - num of arguments
-/-- : represent flags
	- : used usually for single letters
	-- : used for longer names of flags
	ex) -a == --all
	single dashes can be combined: ls -l -a == ls -la or ls -al

mkdir src
mkdir docs 
#is equal to
mkdir src docs

globbing - special patterns that the shell will expand before calling the program
	- instead of long nonrecursive code, we can just run **rm *.py** which will search for files in urrent folder matching pattern .py
	- most common globs are: * (0 or more of anything), ? (exactly one of anything), and {} (expand comma-separated list of patterns into multiple arguments)

cat myfile | grep -P '\d+' | uniq -c
	- all programs execute at once
	- shell is connecting output of cat to input of grep and output of grep to input of uniq

stdin - standard input
- : accepted as filename to mean "read from stdin"
stdout - used for piping output of program to next command in pipeline
stderr - alternative stream that is intended for programs to report warnings 
fzf - fuzzy finder, reads lines from stdin and provides interactive interface to filter and select

foo=bar + $foo - used to assign variables in bash

shell variables are ONLY STRINGS
'' - literal strings and will not expand variables, perform command substitution, or process escape sequences
"" - delimited strings will
printenv - find current environment variables
export - modifies current environment and all child processes will inherit
unset - delete variable

SSH 
ssh-keygen : generates key pair
ssh-keygen -y -f/path/to/key - check if you have passphrase and validate it

- bash - ~/.bashrc, ~/.bash_profile
- git - ~/.gitconfig
- ssh - ~/.ssh/config
- vim - ~/.vimrc and ~/.vim folder
- tmux - ~/.tmux.conf

export PATH="$PATH:path/to/append" - tells shell to set value of $PATH variable to current value plus new path

tldr - provides simplified, example-focused man pages

alias - create an alias for another command


AI IN SHELL:
command generation:

$ llm cmd "find all python files modified in the last week"
find . -name "*.py" -mtime -7

pipeline integration:
$cat users.txt
Contact: john.doe@example.com
User 'alice_smith' logged in at 3pm
Posted by: @bob_jones on Twitter
Author: Jane Doe (jdoe)
Message from mike_wilson yesterday
Submitted by user: sarah.connor
$ INSTRUCTIONS="Extract just the username from each line, one per line, nothing else"
$ llm "$INSTRUCTIONS" < users.txt
john.doe
alice_smith
bob_jones
jdoe
mike_wilson
sarah.connor
