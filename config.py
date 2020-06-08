
import os
import json
import tkinter as tk
from tkinter import filedialog


#
# This class stores the project configuration
# and handles imports from and exports to files.
#
class Config:
    #
    # Configuration file keywords
    #
    FPGA_EXTENDER = "fpga-extender"
    HARDWARE_REVISION = "hardware-revision"

    PORT_COUNT = 18
    PORTS = "ports"
    PORT_ROLE = "role"
    PORT_ROLE_EMPTY = "Empty"
    PORT_ROLE_DAC = "DAC"
    PORT_ROLE_ADC = "ADC"
    PORT_ROLE_NUCLEO = "Nucleo"
    # The complete list of acceptable port roles
    PORT_ROLES = [
        PORT_ROLE_EMPTY,
        PORT_ROLE_ADC,
        PORT_ROLE_DAC,
        PORT_ROLE_NUCLEO
        ]
    PORT_ROLE_DEFAULT = PORT_ROLE_EMPTY

    PORT_INTERFACE = "interface"
    PORT_INTERFACE_SPI_MASTER = "spi-master"

    PORT_WIZARD = "port-wizard"
    PORT_WIZARD_VERSION = "version"
    PORT_WIZARD_VERSION_ANY = "any"
    PORT_WIZARD_VERSION_THIS = 1


    def __init__(self, importFile=None, importText=None, importJSON=None):
        # Begin with an empty configuration
        self.clear()

        # Import from source, if one was given
        if not (importFile is None):
            self.importFile(importFile)
        elif not (importText is None):
            self.importTXT(text)
        elif not (importJSON is None):
            self.importJSON(plaintext=importJSON)

    #
    # Drop any current configuration and (re)start with a new one
    #
    def clear(self):
        self.configuration = {
            self.FPGA_EXTENDER: {
                self.PORTS: {},
                self.PORT_WIZARD: {}
                }
            }

    #
    # Serialize this object as a list of port roles
    #
    def __str__(self):
        return str(self.getPortRoles())

    #
    # Set the role of the extender port with the given index
    # setting must be one of self.PORT_ROLES.
    # Note: Counting starts with 0, e.g. H_H1 => portindex = 0.
    #
    def setPortRole(self, portName=None, portIndex=None, role=None):
        if (portName is None) and (portIndex is None):
            print("Error: Updating a port role requires the port's name or index.")
            return
        if (role is None):
            print("Error: Port role cannot be None.")
            return
        if (portName is None):
            portName = "H_H{:d}".format(portIndex+1)
        if not (role in self.PORT_ROLES):
            print("Unable to update port {:s}: Illegal setting specified.".format(portName))
            return
        # Make sure, the port exists within the configuration
        self.configuration[self.FPGA_EXTENDER][portName] = {}
        # Set the role of this port
        self.configuration[self.FPGA_EXTENDER][portName][self.PORT_ROLE] = role
        print("Somebody has changed the role of port {:s} to '{:s}'.".format(portName, role))

    #
    # Return the dictionary of FPGA extender ports configured in the JSON
    #
    def getPorts(self):
        ports = self.configuration[self.FPGA_EXTENDER][self.PORTS] or {}
        return ports

    #
    # Return an array of port names used in this project
    #
    def getPortList(self):
        return list(self.getPorts().keys())

    #
    # Return the configured role for a port
    # or the default role, if unsuccessful
    #
    def getPortRole(self, portName):
        if portName in self.getPortList():
            port = self.getPorts()[portName]
            if self.PORT_ROLE in port.keys():
                return port[self.PORT_ROLE] or self.PORT_ROLE_DEFAULT
        return self.PORT_ROLE_DEFAULT

    #
    # Return a list of the roles of all ports
    #
    def getPortRoles(self):
        a = []
        for port in range(self.PORT_COUNT):
            role = self.getPortRole(port)
            a += [role]
        return a

    #
    # Return a list of possible extender port roles
    #
    def getPortOptions(self):
        return self.PORT_ROLES

    #
    # Return the default port extender port role
    #
    def getDefaultValue(self):
        return self.PORT_ROLE_DEFAULT

    #
    # Save the configuration to a file
    #
    # Opens a dialog, if no filename is specified.
    #
    def saveFile(self, fout=None):
        if fout is None:
            # If no filename was given, open a dialog to ask for one.
            fout = filedialog.asksaveasfilename(initialdir="/", defaultextension='.txt', initialfile = "FPGA-Extender_settings",
                                            filetypes = (("Textfile","*.txt"),("JSON File","*.json"),("CSV File","*.csv")))
        extension = fout[-5:].lower()
        if extension[-4:] == ".txt":
            self.saveTXT(fout)
        elif extension[-5:] == ".json":
            self.saveJSON(fout)
        else:
            print("Unable to save configuration to file: Unsupported file format.")
            return

    #
    # Read configuration from file (attempt to guess the file format)
    #
    def importFile(self, filename):
        if len(filename) < 5:
            print("Error: Sorry, filename is too short.")
            return
        extension = filename[-5:].lower()
        if extension[-4:] == ".txt":
            self.importTXT(filename)
        elif extension[-5:] == ".json":
            self.importJSON(filename)
        else:
            print("Unable to import configuration from file: Unsupported file format.")
            return

    #
    # Generate a new configuration from simple text
    #
    def importTXT(self, text):
        print("Importing configuration from text file...")
        self.clear()
        portIndex = 0
        for line in text.split("\n"):
            portIndex += 1
            self.setPortRole(portIndex=portIndex, role=line)
        if portIndex != self.PORT_COUNT:
            print("Warning: Expected {:d} ports, got {:d}.".format(self.PORT_COUNT, portIndex))
        else:
            print("Import successfull: Configured {:d} ports.".format(portIndex))

    #
    # Export the configuration as (simplified) text
    #
    def exportTXT(self):
        print("Exporting configuration as text...")
        result = ""
        for x in self.getPortList():
            result += "{:s}\n".format(self.getPortRole(x))
        return result

    #
    # Save the configuration into a text file
    #
    def saveTXT(self, filename):
        if filename is None:
            print("Error: A filename ist required for saving.")
            return
        txt = self.exportTXT()
        f = open(filename, "w")
        f.write(txt)
        f.close()

    #
    # Parse configuration from file or plaintext JSON
    #
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

        #
        # Make sure the configuration format is supported by this library version
        #
        if self.HARDWARE_REVISION in self.configuration[self.PORT_WIZARD].keys():
            # No specified required version means all versions acceptable

            if (self.configuration[self.PORT_WIZARD_VERSION] == self.PORT_WIZARD_VERSION_ANY):
                try:
                    version = int(self.configuration[self.PORT_WIZARD_VERSION])
                except:
                    print("Configuration error: The wizard version must be an integer.")
                    return False

                if (version < self.PORT_WIZARD_VERSION_THIS):
                    print("Error: This wizard is not compatible with the specified configuration.")
                    return False

        #
        # Check for problems/errors with or within the configuration
        #
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

        #
        # Check port roles
        #
        for port in self.getPortList():
            role = self.getPortRole(port)
            if not (role in self.PORT_ROLES):
                # Port role was not recognized
                m = role.lower()
                for r in self.PORT_ROLES:
                    if m == r.lower():
                        # This role matches (case-insensistive)
                        self.setPortRole(portName=port, role=r)
                        print("Changed port {:s}'s role '{:s}' to '{:s}'.".format(port, role, r))

        return True

    #
    # Export this configuration in JSON format
    #
    def exportJSON(self):
        j = json.dumps(self.configuration, indent=4, sort_keys=True)
        return j

    #
    # Save this configuration as a JSON file
    #
    def saveJSON(self, filename):
        config = self.exportJSON()
        f = open(filename, "w")
        f.write(config)
        f.close()


if __name__ == "__main__":

    hallo = Config()
    print(hallo)
