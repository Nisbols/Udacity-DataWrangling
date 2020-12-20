import xml.etree.ElementTree as ET
import pprint
from collections import defaultdict
import re
import sys
import codecs
import json
import string
import pprint

tree = ET.parse('marionCounty.xml')
root = tree.getroot()
list1 = []   
dict1 = {}
for k in root.iter():
    name = k.tag
    list1.append(name)

for i in list1:
    if i in dict1:
        dict1[i] += 1
    else:
        dict1[i] = 1
    
dict1



lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def key_type(element, keys):
    if element.tag == "tag":
        key = element.attrib['k']
        if lower.match(key):
            keys["lower"] = keys["lower"] + 1
        elif lower_colon.match(key):
            keys["lower_colon"] = keys["lower_colon"] + 1
        elif problemchars.match(key):
            keys["problemchars"] = keys["problemchars"] + 1
        else:
            keys["other"] = keys["other"] + 1

    return keys


def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys


def run(filename):
    keys = process_map(filename)
    pprint.pprint(keys)
    
run("marionCounty.xml")