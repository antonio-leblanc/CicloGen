from tkinter import *
from tkinter import ttk
import os

class ProcessMenu(Frame):
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
        self.entry_grid = {'column':1}
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

        row = self.create_input('fracao_bagaco_cana',"'%' de bagaço na cana",'%',row)
        row = self.create_input('pci_bagaco',"PCI do bagaço",'MJ/kg',row)
        row = self.create_display('energia_especifica',"Energia específica",'MJ/t.cana',row)
        row = self.create_input('fracao_bagaco_combustivel',"Fração de bagaço utilizada como combustivel",'%',row)
        row = self.create_display('energia_disponivel',"Energia disponível",'KW',row)
        
        # --------------------- Energia disp ---------------------
        
        row = self.create_title("Processo",row,self.sub_title_style,self.title_grid)
        
        row = self.create_input('consumo_vapor',"Consumo de vapor no processo",'kg/t.cana',row)
        row = self.create_display('vazao_vapor',"Vazão de vapor necessária no processo",'t/h',row)
        row = self.create_input('t_saida_processo',"Temperatura de saída do processo",'ºC',row)
       

        Button(self,text='Recalcular', command = lambda: self.set_displays(None)).grid(row=row+1,column=1)
        

        # --------------------- Inicializando ---------------------
        init_inputs = {'capacidade_moagem_h':500,
                        'dias_operacao':180,
                        'fracao_bagaco_cana':27,
                        'pci_bagaco':6.99,
                        'fracao_bagaco_combustivel':100,
                        'consumo_vapor':350,
                        't_saida_processo':90
        }

        self.set_inputs(init_inputs)

        self.set_displays(None)

############################### METHODS ###############################
   
    def set_displays(self,value):
        capacidade_moagem_h = float(self.inputs['capacidade_moagem_h'].get())
        dias_operacao = float(self.inputs['dias_operacao'].get())
        pci_bagaco = float(self.inputs['pci_bagaco'].get())
        fracao_bagaco_cana = float(self.inputs['fracao_bagaco_cana'].get())
        consumo_vapor = float(self.inputs['consumo_vapor'].get())
        fracao_bagaco_combustivel = float(self.inputs['fracao_bagaco_combustivel'].get())
        
        capacidade_moagem_d = capacidade_moagem_h*24
        capacidade_moagem_safra = capacidade_moagem_d*dias_operacao
        
        energia_especifica = pci_bagaco*1000*fracao_bagaco_cana/100
        energia_disponivel = energia_especifica*capacidade_moagem_h*fracao_bagaco_combustivel/100/3600*1e3

        vazao_vapor = capacidade_moagem_h*consumo_vapor/1000

        self.displays['capacidade_moagem_d'].set(f'{capacidade_moagem_d:,.0f}'.replace(',',' '))
        self.displays['capacidade_moagem_safra'].set(f'{capacidade_moagem_safra:,.0f}'.replace(',',' '))
        self.displays['energia_especifica'].set(f'{energia_especifica:,.0f}'.replace(',',' '))
        self.displays['energia_disponivel'].set(f'{energia_disponivel:,.0f}'.replace(',',' '))
        self.displays['vazao_vapor'].set(f'{vazao_vapor:,.0f}'.replace(',',' '))

    def get_process_params(self):
        energia_disponivel = float(self.displays['energia_disponivel'].get().replace(' ',''))*1e3 # [W]
        t_saida_processo = float(self.inputs['t_saida_processo'].get()) + 273.15 # [K]
        
        
        process_params = {'energia_disponivel':energia_disponivel,
                          't_saida_processo':t_saida_processo}
        # print (process_params)
        return process_params





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

    def set_inputs(self, inputs_dict):
        for key,value in inputs_dict.items():
            self.inputs[key].insert(0,value)