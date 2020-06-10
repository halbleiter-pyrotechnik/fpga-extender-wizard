#!/usr/bin/python3

#
# This wizard parses a project configuration file
# for the FPGA extender board and generates the
# requested source code files.
#

import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from config import Config
from code_generator import CodeGenerator


def runWizard(filename=None, plaintext=None):
    config = Config(importFile=filename, importJSON=plaintext)
    code_generator = CodeGenerator(config)
    code_generator.stats()
    code_generator.exportVerilog()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: wizard.py <configuration file>")
        sys.exit(1)

    runWizard(filename=sys.argv[1])
