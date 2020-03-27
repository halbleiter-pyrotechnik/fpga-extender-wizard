#!/usr/bin/python3

#
# This wizard parses a project configuration file
# for the FPGA extender board and generates the
# requested source code files.
#

import sys, os, json


def importJSON(filename):
    if not os.path.exists(filename):
        print("Error: File not found.")
        sys.exit(1)

    if not os.path.isfile(filename):
        print("Error: Argument must be a file.")
        sys.exit(2)

    try:
        filecontent = open(filename, "r").read()
    except:
        print("Error: Unable to read the specified file.")
        sys.exit(3)

    try:
        json = json.loads(filecontent)
    except:
        print("Error: Unable to parse configuration. Please check the syntax of your file.")
        sys.exit(4)

    return json


def checkConfigurationPrerequisites(json):
    # if json.hasKey
    print(json)


def startWizard():
    if len(sys.argv) < 2:
        print("Usage: wizard.py <configuration file>")
        sys.exit(1)

    json = importJSON(sys.argv[1])

    checkConfigurationPrerequisites(json)


if __name__ == "__main__":
    startWizard()
