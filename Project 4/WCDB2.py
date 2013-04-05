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
    assert len ( loginInfo ) == 4
    c = _mysql.connect(
        host = loginInfo [ 0 ],
        user = loginInfo [ 1 ],
        passwd = loginInfo [ 2 ],
        db = loginInfo [ 3 ] )
    assert str(type(c)) == "<type '_mysql.connection'>"
    return c

def sqlQuery (c, s) :
    """
    queries the mysql database
    c is the mysql connection
    s is the query
    returns the result of the query (a tuple)
    """
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
    """
    parses the command line arguments into [ hostname, user, password, database ]
    args are the command line arguments
    """
    assert len ( args ) == 5
    loginInfo = []
    for s in args :
        loginInfo.append ( s )
    loginInfo.pop ( 0 )
    assert len ( loginInfo ) == 4
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
    assert str ( type ( xml ) ) == "<type 'instance'>"
    return xml

def exportXml ( w, xml ):
    """
    converts an ElementTree to a string, then outputs a formatted xml document to stdout ( a file )
    w is the writer
    xml is an ElementTree
    """
    assert str ( type ( xml ) ) == "<type 'str'>"
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
    assert str(type(c)) == "<type '_mysql.connection'>"
    sqlQuery ( c, "drop table if exists Crises;" )
    sqlQuery ( c, "drop table if exists Organizations;" )
    sqlQuery ( c, "drop table if exists People;" )
    sqlQuery ( c, "drop table if exists CrisisLocations;" )
    sqlQuery ( c, "drop table if exists PeopleLocations;" )
    sqlQuery ( c, "drop table if exists OrganizationLocations;" )
    sqlQuery ( c, "drop table if exists HumanImpact;" )
    sqlQuery ( c, "drop table if exists ResourceNeeded;" )
    sqlQuery ( c, "drop table if exists WaysToHelp;" )
    sqlQuery ( c, "drop table if exists PersonExternalResources;" )
    sqlQuery ( c, "drop table if exists OrganizationExternalResources;" )
    sqlQuery ( c, "drop table if exists CrisisExternalResources;" )
    sqlQuery ( c, "drop table if exists PeopleToOrganizations;" )
    sqlQuery ( c, "drop table if exists OrganizationsToCrises;" )
    sqlQuery ( c, "drop table if exists CrisesToPeople;" )
    sqlQuery ( c, "drop table if exists OrganizationKind;" )
    sqlQuery ( c, "drop table if exists PersonKind;" )
    sqlQuery ( c, "drop table if exists CrisisKind;" )
    
    sqlQuery ( c, "create table Crises ( crisisID text, name text, crisisKindID text, startDate date, startTime time, endDate date, endTime time, economicImpact text );" )
    sqlQuery ( c, "create table Organizations ( orgID text, name text, orgKindID text, history text, phone bigint, fax bigint, email text, address text, locality text, region text, postalCode text, country text );" )
    sqlQuery ( c, "create table People ( personID text, firstName text, middleName text, lastName text, suffix text, personKindID text );" )
    sqlQuery ( c, "create table CrisisLocations ( crisisID text, locality text, region text, country text );" )
    sqlQuery ( c, "create table PeopleLocations ( personID text, locality text, region text, country text );" )
    sqlQuery ( c, "create table OrganizationLocations ( orgID text, locality text, region text, country text );" )
    sqlQuery ( c, "create table HumanImpact ( crisisID text, type text, number int );" )
    sqlQuery ( c, "create table ResourceNeeded ( crisisID text, resource text );" )
    sqlQuery ( c, "create table WaysToHelp ( crisisID text, helpType text );" )
    sqlQuery ( c, "create table PersonExternalResources ( personID text, type text, url text );" )
    sqlQuery ( c, "create table OrganizationExternalResources ( orgID text, type text, url text );" )
    sqlQuery ( c, "create table CrisisExternalResources ( crisisID text, type text, url text );" )
    sqlQuery ( c, "create table PeopleToOrganizations ( personID text, orgID text );" )
    sqlQuery ( c, "create table OrganizationsToCrises ( orgID text, crisisID text );" )
    sqlQuery ( c, "create table CrisesToPeople ( crisisID text, personID text );" )
    sqlQuery ( c, "create table OrganizationKind ( orgKindID text, name text, description text );" )
    sqlQuery ( c, "create table PersonKind ( personKindID text, name text, description text );" )
    sqlQuery ( c, "create table CrisisKind ( crisisKindID text, name text, description text );" )
    sqlQuery ( c, "show tables;" )

def openTagAtt ( x, attName, attVal ):
    """
    builds a string of an opening xml element with a chosen tag, attribute, and value
    x is the tag
    attName is the attribute name
    attVal is the attribute value
    """
    assert str(type(x)) == "<type 'str'>"
    assert str(type(attName)) == "<type 'str'>"
    assert str(type(attVal)) == "<type 'str'>"
    tag = "<" + str ( x ) + " " + str ( attName ) + "='" + str ( attVal ) +"'>"
    assert str ( type ( tag ) ) == "<type 'str'>"
    return tag

def closeTagAtt ( x, attName, attVal ):
    """
    builds a string of an opening and closing xml element with a chosen tag, attribute, and value
    x is the tag
    attName is the attribute name
    attVal is the attribute value
    """
    assert str(type(x)) == "<type 'str'>"
    assert str(type(attName)) == "<type 'str'>"
    assert str(type(attVal)) == "<type 'str'>"
    tag = "<" + str ( x ) + " " + str ( attName ) + "='" + str ( attVal ) +"'/>"
    assert str ( type ( tag ) ) == "<type 'str'>"
    return tag

def openTag ( x ):
    """
    builds a string of an opening xml element with a chosen tag
    x is the tag
    """
    assert str(type(x)) == "<type 'str'>"
    tag = "<" + str ( x ) + ">"
    assert str ( type ( tag ) ) == "<type 'str'>"
    return tag

def openCloseTag ( x, text ):
    """
    builds a string of an opening and closing xml element with a chosen tag and inner text
    x is the tag
    text is the text
    """
    assert str(type(x)) == "<type 'str'>"
    assert str(type(text)) == "<type 'str'>"
    tag = "<" + str ( x ) + ">" + text + "</" + str ( x ) + ">"
    assert str ( type ( tag ) ) == "<type 'str'>"
    return tag

def closeTag ( x ):
    """
    builds a string of a closing xml element with a chosen tag
    x is the tag
    """
    assert str(type(x)) == "<type 'str'>"
    tag = "</" + str ( x ) + ">"
    assert str ( type ( tag ) ) == "<type 'str'>"
    return tag

def exportCrises ( c ) :
    """
    exports the crises from the mysql database
    c is the mysql database connection
    """
    assert str(type(c)) == "<type '_mysql.connection'>"
    xml = ""
    cr = sqlQuery ( c, "select * from Crises;" )
    for i in cr :
        cL = sqlQuery ( c, "select * from CrisisLocations where crisisID = '" + i [ 0 ] + "';" )
        hI = sqlQuery ( c, "select * from HumanImpact where crisisID = '" + i [ 0 ] + "';" )
        rN = sqlQuery ( c, "select * from ResourceNeeded where crisisID = '" + i [ 0 ] + "';" )
        wTH = sqlQuery ( c, "select * from WaysToHelp where crisisID = '" + i [ 0 ] + "';" )
        cER = sqlQuery ( c, "select * from CrisisExternalResources where crisisID = '" + i [ 0 ] + "';" )
        cTP = sqlQuery ( c, "select * from CrisesToPeople where crisisID = '" + i [ 0 ] + "';" )
        oTC = sqlQuery ( c, "select * from OrganizationsToCrises where crisisID = '" + i [ 0 ] + "';" )
        xml += openTagAtt ( "Crisis", "crisisIdent", i [ 0 ] )
        xml += openCloseTag ( "Name", i [ 1 ] )
        xml += closeTagAtt ( "Kind", "crisisKindIdent", i [ 2 ] )
        for j in cL :
            xml += openTag ( "Location" )
            xml += openCloseTag ( "Locality", j [ 1 ] )
            xml += openCloseTag ( "Region", j [ 2 ] )
            xml += openCloseTag ( "Country", j [ 3 ] )
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
            xml += openCloseTag ( "Type", j [ 1 ] )
            xml += openCloseTag ( "Number", j [ 2 ] )
            xml += closeTag ( "HumanImpact" )
        xml += openCloseTag ( "EconomicImpact", i [ 7 ] )
        for j in rN :
            xml += openCloseTag ( "ResourceNeeded", j [ 1 ] )
        for j in wTH :
            xml += openCloseTag ( "WaysToHelp", j [ 1 ] )
        xml += openTag ( "ExternalResources" )
        for j in cER :
            xml += openCloseTag ( j [ 1 ] , j [ 2 ] )
        xml += closeTag ( "ExternalResources" )
        xml += openTag ( "RelatedPersons" )
        for j in cTP :
            xml += closeTagAtt ( "RelatedPerson" , "personIdent", j [ 1 ] )
        xml += closeTag ( "RelatedPersons" )
        xml += openTag ( "RelatedOrganizations" )
        for j in oTC :
            xml += closeTagAtt ( "RelatedOrganization" , "organizationIdent", j [ 0 ] )
        xml += closeTag ( "RelatedOrganizations" )
        xml += closeTag ( "Crisis" )
    assert str ( type ( xml ) ) == "<type 'str'>"
    return xml

def exportOrgs ( c ) :
    """
    exports the organizations from the mysql database
    c is the mysql database connection
    """
    assert str(type(c)) == "<type '_mysql.connection'>"
    xml = ""
    o = sqlQuery ( c, "select * from Organizations;" )
    for i in o:
        oL = sqlQuery ( c, "select * from OrganizationLocations where orgID = '"+i[0]+"';" )
        oER = sqlQuery ( c, "select * from OrganizationExternalResources where orgID = '"+i[0]+"';" )
        oTC = sqlQuery ( c, "select * from OrganizationsToCrises where orgID = '"+i[0]+"';" )
        pTO = sqlQuery ( c, "select * from PeopleToOrganizations where orgID = '"+i[0]+"';" )
        xml += openTagAtt ( "Organization", "organizationIdent", i[0])
        xml += openCloseTag ( "Name", i[1])
        xml += closeTagAtt ( "Kind", "organizationKindIdent", i[2])
        for j in oL :
            xml += openTag ( "Location" )
            xml += openCloseTag ( "Locality", j [ 1 ] )
            xml += openCloseTag ( "Region", j [ 2 ] )
            xml += openCloseTag ( "Country", j [ 3 ] )
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
            xml += openCloseTag ( j[1], j[2])
        xml += closeTag ("ExternalResources")
        xml += openTag ("RelatedCrises")
        for j in oTC:
            xml += closeTagAtt ("RelatedCrisis", "crisisIdent", j[1])
        xml += closeTag ("RelatedCrises")
        xml += openTag ("RelatedPersons")
        for j in pTO:
            xml += closeTagAtt ("RelatedPerson", "personIdent", j[0])
        xml += closeTag ("RelatedPersons")
        xml += closeTag ("Organization")
    assert str ( type ( xml ) ) == "<type 'str'>"
    return xml

def exportPeople ( c ) :
    """
    exports the people from the mysql database
    c is the mysql database connection
    """
    assert str(type(c)) == "<type '_mysql.connection'>"
    xml = ""
    p = sqlQuery ( c, "select * from People;" )
    for i in p :
        pL = sqlQuery ( c, "select * from PeopleLocations where personID = '" + i [ 0 ] + "';" )
        pER = sqlQuery ( c, "select * from PersonExternalResources where personID = '" + i [ 0 ] + "';" )
        pTO = sqlQuery ( c, "select * from PeopleToOrganizations where personID = '" + i [ 0 ] + "';" )
        cTP = sqlQuery ( c, "select * from CrisesToPeople where personID = '" + i [ 0 ] + "';" )
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
            xml += openCloseTag ( "Locality", j [ 1 ] )
            xml += openCloseTag ( "Region", j [ 2 ] )
            xml += openCloseTag ( "Country", j [ 3 ] )
            xml += closeTag ( "Location" )
        xml += openTag ( "ExternalResources" )
        for j in pER :
            xml += openCloseTag ( j [ 1 ] , j [ 2 ] )
        xml += closeTag ( "ExternalResources" )
        xml += openTag ( "RelatedCrises" )
        for j in cTP :
            xml += closeTagAtt ( "RelatedCrisis" , "crisisIdent", j [ 0 ] )
        xml += closeTag ( "RelatedCrises" )
        xml += openTag ( "RelatedOrganizations" )
        for j in pTO :
            xml += closeTagAtt ( "RelatedOrganization" , "organizationIdent", j [ 1 ] )
        xml += closeTag ( "RelatedOrganizations" )
        xml += closeTag ( "Person" )
    assert str ( type ( xml ) ) == "<type 'str'>"
    return xml

def exportTypes( c ) :
    """
    exports the crisis, organization, and person types from the mysql database
    c is the mysql database connection
    """
    assert str(type(c)) == "<type '_mysql.connection'>"
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
    assert str ( type ( xml ) ) == "<type 'str'>"
    return xml

def importCrisis ( c, crisisInstance ):
    """
    imports an Element of type Crisis into the mysql database
    c is the mysql database connection
    crisisInstance is the element
    """    
    assert str(type(c)) == "<type '_mysql.connection'>"
    assert str(type(crisisInstance)) == "<type 'instance'>"
    crisisID = crisisInstance.attrib["crisisIdent"]
    
    #Gets location sub elements in list. Inserts into CrisisLocation table by indexing list
    allLocations = crisisInstance.findall("Location")
    if len(allLocations) != 0:
        for instance in allLocations:
            if len ( instance ) == 2 :
                sqlQuery ( c, "insert into CrisisLocations values ( '"+crisisID+"', '"+instance[0].text+"', 'Null', '"+instance[1].text+"');")
            else :
                sqlQuery ( c, "insert into CrisisLocations values ( '"+crisisID+"', '"+instance[0].text+"', '"+instance[1].text+"', '"+instance[2].text+"');")

    #Gets list of all resources needed. Iterates through lists and inserts into ResourceNeeded table
    resourcesNeeded = crisisInstance.findall("ResourceNeeded")

    if len(resourcesNeeded) != 0:
        for instance in resourcesNeeded:
            sqlQuery ( c, "insert into ResourceNeeded values ( '"+crisisID+"', '"+instance.text+"');")
    
    #Gets all URL's in a list. Indexes list, splices tag to get type, inserts data into table
    externalResources = crisisInstance.find("ExternalResources")
    
#Get all resources. Checks for Citation because it's the only one not ending in 'URL'. Get index of URL for others to splice off. Add to table
    if len(externalResources) != 0:
        for instance in externalResources:
            sqlQuery ( c, "insert into CrisisExternalResources values ( '"+crisisID+"', '"+instance.tag+"', '"+instance.text+"');")
                

    #Gets list of all RelatedPeople and inserts into CrisesToPeople table
    relatedPeople = crisisInstance.findall(".//" + "RelatedPerson")

    if len(relatedPeople) != 0:
        for instance in relatedPeople:
            sqlQuery ( c, "insert into CrisesToPeople values ( '"+crisisID+"', '"+instance.attrib["personIdent"]+"');")

     #Gets list of all RelatedOrganizations and inserts into OrganizationsToCrises table
    relatedOrgs = crisisInstance.findall(".//" + "RelatedOrganization")

    if len(relatedOrgs) != 0:
        for instance in relatedOrgs:
            sqlQuery ( c, "insert into OrganizationsToCrises values ( '"+instance.attrib["organizationIdent"]+"', '"+crisisID+"');")

    #Gets all tags titled WaysToHelp, and inserts into corresponding table by indexing the list they're stored in
    waysToHelp = crisisInstance.findall("WaysToHelp")
    
    if len(waysToHelp) != 0:
        for instance in waysToHelp:
            sqlQuery ( c, "insert into WaysToHelp values ( '"+crisisID+"', '"+instance.text+"');")

    #Gets list of HumanImpact elements. Iterates through list and inserts into HumanImpact table
    humanImpact = crisisInstance.findall("HumanImpact")

    if len(humanImpact) !=0:
        for instance in humanImpact:
            sqlQuery ( c, "insert into HumanImpact values ( '"+crisisID+"', '"+instance[0].text+"', '"+instance[1].text+"');")

    #Finds values of remaining elements and inserts into Crises table
    name = crisisInstance.find("Name").text
    kind = crisisInstance.find("Kind").attrib["crisisKindIdent"]
    startDateTime = crisisInstance.find("StartDateTime")
    startDate = startDateTime[0].text
    if len(startDateTime) > 1:
        startTime = startDateTime[1].text
    else:
        startTime = '00:00:00'
    endDateTime = crisisInstance.find("EndDateTime")
    if endDateTime != None :
        endDate = endDateTime[0].text
        if len(endDateTime) > 1:
            endTime = endDateTime[1].text
        else:
            endTime = '00:00:00'
    else :
        endDate = startDate
        endTime = '23:59:59'
    econImpact = crisisInstance.find("EconomicImpact").text

    sqlQuery ( c, "insert into Crises values ( '"+crisisID+"', '"+name+"', '"+kind+"', '"+startDate+"', '"+startTime+"', '"+endDate+"', '"+endTime+"', '"+econImpact+"');")

def importOrg ( c, orgInstance ):
    """
    imports an Element of type Organization into the mysql database
    c is the mysql database connection
    orgInstance is the element
    """
    assert str(type(c)) == "<type '_mysql.connection'>"
    assert str(type(orgInstance)) == "<type 'instance'>"
    orgID = orgInstance.attrib["organizationIdent"]

    #Gets location sub elements in list. Inserts into CrisisLocation table by indexing list
    allLocations = orgInstance.findall("Location")        
    if len(allLocations) != 0:
        for instance in allLocations:
            sqlQuery ( c, "insert into OrganizationLocations values ( '"+orgID+"', '"+instance[0].text+"', '"+instance[1].text+"', '"+instance[2].text+"');")

    #Get all resources. Checks for Citation because it's the only one not ending in 'URL'. Get index of URL for others to splice off. Add to table
    externalResources = orgInstance.find("ExternalResources")
    if len(externalResources) != 0:
        for instance in externalResources:
            sqlQuery ( c, "insert into OrganizationExternalResources values ( '"+orgID+"', '"+instance.tag+"', '"+instance.text+"');")

    #Get all values for Organizations table and insert to DB
    postalAddress = orgInstance.find(".//" + "PostalAddress")
    name = orgInstance.find("Name").text
    kind = orgInstance.find("Kind").attrib["organizationKindIdent"]
    history = orgInstance.find("History").text
    phone = str(orgInstance.find(".//" + "Telephone").text)
    fax = str(orgInstance.find(".//" + "Fax").text)
    email = orgInstance.find(".//" + "Email").text
    address = postalAddress[0].text
    locality = postalAddress[1].text
    region = postalAddress[2].text
    postalCode = postalAddress[3].text
    country = postalAddress[4].text
    sqlQuery (c , "insert into Organizations values ( '"+orgID+"', '"+name+"', '"+kind+"', '"+history+"', "+phone+", "+fax+", '"+email+"', '"+address+"', '"+locality+"', '"+region+"', '"+postalCode+"', '"+country+"');")

def importPerson ( c, peopleInstance ):
    """
    imports an Element of type Person into the mysql database
    c is the mysql database connection
    personInstance is the element
    """
    assert str(type(c)) == "<type '_mysql.connection'>"
    assert str(type(peopleInstance)) == "<type 'instance'>"
    personID = peopleInstance.attrib["personIdent"]
        
    #Gets location sub elements in list. Inserts into PeopleLocation table by indexing list
    locationElements = list(peopleInstance.findall("Location"))
    for instance in locationElements:
        sqlQuery ( c, "insert into PeopleLocations values ( '"+personID+"', '"+instance[0].text+"', '"+instance[1].text+"', '"+instance[2].text+"');")
    
    #Gets list of all RelatedOrganizations and inserts into PeopleToOrganizations table
    relatedOrgs = peopleInstance.find("RelatedOrganizations")
    if relatedOrgs != None :
        for instance in relatedOrgs:
            sqlQuery ( c, "insert into PeopleToOrganizations values ( '"+personID+"', '"+instance.attrib["organizationIdent"]+"');")

    #Gets all URL's in a list. Indexes list, splices tag to get type, inserts data into table
    externalResources = peopleInstance.find("ExternalResources")
    
    #Get all resources. Checks for Citation because it's the only one not ending in 'URL'. Get index of URL for others to splice off. Add to table
    for instance in externalResources:
        sqlQuery ( c, "insert into PersonExternalResources values ( '"+personID+"', '"+instance.tag+"', '"+instance.text+"');")
    
    #Finds values of remaining elements and inserts into People table
    firstName = peopleInstance.find(".//" + "FirstName").text
    middleName = peopleInstance.findtext(".//" + "MiddleName", "")
    lastName = peopleInstance.find(".//" + "LastName").text
    suffix = peopleInstance.findtext("Suffix", "")
    kind = peopleInstance.find("Kind").attrib["personKindIdent"]
    sqlQuery ( c, "insert into People values ( '"+personID+"', '"+firstName+"', '"+middleName+"', '"+lastName+"', '"+suffix+"', '"+kind+"');")

def importCrisisKind ( c, crisisKindInstance ):
    """
    imports an Element of type CrisisKind into the mysql database
    c is the mysql database connection
    crisisKindInstance is the element
    """
    assert str(type(c)) == "<type '_mysql.connection'>"
    assert str(type(crisisKindInstance)) == "<type 'instance'>"
    crisisKindID = crisisKindInstance.attrib["crisisKindIdent"]
    name = crisisKindInstance.find("Name").text
    description = crisisKindInstance.find("Description").text
    sqlQuery ( c, "insert into CrisisKind values ( '"+crisisKindID+"', '"+name+"', '"+description+"');")

def importOrgKind ( c, orgKindInstance ) :
    """
    imports an Element of type OrganizationKing into the mysql database
    c is the mysql database connection
    orgKindInstance is the element
    """
    assert str(type(c)) == "<type '_mysql.connection'>"
    assert str(type(orgKindInstance)) == "<type 'instance'>"
    orgKindID = orgKindInstance.attrib["organizationKindIdent"]
    name = orgKindInstance.find("Name").text
    description = orgKindInstance.find("Description").text  
    sqlQuery ( c, "insert into OrganizationKind values ( '"+orgKindID+"', '"+name+"', '"+description+"');")

def importPersonKind ( c, personKindInstance ) :
    """
    assert str(type(c)) == "<type '_mysql.connection'>"
    imports an Element of type PersonKind into the mysql database
    c is the mysql database connection
    personKindInstance is the element
    """
    assert str(type(c)) == "<type '_mysql.connection'>"
    assert str(type(personKindInstance)) == "<type 'instance'>"
    personKindID = personKindInstance.attrib["personKindIdent"]
    name = personKindInstance.find("Name").text
    description = personKindInstance.find("Description").text  
    sqlQuery ( c, "insert into PersonKind values ( '"+personKindID+"', '"+name+"', '"+description+"');")

def importDB ( c, xml ) :
    """
    imports an ElementTree into the mysql database
    c is the mysql database connection
    xml is the ElementTree
    """
    assert str(type(c)) == "<type '_mysql.connection'>"
    assert str ( type ( xml ) ) == "<type 'instance'>"
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
    assert str(type(c)) == "<type '_mysql.connection'>"
    xml = openTag ( "WorldCrises" )
    xml += exportCrises ( c )
    xml += exportOrgs ( c )
    xml += exportPeople ( c )
    xml += exportTypes ( c )
    xml += closeTag ( "WorldCrises" )
    assert str ( type ( xml ) ) == "<type 'str'>"
    return xml
    
def start ( r, w, args ):
    """
    imports an xml document into an ElementTree, imports that ElementTree into a mysql database,
    then outputs the mysql database to a valid xml document, which is then written to the output file
    r is the reader
    w is the writer
    args are the commandline arguments
    """
    sqlLoginInfo = parseArgs ( args )
    sql = sqlLogin ( sqlLoginInfo )
    xml = importXml ( r )
    createTables ( sql )
    importDB ( sql, xml )
    exportXML = exportDB ( sql )
    sql.close ()
    exportXml ( w, exportXML )