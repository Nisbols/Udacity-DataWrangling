import xml.etree.ElementTree as ET
import pprint
from collections import defaultdict
import re
import sys
import codecs
import json
import string

# Variable for the map data
MAP = 'marionCounty.xml'

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons"]
# Mapping of the abbervations
mapping = { "St ": "Street ",
            "St. ": "Street",
            "Ave. ": "Avenue",
            "Ave ": "Avenue ",
            "Rd. ": "Road",
            "HWY ": "Highway ",
            "Hwy ": "Highway ",
            "Rd ": "Road ",
            "S. ": "South ",
            "N. ": "North ",
            "E. ": "East ",
            "W. ": "West ",
            "US ": "US ",
            "Us ": "US ",
            "CR " : "County Road ",
            "NE ": "Northeast ",
            "NW ": "Northwest ",
            "SE ": "Southeast ",
            "SW ": "Southwest "
            }

# checks the street name and updates it 
def audit_street(street):
    street_names = street.split()
    for i,name in enumerate(street_names):
        if name in mapping.keys():
            street_names[i] = mapping[name]
    street = ' '.join(street_names)
    return street


def audit(element):
    
    '''call certain function defined above to audit the tag value'''
    if element.tag == 'way' or element.tag == 'node':
        for tag in element.iter('tag'):
            tag_key = tag.attrib['k']
            tag_value = tag.attrib['v']
            if tag_key == 'addr:street':
                tag.attrib['v'] = audit_street(tag_value)
    return element


# Updating the names to keep them using the same standard
def update_name(name, mapping):    
    for key in mapping:
        if key in name:
            name = string.replace(name,key,mapping[key])
    return name

def run(osm_file):
    st_types = audit(osm_file)
    pprint.pprint(dict(st_types))

    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name
            