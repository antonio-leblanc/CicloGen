from tkinter import *
from tkinter import ttk 

from page_two_components import *

from canvas_display import*
from thermo_cycle import *

#############################################################################################
####################################### PAGINA 1 ############################################
#############################################################################################
TITULO_CICLO_1 = 'Ciclo 1: Turbinas de contrapressão e condensação'
TITULO_CICLO_2 = 'Ciclo 2: Turbina de extração-condensação'

#############################################################################################
## 1)       HEAD 
#############################################################################################

class Head(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.title = Label(self, text='SOFTWARE DE OTIMIZAÇÂO E ANALISE DE CICLOS DE RANKINE [v0.8]',font=("Helvetica", 16,'bold'), width=104, height=2, bg='#244AC6', relief=SOLID)
        self.title.grid()

#############################################################################################
## 2)       LEFT MENU 
#############################################################################################

class LeftMenu(ttk.Notebook):
    def __init__(self,parent):
        ttk.Notebook.__init__(self,parent)
        self.parent = parent
        
        self.parameters_tab = Parameters_tab(self)
        self.components_tab = ComponentsMenu(self)
    
        self.add(self.parameters_tab, text = 'Parâmetros')
        self.add(self.components_tab, text = 'Componentes')
    

    def update_cycle(self,value):
        self.parent.update_cycle()
    
    def get_params(self):
        return self.parameters_tab.get_params()
    
    def calculate(self):
        self.parent.calculate()
    
    def get_cycle_type(self):
        return self.parameters_tab.get_cycle_type()
    
    def set_entries(self, entries_dict):
        self.parameters_tab.set_entries(entries_dict)
    
    def set_cycle_type(self, cycle_type):
        self.parameters_tab.set_cycle_type(cycle_type)

#2.1 ################################# Parameters tab #################################

class Parameters_tab(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, borderwidth=1.5, relief=SOLID)

        self.parent = parent
        self.entries = {}
                
        # --------------------- Styles ---------------------
        title_style= {'bg':'red', 'font':("Arial", 10,'bold'),'relief':FLAT, 'pady':4}
        sub_title_style= {'bg':'gray', 'font':("Arial", 8,'bold'), 'pady':2}
        property_style= {'bd':1, 'anchor':'w', 'pady':4, 'width':44}
        unit_style= {'bd':1, 'pady':4}

        entry_style= {'bd':1, 'relief':SOLID,'width':10, 'justify':CENTER}
        button_style= {'text' :"Simular",'bd':2, 'cursor':'dot', 'relief':SOLID, 'font':("Arial", 10,'bold'), 'bg':'white', 'width':14}

        # --------------------- Title ------------------------------
        Label(self, text="DEFINIÇÂO DOS PARÂMETROS", **title_style).grid(row=0,column=0, columnspan=3, sticky='we')
        
        # --------------------- Tipo de ciclo ---------------------
        Label(self, text='Tipo de ciclo', **sub_title_style).grid(row=1, column=0, columnspan=3, sticky='ew')
        self.cycle_type = StringVar()
        cycle_opts = [TITULO_CICLO_1, TITULO_CICLO_2]
        ttk.OptionMenu(self, self.cycle_type, cycle_opts[0], *cycle_opts,command= self.parent.update_cycle ).grid(row=2,column=0,columnspan=3,sticky='ew')

        # --------------------- Temperaturas ---------------------
        Label(self, text='Temperaturas', **sub_title_style).grid(row=3, column=0, columnspan=3, sticky='ew')
        
        Label(self, text=' (1) - Saida da Caldeira ', **property_style).grid(row=4, column=0,sticky='ew')
        Label(self, text=' Perda de temperatura entre os pontos (1) e (2)', **property_style).grid(row=5, column=0,sticky='ew')
        Label(self, text='°C', **unit_style).grid(row=4, column=2,sticky='ew')
        Label(self, text='°C', **unit_style).grid(row=5, column=2,sticky='ew')
        self.entries['t1'] = Entry(self, **entry_style)
        self.entries['t1'].grid(row=4,column=1)
        self.entries['delta_t'] = Entry(self, **entry_style)
        self.entries['delta_t'].grid(row=5,column=1)

        # --------------------- Pressões ---------------------
        Label(self, text='Pressões', **sub_title_style).grid(row=6, column=0, columnspan=3,sticky='ew')
        Label(self, text=' (1) - Linha de vapor de alta pressão', **property_style).grid(row=7, column=0,sticky='ew')
        Label(self, text=' (5) - Linha de vapor de baixa pressão', **property_style).grid(row=9, column=0,sticky='ew')
        Label(self, text=' (3) - Linha de vapor de média pressão', **property_style).grid(row=8, column=0,sticky='ew')
        Label(self, text=' Perda de carga entre os pontos (1) e (2)', **property_style).grid(row=10, column=0,sticky='ew')
        Label(self, text='bar', **unit_style).grid(row=7, column=2,sticky='ew')
        Label(self, text='bar', **unit_style).grid(row=8, column=2,sticky='ew')
        Label(self, text='bar', **unit_style).grid(row=9, column=2,sticky='ew')
        Label(self, text='bar', **unit_style).grid(row=10, column=2,sticky='ew')

        self.entries['p1'] = Entry(self, **entry_style)
        self.entries['p1'].grid(row=7,column=1)
        self.entries['p3'] = Entry(self, **entry_style)
        self.entries['p3'].grid(row=8,column=1)
        self.entries['p5'] = Entry(self, **entry_style)
        self.entries['p5'].grid(row=9,column=1)
        self.entries['delta_p'] = Entry(self, **entry_style)
        self.entries['delta_p'].grid(row=10,column=1)

        # --------------------- Vazões ---------------------
        self.label_vazao_2_4 = StringVar()
        Label(self, text='Vazões', **sub_title_style).grid(row=11, column=0, columnspan=3,sticky='ew')
        Label(self, text=' (1) - Vazão total do ciclo', **property_style).grid(row=12, column=0,sticky='ew')
        Label(self, textvariable =self.label_vazao_2_4, **property_style).grid(row=13, column=0,sticky='ew')
        Label(self, text='(14) - Fração da vazão de 10 enviada ao Desaerador', **property_style).grid(row=14, column=0,sticky='ew')
        Label(self, text=' (9) - Fração da vazão de 7 enviada ao Dessuperaquecedor', **property_style).grid(row=15, column=0,sticky='ew')
        Label(self, text='ton/h', **unit_style).grid(row=12, column=2,sticky='ew')
        Label(self, text='%', **unit_style).grid(row=13, column=2,sticky='ew')
        Label(self, text='%', **unit_style).grid(row=14, column=2,sticky='ew')
        Label(self, text='%', **unit_style).grid(row=15, column=2,sticky='ew')
        
        self.entries['m1'] = Entry(self, **entry_style)
        self.entries['m1'].grid(row=12,column=1)
        self.entries['f2_10'] = Entry(self, **entry_style)
        self.entries['f2_10'].grid(row=13,column=1)
        self.entries['f14'] = Entry(self, **entry_style)
        self.entries['f14'].grid(row=14,column=1)
        self.entries['f9'] = Entry(self, **entry_style)
        self.entries['f9'].grid(row=15,column=1)

        # --------------------- Processo ---------------------
        
        Label(self, text='Processo', **sub_title_style).grid(row=16, column=0, columnspan=3,sticky='ew')
        Label(self, text=' Calor fornecido ao processo', **property_style).grid(row=17, column=0,sticky='ew')
        Label(self, text=' Potência demandada por outros equipamentos', **property_style).grid(row=18, column=0,sticky='ew')
        Label(self, text='MW', **unit_style).grid(row=17, column=2,sticky='ew')
        Label(self, text='MW', **unit_style).grid(row=18, column=2,sticky='ew')

        self.entries['W_process'] = Entry(self, **entry_style)
        self.entries['W_other_equip'] = Entry(self, **entry_style)
        
        self.entries['W_process'].grid(row=17,column=1)
        self.entries['W_other_equip'].grid(row=18,column=1)
     

        # --------------------- Button ---------------------
        # melhorar aparencia dele
        Button(self, command = lambda: self.parent.calculate(),**button_style).grid(row=20,column=0,columnspan=3,pady=3)

        # ------------------ Initialization -------------------
        self.set_cycle_type(1)
    
    def set_entries(self, entries_dict):
        for entry,value in entries_dict.items():
            self.entries[entry].insert(0,value)

    def get_params(self):
        temperatures = ['t1']
        pressures = ['p1','p3','p5','delta_p']
        flow = ['m1']
        percentages = ['f2_10','f14','f9']
        work = ['W_process','W_other_equip']
        params_dic = {}
        for key, v in self.entries.items():
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
            self.label_vazao_2_4.set(' (2) - Fração da vazão de 1 enviada a Turbina 1')
        else:
            self.label_vazao_2_4.set(' (10) - Fração de extração da Turbina')

#############################################################################################
## 3)      INFO DISPLAY 
#############################################################################################

class InfoDisplay(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent, borderwidth=1.5, relief=SOLID)
        self.parent = parent
        
        self.state = {}
        self.component = {}
        state_attribute_list = ['name','fluid_state','T','P','H','S','X','m']
        component_attribute_list = ['name','prop','value','unit']
        
        for state_att in state_attribute_list:
            self.state[state_att] = StringVar()
        
        for component_att in component_attribute_list:
            self.component[component_att] = StringVar()

        # ---------------------- STYLES ----------------------
        title_style= {'bg':'red', 'font':("Arial", 10,'bold'),'relief':FLAT, 'pady':4}
        sub_title_style= {'bg':'gray', 'font':("Arial", 8,'bold'), 'pady':2}
        
        property_style= {'bd':1, 'anchor':'w', 'pady':4}
        value_style= {'bd':1, 'width':10,'relief':SOLID, 'bg':'#dbdbdb','pady':2,'padx':1}
        unit_style= {'bd':1, 'pady':4, 'width':6}
        # ---------------------- TITLE ----------------------
        Label(self, text='INFORMAÇÕES', **title_style).grid(row=0, column=0, columnspan=4, sticky='ew')
        
        # ---------------------- INFO ESTADO ----------------------
        Label(self, textvariable=self.state['name'], **sub_title_style).grid(row=1, column=0, columnspan=3, sticky='ew')
        
        Label(self, textvariable=self.state['fluid_state'], **value_style).grid(row=2, column=1, columnspan=2, sticky='ew')
        
        Label(self, text='Estado', **property_style).grid(row=2, column=0,sticky='ew')
        Label(self, text='Temperatura', **property_style).grid(row=3, column=0,sticky='ew')
        Label(self, text='Pressão', **property_style).grid(row=4, column=0,sticky='ew')
        Label(self, text='Entalpia', **property_style).grid(row=5, column=0,sticky='ew')
        Label(self, text='Entropia', **property_style).grid(row=6, column=0,sticky='ew')
        Label(self, text='Título', **property_style).grid(row=7, column=0,sticky='ew')
        Label(self, text='Vazão', **property_style).grid(row=8, column=0,sticky='ew')
        
        Label(self, textvariable = self.state['T'], **value_style).grid(row=3,column=1, sticky='ew')
        Label(self, textvariable = self.state['P'], **value_style).grid(row=4,column=1, sticky='ew') 
        Label(self, textvariable = self.state['H'], **value_style).grid(row=5,column=1, sticky='ew') 
        Label(self, textvariable = self.state['S'], **value_style).grid(row=6,column=1, sticky='ew')
        Label(self, textvariable = self.state['X'], **value_style).grid(row=7,column=1, sticky='ew')
        Label(self, textvariable = self.state['m'], **value_style).grid(row=8,column=1, sticky='ew')

        Label(self, text='°C', **unit_style).grid(row=3, column=2,sticky='ew')
        Label(self, text='bar', **unit_style).grid(row=4, column=2,sticky='ew')
        Label(self, text='kJ/kg', **unit_style).grid(row=5, column=2,sticky='ew')
        Label(self, text='kJ/kgK', **unit_style).grid(row=6, column=2,sticky='ew')
        Label(self, text='%', **unit_style).grid(row=7, column=2,sticky='ew')
        Label(self, text='ton/h', **unit_style).grid(row=8, column=2,sticky='ew')

               
    def set_state_info(self,info):
        E = info.get('E')[1:]
        E = f'Ponto {E}'
        fluid_state = info.get('fluid_state')
        T = info.get('T') - 273.15
        P = info.get('P') / 1e5
        H = info.get('H') / 1e3
        S = info.get('S') / 1e3
        X = info.get('X') *100
        m = info.get('m') * 3.6        
        
        self.state['name'].set(E)
        self.state['fluid_state'].set(fluid_state)
        self.state['T'].set(f'{T:.1f}')
        self.state['P'].set(f'{P:.2f}')
        self.state['H'].set(f'{H:.2f}')
        self.state['S'].set(f'{S:.4f}')
        self.state['X'].set(f'{X:.1f}') if X>=0 else self.state['X'].set('-')
        self.state['m'].set(f'{m:.1f}')
  
    def set_component_info(self,info):
        name = info.get('name')
        prop = info.get('prop')
        value = info.get('value')
        unit = info.get('unit')
        
        self.component['name'].set(name)        
        self.component['prop'].set(prop)
        self.component['value'].set(f'{value:,.2f}'.replace(',',' '))
        self.component['unit'].set(unit)        

#############################################################################################
## 4)    RESULT DISPLAY 
#############################################################################################

class ResultDisplay(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent, borderwidth=1.5, relief=SOLID)
        self.parent = parent
        self.results = {}
        
        results_list = ['Wb','Wt','W_other_equip','W_exceding','Qh','Ql','Qp','n_th']
        for result in results_list:
            self.results[result] = StringVar()

        # ---------------------- Styles ----------------------
        title_style= {'bg':'red', 'font':("Arial", 10,'bold'),'relief':FLAT, 'pady':4}
        sub_title_style= {'bg':'gray', 'font':("Arial", 8,'bold'), 'pady':2}
        
        property_style= {'bd':1, 'anchor':'w', 'pady':4}
        value_style= {'bd':1, 'width':9,'relief':SOLID, 'pady':2, 'bg':'#dbdbdb'}
        unit_style= {'bd':1, 'pady':4}


        # ---------------------- Title ----------------------
        Label(self, text='RESULTADOS', **title_style).grid(row=0, column=0, columnspan=3, sticky='ew')
        
        # ---------------------- Energia Elétrica ----------------------
        Label(self, text='Energia Elétrica', **sub_title_style).grid(row=1, column=0, columnspan=3, sticky='ew')
        
        Label(self, text='Potência consumida pelas bombas', **property_style).grid(row=2, column=0,sticky='ew')
        Label(self, text='Potência consumida por outros equipamentos', **property_style).grid(row=3, column=0,sticky='ew')
        Label(self, text='Potência gerada pelas Turbinas', **property_style).grid(row=4, column=0,sticky='ew')
        Label(self, text='Excedente comercializável', **property_style).grid(row=5, column=0,sticky='ew')
        
        Label(self, textvariable = self.results['Wb'], **value_style).grid(row=2,column=1, sticky='ew')
        Label(self, textvariable = self.results['W_other_equip'], **value_style).grid(row=3,column=1, sticky='ew') 
        Label(self, textvariable = self.results['Wt'], **value_style).grid(row=4,column=1, sticky='ew') 
        Label(self, textvariable = self.results['W_exceding'], **value_style).grid(row=5,column=1, sticky='ew')

        Label(self, text='kW', **unit_style).grid(row=2, column=2,sticky='ew')
        Label(self, text='kW', **unit_style).grid(row=3, column=2,sticky='ew')
        Label(self, text='kW', **unit_style).grid(row=4, column=2,sticky='ew')
        Label(self, text='kW', **unit_style).grid(row=5, column=2,sticky='ew')

        # ---------------------- Energia Térmica ----------------------
        Label(self, text='Energia Térmica', **sub_title_style).grid(row=6, column=0, columnspan=3, sticky='ew')
        
        Label(self, text='Calor fornecido a Caldeira', **property_style).grid(row=7, column=0,sticky='ew')
        Label(self, text='Calor cedido ao condensador', **property_style).grid(row=8, column=0,sticky='ew')
        Label(self, text='Calor cedido ao processo', **property_style).grid(row=9, column=0,sticky='ew')
        
        Label(self, textvariable = self.results['Qh'], **value_style).grid(row=7,column=1, sticky='ew')
        Label(self, textvariable = self.results['Ql'], **value_style).grid(row=8,column=1, sticky='ew') 
        Label(self, textvariable = self.results['Qp'], **value_style).grid(row=9,column=1, sticky='ew') 

        Label(self, text='kW', **unit_style).grid(row=7, column=2,sticky='ew')
        Label(self, text='kW', **unit_style).grid(row=8, column=2,sticky='ew')
        Label(self, text='kW', **unit_style).grid(row=9, column=2,sticky='ew')

        # ---------------------- Indices de desempenho ----------------------
        Label(self, text='Indices de desempenho', **sub_title_style).grid(row=10, column=0, columnspan=3, sticky='ew')
        
        Label(self, text='Eficiência Térmica', **property_style).grid(row=11, column=0,sticky='ew')
        
        Label(self, textvariable = self.results['n_th'], **value_style).grid(row=11,column=1, sticky='ew')

        Label(self, text='%', **unit_style).grid(row=11, column=2,sticky='ew')

    def set_results(self, results):
        Wb = results.get('Wb') / 1000
        Wt = results.get('Wt') / 1000
        Qh = results.get('Qh') / 1000
        Ql = results.get('Ql') / 1000
        Qp = results.get('Qp') / 1000
        
        W_other_equip = results.get('W_other_equip') / 1000
        W_exceding = results.get('W_exceding') / 1000
        n_th = results.get('n_th')

        self.results['Wb'].set(f'{Wb:,.1f}'.replace(',',' '))
        self.results['Wt'].set(f'{Wt:,.1f}'.replace(',',' '))
        self.results['Qh'].set(f'{Qh:,.1f}'.replace(',',' '))
        self.results['Ql'].set(f'{Ql:,.1f}'.replace(',',' '))
        self.results['Qp'].set(f'{Qp:,.1f}'.replace(',',' '))
        self.results['W_other_equip'].set(f'{W_other_equip:,.1f}'.replace(',',' '))
        self.results['W_exceding'].set(f'{W_exceding:,.1f}'.replace(',',' '))
        self.results['n_th'].set(f'{100*n_th:.2f}')
