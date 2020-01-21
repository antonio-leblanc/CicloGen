from tkinter import *
from tkinter import ttk

#############################################################################################
## 3)      INFO DISPLAY 
#############################################################################################

class InfoDisplay(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent, borderwidth=1.5, relief=SOLID)
        self.parent = parent
        self.display = {'name':StringVar(),'fluid_state':StringVar()}

        # ---------------------- STYLES ----------------------
        self.title_style= {'bg':'red', 'font':'Arial 11 bold', 'pady':4}
        self.sub_title_style= {'bg':'gray', 'font':'Arial 10 bold', 'pady':1}
        
        self.property_style= {'font':'Arial 11' ,'anchor':'w', 'pady':3}
        self.value_style= {'font':'Arial 10','bd':1, 'width':11,'relief':SOLID, 'bg':'gray90','pady':1,'padx':1}
        self.unit_style= {'font':'Arial 11', 'pady':1, 'width':7}
        
        # ---------------------- Grids ----------------------
        self.title_grid= {'column':0, 'columnspan':3, 'sticky':'we'}
        self.property_grid = {'column':0 , 'sticky':'ew'}
        self.value_grid = {'column':1, 'sticky':'ew'}
        self.unit_grid = {'column':2 , 'sticky':'ew'}

        # ---------------------- TITLE ----------------------
        row = 0
        row = self.create_title('INFORMAÇÕES',self.title_style,row)
        
        # ---------------------- INFO ESTADO ----------------------
        Label(self, textvariable=self.display['name'], **self.sub_title_style).grid(row=row, column=0, columnspan=3, sticky='ew')
        row+=1
        Label(self, text='Estado', **self.property_style).grid(row=2, column=0,sticky='ew')
        Label(self, textvariable=self.display['fluid_state'], **self.value_style).grid(row=row, column=1, columnspan=2, sticky='ew')
        row+=1
        
        row = self.create_display('T','Temperatura','ºC',row)
        row = self.create_display('P','Pressão','bar',row)
        row = self.create_display('H','Entalpia','kJ/kg',row)
        row = self.create_display('S','Entropia','kJ/kgK',row)
        row = self.create_display('X','Título','%',row)
        row = self.create_display('m','Vazão','ton/h',row)
    
    def create_display(self,id,text,unit,row):
        self.display[id] = StringVar()
        Label(self, text=text, **self.property_style).grid(row=row, **self.property_grid)
        Label(self, textvariable = self.display[id], **self.value_style).grid(row=row, **self.value_grid)
        Label(self, text=unit, **self.unit_style).grid(row=row, **self.unit_grid)
        return row+1

    def create_title(self,text,style,row):
        Label(self, text=text, **style).grid(row=row, **self.title_grid)
        return row+1
               
    def set_state_info(self,info):
        E = info.get('E')[1:]
        E = f'Ponto {E}'
        fluid_state = info.get('fluid_state')
        T = info.get('T') - 273.15
        P = info.get('P') / 1e5
        H = info.get('H') / 1e3
        S = info.get('S') / 1e3
        X = info.get('X') *100
        m = info.get('m') * 3.6        
        
        self.display['name'].set(E)
        self.display['fluid_state'].set(fluid_state)
        self.display['T'].set(f'{T:.1f}')
        self.display['P'].set(f'{P:.2f}')
        self.display['H'].set(f'{H:.2f}')
        self.display['S'].set(f'{S:.4f}')
        self.display['X'].set(f'{X:.1f}') if X>=0 else self.display['X'].set('-')
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



        
