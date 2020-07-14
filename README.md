
With the port wizard an attempt is made to simplify the
generation of the pinout configuration for a logic design.
It analyzes an (already imported) netlist and uses a simple
port usage configuration to generate Verilog input/output module ports.

With the created GUI for the FPGA Extender PCB the user is
enabled to choose an option in the dropdown menu for each
of the 18 available ports on the board.
The GUI is structured in a model-view-controller pattern (MVC).
A config.py and the main.py are added instead of the model window.
The controller does not require any information of the view model. 

To start the GUI the user has to open main.py which
initializes the constructor of the class Controller. 
The constructor of the controller initializes the constructor of
the class Config and of the class View.

The view model is populating the background, the dropdown 
menu and the buttons in a popup window.
The save button opens another popup window which provides
the data type option that the user want to save the current
setting in. The user is enabled to choose a name and the 
data type. The close button closes the GUI window and stops
the program by leaving the program loop. 
The dropwdown menues offer five options: Empty, ADC, DAC, 
Nucleo. 
After the user finallized the desired settings the chosen 
options and the associated port will be saved in the file.
By saving the file with the same name as it already exists 
in the chosen directory, it overwrites the old file.
