from tkinter import *
from tkinter import ttk 

from ciclogen_module.process_params_tab import *
from ciclogen_module.cycle_params_tab import *

############################################################################################
#    PARAMETERS MENU 
#############################################################################################

class ParametersMenu(ttk.Notebook):
    def __init__(self,parent,master):
        ttk.Notebook.__init__(self,parent)
        self.parent = parent
        self.master = master
        
        self.cycle_tab = CycleParamsTab(self)
        self.process_tab = ProcessParamsTab(self)
    
        self.add(self.cycle_tab, text = '        Parâmetros do Ciclo            ')
        self.add(self.process_tab, text ='        Parâmetros do Processo         ')    
  
 # ----------------- Geters ---------------------------
    def get_cycle_params(self):
        return self.cycle_tab.get_cycle_params()
 
    def get_process_params(self):
        return self.process_tab.get_process_params()
    
    def get_cycle_type(self):
        return self.cycle_tab.get_cycle_type()

 # ----------------- Seters ---------------------------
    
    def set_cycle_type(self, cycle_type):
        self.cycle_tab.set_cycle_type(cycle_type)
    
    def set_results(self, cycle_results):
        self.cycle_tab.set_results(cycle_results)

 # ----------------- Calculation ---------------------------
    def update_cycle(self,value):
        self.master.update_cycle()
    
    def calculate(self):
        self.master.calculate()
