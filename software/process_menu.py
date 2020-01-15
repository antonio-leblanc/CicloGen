from tkinter import *
from tkinter import ttk
import os


class ProcessMenu(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, borderwidth=1.5, relief=SOLID)
        self.parent = parent
        self.inputs = {}
        self.display = {}

        self.grid_columnconfigure(0, weight=1)

        # --------------------- Styles ---------------------
        self.title_style= {'bg':'red', 'font':'Arial 11 bold', 'pady':4}
        self.sub_title_style= {'bg':'gray', 'font':'Arial 10 bold', 'pady':1}
        
        self.property_style= {'font':'Arial 11', 'anchor':'w', 'pady':2}
        self.entry_style= {'font':'Arial 11', 'bd':1, 'relief':SOLID,'width':10, 'justify':CENTER}
        self.value_style= {'font':'Arial 11', 'bd':1, 'relief':SOLID, 'bg':'gray90','width':10}
        self.unit_style= {'font':'Arial 11','padx':1}

        self.title_grid= {'column':0, 'columnspan':3, 'sticky':'we'}
        self.property_grid = {'column':0 , 'sticky':'ew'}
        self.value_grid = {'column':1, 'sticky':'ew'}
        self.entry_grid = {'column':1}
        self.unit_grid = {'column':2 , 'sticky':'ew'}
        
        # --------------------- Title ------------------------------
        row = 0
        row = self.create_title("Dados do Processo",row,self.title_style,self.title_grid)
        
        # --------------------- Capadidade ---------------------
        row = self.create_title("Safra",row,self.sub_title_style,self.title_grid)

        row = self.create_input('capacidade_moagem_h','Capacidade de moagem por hora','ton/h',row)
        row = self.create_display('capacidade_moagem_d','Capacidade de moagem por dia','ton/dia',row)
        row = self.create_input('dias_operacao','Dias de operação','dias/ano',row)
        row = self.create_display('capacidade_moagem_safra','Capacidade de moagem por safra','ton/safra',row)
        
        # --------------------- Capadidade ---------------------

        row = self.create_title("Processo",row,self.sub_title_style,self.title_grid)

        row = self.create_input('fracao_bagaco_cana',"'%' de bagaço na cana",'%',row)
        row = self.create_input('pci_bagaco',"PCI do bagaço",'MJ/kg',row)
        row = self.create_display('energia_disponivel',"Energia disponível",'MJ/t.cana',row)
        row = self.create_input('consumo_vapor',"Consumo de vapor no processo",'kg/t.cana',row)
        row = self.create_display('vazao_vapor',"Vazão de vapor necessária no processo",'t/h',row)
        row = self.create_display('vazao_vapor2',"Vazão de vapor necessária no processo2",'t/h',row)
       
        
        Button(self,text='Recalcular', command = lambda: self.set_displays(None)).grid(row=row+1,column=1)

        # --------------------- Inicializando ---------------------
        init_inputs = {'capacidade_moagem_h':500,
                        'dias_operacao':180,
                        'fracao_bagaco_cana':27,
                        'pci_bagaco':6.99,
                        'consumo_vapor':350
        }

        self.set_inputs(init_inputs)

        self.set_displays(None)
############################### METHODS ###############################

    def create_title(self,text,row,style,column_grid):
        Label(self, text=text, **style).grid(row=row, **column_grid)
        return row+1


    def create_display(self,id,text,unit,row):
        self.display[id] = StringVar()
        Label(self, text=text, **self.property_style).grid(row=row, **self.property_grid)
        Label(self, textvariable = self.display[id], **self.value_style).grid(row=row,**self.value_grid)        
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
    
    def set_displays(self,displays_dict):
        capacidade_moagem_h = float(self.inputs['capacidade_moagem_h'].get())
        dias_operacao = float(self.inputs['dias_operacao'].get())
        pci_bagaco = float(self.inputs['pci_bagaco'].get())
        fracao_bagaco_cana = float(self.inputs['fracao_bagaco_cana'].get())
        consumo_vapor = float(self.inputs['consumo_vapor'].get())
        
        capacidade_moagem_d = capacidade_moagem_h*24
        capacidade_moagem_safra = capacidade_moagem_d*dias_operacao
        
        energia_disponivel = pci_bagaco*1000*fracao_bagaco_cana/100
        vazao_vapor = capacidade_moagem_h*consumo_vapor/1000

        self.display['capacidade_moagem_d'].set(f'{capacidade_moagem_d:,.0f}'.replace(',',' '))
        self.display['capacidade_moagem_safra'].set(f'{capacidade_moagem_safra:,.0f}'.replace(',',' '))
        self.display['energia_disponivel'].set(f'{energia_disponivel:,.0f}'.replace(',',' '))
        self.display['vazao_vapor'].set(f'{vazao_vapor:,.0f}'.replace(',',' '))
        