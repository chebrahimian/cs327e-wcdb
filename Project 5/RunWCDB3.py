import sys

from WCDB3 import start

# to run the program, use this command:
# python RunWCDB3.py > [output file] [hostname] [username] [password] [database]
#start ( n, f, w, args ):
"""
imports an xml document into an ElementTree, imports that ElementTree into a mysql database,
then outputs the mysql database to a valid xml document, which is then written to the output file
n is the name of the folder containg the input files
f is the list of input files
w is the writer
args are the commandline arguments
"""
folder = "C:\Users\lsalsini\Documents\School\merge"
list = ['Better-Late-Than-Never.xml', 'Bonsai.xml', 'Byte-Me.xml',\
 'IsTuchenHereToday.xml', 'Miners.xml', 'Nameless.xml', 'Poseidon.xml',\
 'Tech-Knuckle-Support.xml', 'Virsus.xml']


start ( folder, list, sys.stdout, sys.argv )