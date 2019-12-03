from tkinter import *
from tkinter import ttk
import pandas as pd
import os
DATA_PATH = os.path.join('dados_componentes.xlsx')


class ComponentsMenu(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, borderwidth=1.5, relief=SOLID)
        self.parent = parent
        self.component_model = {}
        self.component_data = {}

        self.import_data()

        for component in ['caldeira','turbina1','turbina2','bomba1','bomba2']:
            self.component_model[component] = StringVar()
        
        components_data_list = ['t_saida_caldeira','p_saida_caldeira','n_caldeira',
                                'p_max_t1','p_saida_t1','n_t1',
                                'p_max_t2','p_saida_t2','n_t2',
                                'n_b1','n_b2']

        for c_data in components_data_list:
            self.component_data[c_data] = StringVar()

        # --------------------- Styles ---------------------
        title_style= {'bg':'red', 'font':("Arial", 10,'bold'), 'pady':4}
        sub_title_style= {'bg':'gray', 'font':("Arial", 8,'bold'), 'pady':2}
        
        property_style= {'bd':1, 'anchor':'w', 'pady':4, 'width':30}
        value_style= {'bd':1, 'relief':SOLID, 'bg':'#dbdbdb', 'pady':2,'padx':1}
        unit_style= {'bd':1, 'pady':4}

        property_grid = {'column':0 , 'sticky':'ew'}
        value_grid = {'column':1, 'sticky':'ew'}
        unit_grid = {'column':2 , 'sticky':'ew'}
        
        # --------------------- Title ------------------------------
        Label(self, text="Especificação dos componentes", **title_style).grid(row=0,column=0, columnspan=3, sticky='we')
        
        # --------------------- Caldeira ---------------------
        row = 1
        Label(self, text='Caldeira', **sub_title_style).grid(row=row, column=0, columnspan=3, sticky='ew')

        Label(self, text='Modelo', **property_style).grid(row=row+1, **property_grid)
        ttk.OptionMenu(self, self.component_model['caldeira'], self.boilers_list[0], *self.boilers_list,command= self.set_boiler).grid(row=row+1,column=1,columnspan=2,sticky='ew')

        Label(self, text='Temperatura de saída', **property_style).grid(row=row+2, **property_grid)
        Label(self, text='Pressão de Saida', **property_style).grid(row=row+3, **property_grid)
        Label(self, text='Rendimento', **property_style).grid(row=row+4, **property_grid)

        Label(self, text='°C', **unit_style).grid(row=row+2, **unit_grid)
        Label(self, text='bar', **unit_style).grid(row=row+3, **unit_grid)
        Label(self, text='%', **unit_style).grid(row=row+4, **unit_grid)
        
        Label(self, textvariable = self.component_data['t_saida_caldeira'], **value_style).grid(row=row+2,**value_grid)        
        Label(self, textvariable = self.component_data['p_saida_caldeira'], **value_style).grid(row=row+3, **value_grid)        
        Label(self, textvariable = self.component_data['n_caldeira'], **value_style).grid(row=row+4, **value_grid)        

        # --------------------- Turbina 1 ---------------------
        row = 6
        Label(self, text='Turbina 1', **sub_title_style).grid(row=row, column=0, columnspan=3, sticky='ew')
        Label(self, text='Modelo', **property_style).grid(row=row+1, **property_grid)
        ttk.OptionMenu(self, self.component_model['turbina1'], self.turbines_list[0], *self.turbines_list,command= self.set_turbine).grid(row=row+1,column=1,columnspan=2,sticky='ew')

        Label(self, text='Pressão max', **property_style).grid(row=row+2, **property_grid)
        Label(self, text='Pressão de Saida', **property_style).grid(row=row+3, **property_grid)
        Label(self, text='Rendimento', **property_style).grid(row=row+4, **property_grid)
        
        Label(self, text='°C', **unit_style).grid(row=row+2,**unit_grid)
        Label(self, text='bar', **unit_style).grid(row=row+3, **unit_grid)
        Label(self, text='%', **unit_style).grid(row=row+4, **unit_grid)

        Label(self, textvariable = self.component_data['p_max_t1'], **value_style).grid(row=row+2,**value_grid)        
        Label(self, textvariable = self.component_data['p_saida_t1'], **value_style).grid(row=row+3, **value_grid)        
        Label(self, textvariable = self.component_data['n_t1'], **value_style).grid(row=row+4, **value_grid)

        # --------------------- Turbina 2 ---------------------
        row = 11
        Label(self, text='Turbina 2', **sub_title_style).grid(row=row, column=0, columnspan=3, sticky='ew')
        Label(self, text='Modelo', **property_style).grid(row=row+1, **property_grid)
        ttk.OptionMenu(self, self.component_model['turbina2'], self.turbines_list[0], *self.turbines_list,command= self.set_turbine).grid(row=row+1,column=1,columnspan=2,sticky='ew')

        Label(self, text='Pressão max', **property_style).grid(row=row+2, **property_grid)
        Label(self, text='Pressão de Saida', **property_style).grid(row=row+3, **property_grid)
        Label(self, text='Rendimento', **property_style).grid(row=row+4, **property_grid)
        
        Label(self, text='°C', **unit_style).grid(row=row+2,**unit_grid)
        Label(self, text='bar', **unit_style).grid(row=row+3, **unit_grid)
        Label(self, text='%', **unit_style).grid(row=row+4, **unit_grid)

        Label(self, textvariable = self.component_data['p_max_t2'], **value_style).grid(row=row+2,**value_grid)        
        Label(self, textvariable = self.component_data['p_saida_t2'], **value_style).grid(row=row+3, **value_grid)        
        Label(self, textvariable = self.component_data['n_t2'], **value_style).grid(row=row+4, **value_grid)    

     # --------------------- Bomba 1 ---------------------
        row = 16
        Label(self, text='Bomba 1', **sub_title_style).grid(row=row, column=0, columnspan=3, sticky='ew')
        Label(self, text='Modelo', **property_style).grid(row=row+1, **property_grid)
        ttk.OptionMenu(self, self.component_model['bomba1'], self.pumps_list[0], *self.pumps_list,command= self.set_pump).grid(row=row+1,column=1,columnspan=2,sticky='ew')

        Label(self, text='Rendimento', **property_style).grid(row=row+2, **property_grid)
        Label(self, text='%', **unit_style).grid(row=row+2, **unit_grid)
        Label(self, textvariable = self.component_data['n_b1'], **value_style).grid(row=row+2, **value_grid)  

     # --------------------- Bomba 2 ---------------------
        row = 19
        Label(self, text='Bomba 2', **sub_title_style).grid(row=row, column=0, columnspan=3, sticky='ew')
        Label(self, text='Modelo', **property_style).grid(row=row+1, **property_grid)
        ttk.OptionMenu(self, self.component_model['bomba2'], self.pumps_list[0], *self.pumps_list,command= self.set_pump).grid(row=row+1,column=1,columnspan=2,sticky='ew')

        Label(self, text='Rendimento', **property_style).grid(row=row+2, **property_grid)
        Label(self, text='%', **unit_style).grid(row=row+2, **unit_grid)
        Label(self, textvariable = self.component_data['n_b2'], **value_style).grid(row=row+2, **value_grid)  
        
        # --------------------- Inicializando ---------------------
        self.set_boiler(0)
        self.set_turbine(0)
        self.set_pump(0)

############################### METHODS ###############################

    def get_components_params(self):
        params_dic = {}
        for n in ['n_caldeira','n_t1','n_t2','n_b1','n_b2']:
            params_dic[n] = float(self.component_data[n].get())/100 
        print (params_dic)
        return params_dic

    def import_data(self):
        self.df_boilers = pd.read_excel(DATA_PATH,0,index_col='MODELO')
        self.df_turbines = pd.read_excel(DATA_PATH,1,index_col='MODELO')
        self.df_pumps = pd.read_excel(DATA_PATH,2,index_col='MODELO')

        self.boilers_list = self.df_boilers.index.tolist()
        self.turbines_list = self.df_turbines.index.tolist()
        self.pumps_list = self.df_pumps.index.tolist()
   
    def set_boiler(self,value):
        modelo = self.component_model['caldeira'].get()
        
        t_saida_caldeira = self.df_boilers.loc[modelo,'T_SAIDA_C']
        p_saida_caldeira = self.df_boilers.loc[modelo,'P_SAIDA_BAR']
        n_caldeira = self.df_boilers.loc[modelo,'EFICIENCIA_%']
        
        self.component_data['t_saida_caldeira'].set(t_saida_caldeira)
        self.component_data['p_saida_caldeira'].set(p_saida_caldeira)
        self.component_data['n_caldeira'].set(n_caldeira)

    def set_turbine(self,value):
        modelo1 = self.component_model['turbina1'].get()
        modelo2 = self.component_model['turbina2'].get()
        
        p_max_t1 = self.df_turbines.loc[modelo1,'P_MAX_ENTRADA']
        p_saida_t1 = self.df_turbines.loc[modelo1,'P_SAIDA_BAR']
        n_t1 = self.df_turbines.loc[modelo1,'EFICIENCIA_%']

        p_max_t2 = self.df_turbines.loc[modelo2,'P_MAX_ENTRADA']
        p_saida_t2 = self.df_turbines.loc[modelo2,'P_SAIDA_BAR']
        n_t2 = self.df_turbines.loc[modelo2,'EFICIENCIA_%']
        
        self.component_data['p_max_t1'].set(p_max_t1)
        self.component_data['p_saida_t1'].set(p_saida_t1)
        self.component_data['n_t1'].set(n_t1)
            
        self.component_data['p_max_t2'].set(p_max_t2)
        self.component_data['p_saida_t2'].set(p_saida_t2)
        self.component_data['n_t2'].set(n_t2)

    def set_pump(self,value):
        modelo1 = self.component_model['bomba1'].get()
        modelo2 = self.component_model['bomba2'].get()

        n_b1 = self.df_pumps.loc[modelo1,'EFICIENCIA_%']
        n_b2 = self.df_pumps.loc[modelo2,'EFICIENCIA_%']

        self.component_data['n_b1'].set(n_b1)
        self.component_data['n_b2'].set(n_b2)
