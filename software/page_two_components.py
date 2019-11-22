from tkinter import *
from tkinter import ttk
import pandas as pd
DATA_PATH = 'dados_componentes.xlsx'

class ComponentsMenu(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, borderwidth=1.5, relief=SOLID)
        self.parent = parent
        self.component_data = {}

        components_data_list = ['t_saida_caldeira','p_saida_caldeira','n_caldeira','B2','Caldeira']
        for c_data in components_data_list:
            self.component_data[c_data] = StringVar()

        # --------------------- Styles ---------------------
        title_style= {'bg':'red', 'font':("Arial", 10,'bold'),'relief':FLAT, 'pady':4}
        sub_title_style= {'bg':'gray', 'font':("Arial", 8,'bold'), 'pady':2}
        property_style= {'bd':1, 'anchor':'w', 'pady':4, 'width':30}
        unit_style= {'bd':1, 'pady':4}

        entry_style= {'bd':1, 'relief':SOLID,'width':10, 'justify':CENTER}
        # --------------------- Title ------------------------------
        Label(self, text="Especificação dos componentes", **title_style).grid(row=0,column=0, columnspan=2, sticky='we')
        
        # --------------------- Caldeira ---------------------
        Label(self, text='Caldeira', **sub_title_style).grid(row=1, column=0, columnspan=3, sticky='ew')

        Label(self, text='Temperatura de saída', **property_style).grid(row=2, column=0,sticky='ew')
        Label(self, text='Pressão de Saida', **property_style).grid(row=3, column=0,sticky='ew')
        Label(self, text='Rendimento', **property_style).grid(row=4, column=0,sticky='ew')
        Label(self, text='°C', **unit_style).grid(row=2, column=2,sticky='ew')
        Label(self, text='bar', **unit_style).grid(row=3, column=2,sticky='ew')
        Label(self, text='%', **unit_style).grid(row=4, column=2,sticky='ew')
        
        self.component_data['t_saida_caldeira'] = Entry(self, **entry_style)
        self.component_data['p_saida_caldeira'] = Entry(self, **entry_style)
        self.component_data['n_caldeira'] = Entry(self, **entry_style)
        
        self.component_data['t_saida_caldeira'].grid(row=2,column=1)
        self.component_data['p_saida_caldeira'].grid(row=3,column=1)
        self.component_data['n_caldeira'].grid(row=4,column=1)

        # --------------------- Turbinas ---------------------
        Label(self, text='Turbina 1', **sub_title_style).grid(row=5, column=0, columnspan=3, sticky='ew')

        Label(self, text='Pressão max', **property_style).grid(row=6, column=0,sticky='ew')
        Label(self, text='Pressão de Saida', **property_style).grid(row=7, column=0,sticky='ew')
        Label(self, text='Rendimento', **property_style).grid(row=8, column=0,sticky='ew')
        Label(self, text='°C', **unit_style).grid(row=6, column=2,sticky='ew')
        Label(self, text='bar', **unit_style).grid(row=7, column=2,sticky='ew')
        Label(self, text='%', **unit_style).grid(row=8, column=2,sticky='ew')
        
        self.component_data['t_saida_caldeira'] = Entry(self, **entry_style)
        self.component_data['p_saida_caldeira'] = Entry(self, **entry_style)
        self.component_data['n_caldeira'] = Entry(self, **entry_style)
        
        self.component_data['t_saida_caldeira'].grid(row=6,column=1)
        self.component_data['p_saida_caldeira'].grid(row=7,column=1)
        self.component_data['n_caldeira'].grid(row=8,column=1)
               
    def get_components_params(self):
        params_dic = {}
        for key, v in self.component_data.items():
            value = v.get()
            params_dic[key] = value
        print (params_dic)
        return params_dic

    def import_data(self):
        pass