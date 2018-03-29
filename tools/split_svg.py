#!/usr/bin/env python3

import os;
import argparse;
from xml.dom.minidom import parse, parseString
from xml.dom import Node

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--source", required=True, help="input svg filename")
parser.add_argument("-o", "--outdir", required=True, help="output directory")
parser.add_argument("-f", "--ffscript", required=True, help="ff script to generate")
args = parser.parse_args()

output_basename = os.path.splitext(os.path.basename(args.source))[0]
dom = parse(args.source)

# get info
fontname = ""
familyname = ""
humanname = ""
weight = ""
version = "1.0"
copyright = ""

infodata = dom.getElementsByTagName("cc:Work")[0]
for n in infodata.childNodes:
    if n.nodeType == Node.ELEMENT_NODE:
        if n.tagName == "dc:title":
            familyname = getText(n.childNodes)
        elif n.tagName == "dc:relation":
            weight = getText(n.childNodes)
        elif n.tagName == "cc:license":
            copyright = n.getAttribute("rdf:resource")

fontname = (familyname + weight).replace(" ", "")
humanname = familyname + " " + weight

# collect up all the characters
chars = []
for node in dom.documentElement.childNodes:
    if node.nodeType == Node.ELEMENT_NODE and node.tagName == "path":
        chars.append(node.getAttribute("id"))


ff_script = open(args.ffscript, "w")
ff_script.write("#!/usr/bin/env fontforge\n")
ff_script.write("New()\n")
ff_script.write("SetFontNames(\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")\n" % (fontname, familyname, humanname, weight, copyright, version))
ff_script.write("ScaleToEm(1024)\n")
ff_script.write("Reencode(\"UnicodeFull\")\n")
ff_script.write("Select(0u0020)\n")
ff_script.write("SetWidth(600)\n")

# now build a bunch of svg files with all the attributes of the
# original, but excluding all the characters we don't care about
for c in chars:
    # reparsing the XML every iteration is dumb but easy
    dom = parse(args.source)
    for node in dom.documentElement.childNodes:
        if node.nodeType == Node.ELEMENT_NODE and node.tagName == "path":
            if node.getAttribute("id") != c:
                dom.documentElement.removeChild(node)

    output_svg = args.outdir + "/" + output_basename + "-" + c + ".svg"
    file_handle = open(output_svg, "w")
    dom.writexml(file_handle)
    file_handle.close()

    ff_script.write("Select(" + c + ")\n");
    ff_script.write("Import(\"" + output_svg + "\")\n")
    ff_script.write("AutoWidth(200)\n");

ff_script.write("Generate($1)\n")

