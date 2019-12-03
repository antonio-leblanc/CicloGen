
from page_one_components import*
from page_two_components import*

from tkinter import *
from tkinter import ttk 
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure



WINDOW_TITLE = 'COGEN_SOFTWARE_V_09'

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
        
        # 2) ------ Left Menu ---------
        self.left_menu = LeftMenu(self)
        self.left_menu.grid(row=1, column=0,rowspan=2, sticky='nw', padx=10, pady=5)
        
        # 3) ----- Info Display ----
        self.info_display = InfoDisplay(self)
        self.info_display.grid(row=1, column=2, sticky='nw', padx=10, pady=10)
                
        # 4) ----- Result Display ----
        self.result_display = ResultDisplay(self)
        self.result_display.grid(row=2, column=2, sticky='nw', padx=10)
                
        # 5) ------ Cycle display -----
        self.canvas = Canvas_cycle(self)
        self.canvas.grid(row=1, column=1,rowspan=2,sticky='new',pady=25)
        
        # ttk.Button(self, text='Escolha de componentes',command = lambda: master.show_frame(PageTwo)).grid(row=5,column=0)
        
        # --------------- Cycle Inicializaion ---------------
        entries_init_values = {'t1': '530', 'delta_t': '0', 'p1': '68', 'p3': '2.5', 'p5': '.08', 
        'delta_p': '-10', 'm1': '160', 'f2_10': '30', 'f14': '10', 'f9': '40', 'W_process': '30','W_other_equip':'10'}
        self.left_menu.set_entries(entries_init_values)
        self.cycle = Rankine_cycle()
        self.calculate()
        self.update_cycle()
        self.show_state_info('E1')
        self.show_component_info('Caldeira')
    
    def calculate(self):
        cycle_parameters = self.left_menu.get_cycle_params()
        
        component_parameters = self.left_menu.get_components_params()
        
        self.cycle.calculate(cycle_parameters,component_parameters)

        cycle_results = self.cycle.get_results()
        self.result_display.set_results(cycle_results)
    
    def show_state_info(self,estado):
        info = self.cycle.get_state_info(estado)
        info['E'] = estado
        self.info_display.set_state_info(info)
    
    def show_component_info(self,component):
        info = self.cycle.get_component_info(component)
        self.info_display.set_component_info(info)
    
    def update_cycle(self):
        cycle_type = self.left_menu.get_cycle_type()

        self.left_menu.set_cycle_type(cycle_type)
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
        
        # 2 -------- Components Menu -------- #
        self.components_menu = ComponentsMenu(self)
        self.components_menu.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky='w')

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
                
        for F in [PageOne,PageTwo]:
            frame = F(container,self)
            self.frames[F]=frame
            frame.grid(row=0,column=0,sticky='nswe')
        
        self.show_frame(PageOne)
        
    def show_frame(self,cont):
        frame = self.frames[cont]
        frame.tkraise()
    
    
        
########################## RUNNING THE MAIN APP ###########################
root = Rankine_App()
root.mainloop()
###########################################################################

# FOR TESTING THE CANVAS ONLY
# master = Tk()

# canvas = Canvas_cycle(master)
# canvas.pack()

# mainloop()