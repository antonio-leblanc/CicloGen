from tkinter import Canvas

"""" _____________________________CANVAS FOR CICLE CISPLAY________________________________ """

####################################################################################################
######################################## CLASS DEFINITIONS #########################################

#_____________ GLOBAL PARAMS
red_line = {'fill':'red', 'width':2}
blue_line = {'fill':'blue', 'width':2}
gray_line = {'fill':'gray', 'width':2}


# CANVAS TURBINE ___________________________________________________________

class Canvas_turbine:
    def __init__(self,canvas, x, y, s=20, in_tag='', out_tag='', comp_tag='', text='Turbina'):
        self.canvas = canvas
        self.x=x
        self.y=y
        self.s=s
        
        self.canvas.create_line(x,y, x,y+s, tags = in_tag, **red_line, arrow = 'last')
        self.canvas.create_line(x+1.5*s,y+3*s, x+1.5*s,y+4.5*s, tags = out_tag, **red_line)
        
        t_params = {'tags':comp_tag, 'fill':'gray', 'activefill':'black','outline':'black', 'width':2}
        self.canvas.create_polygon(x, y+s, x+3*s, y, x+3*s, y+4*s, x,y+3*s, **t_params)

        self.text_id = self.canvas.create_text(x+1.5*s,y+2*s, text=text, tags=comp_tag, font='Arial 8')

    def get_in_coords(self):
        return (self.x,self.y)

    def get_out_coords(self):
        return (self.x+1.5*self.s,self.y+4.5*self.s)

    def set_text(self, new_text):
        self.canvas.itemconfig(self.text_id , text=new_text)

# CANVAS PUMP _______________________________________________________________________________________      
class Canvas_pump:
    def __init__(self,canvas, x, y, s=20, in_tag='', out_tag='', comp_tag='', text='Bomba',fill='#5a00ad', activefill='#38006b'):
        self.canvas = canvas
        self.x=x
        self.y=y
        self.s=s
        self.canvas.create_line(x+2*s, y, x+s, y, tags = in_tag, **blue_line, arrow='last')
        self.canvas.create_line(x-2*s, y, x-s, y, tags = out_tag, **blue_line)

        self.canvas.create_polygon(x, y, x+s, y+1.5*s, x-s, y+1.5*s, fill=fill, tags=comp_tag, outline='black', width=2)

        self.canvas.create_oval(x-s, y-s, x+s, y+s, fill=fill,activefill=activefill, tags=comp_tag, width=2)
        self.canvas.create_text(x,y+2*s, text=text, tags=comp_tag, font='Arial 9')
        
    def get_in_coords(self):
        return (self.x+2*self.s,self.y)
    def get_out_coords(self):
        return (self.x-2*self.s,self.y)
        
#________________________________________________________________________________________      
        
class Canvas_boiler:
    def __init__(self,canvas, x, y, s=20, in_tag='', out_tag='', comp_tag='', text='Caldeira',fill='red', activefill='#870000',):
        self.canvas = canvas
        self.x=x
        self.y=y
        self.s=s
        self.canvas.create_line(x, y-2*s, x, y-3*s, tags = in_tag, **red_line)
        self.canvas.create_line(x, y+2*s, x, y+3*s, tags = out_tag, **blue_line)
        self.canvas.create_rectangle(x-1.5*s, y-2*s, x+1.5*s, y+2*s, fill=fill, activefill=activefill, tags=comp_tag, width=2)
        self.canvas.create_text(x,y, text=text, anchor='c', tags=comp_tag)

    def get_in_coords(self):
        return (self.x,self.y+3*self.s)
    def get_out_coords(self):
        return (self.x,self.y-3*self.s)
#________________________________________________________________________________________      
                
class Canvas_box:
    def __init__(self,canvas, x, y, width=80, height=40, comp_tag='', fill='yellow',activefill='orange', text='', font='Arial 10'):
        self.canvas = canvas
        self.x=x
        self.y=y
        
        self.dx = width/2
        self.dy = height/2

        self.canvas.create_rectangle(x-self.dx, y-self.dy, x+self.dx, y+self.dy, tags=comp_tag, fill=fill, activefill=activefill, width=2)
        self.canvas.create_text(x,y, text=text, tags=comp_tag, font=font)

    def get_N_coords(self):
        return (self.x, self.y - self.dy)
    def get_E_coords(self):
        return (self.x+self.dx, self.y)
    def get_W_coords(self):
        return (self.x-self.dx, self.y)
    def get_S_coords(self):
        return (self.x, self.y + self.dy)
#________________________________________________________________________________________      

class Canvas_condenser:
    def __init__(self,canvas, x, y, s=22, in_tag='', out_tag='', comp_tag='', text='Condensador',fill='deep sky blue', activefill='blue'): 
        self.canvas = canvas
        self.x=x
        self.y=y
        self.s=s
        self.canvas.create_line(x, y-2.5*s, x, y-1.5*s, tags = in_tag, **red_line, arrow = 'last')
        self.canvas.create_line(x, y+1.5*s, x, y+2.5*s, tags = in_tag, **blue_line)
        self.canvas.create_oval(x-1.5*s, y-1.5*s, x+1.5*s, y+1.5*s, fill=fill, activefill=activefill, tags=comp_tag, width=2)
        self.canvas.create_text(x,y, text=text, tags=comp_tag, font='Arial 8')

    def get_in_coords(self):
        return (self.x,self.y-self.s*2.5+1)
    def get_out_coords(self):
        return (self.x, self.y+self.s*2.5)

#________________________________________________________________________________________      
        
class Canvas_state:
    def __init__(self, canvas, x, y, state, anchor='e', color='red'):
        r=3
        canvas.create_oval(x-r, y-r, x+r, y+r, fill = color, tags=f'E{state}')
        t_params = {'tags':f'E{state}', 'font' : 'Arial 10'}
        
        if anchor == 'n':
            canvas.create_text(x, y+5, text = str(state), anchor='n', **t_params)
        elif anchor == 'e':
            canvas.create_text(x-5, y, text = str(state), anchor='e', **t_params)
        elif anchor == 'w':
            canvas.create_text(x+5, y, text = str(state), anchor='w', **t_params)
        elif anchor == 's':
            canvas.create_text(x, y-5, text = str(state), anchor='s', **t_params)
#________________________________________________________________________________________      

        
def middle(x1,y1,x2,y2):
    return (x1+x2)/2,(y1+y2)/2


####################################################################################################
############################################# MAIN CICLE ###########################################
CANVAS_WIDTH = 550
CANVAS_HEIGTH = 450

class Canvas_cycle(Canvas):
    def __init__(self , parent,master):
        Canvas.__init__(self,parent, width=CANVAS_WIDTH, height=CANVAS_HEIGTH, bg = 'white', highlightbackground = 'black')
        self.parent = parent
        self.master = master

        # A) CALDEIRA __________________________________________________________________________________________
        x_caldeira = 60
        y_caldeira = 150
        boiler = Canvas_boiler(self,x_caldeira,y_caldeira,in_tag='E16',out_tag='E1', comp_tag='Caldeira')
            # Texto estado 1
        xb,yb = boiler.get_out_coords()
        Canvas_state(self, xb,yb, 1, anchor='e', color='red')
                
        # B) TURBINA 1 __________________________________________________________________________________________
        x0_t1 = 300
        y0 = 40
        dy0_t1 = 20
        y0_t1 = y0+dy0_t1
        self.turbine1 = Canvas_turbine(self, x0_t1, y0_t1, in_tag='E2', out_tag='E3', comp_tag='T1', text='T1')
            # Linha estado 1
        self.create_line(xb,yb, xb,y0, x0_t1,y0, tags='E1', **red_line)
            # Linha estado 2
        self.create_line(x0_t1,y0, x0_t1,y0_t1, tags='E2', **red_line)
        Canvas_state(self, x0_t1,y0_t1, 2)
            # Texto estado 3        
        x_te,y_te = self.turbine1.get_out_coords()
        Canvas_state(self, x_te,y_te-10, 3)
            # Texto estado 10        
        y_estado_10 = y_te + 30
        self.create_line(x_te,y_te, x_te,y_estado_10, tags='E10', **red_line)
        Canvas_state(self, x_te,y_te+15, 10)
        
        # C) TURBINA 2 __________________________________________________________________________________________
        dx_t12 = 180
        dy_t12 = 20
        x0_t2 = x0_t1+dx_t12
        y0_t2 = y0_t1+dy_t12
        self.turbine2 = Canvas_turbine(self, x0_t2, y0_t2, in_tag='E4', out_tag='E5', comp_tag='T2', text='T2')
        
        x_t1,y_t1 = self.turbine1.get_out_coords()

        self.linha_com_extrac = self.create_line(x_t1,y_t1, x_t1+40,y_t1, x_t1+40,y0_t1, x0_t2,y0_t1, tags='E4', **red_line)
        self.linha_sem_extrac = self.create_line(x0_t1,y0, x0_t2,y0,x0_t2,y0_t1, tags='E4', **red_line)

        self.create_line(x0_t2,y0_t1,x0_t2,y0_t2, tags='E4', **red_line)
        Canvas_state(self,x0_t2 ,y0_t2-10, 4)
        
        # D) DESSUPERAQUECEDOR ____________________________________________________________________________________
        dy_t1_dessup = 100
        dessup = Canvas_box(self, x_te,y_te+dy_t1_dessup, width = 120, comp_tag='Dessup', text='Dessuperaquecedor')
            # Linha estado 11
        x_n,y_n = dessup.get_N_coords()
        self.create_line(x_n,y_estado_10-5, x_n,y_n, tags='E11', **red_line, arrow='last')
        Canvas_state(self,x_n ,y_n-30, 11)

        # E) PROCESSO ____________________________________________________________________________________
        x_s,y_s = dessup.get_S_coords()
        dy_dessup_proc = 70
        process = Canvas_box(self,x_s,y_s+dy_dessup_proc, comp_tag='Processo', fill='#01870f', activefill='#005409',text='Processo')
            # Linha estado 12
        x_n,y_n = process.get_N_coords()
        self.create_line(x_s,y_s, x_n,y_n, tags='E12', arrow='last', **red_line)
        Canvas_state(self,x_n ,y_n-30, 12)

        
        #F) DESAERADOR _______________________________________________________________________________________________
        x_s,y_s = process.get_S_coords()
        dx_proc = -80
        dy_proc = 40
        desaerador = Canvas_box(self,x_s+dx_proc, y_s+dy_proc, comp_tag='Desaerador', fill='#0040a1',activefill='#002c6e', text='Desaerador')
            # Linha estado 13
        x_e,y_e = desaerador.get_E_coords()
        self.create_line(x_s,y_s, x_s,y_e-5, x_e,y_e-5, tags='E13', arrow='last', **blue_line)
        Canvas_state(self,x_s,y_s+20, 13, color='blue')
            # Linha estado 14
        x_n,y_n = desaerador.get_N_coords()
        self.create_line(x_te,y_estado_10, x_n,y_estado_10, x_n,y_n, tags='E14', arrow='last', **red_line)
        Canvas_state(self,x_n,y_n-70, 14)

        # G) CONDENSADOR__________________________________________________________________________________________________
        x_t2,y_t2 = self.turbine2.get_out_coords()
        dy_t2_cond = 80
        condenser = Canvas_condenser(self, x_t2,y_t2+dy_t2_cond,in_tag='E5', out_tag='E6', comp_tag='Condensador', text='Condensador')
            # Linha estado 5
        x2,y2 = condenser.get_in_coords()
        self.create_line(x_t2,y_t2, x2,y2, tags='E5', **red_line)
        Canvas_state(self, x_t2,y_t2+10, 5, anchor='e', color='red')

        # H) BOMBA 1 ____________________________________________________________________________________________________
        xc,yc = condenser.get_out_coords()
        xd,yd = desaerador.get_E_coords()
        pump1 = Canvas_pump(self,xc-40,yd+5, in_tag='E6', out_tag='E7', comp_tag='B1', text='Bomba 1')
            # Linha estado 6
        xp,yp = pump1.get_in_coords()
        self.create_line(xc,yc, xp,yp, tags='E6', **blue_line)
        Canvas_state(self, xc,yc+30, 6, anchor='e', color='blue')
            # Linha estado 7
        xp,yp = pump1.get_out_coords()
        x_estado_7 = xp-20
        self.create_line(xp,yp, x_estado_7,yp, tags='E7',  **blue_line)
        Canvas_state(self, xp,yp, 7, anchor='n', color='blue')
            # Linha estado 8
        self.create_line(x_estado_7,yp, xd,yp, tags='E8', arrow='last', **blue_line)
        Canvas_state(self, x_estado_7-30,yp, 8, anchor='n', color='blue')
            # Linha estado 9
        x_e,y_e = dessup.get_E_coords()
        self.create_line(x_estado_7,yp, x_estado_7,y_e, x_e,y_e, tags='E9', arrow='last', **blue_line)
        Canvas_state(self, x_estado_7,y_e+40, 9 , color='blue')

        # I) BOMBA 2 ____________________________________________________________________________________________________
        x_w,y_w = desaerador.get_W_coords()
        xb,yb = boiler.get_in_coords()
        dx_cald_b2 = 50
        pump2 = Canvas_pump(self, xb+dx_cald_b2,y_w, in_tag='E15', out_tag='16', comp_tag='B2', text='Bomba 2')

            # Linha estado 15
        xp,yp = pump2.get_in_coords()
        self.create_line(x_w,y_w, xp,yp, tags='E15', **blue_line)
        Canvas_state(self, x_w-25,y_w, 15, anchor='n', color='blue')
            # Linha estado 16
        xp,yp = pump2.get_out_coords()
        self.create_line(xp,yp, xb,yp, xb,yb, tags='E16', **blue_line)
        Canvas_state(self, xb,yp-40, 16, anchor='e', color='blue')

        # TITLE ____________________________________________________________________________________________________
        self.cycle_title = self.create_text(CANVAS_WIDTH/2,15, text='', font='Helvetica 12', tags='E1')
       
        #_________________ Binding ____________________________
        self.bind("<Button-1>", lambda event: self.click(event))
    
    def click(self,event):
        item = self.find_closest(event.x, event.y)
        tags = self.gettags(item)
        estados = [f'E{i}' for i in range(1,19)]
        componentes = ['Caldeira','T1','T2','T3','B1','B2','M1','M2','Dessup','Desaerador','Condensador','Processo']
        
        estado = list(set(tags)&set(estados))
        componente = list(set(tags)&set(componentes))
        if estado:
            # print (estado) 
            self.master.show_state_info(estado[0])
        else:
            # print(componente)
            self.master.show_component_info(componente[0])

    def set_cycle_type(self,cycle_type):
        if cycle_type == 1:
            self.itemconfig(self.cycle_title, text='Ciclo A : Turbinas de Contrapressão e Condensação')
            self.itemconfig(self.linha_com_extrac, state='hidden' )
            self.itemconfig(self.linha_sem_extrac, state='normal' )
            self.turbine1.set_text('Turbina 1:\nContra-\npressão')
            self.turbine2.set_text('Turbina 2:\nConden-\nsação')

        else:
            self.itemconfig(self.cycle_title, text='Ciclo B : Turbina de Extração-Condensação')
            self.itemconfig(self.linha_com_extrac, state='normal' )
            self.itemconfig(self.linha_sem_extrac, state='hidden' )
            self.turbine1.set_text('1°Estágio')
            self.turbine2.set_text('2°Estágio')

