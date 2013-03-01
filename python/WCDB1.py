import xml.etree.ElementTree as ET
import xml.dom.minidom as MD
import sys

def importXml ( r ):
    text = r.read ()
    xml = ET.fromstring ( text )
    return xml

def exportXml ( w, xml ):
    text = ET.tostring ( xml )
    reparsed = MD.parseString ( text )
    w.write ( reparsed.toprettyxml ( indent = "    " ) )
    
def start ( r, w ):
    xml = importXml ( r )
    exportXml ( w, xml )

start ( sys.stdin, sys.stdout )