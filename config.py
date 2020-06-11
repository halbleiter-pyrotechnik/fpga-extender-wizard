
import os
import json
import tkinter as tk
from tkinter import filedialog


#
# Store and handle extender port-related configuration
#
class Port:
    ROLE = "role"
    ROLE_EMPTY = "Empty"
    ROLE_DAC = "DAC"
    ROLE_ADC = "ADC"
    ROLE_NUCLEO = "Nucleo"
    # The complete list of acceptable port roles
    ROLES = [
        ROLE_EMPTY,
        ROLE_ADC,
        ROLE_DAC,
        ROLE_NUCLEO
        ]
    ROLE_DEFAULT = ROLE_EMPTY

    def __init__(self, portName=None, importDict=None):
        self.name = "H_H0"
        self.config = {}
        if (portName is None) or (importDict is None):
            return
        self.name = portName
        self.config = importDict

    def getName(self):
        return self.name

    def getConfig(self):
        return self.config

    def getRole(self):
        if self.ROLE in self.config.keys():
            return self.convertToAcceptableRole(self.config[self.ROLE])
        return self.getDefaultRole()

    def setRole(self, newRole):
        if (role is None):
            print("Error: Port role cannot be None.")
            return
        if newRole in self.getPossibleRoles():
            self.config[ROLE] = newRole
            return
        print("Error: Unsupported port role '{:s}'.".format(newRole))

    def getAcceptableRoles(self):
        return self.ROLES

    def convertToAcceptableRole(self, role):
        acceptablePortRoles = self.getAcceptableRoles()
        if role in acceptablePortRoles:
            return role
        # Port role was not recognized; search for case-insensistive matches
        m = role.lower()
        for r in acceptablePortRoles:
            if m == r.lower():
                return r
        # Role is not acceptable
        return None

    def isAcceptableRole(self, role):
        return not (self.convertToAcceptableRole(role) is None)

    def getDefaultRole(self):
        return self.ROLE_DEFAULT


#
# Store and handle ports configured as MCU interface
#
class PortMCU(Port):
    BITCOUNT = "bitcount"

    def __init__(self, portName=None, importDict=None):
        Port.__init__(self, portName, importDict)
        self.bitcount = 0
        if self.BITCOUNT in self.config.keys():
            try:
                self.bitcount = int(self.config[self.BITCOUNT])
            except:
                pass

    def getBitCount(self):
        return self.bitcount


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
    # setting must be one of self.ROLES.
    # Note: Counting starts with 0, e.g. H_H1 => portindex = 0.
    #
    def setPortRole(self, portName=None, portIndex=None, role=None):
        if (portName is None) and (portIndex is None):
            print("Error: Updating a port role requires the port's name or index.")
            return
        if (portName is None):
            portName = "H_H{:d}".format(portIndex+1)

        port = self.getPortByName(portName)
        if port is None:
            print("Error: No such port: '{:s}'".format(portName))
            return
        port.setRole(role)


    #
    # Return the dictionary of FPGA extender ports configured in the JSON
    #
    def getPorts(self):
        return self.configuration[self.FPGA_EXTENDER][self.PORTS] or {}

    #
    # Return an array of configured port objects
    #
    def getPortList(self):
        return list(self.getPorts().values())

    #
    # Return an array of port names used in this project
    #
    def getPortNameList(self):
        return list(self.getPorts().keys())

    #
    # Return the Port object with the given name or None
    #
    def getPortByName(self, portName):
        if portName is None:
            return None
        for port in self.getPorts():
            if port.getName() == portName:
                return port
        return None

    #
    # Return the configured role for a port
    # or the default role, if unsuccessful
    #
    def getPortRole(self, portName):
        port = self.getPortByName(portName)
        if port is None:
            return self.ROLE_DEFAULT
        return port.getRole()

    #
    # Return a list of the configured roles of all ports
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
        return Port.getAcceptableRoles()

    #
    # Return the default port extender port role
    #
    def getDefaultValue(self):
        return Port.getDefaultRole()

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
            print("Error: Unable to save configuration to file. The file format could not be detected.")
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
            print("Error: Unable to import configuration from file. The file format could not be detected.")
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
        # Convert ports to objects
        #
        for portName in self.getPortNameList():
            d = self.configuration[self.FPGA_EXTENDER][self.PORTS][portName]
            obj = Port(portName, d)
            if obj.getRole() == Port.ROLE_NUCLEO:
                obj = PortMCU(portName, d)
            self.configuration[self.FPGA_EXTENDER][self.PORTS][portName] = obj

        print(self.getPortList())

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
