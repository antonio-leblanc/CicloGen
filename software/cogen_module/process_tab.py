from tkinter import *
from tkinter import ttk
import os

class ProcessTab(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, borderwidth=1.5, relief=SOLID)
        self.parent = parent
        self.inputs = {}
        self.displays = {}

        self.grid_columnconfigure(0, weight=1)

        # --------------------- Styles ---------------------
        self.title_style= {'bg':'red', 'font':'Arial 11 bold', 'pady':4}
        self.sub_title_style= {'bg':'gray', 'font':'Arial 10 bold', 'pady':1}
        
        self.property_style= {'font':'Arial 11', 'anchor':'w', 'pady':2}
        self.entry_style= {'font':'Arial 11', 'bd':1, 'relief':SOLID,'width':11, 'justify':CENTER}
        self.value_style= {'font':'Arial 11', 'bd':1, 'relief':SOLID, 'bg':'gray90','width':9}
        self.unit_style= {'font':'Arial 11','padx':2}

        self.title_grid= {'column':0, 'columnspan':3, 'sticky':'we'}
        self.property_grid = {'column':0 , 'sticky':'ew'}
        self.value_grid = {'column':1, 'sticky':'ew'}
        self.entry_grid = {'column':1,'sticky':'ew'}
        self.unit_grid = {'column':2 , 'sticky':'ew'}
        
        # --------------------- Title ------------------------------
        row = 0
        row = self.create_title("Dados do Processo",row,self.title_style,self.title_grid)
        
        # --------------------- Safra ---------------------
        row = self.create_title("Safra",row,self.sub_title_style,self.title_grid)

        row = self.create_input('capacidade_moagem_h','Capacidade de moagem por hora','ton/h',row)
        row = self.create_display('capacidade_moagem_d','Capacidade de moagem por dia','ton/dia',row)
        row = self.create_input('dias_operacao','Dias de operação','dias/ano',row)
        row = self.create_display('capacidade_moagem_safra','Capacidade de moagem por safra','ton/safra',row)
        
        # --------------------- Energia disp ---------------------

        row = self.create_title("Energia Disponível",row,self.sub_title_style,self.title_grid)

        row = self.create_input('fracao_bagaco_cana',"Fração de bagaço seco na cana",'%',row)
        row = self.create_input('pci_bagaco',"PCI do bagaço",'MJ/kg',row)
        row = self.create_display('energia_especifica',"Energia específica",'MJ/t.cana',row)
        row = self.create_display('eficiencia_caldeira',"Eficiência da caldeira",'%',row)
        row = self.create_display('energia_disponivel',"Energia disponível",'KW',row)
        
        # --------------------- Energia disp ---------------------
        
        row = self.create_title("Processo",row,self.sub_title_style,self.title_grid)
        
        row = self.create_input('consumo_vapor',"Consumo de vapor no processo",'kg/t.cana',row)
        row = self.create_display('vazao_vapor',"Vazão de vapor necessária no processo",'t/h',row)
        row = self.create_input('t_saida_processo',"Temperatura de saída do processo",'ºC',row)
        row = self.create_input('demanda_mecanica_equip',"Demanda energética mecânica específica",'kWh/t',row)
        row = self.create_input('demanda_eletrica_equip',"Demanda energética elétrica específica",'kWh/t',row)
        row = self.create_display('potencia_demandada',"Potência total demandada",'kW',row)
       

        Button(self,text='Recalcular', command = lambda: self.calculate_displays(None)).grid(row=row+1,column=1)
        

        # --------------------- Inicializando ---------------------
        init_inputs = {'capacidade_moagem_h':500,
                        'dias_operacao':180,
                        'fracao_bagaco_cana':27,
                        'pci_bagaco':6.99,
                        'consumo_vapor':350,
                        't_saida_processo':90,
                        'demanda_mecanica_equip':16,
                        'demanda_eletrica_equip':12
        }

        init_display = {'eficiencia_caldeira':.85}
        
        self.set_inputs(init_inputs)
        self.set_displays(init_display)
        self.calculate_displays(None)

############################### METHODS ###############################
   
    def calculate_displays(self,value):
        capacidade_moagem_h = self.get_input('capacidade_moagem_h')
        dias_operacao       = self.get_input('dias_operacao')
        pci_bagaco          = self.get_input('pci_bagaco')
        fracao_bagaco_cana  = self.get_input('fracao_bagaco_cana')
        consumo_vapor       = self.get_input('consumo_vapor')
        demanda_mecanica_equip = self.get_input('demanda_mecanica_equip')
        demanda_eletrica_equip = self.get_input('demanda_eletrica_equip')
        eficiencia_caldeira    = float(self.displays['eficiencia_caldeira'].get())

        capacidade_moagem_d = capacidade_moagem_h*24
        capacidade_moagem_safra = capacidade_moagem_d*dias_operacao
        
        energia_especifica = pci_bagaco*1000*fracao_bagaco_cana/100
        energia_disponivel = energia_especifica*capacidade_moagem_h*eficiencia_caldeira/3600*1e3

        vazao_vapor = capacidade_moagem_h*consumo_vapor/1000

        potencia_demandada=(demanda_mecanica_equip+demanda_eletrica_equip)*capacidade_moagem_h

        self.displays['capacidade_moagem_d'].set(f'{capacidade_moagem_d:,.0f}'.replace(',',' '))
        self.displays['capacidade_moagem_safra'].set(f'{capacidade_moagem_safra:,.0f}'.replace(',',' '))
        self.displays['energia_especifica'].set(f'{energia_especifica:,.0f}'.replace(',',' '))
        self.displays['energia_disponivel'].set(f'{energia_disponivel:,.0f}'.replace(',',' '))
        self.displays['vazao_vapor'].set(f'{vazao_vapor:.0f}')
        self.displays['potencia_demandada'].set(f'{potencia_demandada:,.0f}'.replace(',',' '))
        
    def set_inputs(self, inputs_dict):
        for key,value in inputs_dict.items():
            self.inputs[key].insert(0,value)

    def set_displays(self,display_dic):
        eficiencia_caldeira = display_dic['eficiencia_caldeira']
        self.displays['eficiencia_caldeira'].set(f'{eficiencia_caldeira:.2f}')


#--------------------------Geters------------------------------------#

    def get_process_params(self):
        energia_disponivel = self.get_display('energia_disponivel')*1e3   # [W]
        potencia_demandada = self.get_display('potencia_demandada')*1e3   # [W]
        t_saida_processo   =  self.get_input('t_saida_processo') + 273.15 # [K]
        vazao_vapor        = self.get_display('vazao_vapor') / 3.6        # [kg/s]
        
        
        process_params = {'energia_disponivel':energia_disponivel,
                          't_saida_processo':t_saida_processo,
                          'vazao_necessaria_processo':vazao_vapor,
                          'potencia_demandada':potencia_demandada}
        # print (process_params)
        return process_params


    def get_input(self, input_id):
        return float(self.inputs[input_id].get())


    def get_display(self, display_id):
        return float(self.displays[display_id].get().replace(' ',''))


#--------------------------Frontend------------------------------------#

    def create_title(self,text,row,style,column_grid):
        Label(self, text=text, **style).grid(row=row, **column_grid)
        return row+1


    def create_display(self,id,text,unit,row):
        self.displays[id] = StringVar()
        Label(self, text=text, **self.property_style).grid(row=row, **self.property_grid)
        Label(self, textvariable = self.displays[id], **self.value_style).grid(row=row,**self.value_grid)        
        Label(self, text=unit, **self.unit_style).grid(row=row, **self.unit_grid)
        return row+1

    def create_input(self,id,text,unit,row):
        Label(self, text=text, **self.property_style).grid(row=row, **self.property_grid)
        Label(self, text=unit, **self.unit_style).grid(row=row, **self.unit_grid)
        self.inputs[id] = Entry(self, **self.entry_style)
        self.inputs[id].grid(row=row, **self.entry_grid)
        return row+1
