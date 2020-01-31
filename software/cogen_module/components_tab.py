from tkinter import *
from tkinter import ttk
import pandas as pd
import os
DATA_PATH = os.path.join('dados_componentes.xlsx')


class ComponentsTab(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, borderwidth=1.5, relief=SOLID)
        self.parent = parent
        self.component_model = {}
        self.display = {}
        self.grid_columnconfigure(0, weight=1)

        self.import_data()


        # --------------------- Styles ---------------------
        self.title_style= {'bg':'red', 'font':'Arial 11 bold', 'pady':4}
        self.sub_title_style= {'bg':'gray', 'font':'Arial 10 bold', 'pady':1}
        
        self.property_style= {'font':'Arial 11', 'anchor':'w', 'pady':2, 'width':30}
        self.value_style= {'font':'Arial 11', 'bd':1, 'relief':SOLID, 'bg':'gray90','padx':1,'width':11}
        self.unit_style= {'font':'Arial 11','width':6}

        # --------------------- Grids ---------------------
        self.title_grid= {'column':0, 'columnspan':3, 'sticky':'we'}
        self.sub_title_grid= {'column':0,'columnspan':3, 'sticky':'nswe'}
        self.opt_menu_grid= {'column':1,'columnspan':2, 'sticky':'we','pady':1}
        
        self.property_grid = {'column':0 , 'sticky':'ew'}
        self.value_grid = {'column':1, 'sticky':'ew'}
        self.unit_grid = {'column':2 , 'sticky':'ew'}
        
        # --------------------- Title ------------------------------
        row = 0
        row = self.create_title('Especificação dos componentes', self.title_style, row)
        
        # --------------------- Caldeira ---------------------
        
        row = self.create_title('Modelo de Caldeira',self.sub_title_style,row, self.sub_title_grid)


        row = self.create_optmenu('caldeira',  self.boilers_list[0], self.boilers_list, self.set_boiler,row)
        row = self.create_display('t_saida_caldeira','Temperatura de saída','°C',row)
        row = self.create_display('p_saida_caldeira','Pressão de saída','bar',row)
        row = self.create_display('n_caldeira','Rendimento','%',row)
    
        # --------------------- Turbina 1 ---------------------
        
        row = self.create_title('Modelo da Turbina 1',self.sub_title_style,row, self.sub_title_grid)

        row = self.create_optmenu('turbina1',  self.turbines_list[0], self.turbines_list, self.set_turbine,row)
        # row = self.create_display('p_max_t1','Pressão máxima de entrada','°C',row)
        row = self.create_display('p_saida_t1','Pressão de saída','bar',row)
        row = self.create_display('n_t1','Rendimento','%',row)

        # --------------------- Turbina 2 ---------------------

        row = self.create_title('Modelo da Turbina 2',self.sub_title_style,row, self.sub_title_grid)
        
        row = self.create_optmenu('turbina2',  self.turbines_list[0], self.turbines_list, self.set_turbine,row)
        # row = self.create_display('p_max_t2','Pressão máxima de entrada','°C',row)
        row = self.create_display('p_saida_t2','Pressão de saída','bar',row)
        row = self.create_display('n_t2','Rendimento','%',row)    

     # --------------------- Bomba 1 ---------------------
        row = self.create_title('Modelo da Bomba 1',self.sub_title_style,row, self.sub_title_grid)

        row = self.create_optmenu('bomba1',  self.pumps_list[0], self.pumps_list, self.set_pump,row)
        row = self.create_display('n_b1','Rendimento','%',row)   

      # --------------------- Bomba 2 ---------------------

        row = self.create_title('Modelo da Bomba 2',self.sub_title_style,row, self.sub_title_grid)

        row = self.create_optmenu('bomba2',  self.pumps_list[0], self.pumps_list, self.set_pump,row)
        row = self.create_display('n_b2','Rendimento','%',row)    
        
        # --------------------- Botao ---------------------
        Label(self, bg='gray').grid(sticky='nwse', row=row, column=0, columnspan=3)
        button_style= {'text' :"Atualizar Componentes",'bd':2, 'cursor':'dot', 'relief':SOLID, 'font':'Arial 10 bold', 'bg':'white'}
        Button(self,command=self.parent.update_components, **button_style).grid(row=row, column=0, columnspan=3, pady=2)

        # --------------------- Inicializando ---------------------
        self.set_boiler(0)
        self.set_turbine(0)
        self.set_pump(0)

############################### METHODS ###############################

    def get_components_params(self):
        params_dic = {}
        for n in ['n_caldeira','n_t1','n_t2','n_b1','n_b2']:
            params_dic[n] = float(self.display[n].get())/100
        for p in ['p_saida_t1', 'p_saida_t2','p_saida_caldeira']:
            params_dic[p] = float(self.display[p].get())
        for t in ['t_saida_caldeira']:
            params_dic[t] = float(self.display[t].get())
    
        # print (params_dic)
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
        
        self.display['t_saida_caldeira'].set(t_saida_caldeira)
        self.display['p_saida_caldeira'].set(p_saida_caldeira)
        self.display['n_caldeira'].set(n_caldeira)

    def set_turbine(self,value):
        modelo1 = self.component_model['turbina1'].get()
        modelo2 = self.component_model['turbina2'].get()
        
        p_max_t1 = self.df_turbines.loc[modelo1,'P_MAX_ENTRADA']
        p_saida_t1 = self.df_turbines.loc[modelo1,'P_SAIDA_BAR']
        n_t1 = self.df_turbines.loc[modelo1,'EFICIENCIA_%']

        p_max_t2 = self.df_turbines.loc[modelo2,'P_MAX_ENTRADA']
        p_saida_t2 = self.df_turbines.loc[modelo2,'P_SAIDA_BAR']
        n_t2 = self.df_turbines.loc[modelo2,'EFICIENCIA_%']
        
        # self.display['p_max_t1'].set(p_max_t1)
        self.display['p_saida_t1'].set(p_saida_t1)
        self.display['n_t1'].set(n_t1)
            
        # self.display['p_max_t2'].set(p_max_t2)
        self.display['p_saida_t2'].set(p_saida_t2)
        self.display['n_t2'].set(n_t2)

    def set_pump(self,value):
        modelo1 = self.component_model['bomba1'].get()
        modelo2 = self.component_model['bomba2'].get()

        n_b1 = self.df_pumps.loc[modelo1,'EFICIENCIA_%']
        n_b2 = self.df_pumps.loc[modelo2,'EFICIENCIA_%']

        self.display['n_b1'].set(n_b1)
        self.display['n_b2'].set(n_b2)

    def create_optmenu(self,id, init_value, options,command,row):
        self.component_model[id] = StringVar()
        ttk.OptionMenu(self, self.component_model[id], init_value, *options,command= command).grid(row=row, **self.opt_menu_grid)
        Label(self, text='Modelo', **self.property_style).grid(row=row, **self.property_grid)
        return row+1

    def create_display(self,id,text,unit,row):
        self.display[id] = StringVar()
        Label(self, text=text, **self.property_style).grid(row=row, **self.property_grid)
        Label(self, textvariable = self.display[id], **self.value_style).grid(row=row, **self.value_grid)
        Label(self, text=unit, **self.unit_style).grid(row=row, **self.unit_grid)
        return row+1

    def create_title(self,text,style,row, grid=None):
        grid = self.title_grid if not grid else grid
        Label(self, text=text, **style).grid(row=row, **grid)
        
        return row+1