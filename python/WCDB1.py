import xml.etree.ElementTree as ET
import xml.dom.minidom as MD
import re

def importXml ( r ):
    """
    reads in xml from stdin (a file) and parses it into an ElementTree
    r is the reader
    returns an ElementTree
    """
    rawText = r.read ()
    rawText = rawText.strip ()
    xml = ET.fromstring ( rawText )
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
    
def start ( r, w ):
    """
    imports an xml document into an ElementTree, then outputs the ElementTree back to a file
    r is the reader
    w is the writer
    """
    xml = importXml ( r )
    exportXml ( w, xml )