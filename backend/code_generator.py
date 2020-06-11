#!/usr/bin/python3

import sys
sys.path.append("..")
from config import *


#
# This class controls Verilog code generation
# according to the configuration in a referenced configuration object
#
class CodeGenerator:
    #
    # Store a reference to the configuration object
    #
    def __init__(self, config):
        self.config = config
        self.clear()

    #
    # Flush all code generation-related variables
    #
    def clear(self):
        self.includes = []
        self.includeCode = ""
        self.wires = ""
        self.ports = ""
        self.instances = ""

        self.portCounterADC = 0
        self.portCounterDAC = 0
        self.portCounterMCU = 0

    #
    # Summarize the FPGA extender configuration
    #
    def stats(self):
        ports = self.config.getPortList()
        count = len(ports)
        print("FPGA extender: {:d} port{:s} configured.".format(count, "s are" if (count > 1) else " is"))

    #
    # Add a file to the list of Verilog files
    # to be included be the generated project
    #
    def addInclude(self, filename):
        if not (filename in self.includes):
            self.includes += [filename]

    #
    # This method generates Verilog code for an ADC
    #
    def generateCodeADC(self, port):
        portName = port.getName()
        self.portCounterADC += 1

        ports = "/*\n * ADC{:d} is connected to extender port {:s}\n */\n".format(self.portCounterADC, portName)
        wires = "/*\n * Wires connecting ADC{:d}\n */\nwire ".format(self.portCounterADC)
        assignments = ""
        instances = ""
        portName = portName.lower()
        self.addInclude("spi_stimulus.v")
        self.addInclude("spi_receiver.v")

        nss_signal = "adc_nss"
        ports += "output {:s}_pin5,\n".format(portName)
        assignments += "assign {:s}_pin5 = {:s};\n".format(portName, nss_signal)
        if self.portCounterADC == 1:
            # nSS is shared among all DACs
            wires += "{:s}, ".format(nss_signal)

        sclk_signal = "adc_sclk"
        ports += "output {:s}_pin1,\n".format(portName)
        assignments += "assign {:s}_pin1 = {:s};\n".format(portName, sclk_signal)
        if self.portCounterADC == 1:
            # SCLK is shared among all DACs
            wires += "{:s}, ".format(sclk_signal)

        miso_signal = "adc{:d}_miso".format(self.portCounterADC)
        ports += "input  {:s}_pin3,\n\n".format(portName)
        assignments += "assign {:s} = {:s}_pin3;\n".format(miso_signal, portName)
        wires += "{:s};\n".format(miso_signal)

        buffer_bus = "adc{:d}_buffer".format(self.portCounterADC)
        wires += "wire[15:0] {:s};\n".format(buffer_bus)
        value_bus = "adc{:d}_value".format(self.portCounterADC)
        wires += "wire[11:0] {:s};\n".format(value_bus)
        assignments += "assign {:s}[11:0] = {:s}[13:2];\n\n".format(value_bus, buffer_bus)

        if self.portCounterADC == 1:
            wires += "wire adc_acquisition_trigger, adc_acquisition_complete;\n"

        wires += assignments

        if self.portCounterADC == 1:
            # SPI requires a stimulus
            instances += \
"""/**
 * Generate SPI signals for data download from ADCs
 */
spi_stimulus
    #(
        .bitcount       (16),
        .ss_polarity    (0),
        .sclk_polarity  (0),
        .tick_count_sclk_delay_leading      (0),
        .tick_count_sclk_delay_trailing     (2),
        .tick_count_complete_delay_trailing (3)
        )
    adc_spi_stimulus
    (
        .clock      (master_clock),
        .trigger    (adc_acquisition_trigger),
        .invalidate (1'b0),
        .ss         (adc_nss),
        .sclk       (adc_sclk),
        .complete   (adc_acquisition_complete)
        );

"""

        instances += \
"""/**
 * Download data from ADC{:d}
 */
spi_receiver
    #(
        .ss_polarity            (0),
        .sclk_polarity          (0),
        .sclk_phase             (1),
        .bitcount               (16),
        .msb_first              (1),
        .use_gated_output       (1),
        .use_external_trigger   (0)
        )
    spi_receiver_adc{:d}
    (
        .clock      (master_clock),
        .trigger    (),
        .ss         (adc_nss),
        .sclk       (adc_sclk),
        .sdi        ({:s}),
        .data       ({:s}),
        .complete   ()
        );

""".format(
        self.portCounterADC,
        self.portCounterADC,
        miso_signal,
        value_bus
        )

        self.ports += ports
        self.wires += wires
        self.instances += instances

    #
    # This method generates code for a DAC
    #
    def generateCodeDAC(self, port):
        portName = port.getName()
        self.portCounterDAC += 1

        ports = "/*\n * DAC{:d} is connected to extender port {:s}\n */\n".format(self.portCounterDAC, portName)
        wires = "/*\n * Wires connecting DAC{:d}\n */\nwire ".format(self.portCounterDAC)
        assignments = ""
        instances = ""
        portName = portName.lower()
        self.addInclude("spi_stimulus.v")
        self.addInclude("spi_transmitter.v")

        nss_signal = "dac_nss"
        ports += "output {:s}_pin5,\n".format(portName)
        assignments += "assign {:s}_pin5 = {:s};\n".format(portName, nss_signal)
        if self.portCounterDAC == 1:
            # nSS is shared among all DACs
            wires += "{:s}, ".format(nss_signal)

        sclk_signal = "dac_sclk"
        ports += "output {:s}_pin1,\n".format(portName)
        assignments += "assign {:s}_pin1 = {:s};\n".format(portName, sclk_signal)
        if self.portCounterDAC == 1:
            # SCLK is shared among all DACs
            wires += "{:s}, ".format(sclk_signal)

        mosi_signal = "dac{:d}_mosi".format(self.portCounterDAC)
        ports += "output {:s}_pin9,\n\n".format(portName)
        assignments += "assign {:s}_pin9 = {:s};\n".format(portName, mosi_signal)
        wires += "{:s};\n".format(mosi_signal)

        buffer_bus = "dac{:d}_buffer".format(self.portCounterDAC)
        wires += "wire[15:0] {:s};\n".format(buffer_bus)
        value_bus = "dac{:d}_value".format(self.portCounterDAC)
        wires += "wire[11:0] {:s};\n".format(value_bus)
        assignments += "assign {:s}[15:12] = 4'b0000;\n".format(buffer_bus)
        assignments += "assign {:s}[11:0] = {:s};\n\n".format(buffer_bus, value_bus)

        if self.portCounterDAC == 1:
            wires += "wire dac_update_trigger, dac_update_complete;\n"

        wires += assignments

        if self.portCounterDAC == 1:
            # SPI requires a stimulus
            instances += \
"""/**
 * Generate SPI signals for data transmission to DACs
 */
spi_stimulus
    #(
        .bitcount       (16),
        .ss_polarity    (0),
        .sclk_polarity  (0)
        )
    dac_spi_stimulus
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
 * Transmit data to DAC{:d}
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

        self.ports += ports
        self.wires += wires
        self.instances += instances


    #
    # This method generates code for a DAC
    #
    def generateCodeMCU(self, port):
        portName = port.getName()
        bitcount = port.getBitCount()
        self.portCounterMCU += 1

        ports = "/*\n * MCU{:d} is connected to extender port {:s}\n */\n".format(self.portCounterMCU, portName)
        wires = "/*\n * Wires connecting MCU{:d}\n */\nwire ".format(self.portCounterMCU)
        assignments = ""
        instances = ""
        portName = portName.lower()
        self.addInclude("spi_stimulus.v")
        self.addInclude("spi_transmitter.v")
        self.addInclude("spi_receiver.v")

        nss_signal = "mcu{:d}_nss".format(self.portCounterMCU)
        ports += "input  {:s}_pin5,\n".format(portName)
        assignments += "assign {:s} = {:s}_pin5;\n".format(nss_signal, portName)
        wires += "{:s}, ".format(nss_signal)

        sclk_signal = "mcu{:d}_sclk".format(self.portCounterMCU)
        ports += "input  {:s}_pin1,\n".format(portName)
        assignments += "assign {:s} = {:s}_pin1;\n".format(sclk_signal, portName)
        wires += "{:s}, ".format(sclk_signal)

        mosi_signal = "mcu{:d}_mosi".format(self.portCounterMCU)
        ports += "input  {:s}_pin9,\n".format(portName)
        assignments += "assign {:s} = {:s}_pin9;\n".format(mosi_signal, portName)
        wires += "{:s}, ".format(mosi_signal)

        miso_signal = "mcu{:d}_miso".format(self.portCounterMCU)
        ports += "output {:s}_pin3,\n\n".format(portName)
        assignments += "assign {:s}_pin3 = {:s};\n".format(portName, miso_signal)
        wires += "{:s};\n".format(miso_signal)

        data_incoming = "mcu{:d}_data_incoming".format(self.portCounterMCU)
        data_outgoing = "mcu{:d}_data_outgoing".format(self.portCounterMCU)
        wires += "wire[{:d}:0] {:s}, {:s};\n".format(bitcount-1, data_incoming, data_outgoing)

        complete_signal = "mcu{:d}_transfer_complete".format(self.portCounterMCU)
        wires += "wire {:s};\n".format(complete_signal)
        wires += assignments
        wires += "\n"

        instances += \
"""/**
 * Transmit data to MCU{:d}
 */
spi_transmitter
    #(
        .ss_polarity    (0),
        // This is a workaround to simulatte CPHA = 0.
        .sclk_polarity  (1),
        // CPHA is not evaluated/supported yet.
        // .sclk_phase     (1),
        .bitcount       ({:d}),
        .msb_first      (1),
        .use_load_input (0)
        )
    spi_transmitter_mcu{:d}
    (
        .clock      (master_clock),
        .ss         ({:s}),
        .sclk       ({:s}),
        .sdo        ({:s}),
        .load       (),
        .data       ({:s}[{:d}:0]),
        .complete   ()
        );

""".format(
        self.portCounterMCU,
        bitcount,
        self.portCounterMCU,
        nss_signal,
        sclk_signal,
        miso_signal,
        data_outgoing,
        bitcount-1
        )

        instances += \
"""/**
 * Receive data from MCU{:d}
 */
spi_receiver
    #(
        .ss_polarity            (0),
        .sclk_polarity          (1),
        // CPHA is not evaluated/supported yet.
        // .sclk_phase             (1),
        .bitcount               ({:d}),
        .msb_first              (1),
        .use_gated_output       (1),
        .use_external_trigger   (0)
        )
    spi_receiver_mcu{:d}
    (
        .clock      (master_clock),
        .trigger    (),
        .ss         ({:s}),
        .sclk       ({:s}),
        .sdi        ({:s}),
        .data       ({:s}[{:d}:0]),
        .complete   ({:s})
        );

""".format(
        self.portCounterMCU,
        bitcount,
        self.portCounterMCU,
        nss_signal,
        sclk_signal,
        mosi_signal,
        data_incoming,
        bitcount-1,
        complete_signal
        )

        self.ports += ports
        self.wires += wires
        self.instances += instances

    #
    # This method generates wires, ports and instances
    # for all ports in the referenced configuration
    #
    def generateCode(self):
        self.clear()

        for port in self.config.getPortList():
            role = port.getRole()
            # print("{:s} has role {:s}.".format(port, role))

            if role == Port.ROLE_ADC:
                self.generateCodeADC(port)
            elif role == Port.ROLE_DAC:
                self.generateCodeDAC(port)
            elif role == Port.ROLE_NUCLEO:
                self.generateCodeMCU(port)
            else:
                print("Warning: Port role '{:s}' was not recognized.".format(role))

        # Convert list to string
        for f in self.includes:
            self.includeCode += "`include \"{:s}\"\n".format(f)

        clockwork = "wire master_clock;\nassign master_clock = clock_12mhz;\n\n"

        self.code = \
            self.includeCode + \
            "\nmodule top(\n" + \
            self.ports + \
            "input clock_12mhz\n);\n\n" + \
            clockwork + \
            self.wires + \
            self.instances + \
            "endmodule\n"
        return self.code

    #
    # This method generates Verilog code for the referenced configuration
    # and prints it to stdout or saves it to a file
    #
    def exportCode(self, filename=None):
        self.generateCode()
        if filename is None:
            print(self.code)
        else:
            f = open(filename, "w")
            f.write(self.code)
            f.close()
