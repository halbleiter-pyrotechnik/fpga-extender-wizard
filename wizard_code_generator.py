#!/usr/bin/python3


#
# This class controls Verilog code generation
# according to the configuration in a referenced configuration object
#
class WizardCodeGenerator:
    #
    # Store a reference to the configuration object
    #
    def __init__(self, config):
        self.config = config

    #
    # Summarize the FPGA extender configuration
    #
    def stats(self):
        print(str(self.config.getPortList()))


    #
    # This method generates module port and wires for a DAC
    #
    def generateDACPort(self, portName):
        portName = portName.lower()
        self.portCounterDAC += 1
        result = "// Ports and wires for DAC{:d}\n".format(self.portCounterDAC)
        result += "output {:s}_pin5;\n".format(portName)
        result += "assign {:s}_pin5 = dac{:d}_ncs;\n".format(portName, self.portCounterDAC)
        result += "output {:s}_pin1;\n".format(portName)
        result += "assign {:s}_pin1 = dac{:d}_sclk;\n".format(portName, self.portCounterDAC)
        result += "output {:s}_pin9;\n".format(portName)
        result += "assign {:s}_pin9 = dac{:d}_mosi;\n".format(portName, self.portCounterDAC)
        # result += "input  {:s}_pin3;\n".format(portName)
        # result += "assign dac{:d}_miso = {:s}_pin3;\n".format(self.portCounterDAC, portName)
        return result


    def generateVerilogPorts(self):
        result = ""
        ports = self.config.getPorts()
        self.portCounterDAC = 0

        for port in ports.keys():
            role = self.config.getPortRole(port)
            print("{:s} has role {:s}.".format(port, role))

            if role == self.config.PORT_ROLE_DAC:
                result += self.generateDACPort(port)

        return result


    def exportVerilogPorts(self, filename=None):
        ports = self.generateVerilogPorts()
        if filename is None:
            print(ports)
        else:
            f = open(filename, "w")
            f.write(ports)
            f.close()


    def generateVerilogBlock(self, index=None):
        if index is None:
            index = self.index
        result = VerilogInstance(
                    name="spi_master_{:d}".format(index),
                    module="spi_master"
                    )
        # TODO: Add parameters and ports
        return result
