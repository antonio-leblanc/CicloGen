from tkinter import *
from tkinter import ttk

#############################################################################################
## 4)    RESULT DISPLAY 
#############################################################################################

class ResultDisplay(Frame):
    def __init__(self, parent,master):
        Frame.__init__(self, parent, borderwidth=1.5, relief=SOLID)
        self.parent = parent
        self.master = master
        self.display = {}
        
        # ---------------------- Styles ----------------------
        self.title_style= {'bg':'#5c7399', 'font':'Arial 11 bold','pady':4, 'relief':'solid'}
        self.sub_title_style= {'bg':'gray', 'font':'Arial 10 bold', 'pady':1, 'relief':'solid'}
        
        self.property_style= {'font':'Arial 11', 'bd':1, 'anchor':'w', 'pady':3}
        self.value_style= {'font':'Arial 11', 'bd':1, 'width':9,'relief':SOLID, 'pady':1, 'bg':'gray90'}
        self.unit_style= {'font':'Arial 11', 'pady':1,'padx':1}
        
        # ---------------------- Grids ----------------------
        self.title_grid= {'column':0, 'columnspan':3, 'sticky':'we'}
        self.property_grid = {'column':0 , 'sticky':'ew'}
        self.value_grid = {'column':1, 'sticky':'ew'}
        self.unit_grid = {'column':2 , 'sticky':'ew'}

        # ---------------------- Title ----------------------
        self.row = 0
        self.create_title('Resultados da Simulação', self.title_style)
        
        # ---------------------- Energia Elétrica ----------------------
        self.create_title('Energia Elétrica - Mecânica', self.sub_title_style)
        
        self.create_display('Wt1','Potência gerada pela turbina 1','kW')
        self.create_display('Wt2','Potência gerada pela turbina 2','kW')
        self.create_display('Wt','Potência total gerada','kW')
        self.create_display('Wb','Potência consumida pelas bombas','kW')
        self.create_display('w_outros_equip','Potência consumida pela planta','kW')
        self.create_display('w_excedente','Excedente comercializável','kW')
        
        # ---------------------- Energia Térmica ----------------------
        self.create_title('Energia Térmica', self.sub_title_style)
        
        self.create_display('Qh','Calor fornecido a caldeira','kW')
        self.create_display('Qp','Calor útil fornecido ao processo','kW')
        self.create_display('Ql','Calor cedido ao condensador','kW')
        
        # ---------------------- Consumo de bagaço ----------------------
        self.create_title('Aproveitamento do Bagaço', self.sub_title_style)


        self.create_display('m_bag_tot','Bagaço total produzido','ton/h')
        self.create_display('m_bag_cald','Bagaço consumido na caldeira','ton/h')
        self.create_display('m_bag_exc','Bagaço excedente - vazão mássica','ton/h')
        self.create_display('bag_exc_safra','Bagaço excedente - safra','ton/safra')
        

        # # ---------------------- Indices de desempenho ----------------------
        self.create_title('Indicadores de desempenho', self.sub_title_style)
        self.create_display('n_th','Eficiência térmica global','%')
        self.create_display('FUE','Fator de utilização de energia - FUE','%')
        self.create_display('IPE','Índice de poupança de energia - IPE','%')
        self.create_display('IGP','Indice de geração de potência - IGP','%')
        self.create_display('RPC','Relação potência calor - RCP','%')
        self.create_display('w_exc_esp','Capacidade de geração de eletricidade','kWh/ton')

        
        
    def set_results(self, results):
        # print (results)
        Wt = results.get('Wt')
        Wt1 = results.get('Wt1')
        Wt2 = results.get('Wt2')
        Wb = results.get('Wb')
        Qh = results.get('Qh')
        Ql = results.get('Ql')
        Qp = results.get('Qp')
        w_exc_esp = results.get('w_exc_esp')
        
        w_outros_equip = results.get('w_outros_equip')
        w_excedente = results.get('w_excedente')
        
        FUE = results.get('FUE')
        IGP = results.get('IGP')
        RPC = results.get('RPC')
        IPE = results.get('IPE')
        n_th = results.get('n_th')

        m_bag_cald = results.get('m_bag_cald')
        m_bag_tot = results.get('m_bag_tot')
        m_bag_exc = results.get('m_bag_exc')
        bag_exc_safra = results.get('bag_exc_safra')

        self.set_display_k('Wt1',Wt1)
        self.set_display_k('Wt2',Wt2)
        self.set_display_k('Wt',Wt)
        self.set_display_k('Wb',Wb)
        self.set_display_k('Qh',Qh)
        self.set_display_k('Ql',Ql)
        self.set_display_k('Qp',Qp)
        
        self.set_display_k('w_exc_esp',w_exc_esp)
        self.set_display_k('w_outros_equip',w_outros_equip)
        self.set_display_k('w_excedente',w_excedente)
        self.set_display_1f('m_bag_cald',m_bag_cald)
        self.set_display_1f('m_bag_tot',m_bag_tot)
        self.set_display_1f('m_bag_exc',m_bag_exc)
        self.set_display_k('bag_exc_safra',bag_exc_safra)
        
        self.set_display_2f('n_th',n_th)
        self.set_display_2f('FUE',FUE)
        self.set_display_2f('IPE',IPE)
        self.set_display_2f('IGP',IGP)
        self.set_display_2f('RPC',RPC)


# # ---------------------- Frontend ----------------------
    
    def create_display(self,id,text,unit):
        self.display[id] = StringVar()
        Label(self, text=text, **self.property_style).grid(row=self.row, **self.property_grid)
        Label(self, textvariable = self.display[id], **self.value_style).grid(row=self.row, **self.value_grid)
        Label(self, text=unit, **self.unit_style).grid(row=self.row, **self.unit_grid)
        self.row+=1

    def create_title(self,text,style):
        Label(self, text=text, **style).grid(row=self.row, **self.title_grid)
        self.row+=1

    def set_display_k(self,id,value):
        self.display[id].set(f'{value:,.0f}'.replace(',',' '))

    def set_display_1f(self,id,value):
        self.display[id].set(f'{value:.1f}')

    def set_display_2f(self,id,value):
        self.display[id].set(f'{value:.2f}')
