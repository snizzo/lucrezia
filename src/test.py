#standard python
from xml.dom import minidom
from xml.dom import Node

xmldoc = minidom.parse("res/Mappe/bagno.map")

data = xmldoc.getElementsByTagName('data')

for d in data:
    print('tilesize' in d.attributes)
    print(d.attributes['tilesize'].value)

