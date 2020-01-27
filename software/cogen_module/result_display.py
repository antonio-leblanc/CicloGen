from tkinter import *
from tkinter import ttk

#############################################################################################
## 4)    RESULT DISPLAY 
#############################################################################################

class ResultDisplay(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent, borderwidth=1.5, relief=SOLID)
        self.parent = parent
        self.display = {}
        
        # ---------------------- Styles ----------------------
        self.title_style= {'bg':'blue', 'font':'Arial 11 bold','pady':4}
        self.sub_title_style= {'bg':'gray', 'font':'Arial 10 bold', 'pady':1}
        
        self.property_style= {'font':'Arial 11', 'bd':1, 'anchor':'w', 'pady':3}
        self.value_style= {'font':'Arial 11', 'bd':1, 'width':9,'relief':SOLID, 'pady':1, 'bg':'gray90'}
        self.unit_style= {'font':'Arial 11', 'pady':1,'padx':1}
        
        # ---------------------- Grids ----------------------
        self.title_grid= {'column':0, 'columnspan':3, 'sticky':'we'}
        self.property_grid = {'column':0 , 'sticky':'ew'}
        self.value_grid = {'column':1, 'sticky':'ew'}
        self.unit_grid = {'column':2 , 'sticky':'ew'}

        # ---------------------- Title ----------------------
        row = 0
        row = self.create_title('RESULTADOS', self.title_style,row)
        
        # ---------------------- Energia Elétrica ----------------------
        row = self.create_title('Energia Elétrica', self.sub_title_style,row)
        row = self.create_display('Wb','Consumo das bombas','kW',row)
        row = self.create_display('w_outros_equip','Consumo de outros equipamentos','kW',row)
        row = self.create_display('Wt','Potência gerada pelas Turbinas','kW',row)
        row = self.create_display('w_excedente','Excedente comercializável','kW',row)
        
        # ---------------------- Energia Térmica ----------------------
        row = self.create_title('Energia Térmica', self.sub_title_style,row)
        row = self.create_display('Qh','Calor fornecido a Caldeira','kW',row)
        row = self.create_display('Ql','Calor cedido ao condensador','kW',row)
        row = self.create_display('Qp','Calor cedido ao processo','kW',row)
        
        # # ---------------------- Indices de desempenho ----------------------
        row = self.create_title('Indices de desempenho', self.sub_title_style,row)
        row = self.create_display('n_th','Eficiência Térmica','%',row)
        
    def create_display(self,id,text,unit,row):
        self.display[id] = StringVar()
        Label(self, text=text, **self.property_style).grid(row=row, **self.property_grid)
        Label(self, textvariable = self.display[id], **self.value_style).grid(row=row, **self.value_grid)
        Label(self, text=unit, **self.unit_style).grid(row=row, **self.unit_grid)
        return row+1

    def create_title(self,text,style,row):
        Label(self, text=text, **style).grid(row=row, **self.title_grid)
        return row+1

    def set_results(self, results):
        print (results)
        Wb = results.get('Wb') / 1000
        Wt = results.get('Wt') / 1000
        Qh = results.get('Qh') / 1000
        Ql = results.get('Ql') / 1000
        Qp = results.get('Qp') / 1000
        
        w_outros_equip = results.get('w_outros_equip') / 1000
        w_excedente = results.get('w_excedente') / 1000
        n_th = results.get('n_th')

        self.display['Wb'].set(f'{Wb:,.0f}'.replace(',',' '))
        self.display['Wt'].set(f'{Wt:,.0f}'.replace(',',' '))
        self.display['Qh'].set(f'{Qh:,.0f}'.replace(',',' '))
        self.display['Ql'].set(f'{Ql:,.0f}'.replace(',',' '))
        self.display['Qp'].set(f'{Qp:,.0f}'.replace(',',' '))
        self.display['w_outros_equip'].set(f'{w_outros_equip:,.0f}'.replace(',',' '))
        self.display['w_excedente'].set(f'{w_excedente:,.0f}'.replace(',',' '))
        self.display['n_th'].set(f'{100*n_th:.2f}')