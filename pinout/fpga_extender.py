#!/usr/bin/python3
#
# This script parses the FPGA extender board netlist
# and generates a pinout constraints file (.pcf)
# for use with an FPGA project.
#


import sys
sys.path.append("..")

from common import *
from simple_csv import *


#
# Return the pin number on the other side of the resistor network
#
def getConnectedResistorEnd(pinNumber):
    answer = {1:2, 2:1, 3:4, 4:3, 5:6, 6:5, 7:8, 8:7}
    return answer[pinNumber]


#
# A little net renaming (required for board revision 1 tango netlist export)
#
def renameSignal(signal):
    s = signal.split("_")

    if len(s) != 2:
        # Not a header signal
        return signal

    a = s[0].lower()
    if (a == "sclk"):
        pin = 1
    elif (a == "miso"):
        pin = 3
    elif (a == "ncs"):
        pin = 5
    elif (a == "mosi"):
        pin = 9
    else:
        # Not a header signal
        return signal

    b = s[1].lower()
    if b[0] != "h":
        # Not a header signal
        return signal
    # The header number must be an integer:
    try:
        header = int(b[1:])
    except:
        return signal

    return "pin" + str(pin) + "_h[" + str(header-1) + "]"


#
# Elaborate the pin association from FPGA balls to SPI signals
#
def generateFPGAExtenderPCF(
        filenameBoardNetlist = None,
        filenameManualConstraints = None,
        filenameNetRenamingRecipe = None,
        filenamePCF = None,
        debug = False
        ):

    # Check function arguments
    if (filenameBoardNetlist is None) \
    or (filenamePCF is None):
        print("Fatal: Argument missing. Aborting.")
        sys.exit(1)

    # Start with onboard pinout
    pcf = PCF()

    #
    # Include all generic/manual pins
    #
    if not (filenameManualConstraints is None):
        if debug:
            print("Evaluating manual pin constraints input ...")

        csv = importCSV(filenameManualConstraints, delimiter=";")
        for row in csv:
            # Disregard rows with less than two columns
            if len(row) < 2:
                continue

            # Disregard rows with an empty column
            column1 = row[0].strip()
            column2 = row[1].strip()
            if (len(column1) < 1) or (len(column2) < 1):
                continue

            # Skip comments
            if column1[0] == "#":
                continue

            # Do not overrule existing constraints
            signalName = column1
            fpgaBall = column2
            if pcf.hasSignal(signalName):
                print("Error: Duplicate FPGA ball declaration for signal {:s}.".format(signalName))
                sys.exit(1)
            if pcf.hasPin(fpgaBall):
                print("Error: Duplicate signal declaration for FPGA ball {:s}.".format(fpgaBall))
                sys.exit(1)

            pcf.addConstraint(
                signal = column1,
                pin    = column2
                )

            if debug:
                print("Constrained signal {:s} to FPGA ball {:s}.".format(column1, column2))
    else:
        if debug:
            print("Warning: No manual constraints file was specified. Skipping.")

    # Import adapter board netlist
    if debug:
        print("Importing board netlist from {:s} ...".format(filenameBoardNetlist))
    netlist = TangoNetlist(filenameBoardNetlist)

    #
    # Detect the balls connected to LEDs on the top board
    #
    # Pins: D-LED<1-4>,1
    #
    for i in range(4):
        led = netlist.getComponentByDesignator("D-LED" + str(i+1))
        if led is None:
            print("Warning: LED{:d} not found in netlist. Skipping.".format(i+1))
            continue

        pin = led.getPinByNumber(1)
        if pin is None:
            print("Warning: LED{:d} component has no pins in the netlist. Skipping.".format(i+1))
            continue

        net = netlist.getNetOnPin(pin)
        if net is None:
            print("Warning: Unable to detect net on LED{:d} pin 1. Skipping.".format(i+1))

        ballLabel = net.getLabel()
        l = len(ballLabel)
        if (l < 2) or (l > 3):
            print("Warning: LED{:d} pin 1 is connected to illegal FPGA ball name {:s}. Skipping.".format(i+1, ballLabel))
            continue

        signalName = "led[{:d}]".format(8+i)
        pcf.addConstraint(
            signal = signalName,
            pin    = ballLabel
            )
        if debug:
            print("Constrained LED{:d} as {:s} to FPGA ball {:s}.".format(i+1, signalName, ballLabel))

    #
    # Detect all SPI nets
    #
    # Netlabels:
    #  - nCS_H<1-n>
    #  - SCLK_H<1-n>
    #  - MOSI_H<1-n>
    #  - MISO_H<1-n>
    #
    number_of_spi_ports = 18

    for i in range(number_of_spi_ports):
        for signalPrefix in ["NCS_H", "SCLK_H", "MOSI_H", "MISO_H"]:
            signalName = signalPrefix + str(i+1)
            if debug:
                print("Searching for signal {:s} ...".format(signalName))

            net = netlist.getNet(signalName)
            if net is None:
                print("Error: Net {:s} not found in the netlist. Aborting.".format(signalName))
                sys.exit(1)

            # The signal will be connected to a resistor (network)
            resistorPin = None
            for pin in net.getPins():
                designator = pin.getComponent().getDesignator()
                if designator.find("R_H") > -1:
                    resistorPin = pin
                    pinName = pin.getName()
                    try:
                        pinNumber = int(pinName)
                    except:
                        print("Error: Unable to convert pin number '{:s}' to integer.".format(pinName))
                        sys.exit(1)
                    break

            if resistorPin is None:
                print("Error: SPI signal {:s} is not connected to a resistor network. Aborting.".format(signalName))
                sys.exit(1)

            if debug:
                print("Signal {:s} is connected to resistor {:s} on pin {:d}.".format(signalName, designator, pinNumber))

            # Elaborate the pin and net on the other end of the resistor
            resistor = resistorPin.getComponent()
            connectedPinNumber = getConnectedResistorEnd(pinNumber)
            theOtherEnd = resistor.getPinByName(connectedPinNumber)
            if theOtherEnd is None:
                print("Error: Unable to detect to where this pin connects. Aborting.")
                sys.exit(1)
            if debug:
                print("Pin {:d} connects to pin {:d} through the resistor array.".format(pinNumber, connectedPinNumber))

            fpgaBall = netlist.getNetOnPin(theOtherEnd, debug=True)
            if fpgaBall is None:
                # The debug=True argument already prints out success respectively failure messages.
                sys.exit(1)

            # Sanity check the elaborated FPGA ball
            ballLabel = fpgaBall.getLabel()
            if (len(ballLabel) < 2) or (len(ballLabel) > 3):
                print("Error: Net {:s} is not a valid FPGA ball. Aborting.".formta(ballLabel))
                sys.exit(1)
            # TODO: Check: A valid ball label consists of exactly one character, followed by one or two digits.

            newSignalName = renameSignal(signalName)
            if (debug and (newSignalName != signalName)):
                print("Renaming signal {:s} to {:s}.".format(signalName, newSignalName))

            pcf.addConstraint(
                signal  = newSignalName,
                pin     = ballLabel
                )
            if debug:
                print("Constrained SPI signal {:s} to FPGA ball {:s}.".format(newSignalName, ballLabel))

    #
    # Detect all BNC connectors on the extender board
    #
    # Component designators: BNC<1-6>
    # Pin: 1
    #
    for i in range(6):
        bnc = netlist.getComponentByDesignator("BNC" + str(i+1))
        if bnc is None:
            print("Warning: BNC{:d} not found in netlist. Skipping.".format(i+1))
            continue

        pin = bnc.getPinByNumber(2)
        if pin is None:
            print("Warning: BNC{:d} component has no pins in the netlist. Skipping.".format(i+1))
            continue

        net = netlist.getNetOnPin(pin)
        if net is None:
            print("Warning: Unable to detect net on BNC{:d} pin 1. Skipping.".format(i+1))

        ballLabel = net.getLabel()
        l = len(ballLabel)
        if (l < 2) or (l > 3):
            print("Warning: BNC{:d} pin 1 is connected to illegal FPGA ball name {:s}. Skipping.".format(i+1, ballLabel))
            continue

        signalName = "bnc[{:d}]".format(i)
        pcf.addConstraint(
            signal = signalName,
            pin    = ballLabel
            )
        if debug:
            print("Constrained BNC{:d} as {:s} to FPGA ball {:s}.".format(i+1, signalName, ballLabel))

    # Sort constraints and save them to file
    #pcf.sortBySignal()
    pcf.saveToFile(filenamePCF)

    if debug:
        print("Generated pin constraits file saved to {:s}.".format(filenamePCF))


if __name__ == "__main__":
    generateFPGAExtenderPCF(
        filenameBoardNetlist        = "tango.net",
        filenameManualConstraints   = "pinout-manual.csv",
        filenamePCF                 = "pinout.pcf",
        debug = True
        )
