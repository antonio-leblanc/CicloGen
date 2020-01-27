from tkinter import *
from tkinter import ttk 

from cogen_module.components_tab import *
from cogen_module.process_tab import *
from cogen_module.thermo_tab import *

############################################################################################
#    PARAMETERS MENU 
#############################################################################################

class ParametersMenu(ttk.Notebook):
    def __init__(self,parent):
        ttk.Notebook.__init__(self,parent)
        self.parent = parent
        
        self.thermo_tab = ThermoTab(self)
        self.components_tab = ComponentsTab(self)
        self.process_tab = ProcessTab(self)
    
        self.add(self.thermo_tab, text = 'Ciclo')
        self.add(self.components_tab, text = 'Componentes')
        self.add(self.process_tab, text = 'Processo')    



 # ----------------- Geters ---------------------------
    def get_cycle_params(self):
        return self.thermo_tab.get_cycle_params()

    def get_components_params(self):
        return self.components_tab.get_components_params()
    
    def get_process_params(self):
        return self.process_tab.get_process_params()
    
    def get_cycle_type(self):
        return self.thermo_tab.get_cycle_type()
    
 # ----------------- Seters ---------------------------
    
    def set_cycle_type(self, cycle_type):
        self.thermo_tab.set_cycle_type(cycle_type)
    
    def set_results(self, cycle_results):
        self.thermo_tab.set_results(cycle_results)

 # ----------------- Calculation ---------------------------
    def update_cycle(self,value):
        self.parent.update_cycle()
    
    def update_components(self):
        components_params = self.get_components_params()
        thermo_inputs = {'p1':components_params['p_saida_caldeira'],
                         'p3':components_params['p_saida_t1'],
                         'p5':components_params['p_saida_t2'],
                         't1':components_params['t_saida_caldeira']
        }

        process_inputs = {'eficiencia_caldeira':components_params['n_caldeira']}
        
        self.thermo_tab.set_inputs(thermo_inputs)
        self.process_tab.set_displays(process_inputs)

    def calculate(self):
        self.parent.calculate()