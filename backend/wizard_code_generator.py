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
    # This method generates code for a DAC
    #
    def generateVerilogDAC(self, portName):
        self.portCounterDAC += 1
        ports = "/*\n * DAC{:d} is connected to extender port {:s}\n */\n".format(self.portCounterDAC, portName)
        wires = ""
        instances = ""
        portName = portName.lower()

        signal = "dac{:d}_ncs".format(self.portCounterDAC)
        ports += "output {:s}_pin5;\n".format(portName)
        ports += "assign {:s}_pin5 = {:s};\n".format(portName, signal)
        wires += "wire {:s};\n".format(signal)

        signal = "dac{:d}_sclk".format(self.portCounterDAC)
        ports += "output {:s}_pin1;\n".format(portName)
        ports += "assign {:s}_pin1 = {:s};\n".format(portName, signal)
        wires += "wire {:s};\n".format(signal)

        signal = "dac{:d}_mosi".format(self.portCounterDAC)
        ports += "output {:s}_pin9;\n".format(portName)
        ports += "assign {:s}_pin9 = {:s};\n".format(portName, signal)
        wires += "wire {:s};\n".format(signal)
        return (wires, ports, instances)


    def generateVerilog(self):
        result = []
        ports = self.config.getPorts()
        self.portCounterDAC = 0

        for port in ports.keys():
            role = self.config.getPortRole(port)
            print("{:s} has role {:s}.".format(port, role))

            if role == self.config.PORT_ROLE_DAC:
                result += [self.generateVerilogDAC(port)]

        return result


    def exportVerilog(self, filename=None):
        code = str(self.generateVerilog())

        if filename is None:
            print(code)
        else:
            f = open(filename, "w")
            f.write(code)
            f.close()
