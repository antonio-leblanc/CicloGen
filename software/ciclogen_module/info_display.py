from tkinter import *
from tkinter import ttk

#############################################################################################
## 3)      INFO DISPLAY 
#############################################################################################

class InfoDisplay(Frame):
    def __init__(self, parent,master):
        Frame.__init__(self, parent, borderwidth=1.5, relief=SOLID)
        self.parent = parent
        self.master = master
        self.display = {'name':StringVar(),'fluid_state':StringVar()}

        # ---------------------- STYLES ----------------------
        self.title_style= {'bg':'#5c7399', 'font':'Arial 11 bold', 'pady':2, 'relief':'solid'}
        self.sub_title_style= {'bg':'gray', 'font':'Arial 10 bold', 'pady':1}
        
        self.property_style= {'font':'Arial 11' ,'anchor':'e', 'pady':3, 'padx':2}
        self.value_style= {'font':'Arial 10','bd':1, 'width':10,'relief':SOLID, 'bg':'gray90','pady':1}
        self.unit_style= {'font':'Arial 11', 'pady':1, 'width':7}
        
        # ---------------------- Grids ----------------------
        self.title_grid= {'column':0, 'columnspan':6, 'sticky':'we'}
        self.property_grid = {'sticky':'ew', 'padx':2}
        self.value_grid = {'padx':2}
        self.unit_grid = {'sticky':'ew','padx':2}

        # ---------------------- TITLE ----------------------
        row = 0
        row = self.create_title('Propriedades da Agua',self.title_style,row)
        
        # ---------------------- INFO ESTADO ----------------------
        Label(self, text='Ponto', **self.property_style).grid(row=1, column=0,sticky='ew')
        Label(self, textvariable=self.display['name'], **self.value_style).grid(row=row, column=1,columnspan=1, sticky='ew')
  
        Label(self, text='Estado', **self.property_style).grid(row=1, column=3,sticky='ew')
        Label(self, textvariable=self.display['fluid_state'], **self.value_style).grid(row=1, column=4, columnspan=2, sticky='ew')

        
        self.create_display('m','Vazão','ton/h',2,0)
        self.create_display('T','Temperatura','ºC',3,0)
        self.create_display('P','Pressão','bar',4,0)
        
        self.create_display('H','Entalpia','kJ/kg',2,3)
        self.create_display('S','Entropia','kJ/kgK',3,3)
        self.create_display('X','Título','%',4,3)
    
    def create_display(self,id,text,unit,row,col):
        self.display[id] = StringVar()
        Label(self, text=text, **self.property_style).grid(row=row, column=col, **self.property_grid)
        Label(self, textvariable = self.display[id], **self.value_style).grid(row=row, column=col+1, **self.value_grid)
        Label(self, text=unit, **self.unit_style).grid(row=row, column=col+2,**self.unit_grid)
        return row+1

    def create_title(self,text,style,row):
        Label(self, text=text, **style).grid(row=row, **self.title_grid)
        return row+1
               
    def set_state_info(self,info):
        E = info.get('E')[1:]
        fluid_state = info.get('fluid_state')
        T = info.get('T')
        P = info.get('P')
        H = info.get('H')
        S = info.get('S')
        X = info.get('X')
        m = info.get('m')        
        
        self.display['name'].set(E)
        self.display['fluid_state'].set(fluid_state)
        self.display['T'].set(f'{T:.1f}')
        self.display['P'].set(f'{P:.2f}')
        self.display['H'].set(f'{H:.2f}')
        self.display['S'].set(f'{S:.4f}')
        self.display['X'].set(f'{X:.1f}') if type(X)==float else self.display['X'].set('-')
        self.display['m'].set(f'{m:.1f}')
  
    def set_component_info(self,info):
        pass
        # name = info.get('name')
        # prop = info.get('prop')
        # value = info.get('value')
        # unit = info.get('unit')
        
        # self.component['name'].set(name)        
        # self.component['prop'].set(prop)
        # self.component['value'].set(f'{value:,.2f}'.replace(',',' '))
        # self.component['unit'].set(unit)   



        