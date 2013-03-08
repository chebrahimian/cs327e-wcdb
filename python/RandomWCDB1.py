import sys
import random

o = sys.stdout

maxLevel = 5
maxChildren = 5
maxAttributes = 4

def openTag ( x, cur, maxA ):
    tabs = ""
    for i in range ( cur ):
        tabs += "\t"
    tag = tabs + "<" + str ( x )
    attributes = addRandomAttributes ( maxA )
    tag += attributes + ">\n"
    return tag

def closeTag ( x, cur ):
    tabs = ""
    for i in range ( cur ):
        tabs += "\t"
    tag = tabs + "</" + str ( x ) + ">\n"
    return tag

def randChar ( a, b ):
    return chr ( random.randint ( ord ( a ), ord ( b ) ) )

def addRandomAttributes ( maxA ):
    xml = ""
    atts = []
    numA = random.randint ( 0, maxA )
    for i in range ( numA ):
        attName = randChar ( "m", "z" )
        while attName in atts:
            attName = randChar ( "m", "z" )
        atts.append ( attName )
        attVal = randChar ( "1", "9" )
        xml += " " + attName + "=\"" + attVal + "\""
    return xml

def generate ( level, maxL, maxC, maxA, rootTag ):

    if ( level == maxL ):
        return ""
    xml = ""
    cTags = [ rootTag ]
    newL = level + 1
    numC = random.randint ( 0, maxC )
    for i in range ( numC ):
        tag = randChar ( "a", "g" )
        while tag in cTags:
            tag = randChar ( "a", "g" )
        cTags.append ( tag )
        xml += openTag ( tag, newL, maxA )
        newXml = generate ( newL, maxL, maxC, maxA, tag )
        if newXml == "":
            xml = xml.rstrip ( "\n" )
            close = closeTag ( tag, newL )
            xml += close.lstrip ( "\t" )
        else:
            xml += newXml
            xml += closeTag ( tag, newL )
    return xml

root = randChar ( "a", "g" )
rootO = openTag ( root, 0, 0 )
rootC = closeTag ( root, 0 )
xml = generate ( 0, maxLevel, maxChildren, maxAttributes, root )
o.write ( rootO + xml + rootC )