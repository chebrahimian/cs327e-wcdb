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

    def test_sqlLogin (self) : # assert that valid sql connection is made
        c = [z, jtn395, Jz.~MPm1Cy, cs327e_jtn395]
        a = sqlLogin(c)
        self.assert_str(type(a)) == "<type '_mysql.connection'>"
            
    # ---------
    # sqlQuery
    # ---------

    def test_sqlQuery (self) : # assert that queries provide valid sql results
        c = [z, jtn395, Jz.~MPm1Cy, cs327e_jtn395]
        s = "create table HumanImpact ( crisisID text, type text, number int );"
        a = sqlLogin(c)
        self.assert_str(type(a)) == "<type '_mysql.connection'>" 
        a.query(s)
        r = a.store_result()
        self.assert_str(type(r)) == "<type '_mysql.result'>"

    def test_sqlQuery2 (self) :
        c = [z, jtn395, Jz.~MPm1Cy, cs327e_jtn395]
        s = "create table HumanImpact ( crisisID text, type text, number int );"
        t = "insert into HumanImpact values ( '123', 'deaths', 12);"
        u = "select number from HumanImpact;"
        a = sqlLogin(c)
        self.assert_str(type(a)) == "<type '_mysql.connection'>" 
        a.query(s)
        a.query(t)
        a.query(u)
        r = a.store_result()
        self.assert_str(type(r)) == "<type '_mysql.result'>"

    def test_sqlQuery3 (self) :
        c = [z, jtn395, Jz.~MPm1Cy, cs327e_jtn395]
        s = "create table HumanImpact ( crisisID text, type text, number int );"
        t = "insert into HumanImpact values ( '123', 'deaths', 12);"
        u = "select * from HumanImpact;"
        a = sqlLogin(c)
        self.assert_str(type(a)) == "<type '_mysql.connection'>" 
        a.query(s)
        a.query(t)
        a.query(u)
        r = a.store_result()
        self.assert_str(type(r)) == "<type '_mysql.result'>"

    # ---------
    # parseArgs
    # ---------

    def test_parseArgs (self) : # assert that items are taken from tuple and put into list
        jj = (z, jtn395, Jz.~MPm1Cy, cs327e_jtn395)
        c = parseArgs(jj)
        self.assert_c == [z, jtn395, Jz.~MPm1Cy, cs327e_jtn395]

    # ------------
    # createTables
    # ------------
    
    def test_createTables (self): # check that tables are successfully entered (returns result)
    	c = [z, jtn395, Jz.~MPm1Cy, cs327e_jtn395]
    	a = sqlLogin(c)
        createTables(a)
        r = "show tables"
    	self.assert_str(type(r)) == "<type '_mysql.result'>"
    
    def test_createTables2 (self): # check that query into tables returns result
    	c = [z, jtn395, Jz.~MPm1Cy, cs327e_jtn395]
    	s = "select * from Crises;"
    	a = sqlLogin(c)
        createTables(a)
    	a.query(s)
    	r = a.store_result()
    	self.assert_str(type(r)) == "<type '_mysql.result'>"
    
    def test_createTables3 (self): # check that correct elements are in database table
    	c = [z, jtn395, Jz.~MPm1Cy, cs327e_jtn395]
    	s = "select crisisID from Crises;"
    	a = sqlLogin(c)
        createTables(a)
    	a.query(s)
    	r = a.store_result()
    	self.assert_str(type(r)) == "<type '_mysql.result'>"

    # ---------
    # addTestData
    # ---------

    def test_addTestData (self) : # check that data added is valid sql 
        a = [z, jtn395, Jz.~MPm1Cy, cs327e_jtn395]
        k = sqlLogin(a)
        createTables(k)
        addTestData(k)
        u = "select crisisID from HumanImpact;"
        k.query(u)
        r = k.store_result()
        self.assert_str(type(r)) == "<type '_mysql.result'>"

    def test_addTestData2 (self) : # check that individual rows can be selected and are valid sql
        a = [z, jtn395, Jz.~MPm1Cy, cs327e_jtn395]
        k = sqlLogin(a)
        createTables(k)
        addTestData(k)
        u = "select crisisID from HumanImpact;"
        k.query(u)
        r = k.use_result()
        t = r.fetch_row(maxrows = 1)
        self.assert_str(type(t)) == "<type '_mysql.result'>"

    def test_addTestData3 (self) : # check that data added matches desired
        a = [z, jtn395, Jz.~MPm1Cy, cs327e_jtn395]
        k = sqlLogin(a)
        createTables(k)
        addTestData(k)
        u = "select crisisID from HumanImpact;"
        k.query(u)
        r = k.use_result()
        t = r.fetch_row(maxrows = 1)
        self.assert_t[0] == 'CCD'

    # ---------
    # openTagAtt
    # ---------

    def test_openTagAtt (self) : # test with string inputs
        k = "xyz"
        l = "abc"
        m = "def"
        n = openTagAtt (k, l, m)
        self.assert_n == "<xyz abc='def'>"

    def test_openTagAtt2 (self) : # int inputs
        k = 123
        l = 456
        m = 789
        n = openTagAtt (k, l, m)
        self.assert_n == "<123 456='789'>"

    def test_openTagAtt3 (self) : # whitespace input
        k = ' '
        l = ' '
        m = ' '
        n = openTagAtt (k, l, m)
        self.assert_n == "<   =' '>"

    # ---------
    # closeTagAtt
    # ---------

    def test_openTagAtt (self) : # str
        k = "xyz"
        l = "abc"
        m = "def"
        n = openTagAtt (k, l, m)
        self.assert_n == "<xyz abc='def'/>"

    def test_openTagAtt2 (self) : # int
        k = 123
        l = 456
        m = 789
        n = openTagAtt (k, l, m)
        self.assert_n == "<123 456='789'/>"

    def test_openTagAtt3 (self) : # whitespace
        k = ' '
        l = ' '
        m = ' '
        n = openTagAtt (k, l, m)
        self.assert_n == "<   =' '/>"

    #--------
    # openTag
    #--------
    
    def test_openTag (self):
    	s = "example" #start with string
    	r = openTag(s)
    	self.assert_(r == "<example>")
    
    def test_openTag2 (self):
    	s = 123 #start with int
    	r = openTag(s)
    	self.assert_(r == "<123>")
    	
    def test_openTag3 (self):
    	s = "" # start with empty string
    	r = openTag(s)
    	self.assert_(r == "<>")
    	    	    	       
    #-------------
    # openCloseTag
    #-------------
    
    def test_openCloseTag (self):
    	s = "example" #start with strings
    	v = "value"
    	r = openCloseTag(s, v)
    	self.assert_(r == "<example>value</example>")
    
    def test_openCloseTag2 (self):
    	s = 123 #start with ints
    	v = 321
    	r = openCloseTag(s, v)
    	self.assert_(r == "<123>321</123>")
    	
    def test_openCloseTag3 (self):
    	s = "" # start with empty string and whitespace
    	v = " "
    	r = openCloseTag(s, v)
    	self.assert_(r == "<> </>")

    #--------
    # closeTag
    #--------
    
    def test_openTag (self):
    	s = "example" #start with string
    	r = openTag(s)
    	self.assert_(r == "</example>")
    
    def test_openTag2 (self):
    	s = 123 #start with int
    	r = openTag(s)
    	self.assert_(r == "</123>")
    	
    def test_openTag3 (self):
    	s = "" # start with empty string
    	r = openTag(s)
    	self.assert_(r == "</>")
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

    def test_exportXml3 (self): # three-layer nested elements
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