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
    text = re.sub ( pattern, "", rawText )
    reparsed = MD.parseString ( text )
    w.write ( reparsed.toprettyxml ( indent = "\t", encoding = "UTF-8" ) )

def createTables ( c ) :
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
    
    sqlQuery ( c, "create table Crises ( crisisID text, name text, crisisKindID text, startDate date, startTime time, economicImpact text );" )
    sqlQuery ( c, "create table Organizations ( orgID text, name text, orgKindID text, history text, phone bigint, fax bigint, email text, address text, postalCode text );" )
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

def addTestData ( c ) :
    """
    sqlQuery ( c, "insert into Organizations values ( 'ORC', 'Red Crescent', 'OTPU', 'The Red Cross idea was born in 1859, when Henry Dunant, a young Swiss man, came upon the scene of a bloody battle in Solferino, Italy, between the armies of imperial Austria and the Franco-Sardinian alliance. Some 40,000 men lay dead or dying on the battlefield and the wounded were lacking medical attention.', 12123380161, 12123380161, 'admin@redcrescentpenang.org.my', 'P.O. Box 303', '1236' );" )
    sqlQuery ( c, "insert into OrganizationLocations values ( 'ORC', 'Geneva', 'Western', 'Switzerland' );" )
    sqlQuery ( c, "insert into OrganizationExternalResources values ( 'ORC', 'Citation', 'IFRC, IranicaOnline, Wikipedia' );" )
    sqlQuery ( c, "insert into OrganizationExternalResources values ( 'ORC', 'ExternalLinkURL', 'http://www.ifrc.org/en/news-and-media/news-stories/international/red-cross-continues-response-to-widening-sars-threat/' );" )
    sqlQuery ( c, "insert into OrganizationExternalResources values ( 'ORC', 'ExternalLinkURL', 'http://www.iranicaonline.org/articles/bam-earthquake-2003' );" )
    sqlQuery ( c, "insert into OrganizationsToCrises values ( 'ORC', 'CIE' );" )
    sqlQuery ( c, "insert into OrganizationsToCrises values ( 'ORC', 'CSO' );" )

    sqlQuery ( c, "insert into Crises values ( 'CCD', 'Chernobyl Disaster', 'Natural', '1986-04-26', '01:23:00', '588M USD' );" )
    sqlQuery ( c, "insert into CrisisLocations values ( 'CCD', 'Pripyat', 'Kiev', 'Ukraine' );" )
    sqlQuery ( c, "insert into HumanImpact values ( 'CCD', 'Casualties', 31 );" )
    sqlQuery ( c, "insert into HumanImpact values ( 'CCD', 'Affected', 500000 );" )
    sqlQuery ( c, "insert into ResourceNeeded values ( 'CCD', 'Labor' );" )
    sqlQuery ( c, "insert into ResourceNeeded values ( 'CCD', 'Transportation' );" )
    sqlQuery ( c, "insert into ResourceNeeded values ( 'CCD', 'Money' );" )
    sqlQuery ( c, "insert into ResourceNeeded values ( 'CCD', 'Shelter' );" )
    sqlQuery ( c, "insert into WaysToHelp values ( 'CCD', 'Providing room and board for refugees' );" )
    sqlQuery ( c, "insert into WaysToHelp values ( 'CCD', 'Medical care for those affected' );" )
    sqlQuery ( c, "insert into CrisisExternalResources values ( 'CCD', 'ImageURL', 'http://i.telegraph.co.uk/multimedia/archive/01755/chernobyl_1755717c.jpg' );" )
    sqlQuery ( c, "insert into CrisisExternalResources values ( 'CCD', 'ExternalLinkURL', 'http://articles.latimes.com/1986-05-04/news/mn-3685_1_soviet-union' );" )
    sqlQuery ( c, "insert into CrisisExternalResources values ( 'CCD', 'ExternalLinkURL', 'http://www.iaea.org/newscenter/focus/chernobyl/' );" )
    sqlQuery ( c, "insert into CrisesToPeople values ( 'CCD', 'PRR' );" )
    sqlQuery ( c, "insert into OrganizationsToCrises values ( 'OIAEA', 'CCD' );" )
    sqlQuery ( c, "insert into OrganizationsToCrises values ( 'OUN', 'CCD' );" )
    
    sqlQuery ( c, "insert into People values ( 'PKA', 'Kofi', 'Atta', 'Annan', '', 'PTHO' );" )
    sqlQuery ( c, "insert into PeopleLocations values ( 'PKA', 'Kumasi', 'Ashanti', 'Ghana' );" )
    sqlQuery ( c, "insert into PeopleToOrganizations values ( 'PKA', 'OUN' );" )
    
    sqlQuery ( c, "insert into OrganizationKind values ( 'OTGO', 'Governmental Organization', 'Administrative unit of the government designed to improve a specific area.' );" )
    sqlQuery ( c, "insert into PersonKind values ( 'PTVI', 'Victim', 'A person harmed, injured, or killed as a result of a crime, accident, or other event or action.' );" )
    sqlQuery ( c, "insert into CrisisKind values ( 'Natural', 'Natural', 'A natural disaster that was not brought on by humankind: earthquake, tsunami, flooding, etc.' );" )
    """

def openTagAtt ( x, attName, attVal ):
    tag = "<" + str ( x ) + " " + str ( attName ) + "='" + str ( attVal ) +"'>"
    return tag

def openTag ( x ):
    tag = "<" + str ( x ) + ">"
    return tag

def openCloseTag ( x, text ):
    tag = "<" + str ( x ) + ">" + text + "</" + str ( x ) + ">"
    return tag

def closeTag ( x ):
    tag = "</" + str ( x ) + ">"
    return tag

def exportCrises ( c ) :
    xml = ""
    cr = sqlQuery ( c, "select * from Crises;" )
    for i in cr :
        cL = sqlQuery ( c, "select * from CrisisLocations where crisisId = '" + i [ 0 ] + "';" )
        hI = sqlQuery ( c, "select * from HumanImpact where crisisId = '" + i [ 0 ] + "';" )
        rN = sqlQuery ( c, "select * from ResourceNeeded where crisisId = '" + i [ 0 ] + "';" )
        wTH = sqlQuery ( c, "select * from WaysToHelp where crisisId = '" + i [ 0 ] + "';" )
        cER = sqlQuery ( c, "select * from CrisisExternalResources where crisisId = '" + i [ 0 ] + "';" )
        cTP = sqlQuery ( c, "select * from CrisesToPeople where crisisId = '" + i [ 0 ] + "';" )
        oTC = sqlQuery ( c, "select * from OrganizationsToCrises where crisisId = '" + i [ 0 ] + "';" )
        xml += openTagAtt ( "Crisis", "crisisIdent", i [ 0 ] )
        xml += openCloseTag ( "Name", i [ 1 ] )
        xml += openTagAtt ( "Kind", "crisisKindIdent", i [ 2 ] )
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
        for j in hI :
            xml += openTag ( "HumanImpact" )
            xml += openCloseTag ( "Type", j [ 1 ] )
            xml += openCloseTag ( "Number", j [ 2 ] )
            xml += closeTag ( "HumanImpact" )
        xml += openCloseTag ( "EconomicImpact", i [ 5 ] )
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
            xml += openTagAtt ( "RelatedPerson" , "personIdent", j [ 1 ] )
        xml += closeTag ( "RelatedPersons" )
        xml += openTag ( "RelatedOrganizations" )
        for j in cTP :
            xml += openTagAtt ( "RelatedOrganization" , "organizationIdent", j [ 1 ] )
        xml += closeTag ( "RelatedOrganizations" )
        xml += closeTag ( "Crisis" )
    return xml

def exportOrgs ( c ) :
    xml = ""
    o = sqlQuery ( c, "select * from Organizations;" )
    oL = sqlQuery ( c, "select * from OrganizationLocations;" )
    oER = sqlQuery ( c, "select * from OrganizationExternalResources;" )
    oTC = sqlQuery ( c, "select * from OrganizationsToCrises;" )
    organizations = sqlQuery ( c, "select * from Organizations;" )
    return xml

def exportPeople ( c ) :
    xml = ""
    p = sqlQuery ( c, "select * from People;" )
    pL = sqlQuery ( c, "select * from PeopleLocations;" )
    pTO = sqlQuery ( c, "select * from PeopleToOrganizations;" )
    return xml

def exportTypes( c ) :
    xml = ""
    cT = sqlQuery ( c, "select * from CrisisKind;" )
    oT = sqlQuery ( c, "select * from OrganizationKind;" )
    pT = sqlQuery ( c, "select * from PersonKind;" )
    return xml

def importCrisis ( c, crisisInstance ):
    
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
            if instance.tag == "Citation":
                sqlQuery ( c, "insert into CrisisExternalResources values ( '"+crisisID+"', '"+'Citation'+"', '"+instance.text+"');")
            else:
                splice = instance.tag.find('URL')
                type = instance.tag[:splice]
                sqlQuery ( c, "insert into CrisisExternalResources values ( '"+crisisID+"', '"+type+"', '"+instance.text+"');")
                

    #Gets list of all RelatedPeople and inserts into CrisesToPeople table
    relatedPeople = crisisInstance.findall("RelatedPerson")

    if len(relatedPeople) != 0:
        for instance in relatedPeople:
            sqlQuery ( c, "insert into CrisesToPeople values ( '"+crisisID+"', '"+instance.attrib["personIdent"]+"');")

     #Gets list of all RelatedOrganizations and inserts into OrganizationsToCrises table
    relatedOrgs = crisisInstance.findall("RelatedOrganization")

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
    dateTime = crisisInstance.find("StartDateTime")
    startDate = dateTime[0].text
    if len(dateTime) > 1:
        startTime = dateTime[1].text
    else:
        startTime = '00:00:00'
    econImpact = crisisInstance.find("EconomicImpact").text

    sqlQuery ( c, "insert into Crises values ( '"+crisisID+"', '"+name+"', '"+kind+"', '"+startDate+"', '"+startTime+"', '"+econImpact+"');")

def importOrg ( c, orgInstance ):
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
            if instance.tag == "Citation":
                sqlQuery ( c, "insert into CrisisExternalResources values ( '"+orgID+"', '"+'Citation'+"', '"+instance.text+"');")
            else:
                splice = instance.tag.find('URL')
                type = instance.tag[:splice]
                sqlQuery ( c, "insert into CrisisExternalResources values ( '"+orgID+"', '"+type+"', '"+instance.text+"');")

    #Get all values for Organizations table and insert to DB
    name = orgInstance.find("Name").text
    kind = orgInstance.find("Kind").attrib["organizationKindIdent"]
    history = orgInstance.find("History").text
    phone = str(orgInstance.find(".//" + "Telephone").text)
    fax = str(orgInstance.find(".//" + "Fax").text)
    email = orgInstance.find(".//" + "Email").text
    address = orgInstance.find(".//" + "StreetAddress").text
    postalCode = orgInstance.find(".//" + "PostalCode").text
    sqlQuery (c , "insert into Organizations values ( '"+orgID+"', '"+name+"', '"+kind+"', '"+history+"', "+phone+", "+fax+", '"+email+"', '"+address+"', '"+postalCode+"');")

def importPerson ( c, peopleInstance ):
    personID = peopleInstance.attrib["personIdent"]
        
    #Gets location sub elements in list. Inserts into PeopleLocation table by indexing list
    locationElements = list(peopleInstance.findall("Location"))
    for instance in locationElements:
        sqlQuery ( c, "insert into PeopleLocations values ( '"+personID+"', '"+instance[0].text+"', '"+instance[1].text+"', '"+instance[2].text+"');")
    
    #Gets list of all RelatedOrganizations and inserts into PeopleToOrganizations table
    relatedOrgs = peopleInstance.findall("RelatedOrganizations")    
    for instance in relatedOrgs:
        sqlQuery ( c, "insert into PeopleToOrganizations values ( '"+personID+"', '"+instance.attrib["organizationIdent"]+"');")

    #Gets all URL's in a list. Indexes list, splices tag to get type, inserts data into table
    externalResources = peopleInstance.find("ExternalResources")
    
    #Get all resources. Checks for Citation because it's the only one not ending in 'URL'. Get index of URL for others to splice off. Add to table
    for instance in externalResources:
        if instance.tag == "Citation":
            sqlQuery ( c, "insert into PersonExternalResources values ( '"+personID+"', 'Citation', '"+instance.text+"');")
        else:
            splice = instance.tag.find('URL')
            type = instance.tag[:splice]
            sqlQuery ( c, "insert into PersonExternalResources values ( '"+personID+"', '"+type+"', '"+instance.text+"');")
    
    #Finds values of remaining elements and inserts into People table
    firstName = peopleInstance.find(".//" + "FirstName").text
    middleName = peopleInstance.findtext(".//" + "MiddleName", "Null")
    lastName = peopleInstance.find(".//" + "LastName").text
    suffix = peopleInstance.findtext("Suffix", "Null")
    kind = peopleInstance.find("Kind").attrib["personKindIdent"]
    sqlQuery ( c, "insert into People values ( '"+personID+"', '"+firstName+"', '"+middleName+"', '"+lastName+"', '"+suffix+"', '"+kind+"');")

def importCrisisKind ( c, crisisKindInstance ):    
    crisisKindID = crisisKindInstance.attrib["crisisKindIdent"]
    name = crisisKindInstance.find("Name").text
    description = crisisKindInstance.find("Description").text
    sqlQuery ( c, "insert into CrisisKind values ( '"+crisisKindID+"', '"+name+"', '"+description+"');")

def importOrgKind ( c, orgKindInstance ):  
    orgKindID = orgKindInstance.attrib["organizationKindIdent"]
    name = orgKindInstance.find("Name").text
    description = orgKindInstance.find("Description").text  
    sqlQuery ( c, "insert into OrganizationKind values ( '"+orgKindID+"', '"+name+"', '"+description+"');")

def importPersonKind ( c, personKindInstance ):  
    personKindID = personKindInstance.attrib["personKindIdent"]
    name = personKindInstance.find("Name").text
    description = personKindInstance.find("Description").text  
    sqlQuery ( c, "insert into PersonKind values ( '"+personKindID+"', '"+name+"', '"+description+"');")

def importDB ( c, xml ) :
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
    xml = openTag ( "WorldCrises" )
    xml += exportCrises ( c )
    xml += exportOrgs ( c )
    xml += exportPeople ( c )
    xml += exportTypes ( c )
    xml += closeTag ( "WorldCrises" )
    return xml
    
def start ( r, w, args ):
    """
    imports an xml document into an ElementTree, then outputs the ElementTree back to a file
    r is the reader
    w is the writer
    """
    sqlLoginInfo = parseArgs ( args )
    sql = sqlLogin ( sqlLoginInfo )
    xml = importXml ( r )
    createTables ( sql )
    #addTestData ( sql )
    importDB ( sql, xml )
    exportXML = exportDB ( sql )
    sql.close ()
    exportXml ( w, xml )