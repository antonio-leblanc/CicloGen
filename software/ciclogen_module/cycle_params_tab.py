from tkinter import *
from tkinter import ttk
import ciclogen_module.init_values as init_values

#############################################################################################

TITULO_CICLO_1 = 'Ciclo A : Turbinas de contrapressão e condensação'
TITULO_CICLO_2 = 'Ciclo B : Turbina de extração-condensação'

cycle_inputs = init_values.cycle_inputs
#############################################################################################

class CycleParamsTab(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, borderwidth=1.5, relief=SOLID)

        self.parent = parent
        self.inputs = {}
        self.displays = {}
        self.grid_columnconfigure(0, weight=1)
                
        # --------------------- Styles ---------------------
        self.title_style= {'font':'Arial 11 bold','bg':'#5c7399', 'pady':4, 'relief':'solid'}
        self.sub_title_style= {'font':'Arial 10 bold','bg':'gray', 'pady':1, 'relief':'solid'}

        self.property_style= {'font':'Arial 11','anchor':'w', 'pady':2, 'padx':1}
        self.entry_style= {'font':'Arial 11', 'bd':1, 'relief':SOLID,'width':10, 'justify':CENTER}
        self.value_style= {'font':'Arial 11', 'bd':1, 'relief':SOLID, 'bg':'gray90','width':9}
        self.unit_style= {'font':'Arial 11', 'pady':2, 'padx':4}
        
        style = ttk.Style()
        style.configure('my.TMenubutton', font=('Helvetica', 11))

        # ---------------------- Grids ----------------------
        self.title_grid= {'column':0, 'columnspan':3, 'sticky':'we'}
        self.property_grid = {'column':0 , 'sticky':'ew'}
        self.entry_grid = {'column':1}
        self.value_grid = {'column':1,'sticky':'ew'}
        self.unit_grid = {'column':2 , 'sticky':'ew','padx':1}

        # --------------------- Title ------------------------------
        self.row = 0
        self.create_title("Parâmetros do Ciclo Termodinâmico", self.title_style)
        # --------------------- Tipo de ciclo ---------------------
        self.create_title('Tipo de Ciclo', self.sub_title_style)

        self.cycle_type = StringVar()
        cycle_opts = [TITULO_CICLO_1, TITULO_CICLO_2]
        ttk.OptionMenu(self, self.cycle_type, cycle_opts[0], *cycle_opts,command= self.parent.update_cycle, style='my.TMenubutton' ).grid(row=self.row,column=0,columnspan=3,sticky='ew')
        self.row+=1

        # --------------------- Temperaturas ---------------------
        self.create_title('Temperaturas', self.sub_title_style)
        
        self.create_input('t1','(1) - Temperatura de saida da caldeira','°C')
        self.create_input('delta_t','Perda de temperatura entre os pontos (1) e (2)','°C')


        # --------------------- Pressões ---------------------
        self.create_title('Pressões', self.sub_title_style)

        self.create_input('p1','(1) - Linha de vapor de alta pressão','bar')
        self.create_input('p3','(5) - Linha de vapor de média pressão','bar')
        self.create_input('p5','(3) - Linha de vapor de baixa pressão','bar')
        self.create_input('delta_p','Perda de carga entre os pontos (1) e (2)','bar')
        
        
        # --------------------- Vazões ---------------------
        self.create_title('Vazões', self.sub_title_style)
        self.create_input('m1','(1) - Vazão total do ciclo','t/h')
        self.create_display('vazao_max_disponivel','Capacidade de geração de vapor - base PCI','t/h')
        
        self.label_vazao_2_4 = StringVar()
        Label(self, textvariable =self.label_vazao_2_4, **self.property_style).grid(row=self.row, **self.property_grid)
        Label(self, text='%', **self.unit_style).grid(row=self.row, **self.unit_grid)
        self.inputs['f2_10'] = Entry(self, **self.entry_style)
        self.inputs['f2_10'].grid(row=self.row,column=1)
        self.row+=1
        
        self.create_input('f14','(14) - Fração de (10) enviada ao desaerador','%')
        self.create_input('f9','(9) - Fração de (7) enviada ao dessuperaquecedor','%')
        
        self.create_display('m_vapor_p_necessario','Vazão necessária no processo','t/h')
        self.create_display('m_vapor_p_disp','Vazão disponível no processo','t/h')

                
        # --------------------- Eficiencias ---------------------
        self.create_title('Eficiências dos Equipamentos', self.sub_title_style)
        self.create_input('n_cald','Eficiência da caldeira','%')
        self.create_input('n_t1','Eficiência da turbina 1','%')
        self.create_input('n_t2','Eficiência da turbina 2','%')
        self.create_input('n_b1','Eficiência da bomba 1','%')
        self.create_input('n_b2','Eficiência da bomba 2','%')


        # ------------------ Initialization -------------------
        self.set_cycle_type(1)
    
        self.set_inputs(cycle_inputs)
    
############################### METHODS ###############################

    def get_cycle_params(self):
        temperatures = ['t1']
        pressures = ['p1','p3','p5','delta_p']
        flow = ['m1']
        percentages = ['f2_10','f14','f9','n_cald','n_t1','n_t2','n_b1','n_b2']
        params_dic = {}
        for key, v in self.inputs.items():
            value = float(v.get().replace(',','.'))
            value = value + 273.15 if key in temperatures else value  # Convert [C] to [K]
            value = value * 1e5 if key in pressures else value        # Convert [bar] to [Pa]
            value = value / 3.6 if key in flow else value             # Convert [t/h] to [kg/s]
            value = value/100 if key in percentages else value        # Convert % to number

            params_dic[key] = value

        params_dic['cycle_type'] = self.get_cycle_type()
        # print(params_dic)
        return params_dic
    
    def get_cycle_type(self):
        if self.cycle_type.get() == TITULO_CICLO_1:
            return 1
        return 2

# ------------------------------Seters-------------------------------- "

    def set_cycle_type(self, cycle_config):
        if cycle_config == 1:
            self.label_vazao_2_4.set('(2) - Fração de (1) enviada a turbina 1')
        else:
            self.label_vazao_2_4.set('(10) - Fração de extração da turbina')

    def set_inputs(self, inputs_dict):
        for key,value in inputs_dict.items():
            if key in self.inputs.keys():
                self.inputs[key].delete(0, 'end')
                self.inputs[key].insert(0,value)

    def set_results(self, results):
        m_vapor_p_necessario = results['m_vapor_p_necessario']
        m_vapor_p_disp = results['m_vapor_p_disp']
        vazao_max_disponivel      = results['vazao_max_disponivel']

        self.displays['m_vapor_p_necessario'].set(f'{m_vapor_p_necessario:.1f}')
        self.displays['m_vapor_p_disp'].set(f'{m_vapor_p_disp:.1f}')
        self.displays['vazao_max_disponivel'].set(f'{vazao_max_disponivel:.1f}')


# ------------------------------Frontend-------------------------------- "

    def create_input(self,id,text,unit):
        Label(self, text=text, **self.property_style).grid(row=self.row, **self.property_grid)
        Label(self, text=unit, **self.unit_style).grid(row=self.row, **self.unit_grid)
        self.inputs[id] = Entry(self, **self.entry_style)
        self.inputs[id].grid(row=self.row, **self.entry_grid)
        self.row+=1

    def create_title(self,text,style):
        Label(self, text=text, **style).grid(row=self.row, **self.title_grid)
        self.row+=1

    
    def create_display(self,id,text,unit):
        self.displays[id] = StringVar()
        Label(self, text=text, **self.property_style).grid(row=self.row, **self.property_grid)
        Label(self, textvariable = self.displays[id], **self.value_style).grid(row=self.row,**self.value_grid)        
        Label(self, text=unit, **self.unit_style).grid(row=self.row, **self.unit_grid)
        self.row+=1

