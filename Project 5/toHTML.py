
def main():
	import sys

	#write this command to run:
	#python practice.py < [file].txt > [file].html
	#the txt file is known, you are creating the html file
	writeToFile (sys.stdin, sys.stdout)
	
def writeToFile(query, w):

	import MySQLdb

	temp = query.readline()

	query = query.read()

	conn = MySQLdb.connect('localhost', 'root', 'database', 'test')
	c = conn.cursor()

	c.execute(query)

	results = c.fetchall()

	w.write("<head>\n")
	w.write("<h3>"+temp+"</h3>\n\n")
	w.write("\n<table border=1>")
	for row in results:
			w.write("<tr>")
			for i in row:
				w.write("<td>"+str(i)+"</td>")
			w.write("</tr>")

	w.write("</table>\n</head>")
	
main()
