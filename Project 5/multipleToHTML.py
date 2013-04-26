"""
Reads in a directory path, directory name, and output name
execute as 
>>> python multipleToHTML.py [input directory] [output file]
Example:
>>> python multipleToHTML.py C:\\Users\\Cameron\\Desktop output.html
"""

import MySQLdb
import sys
import os

def writeToFile(f, w, c):
    temp = f.readline()
    querys = f.read().split ( ";" )
    querys = querys[:-1]
    for q in querys :
        cur = c.cursor()
        cur.execute(q)
        results = cur.fetchall()
        if len (results) > 0 :
            w.write("\n\n<h3>"+temp+"</h3>\n")
            w.write("\n<table border=1>")
            for row in results:
                    w.write("<tr>")
                    for i in row:
                        w.write("<td>"+str(i)+"</td>")
                    w.write("</tr>")
            w.write("</table>\n\n")
        cur.close()

for n,d,f in os.walk ( sys.argv [ 1 ] ) :
    with open ( sys.argv[ 2 ], "w" ) as w :
        w.write("<head>\n")
        conn = MySQLdb.connect('localhost', 'jordan', 'password', 'wcdb3')
        for file in f:
            if (file.endswith(".txt")) :
                with open(n + "\\" + file, "r") as input:
                    w.write(file)
                    writeToFile(input, w, conn)
        conn.close()
        w.write("\n</head>")


