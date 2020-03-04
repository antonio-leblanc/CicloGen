from tkinter import *
from tkinter import ttk
import ciclogen_module.init_values as init_values

process_inputs = init_values.process_inputs

class ProcessParamsTab(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, borderwidth=1.5, relief=SOLID)
        self.parent = parent
        self.inputs = {}
        self.displays = {}

        self.grid_columnconfigure(0, weight=1)

        # --------------------- Styles ---------------------
        self.title_style= {'bg':'#5c7399', 'font':'Arial 11 bold', 'pady':4, 'relief':'solid'}
        self.sub_title_style= {'bg':'gray', 'font':'Arial 10 bold', 'pady':1, 'relief':'solid'}
        
        self.property_style= {'font':'Arial 11', 'anchor':'w', 'pady':3}
        self.entry_style= {'font':'Arial 11', 'bd':1, 'relief':SOLID,'width':10, 'justify':CENTER}
        self.value_style= {'font':'Arial 11', 'bd':1, 'relief':SOLID, 'bg':'gray90','width':8}
        self.unit_style= {'font':'Arial 11','padx':2}

        self.title_grid= {'column':0, 'columnspan':3, 'sticky':'we'}
        self.property_grid = {'column':0 , 'sticky':'ew'}
        self.value_grid = {'column':1, 'sticky':'ew'}
        self.entry_grid = {'column':1,'sticky':'ew'}
        self.unit_grid = {'column':2 , 'sticky':'ew'}
        
        # --------------------- Title ------------------------------
        self.row = 0
        self.create_title("Parâmetros do Processo Industrial",self.title_style,self.title_grid)
        
        # --------------------- Safra ---------------------
        self.create_title("Capacidade de Produção",self.sub_title_style,self.title_grid)

        self.create_input('m_cana_hora','Vazão mássica de cana moída - hora','t.cana/h')
        self.create_display('m_cana_dia','Vazão mássica de cana moída - dia','t.cana/dia')
        self.create_input('dias_operacao','Dias de operação por safra','dias/safra')
        self.create_display('m_cana_safra','Cana processada por safra','t.cana/safra')
        
        # --------------------- Energia disp ---------------------

        self.create_title("Fonte Primária de Energia",self.sub_title_style,self.title_grid)

        self.create_input('fracao_bagaco_cana',"Fração de bagaço na cana",'%')
        self.create_display('m_bag_tot',"Produção total de bagaço",'t.bag/h')
        self.create_input('pci_bagaco',"PCI do bagaço",'kJ/kg')
        self.create_display('Q_disp',"Potência térmica disponível - base PCI",'KW')
        
        # --------------------- Energia disp ---------------------
        
        self.create_title("Demanda Energética do Processo",self.sub_title_style,self.title_grid)
        
        self.create_input('consumo_vapor',"Consumo de vapor no processo",'kg.vap/t.cana')
        self.create_display('m_vapor_p_necessario',"Vazão de vapor necessária no processo",'t.vap/h')
        self.create_input('t_saida_processo',"Temperatura de saída do vapor de processo",'ºC')
        self.create_input('demanda_mecanica_equip',"Demanda energética mecânica específica",'kWh/t.cana')
        self.create_input('demanda_eletrica_equip',"Demanda energética elétrica específica",'kWh/t.cana')
        self.create_display('W_planta',"Potência total demandada",'kW')
       
        button_style = {'text' :'Atualizar Dados','bd':1, 'relief':SOLID, 'font':'Arial 10 bold', 'bg':'white'}
        Button(self,**button_style, command = lambda: self.calculate_displays()).grid(row=self.row+1,column=0, columnspan=3, pady=4, sticky='ew')
        

        # --------------------- Inicializando ---------------------
        
        self.set_inputs(process_inputs)

############################### METHODS ###############################
   
    def calculate_displays(self):
        m_cana_hora = self.get_input('m_cana_hora')
        dias_operacao       = self.get_input('dias_operacao')
        pci_bagaco          = self.get_input('pci_bagaco')                 #[kj/kg]
        fracao_bagaco_cana  = self.get_input('fracao_bagaco_cana') /100
        consumo_vapor       = self.get_input('consumo_vapor')             #[kg/ton]
        demanda_mecanica_equip = self.get_input('demanda_mecanica_equip') #[kWh/ton]
        demanda_eletrica_equip = self.get_input('demanda_eletrica_equip') #[kWh/ton]


        m_cana_dia = m_cana_hora*24         #[t/dia]
        m_cana_safra = m_cana_dia*dias_operacao
        
        m_bag_tot = fracao_bagaco_cana*m_cana_hora     #[t/h]
       
        Q_disp = m_bag_tot*pci_bagaco/3.6                   #[KW]

        m_vapor_p_necessario = m_cana_hora*consumo_vapor/1000   #[t.vapor/h]

        W_planta=(demanda_mecanica_equip+demanda_eletrica_equip)*m_cana_hora #[kW]

        self.set_kdisplay('m_cana_dia',m_cana_dia)
        self.set_kdisplay('m_cana_safra',m_cana_safra)
        self.set_display_1f('m_bag_tot',m_bag_tot)
        self.set_kdisplay('Q_disp',Q_disp)
        self.set_kdisplay('m_vapor_p_necessario',m_vapor_p_necessario)
        self.set_kdisplay('W_planta',W_planta)
        
    def set_inputs(self, inputs_dict):
        for key,value in inputs_dict.items():
            self.inputs[key].insert(0,value)
    
    def set_kdisplay(self,id,value):
        self.displays[id].set(f'{value:,.0f}'.replace(',',' '))
    def set_display_1f(self,id,value):
        self.displays[id].set(f'{value:,.1f}')

#--------------------------Geters------------------------------------#

    def get_process_params(self):
        self.calculate_displays()

        m_cana_hora = self.get_input('m_cana_hora') /3.6                      # [kg/s]       
        dias_operacao = self.get_input('dias_operacao')                       # [dias/ano]       
        Q_disp = self.get_display('Q_disp')*1e3                               # [W]
        W_planta = self.get_display('W_planta')*1e3                           # [W]
        t_saida_processo   =  self.get_input('t_saida_processo') + 273.15     # [K]
        m_vapor_p_necessario = self.get_display('m_vapor_p_necessario') / 3.6 # [kg/s]
        pci_bagaco          = self.get_input('pci_bagaco') *1000              # [J/kg]
        m_bag_tot = self.get_display('m_bag_tot') /3.6                        # [kg/s]

        
        process_params = {
            'Q_disp':Q_disp,
            'm_cana_hora':m_cana_hora,
            'dias_operacao':dias_operacao,
            't_saida_processo':t_saida_processo,
            'm_vapor_p_necessario':m_vapor_p_necessario,
            'W_planta':W_planta,
            'PCI':pci_bagaco,
            'm_bag_tot':m_bag_tot}
        return process_params

    def get_input(self, input_id):
        return float(self.inputs[input_id].get().replace(',','.'))

    def get_display(self, display_id):
        return float(self.displays[display_id].get().replace(' ',''))


#--------------------------Frontend------------------------------------#

    def create_title(self,text,style,column_grid):
        Label(self, text=text, **style).grid(row=self.row, **column_grid)
        self.row+=1


    def create_display(self,id,text,unit):
        self.displays[id] = StringVar()
        Label(self, text=text, **self.property_style).grid(row=self.row, **self.property_grid)
        Label(self, textvariable = self.displays[id], **self.value_style).grid(row=self.row,**self.value_grid)        
        Label(self, text=unit, **self.unit_style).grid(row=self.row, **self.unit_grid)
        self.row+=1

    def create_input(self,id,text,unit):
        Label(self, text=text, **self.property_style).grid(row=self.row, **self.property_grid)
        Label(self, text=unit, **self.unit_style).grid(row=self.row, **self.unit_grid)
        self.inputs[id] = Entry(self, **self.entry_style)
        self.inputs[id].grid(row=self.row, **self.entry_grid)
        self.row+=1
