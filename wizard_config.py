#!/usr/bin/python3

import os
import json


#
# This class stores the project configuration
# and handles imports from and exports to files.
#
class WizardConfigJSON:
    #
    # Configuration keywords
    #
    FPGA_EXTENDER = "fpga-extender"
    HARDWARE_REVISION = "hardware-revision"
    PORTS = "ports"
    PORT_ROLE = "role"
    PORT_ROLE_DAC = "dac"
    PORT_INTERFACE = "interface"
    PORT_INTERFACE_SPI_MASTER = "spi-master"

    PORT_WIZARD = "port-wizard"
    PORT_WIZARD_VERSION = "version"
    PORT_WIZARD_VERSION_ANY = "any"
    PORT_WIZARD_VERSION_THIS = 1

    #
    # The configuration can be parsed from a file or from a string
    #
    def __init__(self, filename=None, plaintext=None):
        if (filename is None) and (plaintext is None):
            return
        self.importJSON(filename=filename, plaintext=plaintext)


    def importJSON(self, filename=None, plaintext=None):
        if not (filename is None):
            if not os.path.exists(filename):
                print("Error: File not found.")
                return False

            if not os.path.isfile(filename):
                print("Error: Argument must be a file.")
                return False

            try:
                plaintext = open(filename, "r").read()
            except:
                print("Error: Unable to read the specified file.")
                return False

        if plaintext is None:
            print("Error: You didn't provide a JSON to import.")
            return False

        try:
            self.configuration = json.loads(plaintext)
        except:
            print("Error: Unable to parse JSON. Please check the syntax of your configuration.")
            return False

        if not self.checkConfiguration():
            return False

        return True


    #
    # Make sure the configuration format is supported by this library version
    #
    def checkWizardVersion(self):
        if not (self.HARDWARE_REVISION in self.configuration[self.PORT_WIZARD].keys()):
            # No specified required version means all versions acceptable
            return True

        if (self.configuration[self.PORT_WIZARD_VERSION] == self.PORT_WIZARD_VERSION_ANY):
            return True

        try:
            version = int(self.configuration[self.PORT_WIZARD_VERSION])
        except:
            print("Configuration error: The wizard version must be an integer.")
            return False

        if (version >= self.PORT_WIZARD_VERSION_THIS):
            return True

        print("Error: This wizard is not compatible with the specified configuration.")
        return False


    #
    # Check for problems/errors with or within the configuration
    #
    def checkConfiguration(self):
        if not self.checkWizardVersion():
            return False

        if not (self.FPGA_EXTENDER in self.configuration.keys()):
            print("Configuration error: Section \"{:s}\" is missing.".format(self.FPGA_EXTENDER))
            return False

        if not (self.HARDWARE_REVISION in self.configuration[self.FPGA_EXTENDER].keys()):
            print("Configuration error: Section \"{:s}\" requires a property \"{:s}\".".format(self.FPGA_EXTENDER, self.HARDWARE_REVISION))
            return False

        if not (self.PORTS in self.configuration[self.FPGA_EXTENDER].keys()):
            print("Configuration error: Section \"{:s}\" requires a subsection \"{:s}\".".format(self.FPGA_EXTENDER, self.PORTS))
            return False

        if not (self.PORT_WIZARD in self.configuration.keys()):
            print("Configuration error: Section \"{:s}\" is missing.".format(self.PORT_WIZARD))
            return False

        return True


    #
    # Return the dictionary of FPGA extender ports configured in the JSON
    #
    def getPorts(self):
        return self.configuration[self.FPGA_EXTENDER][self.PORTS]

    #
    # Return an array of port names used in this project
    #
    def getPortList(self):
        return list(self.getPorts().keys())

    #
    # Return the configured role for a port
    #
    def getPortRole(self, portName):
        return self.getPorts()[portName][self.PORT_ROLE]
