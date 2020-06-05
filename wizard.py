#!/usr/bin/python3

#
# This wizard parses a project configuration file
# for the FPGA extender board and generates the
# requested source code files.
#

import sys
from wizard_config import WizardConfigJSON
from wizard_code_generator import WizardCodeGenerator


def runWizard(filename=None, plaintext=None):
    config = WizardConfigJSON(filename=filename, plaintext=plaintext)
    code_generator = WizardCodeGenerator(config)
    code_generator.stats()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: wizard.py <configuration file>")
        sys.exit(1)

    runWizard(filename=sys.argv[1])
