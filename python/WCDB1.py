import xml.etree.ElementTree as ET
import xml.dom.minidom as MD

def importXml ( r ):
    rawText = r.read ()
    xml = ET.fromstring ( rawText )
    return xml

def exportXml ( w, xml ):
    text = ET.tostring ( xml )
    text = text.strip ( "\t\n\r" )
    reparsed = MD.parseString ( text )
    w.write ( reparsed.toprettyxml ( indent = "    " ) )
    
def start ( r, w ):
    xml = importXml ( r )
    exportXml ( w, xml )