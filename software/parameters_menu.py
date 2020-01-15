from tkinter import *
from tkinter import ttk 

from components_menu import *
from process_menu import *
from result_display import *
from info_display import *

from canvas_display import*
from thermo_cycle import *

#############################################################################################
####################################### PAGINA 1 ############################################
#############################################################################################

TITULO_SOFTWARE = 'SOFTWARE DE SIMULAÇÂO E ANALISE DE CICLOS DE RANKINE COM COGERAÇÂO [v0.9]'
TITULO_CICLO_1 = 'Ciclo 1: Turbinas de contrapressão e condensação'
TITULO_CICLO_2 = 'Ciclo 2: Turbina de extração-condensação'

#############################################################################################
## 1)       HEAD 
#############################################################################################

class Head(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, borderwidth=1.5, relief=SOLID)

        self.title = Label(self, text=TITULO_SOFTWARE,font='Helvetica 16 bold',pady=8, bg='#244AC6')
        self.grid_columnconfigure(0, weight=1)
        self.title.grid(sticky='ew')

#############################################################################################
## 2)       PARAMETERS MENU 
#############################################################################################

class ParametersMenu(ttk.Notebook):
    def __init__(self,parent):
        ttk.Notebook.__init__(self,parent)
        self.parent = parent
        
        self.parameters_tab = ThermoMenu(self)
        self.components_tab = ComponentsMenu(self)
        self.process_tab = ProcessMenu(self)
    
        self.add(self.parameters_tab, text = 'Parâmetros')
        self.add(self.components_tab, text = 'Componentes')
        self.add(self.process_tab, text = 'DadosProcesso')    

    def update_cycle(self,value):
        self.parent.update_cycle()
    
    def get_cycle_params(self):
        return self.parameters_tab.get_cycle_params()

    def get_components_params(self):
        return self.components_tab.get_components_params()
    
    def calculate(self):
        self.parent.calculate()
    
    def get_cycle_type(self):
        return self.parameters_tab.get_cycle_type()
    
    def set_entries(self, inputs_dict):
        self.parameters_tab.set_entries(inputs_dict)
    
    def set_cycle_type(self, cycle_type):
        self.parameters_tab.set_cycle_type(cycle_type)

#2.1 ################################# Thermo tab #################################

class ThermoMenu(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, borderwidth=1.5, relief=SOLID)

        self.parent = parent
        self.inputs = {}
                
        # --------------------- Styles ---------------------
        self.title_style= {'font':'Arial 11 bold','bg':'red', 'pady':4}
        self.sub_title_style= {'font':'Arial 10 bold','bg':'gray', 'pady':1}

        self.property_style= {'font':'Arial 11','anchor':'w', 'pady':2, 'padx':1}
        self.entry_style= {'bd':1, 'relief':SOLID,'width':10, 'justify':CENTER}
        self.unit_style= {'font':'Arial 11', 'pady':2}
        
        # ---------------------- Grids ----------------------
        self.title_grid= {'column':0, 'columnspan':3, 'sticky':'we'}
        self.property_grid = {'column':0 , 'sticky':'ew'}
        self.entry_grid = {'column':1}
        self.unit_grid = {'column':2 , 'sticky':'ew'}

        # --------------------- Title ------------------------------
        row = 0
        row = self.create_title("Parâmetros do ciclo Termodinâmico", self.title_style,row)
        # --------------------- Tipo de ciclo ---------------------
        row = self.create_title('Tipo de ciclo', self.sub_title_style,row)

        self.cycle_type = StringVar()
        cycle_opts = [TITULO_CICLO_1, TITULO_CICLO_2]
        ttk.OptionMenu(self, self.cycle_type, cycle_opts[0], *cycle_opts,command= self.parent.update_cycle ).grid(row=row,column=0,columnspan=3,sticky='ew')
        row+=1

        # --------------------- Temperaturas ---------------------
        row = self.create_title('Temperaturas', self.sub_title_style,row)
        
        row = self.create_input('t1','(1) - Saida da Caldeira','°C',row)
        row = self.create_input('delta_t','Perda de temperatura entre os pontos (1) e (2)','°C',row)


        # --------------------- Pressões ---------------------
        row = self.create_title('Pressões', self.sub_title_style,row)

        row = self.create_input('p1','(1) - Linha de vapor de alta pressão','bar',row)
        row = self.create_input('p3','(5) - Linha de vapor de baixa pressão','bar',row)
        row = self.create_input('p5','(3) - Linha de vapor de média pressão','bar',row)
        row = self.create_input('delta_p','Perda de carga entre os pontos (1) e (2)','bar',row)
        
        # --------------------- Vazões ---------------------
        row = self.create_title('Vazões', self.sub_title_style,row)
        row = self.create_input('m1','(1) - Vazão total do ciclo','ton/h',row)
        
        self.label_vazao_2_4 = StringVar()
        Label(self, textvariable =self.label_vazao_2_4, **self.property_style).grid(row=row, **self.property_grid)
        Label(self, text='%', **self.unit_style).grid(row=row, **self.unit_grid)
        self.inputs['f2_10'] = Entry(self, **self.entry_style)
        self.inputs['f2_10'].grid(row=row,column=1)
        row+=1
        
        row = self.create_input('f14','(14) - Fração de (10) enviada ao Desaerador','%',row)
        row = self.create_input('f9','(9) - Fração de (7) enviada ao Dessuperaquecedor','%',row)


        # --------------------- Processo ---------------------
        
        row = self.create_title('Processo', self.sub_title_style,row)
        row = self.create_input('W_process','Calor fornecido ao processo','MW',row)
        row = self.create_input('W_other_equip','Potência demandada por outros equipamentos','MW',row)

        # ------------------ Initialization -------------------
        self.set_cycle_type(1)
    
        entries_init_values = {'t1': '530', 'delta_t': '0', 'p1': '68', 'p3': '2.5', 'p5': '.08', 
        'delta_p': '-10', 'm1': '160', 'f2_10': '30', 'f14': '10', 'f9': '40', 'W_process': '30','W_other_equip':'10'}
        self.set_inputs(entries_init_values)
    
    def create_input(self,id,text,unit,row):
        Label(self, text=text, **self.property_style).grid(row=row, **self.property_grid)
        Label(self, text=unit, **self.unit_style).grid(row=row, **self.unit_grid)
        self.inputs[id] = Entry(self, **self.entry_style)
        self.inputs[id].grid(row=row, **self.entry_grid)
        return row+1

    def create_title(self,text,style,row):
        Label(self, text=text, **style).grid(row=row, **self.title_grid)
        return row+1

    def set_inputs(self, inputs_dict):
        for entry,value in inputs_dict.items():
            self.inputs[entry].insert(0,value)

    def get_cycle_params(self):
        temperatures = ['t1']
        pressures = ['p1','p3','p5','delta_p']
        flow = ['m1']
        percentages = ['f2_10','f14','f9']
        work = ['W_process','W_other_equip']
        params_dic = {}
        for key, v in self.inputs.items():
            value = float(v.get())
            value = value + 273.15 if key in temperatures else value  # Convert [C] to [K]
            value = value * 1e5 if key in pressures else value        # Convert [bar] to [Pa]
            value = value / 3.6 if key in flow else value             # Convert [ton/h] to [kg/s]
            value = value * 1e6 if key in work else value             # Convert to [MW] to [W]
            value = value/100 if key in percentages else value        # Convert % to number

            params_dic[key] = value

        params_dic['cycle_type'] = self.get_cycle_type()
        print(params_dic)
        return params_dic
    
    def get_cycle_type(self):
        if self.cycle_type.get() == TITULO_CICLO_1:
            return 1
        return 2

    def set_cycle_type(self, cycle_config):
        if cycle_config == 1:
            self.label_vazao_2_4.set('(2) - Fração de (1) enviada a Turbina 1')
        else:
            self.label_vazao_2_4.set('(10) - Fração de extração da Turbina')

