import sys

from WCDB2 import start

# to run the program, use this command:
# python RunWCDB2.py < [input file] > [output file] [hostname] [username] [password] [database]
start ( sys.stdin, sys.stdout, sys.argv )