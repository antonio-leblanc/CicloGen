from tkinter import *
from tkinter import ttk
import pandas as pd
import os
DATA_PATH = os.path.join('dados_componentes.xlsx')

class ComponentsMenu(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, borderwidth=1.5, relief=SOLID)
        self.parent = parent
        self.component_data = {}

        self.import_data()

        components_data_list = ['modelo_caldeira','t_saida_caldeira','p_saida_caldeira','n_caldeira']
        for c_data in components_data_list:
            self.component_data[c_data] = StringVar()


        # --------------------- Styles ---------------------
        title_style= {'bg':'red', 'font':("Arial", 10,'bold'),'relief':FLAT, 'pady':4}
        sub_title_style= {'bg':'gray', 'font':("Arial", 8,'bold'), 'pady':2}
        
        property_style= {'bd':1, 'anchor':'w', 'pady':4, 'width':30}
        value_style= {'bd':1, 'width':10,'relief':SOLID, 'bg':'#dbdbdb','pady':2,'padx':1}
        unit_style= {'bd':1, 'pady':4}

        property_grid = {'column':0 , 'sticky':'ew'}
        value_grid = {'column':1, 'sticky':'ew'}
        unit_grid = {'column':2 , 'sticky':'ew'}
        
        # --------------------- Title ------------------------------
        Label(self, text="Especificação dos componentes", **title_style).grid(row=0,column=0, columnspan=2, sticky='we')
        
        # --------------------- Caldeira ---------------------
        row = 1
        Label(self, text='Caldeira', **sub_title_style).grid(row=row, column=0, columnspan=3, sticky='ew')

        Label(self, text='Modelo', **property_style).grid(row=row+1, **property_grid)
        ttk.OptionMenu(self, self.component_data['modelo_caldeira'], self.boilers_list[0], *self.boilers_list,command= self.set_boiler).grid(row=row+1,column=1,columnspan=2,sticky='ew')

        Label(self, text='Temperatura de saída', **property_style).grid(row=row+2, **property_grid)
        Label(self, text='Pressão de Saida', **property_style).grid(row=row+3, **property_grid)
        Label(self, text='Rendimento', **property_style).grid(row=row+4, **property_grid)

        Label(self, text='°C', **unit_style).grid(row=row+2, **unit_grid)
        Label(self, text='bar', **unit_style).grid(row=row+3, **unit_grid)
        Label(self, text='%', **unit_style).grid(row=row+4, **unit_grid)
        
        Label(self, textvariable = self.component_data['t_saida_caldeira'], **value_style).grid(row=row+2,**value_grid)        
        Label(self, textvariable = self.component_data['p_saida_caldeira'], **value_style).grid(row=row+3, **value_grid)        
        Label(self, textvariable = self.component_data['n_caldeira'], **value_style).grid(row=row+4, **value_grid)        

        # --------------------- Turbinas ---------------------
        Label(self, text='Turbina 1', **sub_title_style).grid(row=5, column=0, columnspan=3, sticky='ew')

        Label(self, text='Pressão max', **property_style).grid(row=6, **property_grid)
        Label(self, text='Pressão de Saida', **property_style).grid(row=7, **property_grid)
        Label(self, text='Rendimento', **property_style).grid(row=8, **property_grid)
        Label(self, text='°C', **unit_style).grid(row=6,**unit_grid)
        Label(self, text='bar', **unit_style).grid(row=7, **unit_grid)
        Label(self, text='%', **unit_style).grid(row=8, **unit_grid)
        
 

               
    def get_components_params(self):
        params_dic = {}
        for key, v in self.component_data.items():
            value = v.get()
            params_dic[key] = value
        print (params_dic)
        return params_dic

    def import_data(self):
        print (os.listdir())
        # df_boilers = pd.read_excel(DATA_PATH,1)
        # self.boilers_list = df_boilers['MODELO'].tolist()
        self.boilers_list=[1,2,3]

    def set_boiler(self,value):
        print ('Ta quase')
