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

        self.create_input('capacidade_moagem_h','Capacidade de moagem por hora','t.cana/h')
        self.create_display('capacidade_moagem_d','Capacidade de moagem por dia','t.cana/dia')
        self.create_input('dias_operacao','Dias de operação','dias/safra')
        self.create_display('capacidade_moagem_safra','Capacidade de moagem por safra','t.cana/safra')
        
        # --------------------- Energia disp ---------------------

        self.create_title("Energia Disponível",self.sub_title_style,self.title_grid)

        self.create_input('fracao_bagaco_cana',"Fração de bagaço seco na cana",'%')
        self.create_display('m_bag_tot',"Produção total de bagaço",'t.bag/h')
        self.create_input('pci_bagaco',"PCI do bagaço",'kJ/kg')
        self.create_display('mPCI_disp',"Energia disponível - base PCI",'KW')
        
        # --------------------- Energia disp ---------------------
        
        self.create_title("Demanda Energética do Processo",self.sub_title_style,self.title_grid)
        
        self.create_input('consumo_vapor',"Consumo de vapor no processo",'kg.vap/t.cana')
        self.create_display('vazao_vapor',"Vazão de vapor necessária no processo",'t.vap/h')
        self.create_input('t_saida_processo',"Temperatura de saída do vapor de processo",'ºC')
        self.create_input('demanda_mecanica_equip',"Demanda energética mecânica específica",'kWh/t.cana')
        self.create_input('demanda_eletrica_equip',"Demanda energética elétrica específica",'kWh/t.cana')
        self.create_display('potencia_demandada',"Potência total demandada",'kW')
       
        button_style = {'text' :'Atualizar Dados','bd':1, 'relief':SOLID, 'font':'Arial 10 bold', 'bg':'white'}
        Button(self,**button_style, command = lambda: self.calculate_displays()).grid(row=self.row+1,column=0, columnspan=3, pady=4, sticky='ew')
        

        # --------------------- Inicializando ---------------------
        
        self.set_inputs(process_inputs)

############################### METHODS ###############################
   
    def calculate_displays(self):
        capacidade_moagem_h = self.get_input('capacidade_moagem_h')
        dias_operacao       = self.get_input('dias_operacao')
        pci_bagaco          = self.get_input('pci_bagaco')
        fracao_bagaco_cana  = self.get_input('fracao_bagaco_cana') /100
        consumo_vapor       = self.get_input('consumo_vapor')
        demanda_mecanica_equip = self.get_input('demanda_mecanica_equip')
        demanda_eletrica_equip = self.get_input('demanda_eletrica_equip')


        capacidade_moagem_d = capacidade_moagem_h*24         #[t/dia]
        capacidade_moagem_safra = capacidade_moagem_d*dias_operacao
        
        m_bag_tot = fracao_bagaco_cana*capacidade_moagem_h   #[t/h]
       
        mPCI_disp = m_bag_tot*pci_bagaco/3.6     #[KW]

        vazao_vapor = capacidade_moagem_h*consumo_vapor/1000   #[t.vapor/h]

        potencia_demandada=(demanda_mecanica_equip+demanda_eletrica_equip)*capacidade_moagem_h #[kW]

        self.set_kdisplay('capacidade_moagem_d',capacidade_moagem_d)
        self.set_kdisplay('capacidade_moagem_safra',capacidade_moagem_safra)
        self.set_display_1f('m_bag_tot',m_bag_tot)
        self.set_kdisplay('mPCI_disp',mPCI_disp)
        self.set_kdisplay('vazao_vapor',vazao_vapor)
        self.set_kdisplay('potencia_demandada',potencia_demandada)
        
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

        capacidade_moagem_h = self.get_input('capacidade_moagem_h') /3.6  # [kg/s]       
        dias_operacao = self.get_input('dias_operacao')                   # [dias/ano]       
        mPCI_disp = self.get_display('mPCI_disp')*1e3                     # [W]
        potencia_demandada = self.get_display('potencia_demandada')*1e3   # [W]
        t_saida_processo   =  self.get_input('t_saida_processo') + 273.15 # [K]
        vazao_vapor        = self.get_display('vazao_vapor') / 3.6        # [kg/s]
        pci_bagaco          = self.get_input('pci_bagaco')                # [kJ/kg]
        m_bag_tot = self.get_display('m_bag_tot') /3.6                    # [kg/s]

        
        process_params = {
            'mPCI_disp':mPCI_disp,
            'capacidade_moagem_h':capacidade_moagem_h,
            'dias_operacao':dias_operacao,
            't_saida_processo':t_saida_processo,
            'vazao_necessaria_processo':vazao_vapor,
            'potencia_demandada':potencia_demandada,
            'PCI':pci_bagaco,
            'm_bag_tot':m_bag_tot}
        return process_params

    def get_input(self, input_id):
        return float(self.inputs[input_id].get())

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
