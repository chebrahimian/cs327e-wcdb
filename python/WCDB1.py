import xml.etree.ElementTree as ET
import xml.dom.minidom as MD
import re

def importXml ( r ):
    rawText = r.read ()
    xml = ET.fromstring ( rawText )
    return xml

def exportXml ( w, xml ):
    rawText = ET.tostring ( xml )
    pattern = re.compile (r'[^\S ]+')
    text = re.sub ( pattern, '', rawText )
    reparsed = MD.parseString ( text )
    w.write ( reparsed.toprettyxml ( indent = "\t" ) )
    
def start ( r, w ):
    xml = importXml ( r )
    exportXml ( w, xml )