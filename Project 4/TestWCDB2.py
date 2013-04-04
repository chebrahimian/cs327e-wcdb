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
        #c = ["z", "jtn395", "Jz.~MPm1Cy", "cs327e_jtn395"]
        c = ["localhost", "jordan", "password", "wcdb2"]
        a = sqlLogin(c)
        self.assert_(str(type(a)) == "<type '_mysql.connection'>")
            
    # ---------
    # sqlQuery
    # ---------

    def test_sqlQuery (self) : # assert that queries provide valid sql results
        #c = ["z", "jtn395", "Jz.~MPm1Cy", "cs327e_jtn395"]
        c = ["localhost", "jordan", "password", "wcdb2"]
        s = "create table HumanImpact ( crisisID text, type text, number int );"
        a = sqlLogin(c)
        self.assert_(str(type(a)) == "<type '_mysql.connection'>")
        a.query("drop table if exists HumanImpact;")
        a.query(s)
        r = a.store_result()
        self.assert_(str(type(r)) == "<type '_mysql.result'>")

    def test_sqlQuery2 (self) :
        #c = ["z", "jtn395", "Jz.~MPm1Cy", "cs327e_jtn395"]
        c = ["localhost", "jordan", "password", "wcdb2"]
        a = sqlLogin(c)
        s = "create table HumanImpact ( crisisID text, type text, number int );"
        t = "insert into HumanImpact values ( '123', 'deaths', 12);"
        u = "select number from HumanImpact;"
        self.assert_(str(type(a)) == "<type '_mysql.connection'>")
        a.query("drop table if exists HumanImpact;")
        a.query(s)
        a.query(t)
        a.query(u)
        r = a.store_result()
        self.assert_(str(type(r)) == "<type '_mysql.result'>")

    def test_sqlQuery3 (self) :
        #c = ["z", "jtn395", "Jz.~MPm1Cy", "cs327e_jtn395"]
        c = ["localhost", "jordan", "password", "wcdb2"]
        s = "create table HumanImpact ( crisisID text, type text, number int );"
        t = "insert into HumanImpact values ( '123', 'deaths', 12);"
        u = "select * from HumanImpact;"
        a = sqlLogin(c)
        self.assert_(str(type(a)) == "<type '_mysql.connection'>")
        a.query("drop table if exists HumanImpact;")
        a.query(s)
        a.query(t)
        a.query(u)
        r = a.store_result()
        self.assert_(str(type(r)) == "<type '_mysql.result'>")

    # ---------
    # parseArgs
    # ---------

    def test_parseArgs (self) : # assert that items are taken from tuple and put into list
        #jj = ["z", "jtn395", "Jz.~MPm1Cy", "cs327e_jtn395"]
        jj = ["localhost", "jordan", "password", "wcdb2"]
        c = parseArgs(jj)
        self.assert_(c == ["z", "jtn395", "Jz.~MPm1Cy", "cs327e_jtn395"])

    # ------------
    # createTables
    # ------------
    
    def test_createTables (self): # check that tables are successfully entered (returns result)
        #c = ["z", "jtn395", "Jz.~MPm1Cy", "cs327e_jtn395"]
        c = ["localhost", "jordan", "password", "wcdb2"]
        a = sqlLogin(c)
        createTables(a)
        s = "show tables"
        a.query(s)
        r = a.store_result()
        self.assert_(str(type(r)) == "<type '_mysql.result'>")
    
    def test_createTables2 (self): # check that query into tables returns result
        #c = ["z", "jtn395", "Jz.~MPm1Cy", "cs327e_jtn395"]
        c = ["localhost", "jordan", "password", "wcdb2"]
        s = "select * from Crises;"
        a = sqlLogin(c)
        createTables(a)
        a.query(s)
        r = a.store_result()
        self.assert_(str(type(r)) == "<type '_mysql.result'>")
    
    def test_createTables3 (self): # check that correct elements are in database table
        #c = ["z", "jtn395", "Jz.~MPm1Cy", "cs327e_jtn395"]
        c = ["localhost", "jordan", "password", "wcdb2"]
        s = "select crisisID from Crises;"
        a = sqlLogin(c)
        createTables(a)
        a.query(s)
        r = a.store_result()
        self.assert_(str(type(r)) == "<type '_mysql.result'>")

    # ---------
    # openTagAtt
    # ---------

    def test_openTagAtt (self) : # test with string inputs
        k = "xyz"
        l = "abc"
        m = "def"
        n = openTagAtt (k, l, m)
        self.assert_(n == "<xyz abc='def'>")

    def test_openTagAtt2 (self) : # int inputs
        k = 123
        l = 456
        m = 789
        n = openTagAtt (k, l, m)
        self.assert_(n == "<123 456='789'>")

    def test_openTagAtt3 (self) : # whitespace input
        k = ' '
        l = ' '
        m = ' '
        n = openTagAtt (k, l, m)
        self.assert_(n == "<   =' '>")

    # ---------
    # closeTagAtt
    # ---------

    def test_openTagAtt (self) : # str
        k = "xyz"
        l = "abc"
        m = "def"
        n = openTagAtt (k, l, m)
        self.assert_(n == "<xyz abc='def'/>")

    def test_openTagAtt2 (self) : # int
        k = 123
        l = 456
        m = 789
        n = openTagAtt (k, l, m)
        self.assert_(n == "<123 456='789'/>")

    def test_openTagAtt3 (self) : # whitespace
        k = ' '
        l = ' '
        m = ' '
        n = openTagAtt (k, l, m)
        self.assert_(n == "<   =' '/>")

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
    # exportCrises
    # ---------

    def test_exportCrises (self) :
        #a = ["z", "jtn395", "Jz.~MPm1Cy", "cs327e_jtn395"]
        a = ["localhost", "jordan", "password", "wcdb2"]
        c = sqlLogin(a)
        createTables(c)
        crisisInstance = "\
        <Crisis crisisIdent='CCD'>\
            <Name>Chernobyl Disaster</Name>\
            <Kind crisisKindIdent='Natural'/>\
            <Location>\
                <Locality>Pripyat</Locality>\
                <Region>Kiev</Region>\
                <Country>Ukraine</Country>\
            </Location>\
            <StartDateTime>\
                <Date>1986-04-26</Date>\
                <Time>01:23:00</Time>\
            </StartDateTime>\
            <HumanImpact>\
                <Type>Casualties</Type>\
                <Number>31</Number>\
            </HumanImpact>\
            <HumanImpact>\
                <Type>Affected</Type>\
                <Number>500000</Number>\
            </HumanImpact>\
            <EconomicImpact>588M USD</EconomicImpact>\
            <ResourceNeeded>Labor</ResourceNeeded>\
            <ResourceNeeded>Transportation</ResourceNeeded>\
            <ResourceNeeded>Money</ResourceNeeded>\
            <ResourceNeeded>Shelter</ResourceNeeded>\
            <WaysToHelp>Providing room and board for refugees</WaysToHelp>\
            <WaysToHelp>Medical care for those affected</WaysToHelp>\
            <ExternalResources>\
                <ImageURL>http://i.telegraph.co.uk/multimedia/archive/01755/chernobyl_1755717c.jpg</ImageURL>\
                <ExternalLinkURL>http://articles.latimes.com/1986-05-04/news/mn-3685_1_soviet-union</ExternalLinkURL>\
                <ExternalLinkURL>http://www.iaea.org/newscenter/focus/chernobyl/</ExternalLinkURL>\
            </ExternalResources>\
            <RelatedPersons>\
                <RelatedPerson personIdent='PRR'/>\
            </RelatedPersons>\
            <RelatedOrganizations>\
                <RelatedOrganization organizationIdent='OIAEA'/>\
                <RelatedOrganization organizationIdent='OUN'/>\
            </RelatedOrganizations>\
        </Crisis>"
        crisisInstance = ET.fromstring(crisisInstance)

        importCrisis (c, crisisInstance)

        query = sqlQuery (c ,"select * from Crises;")

        self.assert_(query[0][0]=="CCD")


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
        a = ["localhost", "jordan", "password", "wcdb2"]
        start(r, w, a)
        self.assert_(w.getvalue() == "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<Root/>\n")

    def test_start2 (self): # Multiple elements in one line
        r = StringIO.StringIO("<Root><E1><E2></E2></E1></Root>")
        w = StringIO.StringIO()
        a = ["localhost", "jordan", "password", "wcdb2"]
        start(r, w, a)
        self.assert_(w.getvalue() == "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<Root>\n\t<E1>\n\t\t<E2/>\n\t</E1>\n</Root>\n")

    def test_start3 (self): # Pretty xml, with one empty element written <E1/> and one empty element as <E2></E2>
        r = StringIO.StringIO("<Root>\n\t<E1/>\n\t<E2></E2>\n</Root>")
        w = StringIO.StringIO()
        a = ["localhost", "jordan", "password", "wcdb2"]
        start(r, w, a)
        self.assert_(w.getvalue() == "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<Root>\n\t<E1/>\n\t<E2/>\n</Root>\n")
      
print "TestXML.py"
unittest.main()
print "Done."