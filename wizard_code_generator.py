#!/usr/bin/python3


PORT_TARGET_DAC_REV1 = "dac-rev1"


class VerilogPort:
    def __init__(self, port, pin, direction, signal):
        self.port = port
        self.pin = pin
        self.direction = direction
        self.signal = signal


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
        print(str(self.config))


    def generateVerilogPorts(self, index=None, ports=[]):
        if index is None:
            index = self.index
        # AVR JTAG pin layout
        ports += [VerilogPort(port=index, pin=5, direction="output", signal="ncs")]
        ports += [VerilogPort(port=index, pin=1, direction="output", signal="sclk")]
        ports += [VerilogPort(port=index, pin=9, direction="output", signal="mosi")]
        ports += [VerilogPort(port=index, pin=3, direction="input",  signal="miso")]
        return ports


    def generateVerilogBlock(self, index=None):
        if index is None:
            index = self.index
        result = VerilogInstance(
                    name="spi_master_{:d}".format(index),
                    module="spi_master"
                    )
        # TODO: Add parameters and ports
        return result
