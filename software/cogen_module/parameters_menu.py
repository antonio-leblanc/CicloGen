from tkinter import *
from tkinter import ttk 

from cogen_module.components_menu import *
from cogen_module.process_menu import *
from cogen_module.thermo_menu import *

############################################################################################
#    PARAMETERS MENU 
#############################################################################################

class ParametersMenu(ttk.Notebook):
    def __init__(self,parent):
        ttk.Notebook.__init__(self,parent)
        self.parent = parent
        
        self.thermo_tab = ThermoMenu(self)
        self.components_tab = ComponentsMenu(self)
        self.process_tab = ProcessMenu(self)
    
        self.add(self.thermo_tab, text = 'Parâmetros')
        self.add(self.components_tab, text = 'Componentes')
        self.add(self.process_tab, text = 'Processo')    

    def update_cycle(self,value):
        self.parent.update_cycle()
    
    def get_cycle_params(self):
        return self.thermo_tab.get_cycle_params()

    def get_components_params(self):
        return self.components_tab.get_components_params()
    
    def calculate(self):
        self.parent.calculate()
    
    def get_cycle_type(self):
        return self.thermo_tab.get_cycle_type()
    
    def set_entries(self, inputs_dict):
        self.thermo_tab.set_entries(inputs_dict)
    
    def set_cycle_type(self, cycle_type):
        self.thermo_tab.set_cycle_type(cycle_type)