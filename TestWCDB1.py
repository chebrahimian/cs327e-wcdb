
"""
To test the program:
    % python TestXML.py >& TestXML.out
    % chmod ugo+x TestXMLpy
    % TestXML.py >& TestXML.out
"""

# -------
# imports
# -------

import StringIO
import unittest

from WCDB1 import *
import xml.dom.minidom as MD
import xml.etree.ElementTree as ET
# -----------
# TestWCDB1
# -----------

class TestWCDB1 (unittest.TestCase) :
	"""
	# ---------
	# importXml
	# ---------
	
	def test_importXml (self) : #xml all in one line
		r = StringIO.StringIO("<THU><Team></Team><Team></Team></THU>")
		a = importXml(r)
		self.assert_(len(a) == 2) #2 because 1st element defines type, 2nd element defines the xml element

	def test_importXml2 (self) : #xml all in one line, starts with tab
		r = StringIO.StringIO("\t<Root><THU><Team></Team></THU><Team></Team></Root>")
		a = importXml(r)
		self.assert_(len(a) == 2)


	def test_importXml3 (self) : #xml in multiple lines w/o tabs
		r = StringIO.StringIO("<Root><THU>\n\n\t<Team>\n\t</Team>\n</THU>\n<Team></Team>\n</Root>")
		a = importXml(r)
		self.assert_(len(a) == 2)

	def test_importXml4 (self) : #xml in multiple lines with tabs (pretty xml)
		r = StringIO.StringIO("<Root><THU>\n\n\t<Team>\n\t</Team>\n</THU>\n<Team></Team>\n</Root>")
		a = importXml(r)
		self.assert_(len(a) == 2)
	"""
	# ---------
	# exportXml
	# ---------
	def test_exportXml (self):
		r = "<Root><THU></THU></Root>"
		w = StringIO.StringIO()
		xml = ET.fromstring ( r )
		exportXml( w, xml )
		t = w.readline #first line defines element type
		t = w.read()
		self.assert_(t == "<Root>\n\t<THU/>\n</Root>")
"""
	def test_exportXml1 (self):
		r = StringIO.StringIO("<THU><Team></Team></THU>\n<Team></Team>\n")
		w = StringIO.StringIO()
		a = exportXml( w, r )
		self.assert_(a == "<THU>\n\t<Team>\n</Team>\n</THU>\n<Team>\n</Team>")

	def test_exportXml2 (self):
		r = StringIO.StringIO("<THU><Team></Team></THU>\n<Team></Team>\n")
		w = StringIO.StringIO()
		a = exportXml( w, r )
		self.assert_(a == "<THU>\n\t<Team>\n</Team>\n</THU>\n<Team>\n</Team>")

    # -----
    # start
    # -----

	def test_start (self):
		r = StringIO.StringIO("<Root/>")
		w = StringIO.StringIO()
		start(r , w)
		t = w.readline() #first line describes version
		t = w.read()
		self.assert_(t == "<Root/>")

    def test_start2 (self):
        r = StringIO.StringIO("<THU></THU><THU></THU>")
        a = []
        b = xml_read(r, a)
        queryList = b.getElementsByTagName(a[0])
        self.assert_(find_index(b.documentElement, [queryList[0], 0, 0]) == 1)

    def test_start3 (self):
        r = StringIO.StringIO("<THU>\n<Team>\n<ACRush></ACRush>\n<Jelly></Jelly>"+\
                              "<Cooly></Cooly>\n</Team>\n<JiaJia>\n<Team>\n"+\
                              "<Ahyangyi></Ahyangyi>\n<Dragon></Dragon>\n"+\
                              "<Cooly><Amber></Amber></Cooly>\n</Team>\n"+\
                              "</JiaJia>\n</THU>\n<Team><Cooly><Amber></Amber>"+\
                              "<ACRush></ACRush></Cooly></Team>")
        a = []
        b = xml_read(r, a)
        queryList = b.getElementsByTagName(a[0])
        self.assert_(find_index(b.documentElement, [queryList[0], 0, 0]) == 2)
"""

      
print "TestXML.py"
unittest.main()
print "Done."