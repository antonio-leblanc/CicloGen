from tkinter import *
from tkinter import ttk 

from ciclogen_module.components_tab import *
from ciclogen_module.process_tab import *
from ciclogen_module.thermo_tab import *

############################################################################################
#    PARAMETERS MENU 
#############################################################################################

class ParametersMenu(ttk.Notebook):
    def __init__(self,parent,master):
        ttk.Notebook.__init__(self,parent)
        self.parent = parent
        self.master = master
        
        self.thermo_tab = ThermoTab(self)
        self.process_tab = ProcessTab(self)
    
        self.add(self.thermo_tab, text = '        Parâmetros do Ciclo            ')
        self.add(self.process_tab, text ='        Parâmetros do Processo         ')    

        # self.components_tab = ComponentsTab(self)
        # self.add(self.components_tab, text = 'Componentes')

  
 # ----------------- Geters ---------------------------
    def get_cycle_params(self):
        return self.thermo_tab.get_cycle_params()
 
    def get_process_params(self):
        return self.process_tab.get_process_params()
    
    def get_cycle_type(self):
        return self.thermo_tab.get_cycle_type()
    
    # def get_components_params(self):
    #     return self.components_tab.get_components_params()

 # ----------------- Seters ---------------------------
    
    def set_cycle_type(self, cycle_type):
        self.thermo_tab.set_cycle_type(cycle_type)
    
    def set_results(self, cycle_results):
        self.thermo_tab.set_results(cycle_results)

 # ----------------- Calculation ---------------------------
    def update_cycle(self,value):
        self.master.update_cycle()
    
    def calculate(self):
        self.master.calculate()

    # def update_components(self):
    #     components_params = self.get_components_params()
    #     thermo_inputs = {'p1':components_params['p_saida_caldeira'],
    #                      'p3':components_params['p_saida_t1'],
    #                      'p5':components_params['p_saida_t2'],
    #                      't1':components_params['t_saida_caldeira']
    #     }

    #     process_inputs = {'eficiencia_caldeira':components_params['n_caldeira']}
        
    #     self.thermo_tab.set_inputs(thermo_inputs)
    #     self.process_tab.set_displays(process_inputs)