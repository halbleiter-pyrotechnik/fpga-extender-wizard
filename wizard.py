#!/usr/bin/python3

#
# This wizard parses a project configuration file
# for the FPGA extender board and generates the
# requested source code files.
#

import sys, os, json

from wizard_keywords import *


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
        configuration = json.loads(filecontent)
    except:
        print("Error: Unable to parse JSON. Please check the syntax of your configuration.")
        sys.exit(4)

    return configuration


def checkWizardVersion(configuration):
    if (configuration[PORT_WIZARD_VERSION] == PORT_WIZARD_VERSION_ANY):
        return True

    try:
        version = int(configuration[PORT_WIZARD_VERSION])
    except:
        print("Error: The wizard version must be an integer.")
        sys.exit(13)

    if (version >= PORT_WIZARD_VERSION_THIS):
        return True

    print("Error: This wizard is not compatible with the specified configuration.")
    sys.exit(13)


def checkConfigurationPrerequisites(configuration):
    if not (FPGA_EXTENDER in configuration.keys()):
        print("Configuration error: Section \"{:s}\" is missing.".format(FPGA_EXTENDER))
        sys.exit(10)

    if not (HARDWARE_REVISION in configuration[FPGA_EXTENDER].keys()):
        print("Configuration error: Section \"{:s}\" requires a property \"{:s}\".".format(FPGA_EXTENDER, HARDWARE_REVISION))
        sys.exit(11)

    if not (PORTS in configuration[FPGA_EXTENDER].keys()):
        print("Configuration error: Section \"{:s}\" requires a subsection \"{:s}\".".format(FPGA_EXTENDER, PORTS))
        sys.exit(11)

    if not (PORT_WIZARD in configuration.keys()):
        print("Configuration error: Section \"{:s}\" is missing.".format(PORT_WIZARD))
        sys.exit(12)

    if HARDWARE_REVISION in configuration[PORT_WIZARD].keys():
        checkWizardVersion(configuration[PORT_WIZARD])

    return True


def processPortConfiguration(ports):
    for port in ports.keys():
        if not (PORT_FUNCTION in port.keys()):
            print("Configuration error: Port \"{:s}\" has no function.".format(port))
            sys.exit(20)


def startWizard():
    if len(sys.argv) < 2:
        print("Usage: wizard.py <configuration file>")
        sys.exit(1)

    configuration = importJSON(sys.argv[1])
    checkConfigurationPrerequisites(configuration)
    processPortConfiguration(configuration[FPGA_EXTENDER][PORTS])


if __name__ == "__main__":
    startWizard()
