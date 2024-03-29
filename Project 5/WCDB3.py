import xml.etree.ElementTree as ET
import xml.dom.minidom as MD
import re
import _mysql

def sqlLogin ( loginInfo ) :
    """
    logs in to a sql database using the given login info
    loginInfo is a list of [ hostname, username, password, database ]
    returns the mysql connection
    """
    #assert len ( loginInfo ) == 4
    c = _mysql.connect(
        host = loginInfo [ 0 ],
        user = loginInfo [ 1 ],
        passwd = loginInfo [ 2 ],
        db = loginInfo [ 3 ] )
    #assert str(type(c)) == "<type '_mysql.connection'>"
    return c

def sqlQuery (c, s) :
    """
    queries the mysql database
    c is the mysql connection
    s is the query
    returns the result of the query (a tuple)
    """
    #assert str(type(c)) == "<type '_mysql.connection'>"
    #assert type(s)      is str
    c.query(s)
    r = c.use_result()
    if r is None :
        return None
    #assert str(type(r)) == "<type '_mysql.result'>"
    t = r.fetch_row(maxrows = 0)
    #assert type(t) is tuple
    return t

def parseArgs ( args ) :
    """
    parses the command line arguments into [ hostname, user, password, database ]
    args are the command line arguments
    """
    #assert len ( args ) == 5
    loginInfo = []
    for s in args :
        loginInfo.append ( s )
    loginInfo.pop ( 0 )
    #assert len ( loginInfo ) == 4
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
    #assert str ( type ( xml ) ) == "<type 'instance'>"
    return xml

def exportXml ( w, xml ):
    """
    converts an ElementTree to a string, then outputs a formatted xml document to stdout ( a file )
    w is the writer
    xml is an ElementTree
    """
    #assert str ( type ( xml ) ) == "<type 'str'>"
    rawText = xml
    pattern = re.compile (r'[^\S ]+')
    text = re.sub ( pattern, "", rawText )
    reparsed = MD.parseString ( text )
    w.write ( reparsed.toprettyxml ( indent = "\t", encoding = "UTF-8" ) )

def createTables ( c ) :
    """
    clears the mysql database of previous tables if they exist, then inserts the new tables with their datatypes
    c is the mysql connection
    """
    #assert str(type(c)) == "<type '_mysql.connection'>"
    sqlQuery ( c, "drop table if exists Crisis;" )
    sqlQuery ( c, "drop table if exists Organization;" )
    sqlQuery ( c, "drop table if exists Person;" )
    sqlQuery ( c, "drop table if exists Location;" )
    sqlQuery ( c, "drop table if exists HumanImpact;" )
    sqlQuery ( c, "drop table if exists ResourceNeeded;" )
    sqlQuery ( c, "drop table if exists WaysToHelp;" )
    sqlQuery ( c, "drop table if exists ExternalResource;" )
    sqlQuery ( c, "drop table if exists CrisisOrganization;" )
    sqlQuery ( c, "drop table if exists OrganizationPerson;" )
    sqlQuery ( c, "drop table if exists PersonCrisis;" )
    sqlQuery ( c, "drop table if exists CrisisKind;" )
    sqlQuery ( c, "drop table if exists OrganizationKind;" )
    sqlQuery ( c, "drop table if exists PersonKind;" )

    sqlQuery ( c, "CREATE TABLE Crisis ( id char(100) NOT NULL PRIMARY KEY, name text NOT NULL, kind char(100) NOT NULL REFERENCES CrisisKind(id), start_date date NOT NULL, start_time time, end_date date, end_time time, economic_impact char(100) NOT NULL );" )
    sqlQuery ( c, "CREATE TABLE Organization ( id char(100) NOT NULL PRIMARY KEY, name char(100) NOT NULL, kind char(100) NOT NULL REFERENCES OrganizationKind(id), history text NOT NULL, telephone char(100) NOT NULL, fax char(100) NOT NULL, email char(100) NOT NULL, street_address char(100) NOT NULL, locality char(100) NOT NULL, region char(100) NOT NULL, postal_code char(100) NOT NULL, country char(100) NOT NULL );" )
    sqlQuery ( c, "CREATE TABLE Person ( id char(100) NOT NULL PRIMARY KEY, first_name char(100) NOT NULL, middle_name char(100), last_name char(100) NOT NULL, suffix char(100), kind char(100) NOT NULL REFERENCES PersonKind(id) );" )
    sqlQuery ( c, "CREATE TABLE Location ( id int NOT NULL AUTO_INCREMENT PRIMARY KEY, entity_type ENUM('C', 'O', 'P') NOT NULL, entity_id char(100) NOT NULL, locality char(100), region char(100), country char(100) );" )
    sqlQuery ( c, "CREATE TABlE HumanImpact ( id int NOT NULL AUTO_INCREMENT PRIMARY KEY, crisis_id char(100) NOT NULL REFERENCES Crisis(id), type char(100) NOT NULL, number int NOT NULL );" )
    sqlQuery ( c, "CREATE TABLE ResourceNeeded ( id int NOT NULL AUTO_INCREMENT PRIMARY KEY, crisis_id char(100) NOT NULL REFERENCES Crisis(id), description text );" )
    sqlQuery ( c, "CREATE TABLE WaysToHelp ( id int NOT NULL AUTO_INCREMENT PRIMARY KEY, crisis_id char(100) NOT NULL REFERENCES Crisis(id), description text );" )
    sqlQuery ( c, "CREATE TABLE ExternalResource ( id int NOT NULL AUTO_INCREMENT PRIMARY KEY, entity_type ENUM('C', 'O', 'P') NOT NULL, entity_id char(100) NOT NULL, type ENUM('IMAGE', 'VIDEO', 'MAP', 'SOCIAL_NETWORK', 'CITATION', 'EXTERNAL_LINK') NOT NULL, link text NOT NULL );" )
    sqlQuery ( c, "CREATE TABlE CrisisOrganization ( id_crisis char(100) NOT NULL REFERENCES Crisis(id), id_organization char(100) NOT NULL REFERENCES Organization(id), PRIMARY KEY (id_crisis, id_organization) );" )
    sqlQuery ( c, "CREATE TABLE OrganizationPerson ( id_organization char(100) NOT NULL REFERENCES Organization(id), id_person char(100) NOT NULL REFERENCES Person(id), PRIMARY KEY (id_organization, id_person) );" )
    sqlQuery ( c, "CREATE TABLE PersonCrisis ( id_person char(100) NOT NULL REFERENCES Person(id), id_crisis char(100) NOT NULL REFERENCES Crisis(id), PRIMARY KEY (id_person, id_crisis) );" )
    sqlQuery ( c, "CREATE TABLE CrisisKind ( id char(100) NOT NULL PRIMARY KEY, name char(100) NOT NULL, description text NOT NULL );" )
    sqlQuery ( c, "CREATE TABLE OrganizationKind ( id char(100) NOT NULL PRIMARY KEY, name char(100) NOT NULL, description text NOT NULL );" )
    sqlQuery ( c, "CREATE TABLE PersonKind ( id char(100) NOT NULL PRIMARY KEY, name char(100) NOT NULL, description text NOT NULL );" )
    sqlQuery ( c, "show tables;" )

def openTagAtt ( x, attName, attVal ):
    """
    builds a string of an opening xml element with a chosen tag, attribute, and value
    x is the tag
    attName is the attribute name
    attVal is the attribute value
    """
    #assert str(type(x)) == "<type 'str'>"
    #assert str(type(attName)) == "<type 'str'>"
    #assert str(type(attVal)) == "<type 'str'>"
    tag = "<" + str ( x ) + " " + str ( attName ) + "='" + str ( attVal ) +"'>"
    #assert str ( type ( tag ) ) == "<type 'str'>"
    return tag

def closeTagAtt ( x, attName, attVal ):
    """
    builds a string of an opening and closing xml element with a chosen tag, attribute, and value
    x is the tag
    attName is the attribute name
    attVal is the attribute value
    """
    #assert str(type(x)) == "<type 'str'>"
    #assert str(type(attName)) == "<type 'str'>"
    #assert str(type(attVal)) == "<type 'str'>"
    tag = "<" + str ( x ) + " " + str ( attName ) + "='" + str ( attVal ) +"'/>"
    #assert str ( type ( tag ) ) == "<type 'str'>"
    return tag

def openTag ( x ):
    """
    builds a string of an opening xml element with a chosen tag
    x is the tag
    """
    #assert str(type(x)) == "<type 'str'>"
    tag = "<" + str ( x ) + ">"
    #assert str ( type ( tag ) ) == "<type 'str'>"
    return tag

def openCloseTag ( x, text ):
    """
    builds a string of an opening and closing xml element with a chosen tag and inner text
    x is the tag
    text is the text
    """
    #assert str(type(x)) == "<type 'str'>"
    #assert str(type(text)) == "<type 'str'>"
    tag = "<" + str ( x ) + ">" + text + "</" + str ( x ) + ">"
    #assert str ( type ( tag ) ) == "<type 'str'>"
    return tag

def closeTag ( x ):
    """
    builds a string of a closing xml element with a chosen tag
    x is the tag
    """
    #assert str(type(x)) == "<type 'str'>"
    tag = "</" + str ( x ) + ">"
    #assert str ( type ( tag ) ) == "<type 'str'>"
    return tag

def getText ( old ) :
    if ( old == None ) :
        new = ""
    else :
        new = old.strip().replace ( "'", "\\'" )[ :100 ]
    return new

def exportCrises ( c ) :
    """
    exports the crises from the mysql database
    c is the mysql database connection
    """
    #assert str(type(c)) == "<type '_mysql.connection'>"
    xml = ""
    cr = sqlQuery ( c, "select * from Crisis;" )
    for i in cr :
        cL = sqlQuery ( c, "select * from Location where ( entity_type = 'C' and entity_id = '" + i [ 0 ] + "' );" )
        hI = sqlQuery ( c, "select * from HumanImpact where crisis_id = '" + i [ 0 ] + "';" )
        rN = sqlQuery ( c, "select * from ResourceNeeded where crisis_id = '" + i [ 0 ] + "';" )
        wTH = sqlQuery ( c, "select * from WaysToHelp where crisis_id = '" + i [ 0 ] + "';" )
        cER = []
        for r in sqlQuery ( c, "select * from ExternalResource where ( entity_type = 'C' and entity_id = '"+i[0]+"' and type = 'IMAGE' );" ) :
            cER.append ( r )
        for r in sqlQuery ( c, "select * from ExternalResource where ( entity_type = 'C' and entity_id = '"+i[0]+"' and type = 'VIDEO' );" ) :
            cER.append ( r )
        for r in sqlQuery ( c, "select * from ExternalResource where ( entity_type = 'C' and entity_id = '"+i[0]+"' and type = 'MAP' );" ) :
            cER.append ( r )
        for r in sqlQuery ( c, "select * from ExternalResource where ( entity_type = 'C' and entity_id = '"+i[0]+"' and type = 'SOCIAL_NETWORK' );" ) :
            cER.append ( r )
        for r in sqlQuery ( c, "select * from ExternalResource where ( entity_type = 'C' and entity_id = '"+i[0]+"' and type = 'CITATION' );" ) :
            cER.append ( r )
        for r in sqlQuery ( c, "select * from ExternalResource where ( entity_type = 'C' and entity_id = '"+i[0]+"' and type = 'EXTERNAL_LINK' );" ) :
            cER.append ( r )
        cTP = sqlQuery ( c, "select * from PersonCrisis where id_crisis = '" + i [ 0 ] + "';" )
        oTC = sqlQuery ( c, "select * from CrisisOrganization where id_crisis = '" + i [ 0 ] + "';" )
        xml += openTagAtt ( "Crisis", "crisisIdent", i [ 0 ] )
        xml += openCloseTag ( "Name", i [ 1 ] )
        xml += closeTagAtt ( "Kind", "crisisKindIdent", i [ 2 ] )
        for j in cL :
            xml += openTag ( "Location" )
            xml += openCloseTag ( "Locality", j [ 3 ] )
            xml += openCloseTag ( "Region", j [ 4 ] )
            xml += openCloseTag ( "Country", j [ 5 ] )
            xml += closeTag ( "Location" )
        xml += openTag ( "StartDateTime" )
        xml += openCloseTag ( "Date", i [ 3 ] )
        xml += openCloseTag ( "Time", i [ 4 ] )
        xml += closeTag ( "StartDateTime" )
        xml += openTag ( "EndDateTime" )
        xml += openCloseTag ( "Date", i [ 5 ] )
        xml += openCloseTag ( "Time", i [ 6 ] )
        xml += closeTag ( "EndDateTime" )
        for j in hI :
            xml += openTag ( "HumanImpact" )
            xml += openCloseTag ( "Type", j [ 2 ] )
            xml += openCloseTag ( "Number", j [ 3 ] )
            xml += closeTag ( "HumanImpact" )
        xml += openCloseTag ( "EconomicImpact", i [ 7 ] )
        for j in rN :
            xml += openCloseTag ( "ResourceNeeded", j [ 2 ] )
        for j in wTH :
            xml += openCloseTag ( "WaysToHelp", j [ 2 ] )
        xml += openTag ( "ExternalResources" )
        for j in cER :
            resourceTag = createResourceTypeTag ( j [ 3 ] )
            xml += openCloseTag ( resourceTag , j [ 4 ].replace ( "&", "&amp;" ) )
        xml += closeTag ( "ExternalResources" )
        xml += openTag ( "RelatedPersons" )
        for j in cTP :
            xml += closeTagAtt ( "RelatedPerson" , "personIdent", j [ 0 ] )
        xml += closeTag ( "RelatedPersons" )
        xml += openTag ( "RelatedOrganizations" )
        for j in oTC :
            xml += closeTagAtt ( "RelatedOrganization" , "organizationIdent", j [ 1 ] )
        xml += closeTag ( "RelatedOrganizations" )
        xml += closeTag ( "Crisis" )
    #assert str ( type ( xml ) ) == "<type 'str'>"
    return xml

def exportOrgs ( c ) :
    """
    exports the organizations from the mysql database
    c is the mysql database connection
    """
    #assert str(type(c)) == "<type '_mysql.connection'>"
    o = sqlQuery ( c, "select * from Organization;" )
    xml = ""
    for i in o:
        oL = sqlQuery ( c, "select * from Location where ( entity_type = 'O' and entity_id = '"+i[0]+"' );" )
        oER = []
        for r in sqlQuery ( c, "select * from ExternalResource where ( entity_type = 'O' and entity_id = '"+i[0]+"' and type = 'IMAGE' );" ) :
            oER.append ( r )
        for r in sqlQuery ( c, "select * from ExternalResource where ( entity_type = 'O' and entity_id = '"+i[0]+"' and type = 'VIDEO' );" ) :
            oER.append ( r )
        for r in sqlQuery ( c, "select * from ExternalResource where ( entity_type = 'O' and entity_id = '"+i[0]+"' and type = 'MAP' );" ) :
            oER.append ( r )
        for r in sqlQuery ( c, "select * from ExternalResource where ( entity_type = 'O' and entity_id = '"+i[0]+"' and type = 'SOCIAL_NETWORK' );" ) :
            oER.append ( r )
        for r in sqlQuery ( c, "select * from ExternalResource where ( entity_type = 'O' and entity_id = '"+i[0]+"' and type = 'CITATION' );" ) :
            oER.append ( r )
        for r in sqlQuery ( c, "select * from ExternalResource where ( entity_type = 'O' and entity_id = '"+i[0]+"' and type = 'EXTERNAL_LINK' );" ) :
            oER.append ( r )
        oTC = sqlQuery ( c, "select * from CrisisOrganization where id_organization = '"+i[0]+"';" )
        pTO = sqlQuery ( c, "select * from OrganizationPerson where id_organization = '"+i[0]+"';" )
        xml += openTagAtt ( "Organization", "organizationIdent", i[0])
        xml += openCloseTag ( "Name", i[1])
        xml += closeTagAtt ( "Kind", "organizationKindIdent", i[2])
        for j in oL :
            xml += openTag ( "Location" )
            xml += openCloseTag ( "Locality", j [ 3 ] )
            xml += openCloseTag ( "Region", j [ 4 ] )
            xml += openCloseTag ( "Country", j [ 5 ] )
            xml += closeTag ( "Location" )
        xml += openCloseTag ("History", i[3])
        xml += openTag ( "ContactInfo" )
        xml += openCloseTag ("Telephone", i[4])
        xml += openCloseTag ("Fax", i[5])
        xml += openCloseTag ("Email", i[6])
        xml += openTag ("PostalAddress")
        xml += openCloseTag ("StreetAddress", i[7])
        xml += openCloseTag ( "Locality", i[8])
        xml += openCloseTag ( "Region", i[9])
        xml += openCloseTag ( "PostalCode", i[10])
        xml += openCloseTag ( "Country", i[11])
        xml += closeTag ( "PostalAddress" )
        xml += closeTag ( "ContactInfo" )
        xml += openTag ("ExternalResources")
        for j in oER:
            resourceTag = createResourceTypeTag ( j [ 3 ] )
            xml += openCloseTag ( resourceTag , j [ 4 ].replace ( "&", "&amp;" ) )
        xml += closeTag ("ExternalResources")
        xml += openTag ("RelatedCrises")
        for j in oTC:
            xml += closeTagAtt ("RelatedCrisis", "crisisIdent", j[0])
        xml += closeTag ("RelatedCrises")
        xml += openTag ("RelatedPersons")
        for j in pTO:
            xml += closeTagAtt ("RelatedPerson", "personIdent", j[1])
        xml += closeTag ("RelatedPersons")
        xml += closeTag ("Organization")
    #assert str ( type ( xml ) ) == "<type 'str'>"
    return xml

def exportPeople ( c ) :
    """
    exports the people from the mysql database
    c is the mysql database connection
    """
    #assert str(type(c)) == "<type '_mysql.connection'>"
    xml = ""
    p = sqlQuery ( c, "select * from Person;" )
    for i in p :
        pL = sqlQuery ( c, "select * from Location where ( entity_type = 'P' and entity_id = '" + i [ 0 ] + "' );" )
        pER = []
        for r in sqlQuery ( c, "select * from ExternalResource where ( entity_type = 'P' and entity_id = '"+i[0]+"' and type = 'IMAGE' );" ) :
            pER.append ( r )
        for r in sqlQuery ( c, "select * from ExternalResource where ( entity_type = 'P' and entity_id = '"+i[0]+"' and type = 'VIDEO' );" ) :
            pER.append ( r )
        for r in sqlQuery ( c, "select * from ExternalResource where ( entity_type = 'P' and entity_id = '"+i[0]+"' and type = 'MAP' );" ) :
            pER.append ( r )
        for r in sqlQuery ( c, "select * from ExternalResource where ( entity_type = 'P' and entity_id = '"+i[0]+"' and type = 'SOCIAL_NETWORK' );" ) :
            pER.append ( r )
        for r in sqlQuery ( c, "select * from ExternalResource where ( entity_type = 'P' and entity_id = '"+i[0]+"' and type = 'CITATION' );" ) :
            pER.append ( r )
        for r in sqlQuery ( c, "select * from ExternalResource where ( entity_type = 'P' and entity_id = '"+i[0]+"' and type = 'EXTERNAL_LINK' );" ) :
            pER.append ( r )
        pTO = sqlQuery ( c, "select * from OrganizationPerson where id_person = '" + i [ 0 ] + "';" )
        cTP = sqlQuery ( c, "select * from PersonCrisis where id_person = '" + i [ 0 ] + "';" )
        xml += openTagAtt ( "Person", "personIdent", i [ 0 ] )
        xml += openTag ( "Name" )
        xml += openCloseTag ( "FirstName", i [ 1 ] )
        xml += openCloseTag ( "MiddleName", i [ 2 ] )
        xml += openCloseTag ( "LastName", i [ 3 ] )
        xml += openCloseTag ( "Suffix", i [ 4 ] )
        xml += closeTag ( "Name" )
        xml += closeTagAtt ( "Kind", "personKindIdent", i [ 5 ] )
        for j in pL :
            xml += openTag ( "Location" )
            xml += openCloseTag ( "Locality", j [ 3 ] )
            xml += openCloseTag ( "Region", j [ 4 ] )
            xml += openCloseTag ( "Country", j [ 5 ] )
            xml += closeTag ( "Location" )
        xml += openTag ( "ExternalResources" )
        for j in pER :
            resourceTag = createResourceTypeTag ( j [ 3 ] )
            xml += openCloseTag ( resourceTag , j [ 4 ].replace ( "&", "&amp;" ) )
        xml += closeTag ( "ExternalResources" )
        xml += openTag ( "RelatedCrises" )
        for j in cTP :
            xml += closeTagAtt ( "RelatedCrisis" , "crisisIdent", j [ 1 ] )
        xml += closeTag ( "RelatedCrises" )
        xml += openTag ( "RelatedOrganizations" )
        for j in pTO :
            xml += closeTagAtt ( "RelatedOrganization" , "organizationIdent", j [ 0 ] )
        xml += closeTag ( "RelatedOrganizations" )
        xml += closeTag ( "Person" )
    #assert str ( type ( xml ) ) == "<type 'str'>"
    return xml

def exportTypes( c ) :
    """
    exports the crisis, organization, and person types from the mysql database
    c is the mysql database connection
    """
    #assert str(type(c)) == "<type '_mysql.connection'>"
    xml = ""
    cT = sqlQuery ( c, "select * from CrisisKind;" )
    oT = sqlQuery ( c, "select * from OrganizationKind;" )
    pT = sqlQuery ( c, "select * from PersonKind;" )    
    for i in cT:
        xml += openTagAtt ("CrisisKind", "crisisKindIdent", i[0])
        xml += openCloseTag ("Name", i[1])
        xml += openCloseTag ("Description", i[2])
        xml += closeTag ("CrisisKind")    
    for i in oT:
        xml += openTagAtt ("OrganizationKind", "organizationKindIdent", i[0])
        xml += openCloseTag ("Name", i[1])
        xml += openCloseTag ("Description", i[2])
        xml += closeTag ("OrganizationKind")
    for i in pT:
        xml += openTagAtt ("PersonKind", "personKindIdent", i[0])
        xml += openCloseTag ("Name", i[1])
        xml += openCloseTag ("Description", i[2])
        xml += closeTag ("PersonKind")
    #assert str ( type ( xml ) ) == "<type 'str'>"
    return xml

def importCrisis ( c, crisisInstance ):
    """
    imports an Element of type Crisis into the mysql database
    c is the mysql database connection
    crisisInstance is the element
    """    
    #assert str(type(c)) == "<type '_mysql.connection'>"
    #assert str(type(crisisInstance)) == "<type 'instance'>"
    crisisID = crisisInstance.attrib["crisisIdent"]

    curC = sqlQuery ( c, "delete from Crisis where id = '" + crisisID + "';" )
    
    #Gets location sub elements in list. Inserts into CrisisLocation table by indexing list
    allLocations = crisisInstance.findall("Location")
    if len(allLocations) != 0:
        for instance in allLocations:
            tags = []
            for elem in instance :
                tags.append ( elem.tag )
            if ( len ( instance ) == 1 ) :
                if ( "Locality" in tags ) :
                    sqlQuery ( c, "delete from Location where ( entity_type = 'C' and entity_id = '"+crisisID+"' and locality = '"+getText ( instance[0].text )+"' );")
                    sqlQuery ( c, "insert into Location values ( null, 'C', '"+crisisID+"', '"+getText ( instance[0].text )+"', '', '' );")
                elif ( "Region" in tags ) :
                    sqlQuery ( c, "delete from Location where ( entity_type = 'C' and entity_id = '"+crisisID+"' and region = '"+getText ( instance[0].text )+"' );")
                    sqlQuery ( c, "insert into Location values ( null, 'C', '"+crisisID+"', '', '"+getText ( instance[0].text )+"', '' );")
                elif ( "Country" in tags ) :
                    sqlQuery ( c, "delete from Location where ( entity_type = 'C' and entity_id = '"+crisisID+"' and country = '"+getText ( instance[0].text )+"' );")
                    sqlQuery ( c, "insert into Location values ( null, 'C', '"+crisisID+"', '', '', '"+getText ( instance[0].text )+"');")
            elif ( len ( instance ) == 2 ) :
                if ( "Locality" not in tags ) :
                    sqlQuery ( c, "delete from Location where ( entity_type = 'C' and entity_id = '"+crisisID+"' and region = '"+getText ( instance[0].text )+"' ) or ( entity_type = 'C' and entity_id = '"+crisisID+"' and region = '' and country = '"+getText ( instance[1].text )+"');")
                    sqlQuery ( c, "insert into Location values ( null, 'C', '"+crisisID+"', '', '"+getText ( instance[0].text )+"', '"+getText ( instance[1].text )+"');")
                elif ( "Region" not in tags ) :
                    sqlQuery ( c, "delete from Location where ( entity_type = 'C' and entity_id = '"+crisisID+"' and locality = '"+getText ( instance[0].text )+"' ) or ( entity_type = 'C' and entity_id = '"+crisisID+"' and locality = '' and country = '"+getText ( instance[1].text )+"');")
                    sqlQuery ( c, "insert into Location values ( null, 'C', '"+crisisID+"', '"+getText ( instance[0].text )+"', '', '"+getText ( instance[1].text )+"');")
                elif ( "Country" not in tags ) :
                    sqlQuery ( c, "delete from Location where ( entity_type = 'C' and entity_id = '"+crisisID+"' and locality = '"+getText ( instance[0].text )+"' ) or ( entity_type = 'C' and entity_id = '"+crisisID+"' and locality = '' and region = '"+getText ( instance[1].text )+"');")
                    sqlQuery ( c, "insert into Location values ( null, 'C', '"+crisisID+"', '"+getText ( instance[0].text )+"', '"+getText ( instance[1].text )+"', '',);")
            else :
                sqlQuery ( c, "delete from Location where ( entity_type = 'C' and entity_id = '"+crisisID+"' and locality = '"+(getText ( instance[0].text ))+"' ) or ( entity_type = 'C' and entity_id = '"+crisisID+"' and locality = '' and region = '"+(getText ( instance[1].text ))+"') or ( entity_type = 'C' and entity_id = '"+crisisID+"' and locality = '' and region = '"+(getText ( instance[1].text ))+"' and country = '"+(getText ( instance[2].text ))+"');")
                sqlQuery ( c, "insert into Location values ( null, 'C', '"+crisisID+"', '"+ (getText ( instance[0].text )) +"', '"+ (getText ( instance[1].text )) +"', '"+ (getText ( instance[2].text )) +"');")

    #Gets list of all resources needed. Iterates through lists and inserts into ResourceNeeded table
    resourcesNeeded = crisisInstance.findall("ResourceNeeded")

    if len(resourcesNeeded) != 0:
        for instance in resourcesNeeded:
            sqlQuery ( c, "delete from ResourceNeeded where ( crisis_id = '"+crisisID+"' and description = '"+getText ( instance.text )+"' );")
            sqlQuery ( c, "insert into ResourceNeeded values ( null, '"+crisisID+"', '"+getText ( instance.text )+"');")
    
    #Gets all URL's in a list. Indexes list, splices tag to get type, inserts data into table
    externalResources = crisisInstance.find("ExternalResources")
    
#Get all resources. Checks for Citation because it's the only one not ending in 'URL'. Get index of URL for others to splice off. Add to table
    if len(externalResources) != 0:
        for instance in externalResources:
            resourceType = parseResourceType ( instance.tag )
            sqlQuery ( c, "delete from ExternalResource where ( entity_type = 'C' and entity_id = '"+crisisID+"' and type = '"+resourceType+"' and link = '"+getText ( instance.text )+"' );")
            sqlQuery ( c, "insert into ExternalResource values ( null, 'C', '"+crisisID+"', '"+resourceType+"', '"+getText ( instance.text )+"');")
                

    #Gets list of all RelatedPeople and inserts into CrisesToPeople table
    relatedPeople = crisisInstance.findall(".//" + "RelatedPerson")

    if len(relatedPeople) != 0:
        for instance in relatedPeople:
            sqlQuery ( c, "delete from PersonCrisis where ( id_person = '"+instance.attrib["personIdent"]+"' and id_crisis = '"+crisisID+"' );")
            sqlQuery ( c, "insert into PersonCrisis values ( '"+instance.attrib["personIdent"]+"', '"+crisisID+"');")

     #Gets list of all RelatedOrganizations and inserts into OrganizationsToCrises table
    relatedOrgs = crisisInstance.findall(".//" + "RelatedOrganization")

    if len(relatedOrgs) != 0:
        for instance in relatedOrgs:
            sqlQuery ( c, "delete from CrisisOrganization where ( id_crisis = '"+crisisID+"' and id_organization = '"+instance.attrib["organizationIdent"]+"' );")
            sqlQuery ( c, "insert into CrisisOrganization values ( '"+crisisID+"', '"+instance.attrib["organizationIdent"]+"');")

    #Gets all tags titled WaysToHelp, and inserts into corresponding table by indexing the list they're stored in
    waysToHelp = crisisInstance.findall("WaysToHelp")
    
    if len(waysToHelp) != 0:
        for instance in waysToHelp:
            sqlQuery ( c, "delete from WaysToHelp where ( crisis_id = '"+crisisID+"' and description = '"+getText ( instance.text )+"' );")
            sqlQuery ( c, "insert into WaysToHelp values ( null, '"+crisisID+"', '"+getText ( instance.text )+"');")

    #Gets list of HumanImpact elements. Iterates through list and inserts into HumanImpact table
    humanImpact = crisisInstance.findall("HumanImpact")

    if len(humanImpact) !=0:
        for instance in humanImpact:
            sqlQuery ( c, "delete from HumanImpact where ( crisis_id = '"+crisisID+"' and type = '"+getText ( instance[0].text )[ :100 ]+"' );")
            numbertext = getText ( instance[1].text )
            number = int (numberText)
            if number > 2147483647 :
                numbertext = "60 billion"
            sqlQuery ( c, "insert into HumanImpact values ( null, '"+crisisID+"', '"+getText ( instance[0].text )[ :100 ]+"', '"+numbertext+"');")

    #Finds values of remaining elements and inserts into Crises table
    name = getText ( crisisInstance.find("Name").text )
    kind = crisisInstance.find("Kind").attrib["crisisKindIdent"]
    startDateTime = crisisInstance.find("StartDateTime")
    startDate = getText ( startDateTime[0].text ).strip ()
    if len(startDateTime) > 1:
        startTime = getText ( startDateTime[1].text )
    else:
        startTime = '00:00:00'
    endDateTime = crisisInstance.find("EndDateTime")
    if endDateTime != None :
        endDate = getText ( endDateTime[0].text ).strip ()
        if len(endDateTime) > 1:
            endTime = getText ( endDateTime[1].text )
        else:
            endTime = '00:00:00'
    else :
        endDate = startDate
        endTime = '23:59:59'
    econImpact = getText ( crisisInstance.find("EconomicImpact").text )

    sqlQuery ( c, "insert into Crisis values ( '"+crisisID+"', '"+name+"', '"+kind+"', '"+startDate+"', '"+startTime+"', '"+endDate+"', '"+endTime+"', '"+econImpact[ :100 ]+"');")

def importOrg ( c, orgInstance ):
    """
    imports an Element of type Organization into the mysql database
    c is the mysql database connection
    orgInstance is the element
    """
    #assert str(type(c)) == "<type '_mysql.connection'>"
    #assert str(type(orgInstance)) == "<type 'instance'>"
    orgID = orgInstance.attrib["organizationIdent"]
    
    curO = sqlQuery ( c, "delete from Organization where id = '" + orgID + "';" )

    #Gets location sub elements in list. Inserts into CrisisLocation table by indexing list
    allLocations = orgInstance.findall("Location")
    if len(allLocations) != 0:
        for instance in allLocations:
            tags = []
            for elem in instance :
                tags.append ( elem.tag )
            if ( len ( instance ) == 1 ) :
                if ( "Locality" in tags ) :
                    sqlQuery ( c, "delete from Location where ( entity_type = 'O' and entity_id = '"+orgID+"' and locality = '"+getText ( instance[0].text )+"' );")
                    sqlQuery ( c, "insert into Location values ( null, 'O', '"+orgID+"', '"+getText ( instance[0].text )+"', '', '' );")
                elif ( "Region" in tags ) :
                    sqlQuery ( c, "delete from Location where ( entity_type = 'O' and entity_id = '"+orgID+"' and region = '"+getText ( instance[0].text )+"' );")
                    sqlQuery ( c, "insert into Location values ( null, 'O', '"+orgID+"', '', '"+getText ( instance[0].text )+"', '' );")
                elif ( "Country" in tags ) :
                    sqlQuery ( c, "delete from Location where ( entity_type = 'O' and entity_id = '"+orgID+"' and country = '"+getText ( instance[0].text )+"' );")
                    sqlQuery ( c, "insert into Location values ( null, 'O', '"+orgID+"', '', '', '"+getText ( instance[0].text )+"');")
            elif ( len ( instance ) == 2 ) :
                if ( "Locality" not in tags ) :
                    sqlQuery ( c, "delete from Location where ( entity_type = 'O' and entity_id = '"+orgID+"' and region = '"+getText ( instance[0].text )+"' ) or ( entity_type = 'O' and entity_id = '"+orgID+"' and region = '' and country = '"+getText ( instance[1].text )+"');")
                    sqlQuery ( c, "insert into Location values ( null, 'O', '"+orgID+"', '', '"+getText ( instance[0].text )+"', '"+getText ( instance[1].text )+"');")
                elif ( "Region" not in tags ) :
                    sqlQuery ( c, "delete from Location where ( entity_type = 'O' and entity_id = '"+orgID+"' and locality = '"+getText ( instance[0].text )+"' ) or ( entity_type = 'O' and entity_id = '"+orgID+"' and locality = '' and country = '"+getText ( instance[1].text )+"');")
                    sqlQuery ( c, "insert into Location values ( null, 'O', '"+orgID+"', '"+getText ( instance[0].text )+"', '', '"+getText ( instance[1].text )+"');")
                elif ( "Country" not in tags ) :
                    sqlQuery ( c, "delete from Location where ( entity_type = 'O' and entity_id = '"+orgID+"' and locality = '"+getText ( instance[0].text )+"' ) or ( entity_type = 'O' and entity_id = '"+orgID+"' and locality = '' and region = '"+getText ( instance[1].text )+"');")
                    sqlQuery ( c, "insert into Location values ( null, 'O', '"+orgID+"', '"+getText ( instance[0].text )+"', '"+getText ( instance[1].text )+"', '',);")
            elif ( len ( instance ) == 3 ) :
                sqlQuery ( c, "delete from Location where ( entity_type = 'O' and entity_id = '"+orgID+"' and locality = '"+(getText ( instance[0].text ))+"' ) or ( entity_type = 'O' and entity_id = '"+orgID+"' and locality = '' and region = '"+(getText ( instance[1].text ))+"') or ( entity_type = 'O' and entity_id = '"+orgID+"' and locality = '' and region = '"+(getText ( instance[1].text ))+"' and country = '"+(getText ( instance[2].text ))+"');")
                sqlQuery ( c, "insert into Location values ( null, 'O', '"+orgID+"', '"+ (getText ( instance[0].text )) +"', '"+ (getText ( instance[1].text )) +"', '"+ (getText ( instance[2].text )) +"');")

    #Get all resources. Checks for Citation because it's the only one not ending in 'URL'. Get index of URL for others to splice off. Add to table
    externalResources = orgInstance.find("ExternalResources")
    if len(externalResources) != 0:
        for instance in externalResources:
            resourceType = parseResourceType ( instance.tag )
            sqlQuery ( c, "delete from ExternalResource where ( entity_type = 'O' and entity_id = '"+orgID+"' and type = '"+resourceType+"' and link = '"+getText ( instance.text )+"' );")
            sqlQuery ( c, "insert into ExternalResource values ( null, 'O', '"+orgID+"', '"+resourceType+"', '"+getText ( instance.text )+"');")

    #Get all values for Organizations table and insert to DB
    postalAddress = orgInstance.find(".//" + "PostalAddress")
    name = getText ( orgInstance.find("Name").text )
    kind = orgInstance.find("Kind").attrib["organizationKindIdent"]
    history = getText ( orgInstance.find("History").text ).encode ( "ascii", "ignore" )
    phone = getText ( orgInstance.find(".//" + "Telephone").text ) or "0000000000"
    fax = getText ( orgInstance.find(".//" + "Fax").text ) or "0000000000"
    email = getText ( orgInstance.find(".//" + "Email").text )
    address = getText ( postalAddress[0].text )
    locality = getText ( postalAddress[1].text )
    region = getText ( postalAddress[2].text )
    postalCode = getText ( postalAddress[3].text )
    country = getText ( postalAddress[4].text )
    sqlQuery (c , "insert into Organization values ( '"+orgID+"', '"+name+"', '"+kind+"', '"+history+"', '"+phone+"', '"+fax+"', '"+email+"', '"+address+"', '"+locality+"', '"+region+"', '"+postalCode+"', '"+country+"');")

def importPerson ( c, peopleInstance ):
    """
    imports an Element of type Person into the mysql database
    c is the mysql database connection
    personInstance is the element
    """
    #assert str(type(c)) == "<type '_mysql.connection'>"
    #assert str(type(peopleInstance)) == "<type 'instance'>"
    personID = peopleInstance.attrib["personIdent"]

    curP = sqlQuery ( c, "delete from Person where id = '" + personID + "';" )
        
    #Gets location sub elements in list. Inserts into PeopleLocation table by indexing list
    locationElements = list(peopleInstance.findall("Location"))
    for instance in locationElements:
        tags = []
        for elem in instance :
            tags.append ( elem.tag )
        if ( len ( instance ) == 1 ) :
            if ( "Locality" in tags ) :
                sqlQuery ( c, "delete from Location where ( entity_type = 'P' and entity_id = '"+personID+"' and locality = '"+getText ( instance[0].text )+"' );")
                sqlQuery ( c, "insert into Location values ( null, 'P', '"+personID+"', '"+getText ( instance[0].text )+"', '', '' );")
            elif ( "Region" in tags ) :
                sqlQuery ( c, "delete from Location where ( entity_type = 'P' and entity_id = '"+personID+"' and region = '"+getText ( instance[0].text )+"' );")
                sqlQuery ( c, "insert into Location values ( null, 'P', '"+personID+"', '', '"+getText ( instance[0].text )+"', '' );")
            elif ( "Country" in tags ) :
                sqlQuery ( c, "delete from Location where ( entity_type = 'P' and entity_id = '"+personID+"' and country = '"+getText ( instance[0].text )+"' );")
                sqlQuery ( c, "insert into Location values ( null, 'P', '"+personID+"', '', '', '"+getText ( instance[0].text )+"');")
        elif ( len ( instance ) == 2 ) :
            if ( "Locality" not in tags ) :
                sqlQuery ( c, "delete from Location where ( entity_type = 'P' and entity_id = '"+personID+"' and region = '"+getText ( instance[0].text )+"' ) or ( entity_type = 'P' and entity_id = '"+personID+"' and region = '' and country = '"+getText ( instance[1].text )+"');")
                sqlQuery ( c, "insert into Location values ( null, 'P', '"+personID+"', '', '"+getText ( instance[0].text )+"', '"+getText ( instance[1].text )+"');")
            elif ( "Region" not in tags ) :
                sqlQuery ( c, "delete from Location where ( entity_type = 'P' and entity_id = '"+personID+"' and locality = '"+getText ( instance[0].text )+"' ) or ( entity_type = 'P' and entity_id = '"+personID+"' and locality = '' and country = '"+getText ( instance[1].text )+"');")
                sqlQuery ( c, "insert into Location values ( null, 'P', '"+personID+"', '"+getText ( instance[0].text )+"', '', '"+getText ( instance[1].text )+"');")
            elif ( "Country" not in tags ) :
                sqlQuery ( c, "delete from Location where ( entity_type = 'P' and entity_id = '"+personID+"' and locality = '"+getText ( instance[0].text )+"' ) or ( entity_type = 'P' and entity_id = '"+personID+"' and locality = '' and region = '"+getText ( instance[1].text )+"');")
                sqlQuery ( c, "insert into Location values ( null, 'P', '"+personID+"', '"+getText ( instance[0].text )+"', '"+getText ( instance[1].text )+"', '',);")
        else :
            sqlQuery ( c, "delete from Location where ( entity_type = 'P' and entity_id = '"+personID+"' and locality = '"+(getText ( instance[0].text ))+"' ) or ( entity_type = 'P' and entity_id = '"+personID+"' and locality = '' and region = '"+(getText ( instance[1].text ))+"') or ( entity_type = 'P' and entity_id = '"+personID+"' and locality = '' and region = '"+(getText ( instance[1].text ))+"' and country = '"+(getText ( instance[2].text ))+"');")
            sqlQuery ( c, "insert into Location values ( null, 'P', '"+personID+"', '"+ (getText ( instance[0].text )) +"', '"+ (getText ( instance[1].text )) +"', '"+ (getText ( instance[2].text )) +"');")
    
    #Gets list of all RelatedOrganizations and inserts into PeopleToOrganizations table
    relatedOrgs = peopleInstance.find("RelatedOrganizations")
    if relatedOrgs != None :
        for instance in relatedOrgs:
            sqlQuery ( c, "delete from OrganizationPerson where ( id_organization = '"+instance.attrib["organizationIdent"]+"' and id_person = '"+personID+"' );")
            sqlQuery ( c, "insert into OrganizationPerson values ( '"+instance.attrib["organizationIdent"]+"', '"+personID+"');")

    #Gets all URL's in a list. Indexes list, splices tag to get type, inserts data into table
    externalResources = peopleInstance.find("ExternalResources")
    
    #Get all resources. Checks for Citation because it's the only one not ending in 'URL'. Get index of URL for others to splice off. Add to table
    for instance in externalResources:
        resourceType = parseResourceType ( instance.tag )
        sqlQuery ( c, "delete from ExternalResource where ( entity_type = 'P' and entity_id = '"+personID+"' and type = '"+resourceType+"' and link = '"+getText ( instance.text )+"' );")
        sqlQuery ( c, "insert into ExternalResource values ( null, 'P', '"+personID+"', '"+resourceType+"', '"+getText ( instance.text )+"');")
    
    #Finds values of remaining elements and inserts into People table
    firstName = getText ( peopleInstance.find(".//" + "FirstName").text )
    middleName = getText ( peopleInstance.findtext(".//" + "MiddleName", "") )
    lastName = getText ( peopleInstance.find(".//" + "LastName").text )
    suffix = getText ( peopleInstance.findtext("Suffix", "") )
    kind = peopleInstance.find("Kind").attrib["personKindIdent"]
    sqlQuery ( c, "insert into Person values ( '"+personID+"', '"+firstName+"', '"+middleName+"', '"+lastName+"', '"+suffix+"', '"+kind+"');")

def parseResourceType ( t ) :
    x = t.lower ()
    if ( x == "citation" ) :
        x = "citation"
    elif ( x == "externallinkurl" ) :
        x = "external_link"
    elif ( x == "imageurl" ) :
        x = "image"
    elif ( x == "mapurl" ) :
        x = "map"
    elif ( x == "videourl" ) :
        x = "video"
    elif ( x == "socialnetworkurl" ) :
        x = "social_network"
    return x

def createResourceTypeTag ( t ) :
    x = t.lower ()
    if ( x == "citation" ) :
        x = "Citation"
    elif ( x == "external_link" ) :
        x = "ExternalLinkURL"
    elif ( x == "image" ) :
        x = "ImageURL"
    elif ( x == "map" ) :
        x = "MapURL"
    elif ( x == "video" ) :
        x = "VideoURL"
    elif ( x == "social_network" ) :
        x = "SocialNetworkURL"
    return x

def importCrisisKind ( c, crisisKindInstance ):
    """
    imports an Element of type CrisisKind into the mysql database
    c is the mysql database connection
    crisisKindInstance is the element
    """
    #assert str(type(c)) == "<type '_mysql.connection'>"
    #assert str(type(crisisKindInstance)) == "<type 'instance'>"
    crisisKindID = crisisKindInstance.attrib["crisisKindIdent"]
    name = getText ( crisisKindInstance.find("Name").text )
    description = getText ( crisisKindInstance.find("Description").text )
    sqlQuery ( c, "delete from CrisisKind where id = '"+crisisKindID+"';")
    sqlQuery ( c, "insert into CrisisKind values ( '"+crisisKindID+"', '"+name+"', '"+description+"');")

def importOrgKind ( c, orgKindInstance ) :
    """
    imports an Element of type OrganizationKing into the mysql database
    c is the mysql database connection
    orgKindInstance is the element
    """
    #assert str(type(c)) == "<type '_mysql.connection'>"
    #assert str(type(orgKindInstance)) == "<type 'instance'>"
    orgKindID = orgKindInstance.attrib["organizationKindIdent"]
    name = getText ( orgKindInstance.find("Name").text )
    description = getText ( orgKindInstance.find("Description").text )
    sqlQuery ( c, "delete from OrganizationKind where id = '"+orgKindID+"';")
    sqlQuery ( c, "insert into OrganizationKind values ( '"+orgKindID+"', '"+name+"', '"+description+"');")

def importPersonKind ( c, personKindInstance ) :
    """
    #assert str(type(c)) == "<type '_mysql.connection'>"
    imports an Element of type PersonKind into the mysql database
    c is the mysql database connection
    personKindInstance is the element
    """
    #assert str(type(c)) == "<type '_mysql.connection'>"
    #assert str(type(personKindInstance)) == "<type 'instance'>"
    personKindID = personKindInstance.attrib["personKindIdent"]
    name = getText ( personKindInstance.find("Name").text )
    description = getText ( personKindInstance.find("Description").text )
    sqlQuery ( c, "delete from PersonKind where id = '"+personKindID+"';")
    sqlQuery ( c, "insert into PersonKind values ( '"+personKindID+"', '"+name+"', '"+description+"');")

def importDB ( c, xml ) :
    """
    imports an ElementTree into the mysql database
    c is the mysql database connection
    xml is the ElementTree
    """
    #assert str(type(c)) == "<type '_mysql.connection'>"
    #assert str ( type ( xml ) ) == "<type 'instance'>"
    for e in xml :
        if e.tag == "Crisis" :
            importCrisis ( c, e )
        elif e.tag == "Organization" :
            importOrg ( c, e )
        elif e.tag == "Person" :
            importPerson ( c, e )
        elif e.tag == "CrisisKind" :
            importCrisisKind ( c, e )
        elif e.tag == "OrganizationKind" :
            importOrgKind ( c, e )
        elif e.tag == "PersonKind" :
            importPersonKind ( c, e )

def exportDB ( c ) :
    """
    exports the mysql database to an xml document
    c is the mysql database connection
    """
    #assert str(type(c)) == "<type '_mysql.connection'>"
    xml = openTag ( "WorldCrises" )
    xml += exportCrises ( c )
    xml += exportOrgs ( c )
    xml += exportPeople ( c )
    xml += exportTypes ( c )
    xml += closeTag ( "WorldCrises" )
    #assert str ( type ( xml ) ) == "<type 'str'>"
    return xml

def importAllXml ( n, f, c ) :
    """
    imports all xml files in the specified folder into the database
    n is the name of the folder containing the input files
    f is the folder containg the input xml files
    c is the mysql database connection
    """
    for file in f:
        if file.endswith(".xml"):
            with open ( n + "\\" + file, "r" ) as input:
                xml = importXml ( input )
                importDB ( c, xml )
    
def start ( n, f, w, args ):
    """
    imports an xml document into an ElementTree, imports that ElementTree into a mysql database,
    then outputs the mysql database to a valid xml document, which is then written to the output file
    n is the name of the folder containg the input files
    f is the list of input files
    w is the writer
    args are the commandline arguments
    """
    sqlLoginInfo = parseArgs ( args )
    sql = sqlLogin ( sqlLoginInfo )
    createTables ( sql )
    importAllXml ( n, f, sql )
    exportXML = exportDB ( sql )
    sql.close ()
    exportXml ( w, exportXML )
