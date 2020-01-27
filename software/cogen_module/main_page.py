
from cogen_module.parameters_menu import *
from cogen_module.thermo_cycle import *

from cogen_module.result_display import *
from cogen_module.info_display import *
from cogen_module.canvas_display import*

from tkinter import *
from tkinter import ttk 

# import matplotlib
# matplotlib.use('TkAgg')
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.figure import Figure


WINDOW_TITLE = 'COGEN_SOFTWARE_V_09'
HEAD_TITLE = 'SOFTWARE DE SIMULAÇÂO E ANALISE DE CICLOS DE RANKINE COM COGERAÇÂO [v0.9]'

#############################################################################################
## 1)       HEAD 
#############################################################################################

class Head(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, borderwidth=1.5, relief=SOLID)

        self.title = Label(self, text=HEAD_TITLE,font='Helvetica 16 bold',pady=8, bg='#244AC6')
        self.grid_columnconfigure(0, weight=1)
        self.title.grid(sticky='ew')
##############################################################################################
##################                       MAIN PAGE ONE                      ##################
##############################################################################################

class PageOne(Frame):
    def __init__(self,parent, master):
        Frame.__init__(self,parent)
        self.master = master

        # 1) -------- HEAD -------- #
        self.head = Head(self)
        self.head.grid(row=0, column=0, columnspan=4, sticky='ew')
        
        # 2) ------ Parameters Menu ---------
        self.parameters_menu = ParametersMenu(self)
        self.parameters_menu.grid(row=1, column=0,rowspan=2, sticky='nw', padx=10, pady=5)
        
        # 3) ----- Info Display ----
        self.info_display = InfoDisplay(self)
        self.info_display.grid(row=1, column=2, sticky='nw', padx=10, pady=25)
                
        # 4) ----- Result Display ----
        self.result_display = ResultDisplay(self)
        self.result_display.grid(row=2, column=2, sticky='nw', padx=10)
                
        # 5) ------ Cycle display -----
        self.canvas = Canvas_cycle(self)
        self.canvas.grid(row=1, column=1,rowspan=2,sticky='new',pady=25)
        

        button_style= {'text' :"Simular",'bd':2, 'cursor':'dot', 'relief':SOLID, 'font':'Arial 10 bold', 'bg':'white', 'width':14}
        Button(self, command = lambda: self.calculate(),**button_style).grid(row=3,column=1)
        

        # --------------- Cycle Inicializaion ---------------

        self.cycle = Rankine_cycle()
        # self.calculate()
        self.update_cycle()
        self.show_state_info('E1')
        self.show_component_info('Caldeira')
    
    def calculate(self):
        # Get parameters
        cycle_parameters = self.parameters_menu.get_cycle_params()
        component_parameters = self.parameters_menu.get_components_params()
        process_parameters = self.parameters_menu.get_process_params()
        
        #Cycle Calculations
        self.cycle.calculate(cycle_parameters,component_parameters,process_parameters)
        cycle_results = self.cycle.get_results()

        #Use results
        self.parameters_menu.set_results(cycle_results)
        self.result_display.set_results(cycle_results)
    
    def show_state_info(self,estado):
        info = self.cycle.get_state_info(estado)
        info['E'] = estado
        self.info_display.set_state_info(info)
    
    def show_component_info(self,component):
        info = self.cycle.get_component_info(component)
        self.info_display.set_component_info(info)
    
    def update_cycle(self):
        cycle_type = self.parameters_menu.get_cycle_type()

        self.parameters_menu.set_cycle_type(cycle_type)
        self.canvas.set_cycle_type(cycle_type)
        self.calculate()


##############################################################################################
##################                       MAIN PAGE TWO                      ##################
##############################################################################################

class PageTwo(Frame):
    def __init__(self,parent,master):
        Frame.__init__(self,parent)
        self.master = master
        # 1) -------- HEAD -------- #
        self.head = Head(self)
        self.head.grid(row=0, column=0, columnspan=3, sticky='ew')
        
        ttk.Button(self, text='Página Principal',command = lambda: master.show_frame(PageOne)).grid(row=2,column=0, sticky='w')


##################################################################################
################################# MAIN APP #######################################
##################################################################################

class Rankine_App(Tk):
    def __init__(self):
    
        Tk.__init__(self)
        self.title(WINDOW_TITLE)
        
        container = Frame(self)
        container.grid()
        
        self.frames = {}
                
        for Page_frame in [PageOne,PageTwo]:
            frame = Page_frame(container,self)
            self.frames[Page_frame]=frame
            frame.grid(row=0,column=0,sticky='nswe')
        
        self.show_frame(PageOne)
        
    def show_frame(self,cont):
        frame = self.frames[cont]
        frame.tkraise()
    
