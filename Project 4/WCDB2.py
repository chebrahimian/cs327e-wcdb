import xml.etree.ElementTree as ET
import xml.dom.minidom as MD
import re
import _mysql

def sqlLogin ( loginInfo ) :
    c = _mysql.connect(
        host = loginInfo [ 0 ],
        user = loginInfo [ 1 ],
        passwd = loginInfo [ 2 ],
        db = loginInfo [ 3 ] )
    assert str(type(c)) == "<type '_mysql.connection'>"
    return c

def sqlClose () :
    c = _mysql.connect(
        host = loginInfo [ 0 ],
        user = loginInfo [ 1 ],
        passwd = loginInfo [ 2 ] )
    assert str(type(c)) == "<type '_mysql.connection'>"
    return c

def sqlQuery (c, s) :
    assert str(type(c)) == "<type '_mysql.connection'>"
    assert type(s)      is str
    c.query(s)
    r = c.use_result()
    if r is None :
        return None
    assert str(type(r)) == "<type '_mysql.result'>"
    t = r.fetch_row(maxrows = 0)
    assert type(t) is tuple
    return t

def parseArgs ( args ) :
    loginInfo = []
    for s in args :
        loginInfo.append ( s )
    for i in range ( 0 , 3 ) :
        loginInfo.pop ( 0 )
    return loginInfo

def importXml ( r ):
    """
    reads in xml from stdin (a file) and parses it into an ElementTree
    r is the reader
    returns an ElementTree
    """
    rawText = r.read ()
    rawText = rawText.strip ()
    pattern = re.compile (r'[^\S ]+')
    text = re.sub ( pattern, '', rawText )
    xml = ET.fromstring ( text )
    return xml

def exportXml ( w, xml ):
    """
    converts an ElementTree to a string, then outputs a formatted xml document to stdout ( a file )
    w is the writer
    xml is an ElementTree
    """
    rawText = ET.tostring ( xml )
    pattern = re.compile (r'[^\S ]+')
    text = re.sub ( pattern, '', rawText )
    reparsed = MD.parseString ( text )
    w.write ( reparsed.toprettyxml ( indent = "\t", encoding = "UTF-8" ) )

def testQueries ( c ) :
    print sqlQuery ( c, "use wcdb2;" )
    print sqlQuery ( c, "drop table if exists Crises;" )
    print sqlQuery ( c, "drop table if exists Organizations;" )
    print sqlQuery ( c, "drop table if exists People;" )
    print sqlQuery ( c, "drop table if exists CrisisLocations;" )
    print sqlQuery ( c, "drop table if exists PeopleLocations;" )
    print sqlQuery ( c, "drop table if exists HumanImpact;" )
    print sqlQuery ( c, "drop table if exists ResourcesNeeded;" )
    print sqlQuery ( c, "drop table if exists WaysToHelp;" )
    print sqlQuery ( c, "drop table if exists ExternalResources;" )
    print sqlQuery ( c, "drop table if exists ExternalResourceTypes;" )
    print sqlQuery ( c, "drop table if exists PeopleToOrganizations;" )
    print sqlQuery ( c, "drop table if exists OrganizationsToCrises;" )
    print sqlQuery ( c, "drop table if exists CrisesToPeople;" )
    print sqlQuery ( c, "drop table if exists OrganizationTypes;" )
    print sqlQuery ( c, "drop table if exists PersonTypes;" )
    print sqlQuery ( c, "drop table if exists CrisisTypes;" )
    
    print sqlQuery ( c, "create table Crises ( crisisID text, name text, kind text, startDate date, startTime time, economicImpact text);" )
    print sqlQuery ( c, "create table Organizations ( orgID text, name text, kind text, phone int, fax int, email text, address text, locality text, region text, postalCode text, country text);" )
    print sqlQuery ( c, "create table People ( personID text, firstName text, middleName text, lastName text, suffix text, personKindID text);" )
    print sqlQuery ( c, "create table CrisisLocations ( crisisID text, locality text, region text, country text);" )
    print sqlQuery ( c, "create table PeopleLocations ( personID text, locality text, region text, country text);" )
    print sqlQuery ( c, "create table HumanImpact ( crisisID text, type text, number int);" )
    print sqlQuery ( c, "create table ResourcesNeeded ( sID int, sName text, GPA float, sizeHS int);" )
    print sqlQuery ( c, "create table WaysToHelp ( sID int, sName text, GPA float, sizeHS int);" )
    print sqlQuery ( c, "create table ExternalResources ( sID int, sName text, GPA float, sizeHS int);" )
    print sqlQuery ( c, "create table ExternalResourceTypes ( sID int, sName text, GPA float, sizeHS int);" )
    print sqlQuery ( c, "create table PeopleToOrganizations ( sID int, sName text, GPA float, sizeHS int);" )
    print sqlQuery ( c, "create table OrganizationsToCrises ( sID int, sName text, GPA float, sizeHS int);" )
    print sqlQuery ( c, "create table CrisesToPeople ( sID int, sName text, GPA float, sizeHS int);" )
    print sqlQuery ( c, "create table OrganizationTypes ( sID int, sName text, GPA float, sizeHS int);" )
    print sqlQuery ( c, "create table PersonTypes ( sID int, sName text, GPA float, sizeHS int);" )
    print sqlQuery ( c, "create table CrisisTypes ( sID int, sName text, GPA float, sizeHS int);" )
    print sqlQuery ( c, "show tables;" )
    
def start ( r, w, args ):
    """
    imports an xml document into an ElementTree, then outputs the ElementTree back to a file
    r is the reader
    w is the writer
    """
    sqlLoginInfo = parseArgs ( args )
    sql = sqlLogin ( sqlLoginInfo )
    xml = importXml ( r )
    testQueries( sql )
    sql.close()
    exportXml ( w, xml )