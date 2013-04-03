import sys

from WCDB2 import start
#"""
with open ( sys.argv [ 1 ], "r" ) as r :
    with open ( sys.argv [ 2 ], "w" ) as w:
        start ( r, w, sys.argv )
#"""
#start ( sys.stdin, sys.stdout, sys.argv )