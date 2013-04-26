import sys
import os

from WCDB3 import start

# to run the program, use this command:
# python RunWCDB2.py > [output file] [input folder] [hostname] [username] [password] [database]
# start ( sys.stdin, sys.stdout, sys.argv )

for n,d,f in os.walk ( sys.argv [ 1 ] ) :
    start ( n, f, sys.stdout, sys.argv [ 1: ] )
