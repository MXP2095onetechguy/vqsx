#!/usr/bin/env python3

import argparse, sys, glob, os, datetime
import xml.etree.ElementTree as ET
import json

XML = "XML"
PLAINTEXT = "txt"
JSON = "JSON"

CHOICES = [XML, PLAINTEXT, JSON]

if __name__ != "__main__":
    print(".")
    print("Run this as main, not as a module.")
    sys.exit(1)

# Setup argument parser
parser = argparse.ArgumentParser(
                    description="Compiles markdown files into XML, plaintext, JSON and etc..."
                        )

parser.add_argument("-V", "--verbose",
                    dest="verbose",
                    help="Make the compiler verbose in its output.",
                    action="store_true")

parser.add_argument("-o", "--output", 
                    dest="output",
                    help="Where to output the generated compiled file.",
                    type=str,
                    default="a.tout")
parser.add_argument("-t", "--type",
                    dest="outtype",
                    help="Choose the type of output",
                    choices=CHOICES,
                    default=XML)

parser.add_argument("-r", "--recursive",
                    dest="recursive",
                    help="Recursively traverse the directory for the compiled file.",
                    type=bool,
                    default=True)
parser.add_argument("-i", "--include-hidden",
                    dest="includehidden",
                    help="Include hidden?",
                    action="store_true")

parser.add_argument("where",
                    help="Which directory to traverse?",
                    type=str)
args = parser.parse_args(sys.argv[1:])



def pack_packer(files : list[str]) -> dict:
    # Create a dict for txt
    packs = {}

    # Loop over the files and pack to the dict
    for file in files:
        bfile = os.path.basename(file)
        with open(file, "r") as f:
            packs[bfile] = f.read()

    # Return the packed dict
    return packs

def emit_txt(files : list[str], out : str):
    # Get packed dict
    packs = pack_packer(files)

    # Loop over and emit data to file
    with open(out, "w") as f:
        for packname, packval in packs.items():
            f.write(f"==={packname}==={os.linesep}")
            f.write(packval)
            f.write(os.linesep * 3)


def emit_json(files : list[str], out : str):
    # Get packed dict
    packs = pack_packer(files)

    with open(out, "w") as f:
        json.dump(packs, f, indent=None)

def emit_xml(files : list[str], out : str):
    # Construct the Tree with sone default tags
    WHENSTRFTIME = "%B %d, %Y %I:%M:%S %p"
    root = ET.Element("mdcompxml")
    ET.SubElement(root, "meta", when=str(datetime.date.today().strftime(WHENSTRFTIME)))

    # Loop over the files and create the correct element
    for file in files:
        bfile = os.path.basename(file)
        with open(file, "r") as f:
            ET.SubElement(root, "doc", name=bfile).text = f.read()

    # Generate the tree
    tree = ET.ElementTree(root)
    tree.write(output, encoding="UTF-8", xml_declaration=True)


verbose = args.verbose # Verbosity

where = args.where # Where is the directory to search for
recursive = args.recursive # Recursively search?
output = args.output # Output compiled file
otype = args.outtype # Type of output
includehidden = args.includehidden # Include hidden files?

# Create an action dictionary
FILEACT = {
    XML: emit_xml,
    PLAINTEXT: emit_txt,
    JSON: emit_json
}

if verbose: # Print if verbose
    print(f"Generating {otype} to {output}")

# Function to full name and canonicalify filenames for special reasons
def fullnamifier(root : str, notsofullname : str) -> str:
    notsofullname = os.path.join(root, notsofullname)
    notsofullname = os.path.realpath(notsofullname)
    return notsofullname

# Find all files and choose the correct emitter
emitter = FILEACT[otype]
globbed = glob.glob("**/*.md", root_dir=where, recursive=recursive, include_hidden=includehidden)
globbed = list(map(lambda a : fullnamifier(where, a), globbed))
emitter(globbed, output)




sys.exit(0)