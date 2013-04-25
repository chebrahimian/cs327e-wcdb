def main():

	"""
	Reads in a directory path, directory name, and output name
	execute as 
	>>> python multipleToHTML.py pathname filename output name
	Example:
	>>> python multipleToHTML.py C:\\Users\\Cameron\\Desktop querySol output.html
	"""

	import sys
	import os
	mypath = os.path.join(sys.argv[1], sys.argv[2])

	tohtml = os.path.join(sys.argv[1], sys.argv[3])

	w = open(tohtml, "a")

	w.write("<head>\n")

	for file in os.listdir(mypath):
		if file.endswith(".txt"):
			with open(os.path.join(mypath,file), "r") as input:
				w.write(file)
				writeToFile(input, w)
				input.close()

	w.write("\n</head>")
	w.close()



def writeToFile(query, w):

	import MySQLdb

	temp = query.readline()

	query = query.read()

	conn = MySQLdb.connect('localhost', 'root', 'database', 'test')
	c = conn.cursor()

	c.execute(query)

	results = c.fetchall()

	c.close()

	w.write("\n\n<h3>"+temp+"</h3>\n")
	w.write("\n<table border=1>")
	for row in results:
			w.write("<tr>")
			for i in row:
				w.write("<td>"+str(i)+"</td>")
			w.write("</tr>")

	w.write("</table>\n\n")


main()