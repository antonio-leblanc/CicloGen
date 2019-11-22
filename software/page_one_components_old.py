from tkinter import *
from tkinter import ttk 

from canvas_display import*
from thermo_cycle import *

#############################################################################################
####################################### PAGINA 1 ############################################

## 1) HEAD __________________________________________________________________

class Head(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.title = Label(self, text='SOFTWARE DE OTIMIZAÇÂO E ANALISE DE CICLOS DE RANKINE [v0.8]',font=("Helvetica", 16,'bold'), width=100, height=2, bg='#244AC6', relief=SOLID)
        self.title.grid()

## 2) LEFT MENU __________________________________________________________________

class LeftMenu(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, borderwidth=1.5, relief=SOLID)

        self.parent = parent
        self.entry_params = {}
        
        # --------------------- Styles ---------------------
        title_style= {'bg':'red', 'font':("Arial", 10,'bold'),'relief':FLAT, 'pady':4}
        sub_title_style= {'bg':'gray', 'font':("Arial", 8,'bold'), 'pady':2}
        property_style= {'bd':1, 'anchor':'w', 'pady':4, 'width':44}
        unit_style= {'bd':1, 'pady':4}

        entry_style= {'bd':1, 'relief':SOLID,'width':10, 'justify':CENTER}
        button_style= {'text' :"Calcular",'bd':2, 'cursor':'dot', 'relief':SOLID, 'font':("Arial", 10,'bold'), 'bg':'white', 'width':14}

        # --------------------- Title ------------------------------
        Label(self, text="DEFINIÇÂO DOS PARÂMETROS", **title_style).grid(row=0,column=0, columnspan=3, sticky='we')
        
        # --------------------- Labels - Column 0 and 3 ---------------------
        
        Label(self, text='Tipo de ciclo', **sub_title_style).grid(row=1, column=0, columnspan=3, sticky='ew')
        self.cycle_type = StringVar()
        cycle_opts = ['Ciclo 1: Turbina de contrapressão', 'Ciclo 2: Turbina de extração-condensação']
        ttk.OptionMenu(self, self.cycle_type, cycle_opts[0], *cycle_opts,command= self.parent.update_cycle ).grid(row=2,column=0,columnspan=3,sticky='ew')

        Label(self, text='Temperaturas', **sub_title_style).grid(row=3, column=0, columnspan=3, sticky='ew')
        Label(self, text=' (1) - Saida da Caldeira ', **property_style).grid(row=4, column=0,sticky='ew')
        Label(self, text=' Perda de temperatura entre os pontos (1) e (2)', **property_style).grid(row=5, column=0,sticky='ew')
        Label(self, text='°C', **unit_style).grid(row=4, column=2,sticky='ew')
        Label(self, text='°C', **unit_style).grid(row=5, column=2,sticky='ew')

        Label(self, text='Pressões', **sub_title_style).grid(row=6, column=0, columnspan=3,sticky='ew')
        Label(self, text=' (1) - Linha de vapor de alta pressão', **property_style).grid(row=7, column=0,sticky='ew')
        Label(self, text=' (5) - Linha de vapor de baixa pressão', **property_style).grid(row=9, column=0,sticky='ew')
        Label(self, text=' (3) - Linha de vapor de média pressão', **property_style).grid(row=8, column=0,sticky='ew')
        Label(self, text=' Perda de carga entre os pontos (1) e (2)', **property_style).grid(row=10, column=0,sticky='ew')
        Label(self, text='bar', **unit_style).grid(row=7, column=2,sticky='ew')
        Label(self, text='bar', **unit_style).grid(row=8, column=2,sticky='ew')
        Label(self, text='bar', **unit_style).grid(row=9, column=2,sticky='ew')
        Label(self, text='bar', **unit_style).grid(row=10, column=2,sticky='ew')

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
        
        Label(self, text='Processo', **sub_title_style).grid(row=16, column=0, columnspan=3,sticky='ew')
        Label(self, text=' Calor fornecido ao processo', **property_style).grid(row=17, column=0,sticky='ew')
        Label(self, text='MW', **unit_style).grid(row=17, column=2,sticky='ew')


        # --------------------- Entries - Column 1 ---------------------
        
        cycle_params = ['t1','delta_t','p1','p3','p5','delta_p','m1','f2_10','f14','f9','w_process']
        entry_rows =   [  4,        5,   7,   8,   9,       10,  12,   13,  14,  15,            17]
        init_entry_values = ['530','0','68.5','2.45','.07','-10','160','30','10','10','30']
        
        for i in range (len(cycle_params)):
            self.entry_params[cycle_params[i]] = Entry(self, **entry_style)
            self.entry_params[cycle_params[i]].insert(0,init_entry_values[i])
            self.entry_params[cycle_params[i]].grid(row=entry_rows[i],column=1)
     
        # --------------------- Button ---------------------
        # melhorar aparencia dele
        Button(self, command = lambda: self.parent.calculate(),**button_style).grid(row=19,column=0,columnspan=3,pady=3)

        # ------------------ Initialization -------------------
        self.update_cycle(1)

    def get_params(self):
        temperatures = ['t1']
        pressures = ['p1','p3','p5','delta_p']
        flow = ['m1']
        percentages = ['f2_10','f14','f9']
        work = ['w_process']
        params_dic = {}
        for key, v in self.entry_params.items():
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
        if self.cycle_type.get() == 'Ciclo 1: Turbina de contrapressão':
            return 1
        return 2

    def update_cycle(self,config):
        if config == 1:
            self.label_vazao_2_4.set(' (2) - Fração da vazão de 1 enviada a Turbina 1')
        else:
            self.label_vazao_2_4.set(' (10) - Fração de extração da Turbina')

## 3) INFO DISPLAY __________________________________________________________________

class InfoDisplay(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent, borderwidth=1.5, relief=SOLID)
        self.parent = parent

        # Dict that hold the information we want to display, passar o texto inicial como parametro do strVar
        self.state = {'name':StringVar()}
        self.component = {'name':StringVar(), 'prop':StringVar(), 'value':StringVar(),'unit':StringVar()}
       
        # ---------------------- STYLES ----------------------
        title_style= {'bg':'red', 'font':("Arial", 10,'bold'),'relief':SOLID,'bd':1, 'pady':4}
        column_0_style= {'width':15,'bd':0.5,'relief':SOLID, 'bg':'#b1b7ba'}
        column_1_3_style= {'bd':1, 'anchor':'c','relief':SOLID, 'width':6, 'pady':4, 'bg':'#b1b7ba'}
        column_2_style= {'bd':0.5, 'relief':SOLID, 'width':9, 'pady':4}


        # ---------------------- TITLE ----------------------
        Label(self, text='INFORMAÇÕES', **title_style).grid(row=0, column=0, columnspan=4, sticky='ew')
        
        # ---------------------- COLUMN 0 ----------------------
        Label(self, textvariable=self.state['name'], **column_0_style).grid(row=1, column=0, rowspan=6, sticky='nsew')
        Label(self, textvariable=self.component['name'], **column_0_style).grid(row=7, column=0, sticky='nsew')
        
        # ---------------------- COLUMN 1 ----------------------
        state_properties = [ 'T',   'P',     'H',      'S','X',    'm']
        
        for i, state_property in enumerate(state_properties):
            Label(self, text = state_property, **column_1_3_style).grid(row=1+i, column=1, sticky='ew')
        
        Label(self, textvariable = self.component['prop'], **column_1_3_style).grid(row=2+i, column=1, sticky='ew')
        
        # ---------------------- COLUMN 3 ----------------------
        properties_units = ['°C', 'bar', 'kJ/kg', 'kJ/kgK','%','ton/h']
        
        for i, property_unit in enumerate(properties_units):
            Label(self, text = property_unit, **column_1_3_style).grid(row=1+i, column=3, sticky='ew')
        
        Label(self, textvariable = self.component['unit'], **column_1_3_style).grid(row=2+i, column=3, sticky='ew')

        # ---------------------- COLUMN 2 ----------------------
        for i,state_property in enumerate(state_properties):
            self.state[state_property] = StringVar()   
            Label(self, textvariable = self.state[state_property], **column_2_style).grid(row=1+i,column=2,sticky='nsew')
        
        Label(self, textvariable = self.component['value'], **column_2_style).grid(row=2+i,column=2,sticky='nsew')
        
        
    def set_state_info(self,info):
        E = info.get('E')[1:]
        fluid_state = info.get('fluid_state')
        E = f'Ponto {E}\n\n{fluid_state}'
        T = info.get('T') - 273.15
        P = info.get('P') / 1e5
        H = info.get('H') / 1e3
        S = info.get('S') / 1e3
        X = info.get('X') *100
        m = info.get('m') * 3.6        
        
        self.state['name'].set(E)
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

## 4) RESULT DISPLAY __________________________________________________________________

class ResultDisplay(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent, borderwidth=1.5, relief=SOLID)
        self.parent = parent
        self.results = {}
        
        # ---------------------- Styles ----------------------
        title_style= {'bg':'red', 'font':("Arial", 10,'bold'),'relief':FLAT, 'pady':4}
        column_0_style= {'bd':1, 'relief':SOLID, 'pady':4, 'bg':'#b1b7ba', 'anchor':'e'}
        column_1_style= {'bd':1, 'width':9,'relief':SOLID, 'pady':4}
        column_2_style= {'bd':1, 'relief':SOLID, 'pady':4, 'bg':'#b1b7ba', 'width':4}


        # ---------------------- Title ----------------------
        Label(self, text='RESULTADOS', **title_style).grid(row=0, column=0, columnspan=3, sticky='ew')
        
        # ---------------------- Column 0 labels ----------------------
        results_lbls = ['Demanda energética das Bombas', 'Potência gerada pelas Turbinas', 'Calor fornecido à Caldeira', 
                        'Calor cedido ao Condensador','Calor fornecido ao processo', 'Eficiencia térmica']
        for i, result_lbl in enumerate(results_lbls):
            Label(self, text = result_lbl, **column_0_style).grid(row=1+i, column=0, sticky='ew')

        # ---------------------- Column 2 units ----------------------  
        units_list = ['kW','kW','kW','kW','kW','%']
        for i, unit in enumerate(units_list):   
            Label(self, text = unit, **column_2_style).grid(row=1+i, column=2, sticky='ew')

        # ---------------------- Column 1 - Values ----------------------
        resultados = ['Wb','Wt','Qh','Ql','Qp','n_th']
        for i, result in enumerate(resultados):
            self.results[result] = StringVar()
            Label(self, textvariable = self.results[result], **column_1_style).grid(row=i+1,column=1, sticky='ew')   
    
    def set_results(self,Wb,Wt,Qh,Ql,Qp,ef):
        self.results['Wb'].set(f'{Wb:,.1f}'.replace(',',' '))
        self.results['Wt'].set(f'{Wt:,.1f}'.replace(',',' '))
        self.results['Qh'].set(f'{Qh:,.1f}'.replace(',',' '))
        self.results['Ql'].set(f'{Ql:,.1f}'.replace(',',' '))
        self.results['Qp'].set(f'{Qp:,.1f}'.replace(',',' '))
        self.results['n_th'].set(f'{100*ef:.2f}')
