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
        ports = self.config.getPortList()
        count = len(ports)
        print("FPGA extender: {:d} port{:s} configured.".format(count, "s are" if (count > 1) else " is"))


    #
    # This method generates code for a DAC
    #
    def generateVerilogDAC(self, portName):
        self.portCounterDAC += 1
        ports = "/*\n * DAC{:d} is connected to extender port {:s}\n */\n".format(self.portCounterDAC, portName)
        wires = "/*\n * Wires connecting to DAC1 (via SPI)\n */\n"
        portName = portName.lower()

        nss_signal = "dac{:d}_nss".format(self.portCounterDAC)
        ports += "output {:s}_pin5;\n".format(portName)
        ports += "assign {:s}_pin5 = {:s};\n".format(portName, nss_signal)
        wires += "wire {:s}, ".format(nss_signal)

        sclk_signal = "dac{:d}_sclk".format(self.portCounterDAC)
        ports += "output {:s}_pin1;\n".format(portName)
        ports += "assign {:s}_pin1 = {:s};\n".format(portName, sclk_signal)
        wires += "{:s}, ".format(sclk_signal)

        mosi_signal = "dac{:d}_mosi".format(self.portCounterDAC)
        ports += "output {:s}_pin9;\n".format(portName)
        ports += "assign {:s}_pin9 = {:s};\n\n".format(portName, mosi_signal)
        wires += "{:s};\n\n".format(mosi_signal)

        instance = \
"""/**
 * This instance transmits data to DAC{:d}
 */
spi_transmitter
    #(
        .ss_polarity    (0),
        // This is a workaround to simulatte CPHA = 0.
        .sclk_polarity  (1),
        // CPHA is not evaluated/supported yet.
        // .sclk_phase     (1),
        .bitcount       (16),
        .msb_first      (1),
        .use_load_input (0)
        )
    spi_transmitter_dac{:d}
    (
        .clock      (clock_80mhz),
        .ss         ({:s}),
        .sclk       ({:s}),
        .sdo        ({:s}),
        .load       (),
        .data       (dac{:d}_data[15:0]),
        .complete   ()
        );
""".format(
        self.portCounterDAC,
        self.portCounterDAC,
        nss_signal,
        sclk_signal,
        mosi_signal,
        self.portCounterDAC
        )

        return (wires, ports, instance)


    #
    # This method generates wires, ports and instances
    # for all ports in the referenced configuration
    #
    def generateVerilog(self):
        results = []
        ports = self.config.getPorts()
        self.portCounterDAC = 0

        for port in ports.keys():
            role = self.config.getPortRole(port)
            # print("{:s} has role {:s}.".format(port, role))

            if role == self.config.PORT_ROLE_DAC:
                results += [self.generateVerilogDAC(port)]

        self.verilogWires = ""
        self.verilogPorts = ""
        self.verilogInstances = ""
        for e in results:
            self.verilogWires += e[0]
            self.verilogPorts += e[1]
            self.verilogInstances += e[2]

        self.verilogCode =  self.verilogWires + self.verilogPorts + self.verilogInstances
        return self.verilogCode


    #
    # This method generates Verilog code for the referenced configuration
    # and prints it to stdout or saves it to a file
    #
    def exportVerilog(self, filename=None):
        code = str(self.generateVerilog())

        if filename is None:
            print(code)
        else:
            f = open(filename, "w")
            f.write(code)
            f.close()
