
from verilog_port import *
from verilog_instance import *


class SPIMaster:
    def __init__(self, index):
        self.index = index

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
