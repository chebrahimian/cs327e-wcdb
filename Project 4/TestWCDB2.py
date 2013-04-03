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

from WCDB2 import *
import xml.dom.minidom as MD
import xml.etree.ElementTree as ET
# -----------
# TestWCDB2
# -----------

class TestWCDB2 (unittest.TestCase) :

    # ---------
    # sqlLogin
    # ---------

    def test_sqlLogin (self) :
        c = [z, jtn395, Jz.~MPm1Cy, cs327e_jtn395]
        a = sqlLogin(c)
        self.assert_str(type(c)) == "<type '_mysql.connection'>" 
            
    # ---------
    # sqlClose
    # ---------
    
    def test_sqlClose (self) :
        c = [z, jtn395, Jz.~MPm1Cy]
        a = sqlClose(c)
        self.assert_str(type(c)) == "<type '_mysql.connection'>" 
            
    # ---------
    # sqlQuery
    # ---------

    def test_sqlQuery (self) :
        c = [z, jtn395, Jz.~MPm1Cy, cs327e_jtn395]
        s = "create table HumanImpact ( crisisID text, type text, number int );"
        a = sqlLogin(c)
        self.assert_str(type(c)) == "<type '_mysql.connection'>" 
        c.query(s)
        r = c.use_result()
        self.assert_str(type(r)) == "<type '_mysql.result'>"
             
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
        r = StringIO.StringIO("<Root><THU>\n\n<Team>\n</Team>\n</THU>\n<Team></Team>\n</Root>")
        a = importXml(r)
        self.assert_(len(a) == 2)

    def test_importXml4 (self) : #xml in multiple lines with tabs (pretty xml)
        r = StringIO.StringIO("<Root><THU>\n\n\t<Team>\n\t</Team>\n</THU>\n<Team></Team>\n</Root>")
        a = importXml(r)
        self.assert_(len(a) == 2)

    # ---------
    # exportXml
    # ---------

    def test_exportXml (self): # XML all in one line, 1 empty element
        r = "<Root><THU></THU></Root>"
        w = StringIO.StringIO()
        xml = ET.fromstring ( r )
        exportXml( w, xml )
        t = w.getvalue()
        self.assert_(w.getvalue() == "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<Root>\n\t<THU/>\n</Root>\n")

    def test_exportXml2 (self): # XML in one line, with new line characters before and after xml
        r = "\n<THU><Team></Team></THU>\n"
        w = StringIO.StringIO()
        xml = ET.fromstring ( r )
        exportXml( w, xml )
        self.assert_(w.getvalue() == "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<THU>\n\t<Team/>\n</THU>\n")

    def test_exportXml3 (self): # 
        r = "<THU><Team><Cooly></Cooly></Team></THU>"
        w = StringIO.StringIO()
        xml = ET.fromstring ( r )
        exportXml( w, xml )
        self.assert_(w.getvalue() == "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<THU>\n\t<Team>\n\t\t<Cooly/>\n\t</Team>\n</THU>\n")

    # -----
    # start
    # -----

    def test_start (self): # Empty root element
        r = StringIO.StringIO("<Root/>")
        w = StringIO.StringIO()
        start(r , w)
        self.assert_(w.getvalue() == "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<Root/>\n")

    def test_start2 (self): # Multiple elements in one line
        r = StringIO.StringIO("<Root><E1><E2></E2></E1></Root>")
        w = StringIO.StringIO()
        start(r , w)
        self.assert_(w.getvalue() == "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<Root>\n\t<E1>\n\t\t<E2/>\n\t</E1>\n</Root>\n")

    def test_start3 (self): # Pretty xml, with one empty element written <E1/> and one empty element as <E2></E2>
        r = StringIO.StringIO("<Root>\n\t<E1/>\n\t<E2></E2>\n</Root>")
        w = StringIO.StringIO()
        start(r , w)
        self.assert_(w.getvalue() == "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<Root>\n\t<E1/>\n\t<E2/>\n</Root>\n")
      
print "TestXML.py"
unittest.main()
print "Done."