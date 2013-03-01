import xml.etree.ElementTree as ET
import xml.dom.minidom as MD
import re

def importXml ( r ):
    rawText = r.read ()
    xml = ET.fromstring ( rawText )
    return xml

def exportXml ( w, xml ):
    text = ET.tostring ( xml )
    pattern = re.compile(r'\s+')
    text = re.sub(pattern, '', text) 
    reparsed = MD.parseString ( text )
    w.write ( reparsed.toprettyxml ( indent = "    " ) )
    
def start ( r, w ):
    xml = importXml ( r )
    exportXml ( w, xml )