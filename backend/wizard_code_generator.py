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
        wires = "/*\n * Wires connecting DAC{:d}\n */\nwire ".format(self.portCounterDAC)
        instances = ""
        portName = portName.lower()

        nss_signal = "dac_nss"
        ports += "output {:s}_pin5;\n".format(portName)
        ports += "assign {:s}_pin5 = {:s};\n".format(portName, nss_signal)
        if self.portCounterDAC == 1:
            # nSS is shared among all DACs
            wires += "{:s}, ".format(nss_signal)

        sclk_signal = "dac_sclk"
        ports += "output {:s}_pin1;\n".format(portName)
        ports += "assign {:s}_pin1 = {:s};\n".format(portName, sclk_signal)
        if self.portCounterDAC == 1:
            # SCLK is shared among all DACs
            wires += "{:s}, ".format(sclk_signal)

        mosi_signal = "dac{:d}_mosi".format(self.portCounterDAC)
        ports += "output {:s}_pin9;\n".format(portName)
        ports += "assign {:s}_pin9 = {:s};\n\n".format(portName, mosi_signal)
        wires += "{:s};\n".format(mosi_signal)

        buffer_bus = "dac{:d}_buffer".format(self.portCounterDAC)
        wires += "wire[15:0] {:s};\n".format(buffer_bus)
        value_bus = "dac{:d}_value".format(self.portCounterDAC)
        wires += "wire[11:0] {:s};\n".format(value_bus)
        wires += "assign {:s}[15:12] = 4'b0000;\n".format(buffer_bus)
        wires += "assign {:s}[11:0] = {:s};\n\n".format(buffer_bus, value_bus)

        if self.portCounterDAC == 1:
            # SPI requires a stimulus
            instances += \
"""/**
 * This instance generates slave-select and
 * clock signals for the SPI transmission
 */
spi_stimulus
    #(
        .bitcount       (16),
        .ss_polarity    (0),
        .sclk_polarity  (0)
        )
    analog_debugger_spi_stimulus
    (
        .clock      (master_clock),
        .trigger    (dac_update_trigger),
        .abort      (1'b0),
        .ss         (dac_nss),
        .sclk       (dac_sclk),
        .complete   (dac_update_complete)
        );

"""

        instances += \
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
        .clock      (master_clock),
        .ss         ({:s}),
        .sclk       ({:s}),
        .sdo        ({:s}),
        .load       (),
        .data       ({:s}[15:0]),
        .complete   ()
        );

""".format(
        self.portCounterDAC,
        self.portCounterDAC,
        nss_signal,
        sclk_signal,
        mosi_signal,
        buffer_bus,
        self.portCounterDAC
        )

        return (wires, ports, instances)


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
            else:
                print("Warning: Port role '{:s}' was not recognized.".format(role))

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
