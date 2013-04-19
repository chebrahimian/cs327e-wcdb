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

credentials = ["jtn395", "Jz.~MPm1Cy", "cs327e_jtn395"]

class TestWCDB2 (unittest.TestCase) :

    # ---------
    # sqlLogin
    # ---------

    def test_sqlLogin (self) : # assert that valid sql connection is made
        c = ["z", "jtn395", "Jz.~MPm1Cy", "cs327e_jtn395"]
        a = sqlLogin(c)
        self.assert_(str(type(a)) == "<type '_mysql.connection'>")
            
    # ---------
    # sqlQuery
    # ---------

    def test_sqlQuery (self) : # assert that queries provide valid sql results
        c = ["z", "jtn395", "Jz.~MPm1Cy", "cs327e_jtn395"]
        s = "create table HumanImpact ( crisisID text, type text, number int );"
        a = sqlLogin(c)
        self.assert_(str(type(a)) == "<type '_mysql.connection'>")
        a.query("drop table if exists HumanImpact;")
        a.query(s)
        r = a.store_result()
        self.assert_(r == None)

    def test_sqlQuery2 (self) :
        c = ["z", "jtn395", "Jz.~MPm1Cy", "cs327e_jtn395"]
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
        c = ["z", "jtn395", "Jz.~MPm1Cy", "cs327e_jtn395"]
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
        jj = ["c:/fileLocation.file", "z", "jtn395", "Jz.~MPm1Cy", "cs327e_jtn395"]
        c = parseArgs(jj)
        self.assert_(c == ["z", "jtn395", "Jz.~MPm1Cy", "cs327e_jtn395"])

    # ------------
    # createTables
    # ------------
    
    def test_createTables (self): # check that tables are successfully entered (returns result)
        c = ["z", "jtn395", "Jz.~MPm1Cy", "cs327e_jtn395"]
        a = sqlLogin(c)
        createTables(a)
        s = "show tables"
        a.query(s)
        r = a.store_result()
        self.assert_(str(type(r)) == "<type '_mysql.result'>")
    
    def test_createTables2 (self): # check that query into tables returns result
        c = ["z", "jtn395", "Jz.~MPm1Cy", "cs327e_jtn395"]
        s = "select * from Crises;"
        a = sqlLogin(c)
        createTables(a)
        a.query(s)
        r = a.store_result()
        self.assert_(str(type(r)) == "<type '_mysql.result'>")
    
    def test_createTables3 (self): # check that correct elements are in database table
        c = ["z", "jtn395", "Jz.~MPm1Cy", "cs327e_jtn395"]
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

    def test_openTagAtt (self) :
        k = "xyz"
        l = "abc"
        m = "def"
        n = openTagAtt (k, l, m)
        self.assert_(n == "<xyz abc='def'>")

    def test_openTagAtt2 (self) :
        k = "123"
        l = "456"
        m = "789"
        n = openTagAtt (k, l, m)
        self.assert_(n == "<123 456='789'>")

    def test_openTagAtt3 (self) : # whitespace
        k = ' '
        l = ' '
        m = ' '
        n = openTagAtt (k, l, m)
        self.assert_(n == "<   =' '>")

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
        s = "example"
        v = "value"
        r = openCloseTag(s, v)
        self.assert_(r == "<example>value</example>")
    
    def test_openCloseTag2 (self):
        s = "123" 
        v = "321"
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
        s = "example" 
        r = openTag(s)
        self.assert_(r == "<example>")
    
    def test_openTag2 (self):
        s = "123" 
        r = openTag(s)
        self.assert_(r == "<123>")
        
    def test_openTag3 (self):
        s = "" # start with empty string
        r = openTag(s)
        self.assert_(r == "<>")

    # ---------
    # importCrises
    # ---------

    def test_importCrises (self) :
        a = ["z", "jtn395", "Jz.~MPm1Cy", "cs327e_jtn395"]
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

    def test_importCrises2 (self) :
        a = ["z", "jtn395", "Jz.~MPm1Cy", "cs327e_jtn395"]
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
        self.assert_(query[0][1]=="Chernobyl Disaster")

    def test_importCrises3 (self) :
        a = ["z", "jtn395", "Jz.~MPm1Cy", "cs327e_jtn395"]
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
        self.assert_(query[0][2]=="Natural")

    #-------------
    # importTypes
    #-------------

    def test_importGeneralKind(self): 
        c = ["z", "jtn395", "Jz.~MPm1Cy", "cs327e_jtn395"]
        a = sqlLogin(c)
        createTables ( a )
        query = sqlQuery (a, "select * from OrganizationKind")
        self.assert_(query == ())
    
    def test_importOrgKind(self):
        c = ["z", "jtn395", "Jz.~MPm1Cy", "cs327e_jtn395"]
        a = sqlLogin(c)
        createTables ( a )
        xml = "<OrganizationKind organizationKindIdent='OWHO'> \
        <Name>World Health Organization</Name> \
        <Description>A group dedicated to solving health problems</Description> \
    </OrganizationKind>"
        xml = ET.fromstring(xml)
        importOrgKind ( a, xml)
        query = sqlQuery (a, "select * from OrganizationKind")
        self.assert_(query[0][0]=="OWHO")
        
    def test_importCrisisKind(self):
        c = ["z", "jtn395", "Jz.~MPm1Cy", "cs327e_jtn395"]
        a = sqlLogin(c)
        createTables ( a )
        xml = "<CrisisKind crisisKindIdent='Natural'> \
        <Name>Natural</Name> \
        <Description>Naturally caused Disaster</Description> \
    </CrisisKind>"
        xml = ET.fromstring(xml)
        importCrisisKind ( a, xml)
        query = sqlQuery (a, "select * from CrisisKind;")
        self.assert_(query[0][0]=="Natural") 
               
    def test_importPersonKind(self):
        c = ["z", "jtn395", "Jz.~MPm1Cy", "cs327e_jtn395"]
        a = sqlLogin(c)
        createTables ( a )
        xml = "<PersonKind personKindIdent='PTVI'> \
        <Name>Victim</Name> \
        <Description>A person harmed, injured, or killed as a result of a crime, accident, or other event or action.     </Description> \
    </PersonKind>"
        xml = ET.fromstring(xml)
        importPersonKind ( a, xml)
        query = sqlQuery (a, "select * from PersonKind;")
        self.assert_(query[0][0]=="PTVI")

    #-------------
    # exportCrises
    #-------------
    
    def test_exportCrises(self):
        c = ["z", "jtn395", "Jz.~MPm1Cy", "cs327e_jtn395"]
        a = sqlLogin(c)
        createTables ( a )
        xml = exportCrises ( a )
        self.assert_(xml == "")

    def test_exportCrises1(self): 
        c = ["z", "jtn395", "Jz.~MPm1Cy", "cs327e_jtn395"]
        a = sqlLogin(c)
        createTables ( a )
        sqlQuery ( a ,"insert into Crises values ('CCD', 'Chernobly Disaster', 'Natural', '1986-04-26', '01:23:00', '1986-04-26', '01:23:00', '588M USD');")
        xml = exportCrises ( a )
        self.assert_(xml.count("CCD") != 0)

    def test_exportCrises2(self): 
        c = ["z", "jtn395", "Jz.~MPm1Cy", "cs327e_jtn395"]
        a = sqlLogin(c)
        createTables ( a )
        sqlQuery ( a ,"insert into Crises values ('CCD', 'Chernobly Disaster', 'Natural', '1986-04-26', '01:23:00', '1986-04-26', '01:23:00', '588M USD');")
        sqlQuery ( a ,"insert into Crises values ('CTO', 'Chernobly Disaster', 'Natural', '1986-04-26', '01:23:00', '1986-04-26', '01:23:00', '588M USD');")
        xml = exportCrises ( a )
        self.assert_(xml.count("<Crisis") == 2)

    #-------------
    # exportOrganizations
    #-------------

    def test_exportOrgs(self):
        c = ["z", "jtn395", "Jz.~MPm1Cy", "cs327e_jtn395"]
        a = sqlLogin(c)
        createTables ( a )
        xml = exportOrgs ( a )
        self.assert_(xml == "")

    def test_exportOrgs2(self):
<<<<<<< HEAD
        c = ["z", "jtn395", "Jz.~MPm1Cy", "cs327e_jtn395"]
        a = sqlLogin(c)
        createTables ( a )
        sqlQuery( a, "insert into Organizations values ('ORC', 'Red Crescent', 'OTPU', 'History', 12123380161, 12123380161, 'admin@redcrescentpenang.org.my', 'P.O. Box 303', 'Midland', 'TX', '1236', 'USA' );" )
        xml = exportOrgs ( a )
        self.assert_(xml.count("<Organization") == 1)

    def test_exportOrgs3(self):
        c = ["z", "jtn395", "Jz.~MPm1Cy", "cs327e_jtn395"]
        a = sqlLogin(c)
        createTables ( a )
        sqlQuery( a, "insert into Organizations values ('ORC', 'Red Crescent', 'OTPU', 'History', 12123380161, 12123380161, 'admin@redcrescentpenang.org.my', 'P.O. Box 303', 'Midland', 'TX', '1236', 'USA' );" )
        sqlQuery( a, "insert into Organizations values ('ORD', 'Red Crescent', 'OTPU', 'History', 12123380161, 12123380161, 'admin@redcrescentpenang.org.my', 'P.O. Box 303', 'Midland', 'TX', '1236', 'USA' );" )
        xml = exportOrgs ( a )
        self.assert_(xml.count("<Organization") == 2)
=======
        #c = ["z", "jtn395", "Jz.~MPm1Cy", "cs327e_jtn395"]
        c = ["localhost", "jordan", "password", "wcdb2"]
        a = sqlLogin(c)
        createTables ( a )
        sqlQuery( a, "insert into Organizations values 'ORC', 'Red Crescent', 'OTPU', 'The Red Cross idea was born in 1859, when Henry Dunant, a young Swiss man, came upon the scene of a bloody battle in Solferino, Italy, between the armies of imperial Austria and the Franco-Sardinian alliance. Some 40,000 men lay dead or dying on the battlefield and the wounded were lacking medical attention.', 12123380161, 12123380161, 'admin@redcrescentpenang.org.my', 'P.O. Box 303', '1236' );" )
        xml = exportOrgs ( a )
        self.assert_(xml.count("<Organization>" == 1)

    def test_exportOrgs2(self):
        #c = ["z", "jtn395", "Jz.~MPm1Cy", "cs327e_jtn395"]
        c = ["localhost", "jordan", "password", "wcdb2"]
        a = sqlLogin(c)
        createTables ( a )
        sqlQuery( a, "insert into Organizations values 'ORC', 'Red Crescent', 'OTPU', 'The Red Cross idea was born in 1859, when Henry Dunant, a young Swiss man, came upon the scene of a bloody battle in Solferino, Italy, between the armies of imperial Austria and the Franco-Sardinian alliance. Some 40,000 men lay dead or dying on the battlefield and the wounded were lacking medical attention.', 12123380161, 12123380161, 'admin@redcrescentpenang.org.my', 'P.O. Box 303', '1236' );" )
        sqlQuery( a, "insert into Organizations values 'ORT', 'Red Crescent', 'OTPU', 'The Red Cross idea was born in 1859, when Henry Dunant, a young Swiss man, came upon the scene of a bloody battle in Solferino, Italy, between the armies of imperial Austria and the Franco-Sardinian alliance. Some 40,000 men lay dead or dying on the battlefield and the wounded were lacking medical attention.', 12123380161, 12123380161, 'admin@redcrescentpenang.org.my', 'P.O. Box 303', '1236' );" )
        xml = exportOrgs ( a )
        self.assert_(xml.count("<Organization>" == 2)
>>>>>>> mm

    #-------------
    # exportPeople
    #-------------	

    def test_exportPeople(self):
        c = ["z", "jtn395", "Jz.~MPm1Cy", "cs327e_jtn395"]
        a = sqlLogin(c)
        createTables ( a )
        xml = exportPeople ( a )
        self.assert_(xml == "")

<<<<<<< HEAD

    #-------------
    # exportTypes
    #-------------
    
    def test_exportTypes(self):
        c = ["z", "jtn395", "Jz.~MPm1Cy", "cs327e_jtn395"]
        a = sqlLogin(c)
        createTables ( a )
        xml = exportTypes ( a )        
        self.assert_(xml == "")
        
    def test_exportTypes1(self):
        c = ["z", "jtn395", "Jz.~MPm1Cy", "cs327e_jtn395"]
        a = sqlLogin(c)
        createTables ( a )
        sqlQuery ( a, "insert into CrisisKind values ('Natural', 'Natural', 'Natural Disaster');")
        xml = exportTypes ( a )
        self.assert_(xml != "")
        
    def test_exportTypes2(self):
        c = ["z", "jtn395", "Jz.~MPm1Cy", "cs327e_jtn395"]
        a = sqlLogin(c)
        createTables ( a )
        sqlQuery ( a, "insert into CrisisKind values ('Natural', 'Natural', 'Natural Disaster');")
        sqlQuery ( a, "insert into PersonKind values ('PGO', 'Government Official', ' Stuff');")
        xml = exportTypes ( a )
        self.assert_(xml[-13:-1]=="</PersonKind")
=======
    def test_exportPeople2(self):
        #c = ["z", "jtn395", "Jz.~MPm1Cy", "cs327e_jtn395"]
        c = ["localhost", "jordan", "password", "wcdb2"]
        a = sqlLogin(c)
        createTables ( a )
        sqlQuery( a, "insert into Organizations values 'PKA', 'Kofi', 'Atta', 'Annan', '', 'PTHO' );" )
        sqlQuery( a, "insert into Organizations values 'PKA', 'Kofi', 'Atta', 'Annan', '', 'PTHO' );" )
        xml = exportOrgs ( a )
        self.assert_(xml.count("<Organization>" == 2)

    
>>>>>>> mm

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
        exportXml( w, r )
        self.assert_(w.getvalue() == "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<Root>\n\t<THU/>\n</Root>\n")

    def test_exportXml2 (self): # XML in one line, with new line characters before and after xml
        r = "\n<THU><Team></Team></THU>\n"
        w = StringIO.StringIO()
        exportXml( w, r )
        self.assert_(w.getvalue() == "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<THU>\n\t<Team/>\n</THU>\n")

    def test_exportXml3 (self): # three-layer nested elements
        r = "<THU><Team><Cooly></Cooly></Team></THU>"
        w = StringIO.StringIO()
        exportXml( w, r )
        self.assert_(w.getvalue() == "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<THU>\n\t<Team>\n\t\t<Cooly/>\n\t</Team>\n</THU>\n")

    # -----
    # start
    # -----

    def test_start (self): # Empty root element
        r = StringIO.StringIO('<WorldCrises><Crisis crisisIdent="CTMIA">\
		<Name>Three Mile Island Accident</Name>\
		<Kind crisisKindIdent="NonNatural"/>\
		<Location>\
			<Locality>Harrisburg</Locality>\
			<Region>Pennsylvania</Region>\
			<Country>United States</Country>\
		</Location>\
		<StartDateTime>\
			<Date>1979-03-28</Date>\
			<Time>04:00:00</Time>\
		</StartDateTime>\
		<HumanImpact>\
			<Type>Casualties</Type>\
			<Number>0</Number>\
		</HumanImpact>\
		<EconomicImpact>1B USD</EconomicImpact>\
		<ResourceNeeded>Labor</ResourceNeeded>\
		<ResourceNeeded>Transportation</ResourceNeeded>\
		<ResourceNeeded>Money</ResourceNeeded>\
		<ResourceNeeded>Shelter</ResourceNeeded>\
		<WaysToHelp>Room and board for refugees</WaysToHelp>\
		<WaysToHelp>Cleanup</WaysToHelp>\
		<ExternalResources>\
			<ExternalLinkURL>http://www.pbs.org/wgbh/amex/three/peopleevents/pandeAMEX86.html</ExternalLinkURL>\
		</ExternalResources>\
		<RelatedPersons>\
			<RelatedPerson personIdent="PJC"/>\
		</RelatedPersons>\
		<RelatedOrganizations>\
			<RelatedOrganization organizationIdent="OIAEA"/>\
		</RelatedOrganizations>\
	</Crisis></WorldCrises>')
        w = StringIO.StringIO()
        a = ["c:/filelocation.file", "z", "jtn395", "Jz.~MPm1Cy", "cs327e_jtn395"]
        start(r, w, a)
        self.assert_(w.getvalue() != '<?xml version="1.0" encoding="UTF-8"?>\n<WorldCrises>\n\t<Crisis crisisIdent="CTMIA">\n\t\t<Name>Three Mile Island Accident</Name>\n\t\t<Kind crisisKindIdent="NonNatural"/>\n\t\t<Location>\n\t\t\t<Locality>Harrisburg</Locality>\n\t\t\t<Region>Pennsylvania</Region>\n\t\t\t<Country>United States</Country>\n\t\t</Location>\n\t\t<StartDateTime>\n\t\t\t<Date>1979-03-28</Date>\n\t\t\t<Time>04:00:00</Time>\n\t\t</StartDateTime>\n\t\t<EndDateTime>\n\t\t\t<Date>1979-03-28</Date>\n\t\t\t<Time>23:59:59</Time>\n\t\t</EndDateTime>\n\t\t<HumanImpact>\n\t\t\t<Type>Casualties</Type>\n\t\t\t<Number>0</Number>\n\t\t</HumanImpact>\n\t\t<EconomicImpact>1B USD</EconomicImpact>\n\t\t<ResourceNeeded>Labor</ResourceNeeded>\n\t\t<ResourceNeeded>Transportation</ResourceNeeded>\n\t\t<ResourceNeeded>Money</ResourceNeeded>\n\t\t<ResourceNeeded>Shelter</ResourceNeeded>\n\t\t<WaysToHelp>Room and board for refugees</WaysToHelp>\n\t\t<WaysToHelp>Cleanup</WaysToHelp>\n\t\t<ExternalResources>\n\t\t\t<ExternalLinkURL>http://www.pbs.org/wgbh/amex/three/peopleevents/pandeAMEX86.html</ExternalLinkURL>\n\t\t</ExternalResources>\n\t\t<RelatedPersons>\n\t\t\t<RelatedPerson personIdent="PJC"/>\n\t\t</RelatedPersons>\n\t\t<RelatedOrganizations>\n\t\t\t<RelatedOrganization organizationIdent="OIAEA"/>\n\t\t</RelatedOrganizations>\n\t</Crisis>\n</WorldCrises>\n')

    def test_start2 (self): # Multiple elements in one line
        r = StringIO.StringIO('<WorldCrises><Organization organizationIdent="OAC">\
		<Name>Americorps</Name>\
		<Kind organizationKindIdent="OTGO"/>\
		<Location>\
			<Locality>New York City</Locality>\
			<Region>New York</Region>\
			<Country>United States</Country>\
		</Location>\
		<History>The reasoning behind AmeriCorps comes from a long historical tradition of community service through civic associations.</History>\
		<ContactInfo>\
			<Telephone>2026065000</Telephone>\
			<Fax>2026065000</Fax>\
			<Email>americorpsnational@cns.gov</Email>\
			<PostalAddress>\
				<StreetAddress>1201 New York Avenue</StreetAddress>\
				<Locality>New York City</Locality>\
				<Region>New York</Region>\
				<PostalCode>20525</PostalCode>\
				<Country>United States</Country>\
			</PostalAddress>\
		</ContactInfo>\
		<ExternalResources>\
			<Citation>nationalservice.gov</Citation>\
			<ExternalLinkURL>http://www.nationalservice.gov/about/newsroom/releases_detail.asp?tbl_pr_id=2099</ExternalLinkURL>\
		</ExternalResources>\
		<RelatedCrises>\
			<RelatedCrisis crisisIdent="CJTO"/>\
		</RelatedCrises>\
	</Organization></WorldCrises>')
        w = StringIO.StringIO()
        a = ["c:/filelocation.file", "z", "jtn395", "Jz.~MPm1Cy", "cs327e_jtn395"]
        start(r, w, a)
        self.assert_(w.getvalue() != '<?xml version="1.0" encoding="UTF-8"?>\n<WorldCrises>\n\t<Organization organizationIdent="OAC">\n\t\t<Name>Americorps</Name>\n\t\t<Kind organizationKindIdent="OTGO"/>\n\t\t<Location>\n\t\t\t<Locality>New York City</Locality>\n\t\t\t<Region>New York</Region>\n\t\t\t<Country>United States</Country>\n\t\t</Location>\n\t\t<History>The reasoning behind AmeriCorps comes from a long historical tradition of community service through civic associations.</History>\n\t\t<ContactInfo>\n\t\t\t<Telephone>2026065000</Telephone>\n\t\t\t<Fax>2026065000</Fax>\n\t\t\t<Email>americorpsnational@cns.gov</Email>\n\t\t\t<PostalAddress>\n\t\t\t\t<StreetAddress>1201 New York Avenue</StreetAddress>\n\t\t\t\t<Locality>New York City</Locality>\n\t\t\t\t<Region>New York</Region>\n\t\t\t\t<PostalCode>20525</PostalCode>\n\t\t\t\t<Country>United States</Country>\n\t\t\t</PostalAddress>\n\t\t</ContactInfo>\n\t\t<ExternalResources>\n\t\t\t<Citation>nationalservice.gov</Citation>\n\t\t\t<ExternalLinkURL>http://www.nationalservice.gov/about/newsroom/releases_detail.asp?tbl_pr_id=2099</ExternalLinkURL>\n\t\t</ExternalResources>\n\t\t<RelatedCrises/>\n\t\t<RelatedPersons/>\n\t</Organization>\n</WorldCrises>\n')

    def test_start3 (self): # Pretty xml, with one empty element written <E1/> and one empty element as <E2></E2>
        r = StringIO.StringIO('<WorldCrises><Person personIdent="PKA">\
		<Name>\
			<FirstName>Kofi</FirstName>\
			<MiddleName>Atta</MiddleName>\
			<LastName>Annan</LastName>\
		</Name>\
		<Kind personKindIdent="PTHO"/>\
		<Location>\
			<Locality>Kumasi</Locality>\
			<Region>Ashanti</Region>\
			<Country>Ghana</Country>\
		</Location>\
		<ExternalResources>\
			<Citation>UN.org</Citation>\
			<ExternalLinkURL>http://www.un.org/sg/formersg/annan.shtml</ExternalLinkURL>\
		</ExternalResources>\
		<RelatedCrises>\
			<RelatedCrisis crisisIdent="CSE"/>\
		</RelatedCrises>\
		<RelatedOrganizations>\
			<RelatedOrganization organizationIdent="OUN"/>\
		</RelatedOrganizations>\
	</Person></WorldCrises>')
        w = StringIO.StringIO()
        a = ["c:/filelocation.file", "z", "jtn395", "Jz.~MPm1Cy", "cs327e_jtn395"]
        start(r, w, a)
        self.assert_(w.getvalue() != '<?xml version="1.0" encoding="UTF-8"?>\n<WorldCrises>\n\t<Person personIdent="PKA">\n\t\t<Name>\n\t\t\t<FirstName>Kofi</FirstName>\n\t\t\t<MiddleName>Atta</MiddleName>\n\t\t\t<LastName>Annan</LastName>\n\t\t\t<Suffix/>\n\t\t</Name>\n\t\t<Kind personKindIdent="PTHO"/>\n\t\t<Location>\n\t\t\t<Locality>Kumasi</Locality>\n\t\t\t<Region>Ashanti</Region>\n\t\t\t<Country>Ghana</Country>\n\t\t</Location>\n\t\t<ExternalResources>\n\t\t\t<Citation>UN.org</Citation>\n\t\t\t<ExternalLinkURL>http://www.un.org/sg/formersg/annan.shtml</ExternalLinkURL>\n\t\t</ExternalResources>\n\t\t<RelatedCrises/>\n\t\t<RelatedOrganizations>\n\t\t\t<RelatedOrganization organizationIdent="OUN"/>\n\t\t</RelatedOrganizations>\n\t</Person>\n</WorldCrises>\n')
      
print "TestXML.py"
unittest.main()
print "Done."