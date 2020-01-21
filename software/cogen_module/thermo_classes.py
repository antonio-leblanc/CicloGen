import CoolProp.CoolProp as CP
# import CoolProp.Plots as CPP

############################################################################################
############ CONJUNTO DE CLASSES UTILIZADAS NA MODELIZACAO DO CICLO TERMODINAMICO ##########
############################################################################################


' ---------- CLASSE QUE MODELIZA UM ESTADO TERMODINAMICO ------------- '

class State:
    def __init__(self,prop1,value1,prop2,value2, m=1, fluid='Water'):
        self.prop1 = prop1
        self.value1 = value1        
        self.prop2 = prop2
        self.value2 = value2
        self.m = m
        self.fluid = fluid

    def get_T(self):
        return CP.PropsSI('T' ,self.prop1,self.value1,self.prop2,self.value2,self.fluid)        
    def get_P(self):
        return CP.PropsSI('P' ,self.prop1,self.value1,self.prop2,self.value2,self.fluid)
    def get_H(self):
        return CP.PropsSI('H' ,self.prop1,self.value1,self.prop2,self.value2,self.fluid)
    def get_S(self):
        return CP.PropsSI('S' ,self.prop1,self.value1,self.prop2,self.value2,self.fluid)    
    def get_v(self):
        return 1/CP.PropsSI('D' ,self.prop1,self.value1,self.prop2,self.value2,self.fluid)
    def get_Q(self):
        return CP.PropsSI('Q' ,self.prop1,self.value1,self.prop2,self.value2,self.fluid)
    
    def get_m(self):
        return self.m
    def set_m(self,m):
        self.m = m
        
    def get_info(self):
        return {'T':self.get_T(),'P':self.get_P(),'H':self.get_H(),'S':self.get_S(),
               'X':self.get_Q(),'m':self.get_m(),'fluid_state':self.get_fluid_state()}
    
    def get_saturation_T(self):
        return CP.PropsSI('T' ,'Q',0 , 'P',self.get_P(), self.fluid)

    def get_fluid_state(self):
        Q = self.get_Q()
        T = self.get_T()
        saturation_T = self.get_saturation_T()
        
        if Q == 0:
            return 'Líquido Saturado'
        if Q == 1:
            return 'Vapor Saturado'
        if 0<Q<1:
            return 'Região Bifásica'  
        if T<saturation_T :
            return 'Liquido Comprimido'
        if T>saturation_T :
            return 'Vapor Superaquecido'


    def __str__(self):
        t = self.get_T()-271.15
        p = self.get_P()/1000
        h = self.get_H()/1000
        s = self.get_S()/1000
        m = self.get_m()
        text = f'Properties of the point:\n• Temperature [C] = {t:.2f}\n• Pressure [kPa] = {p:,}\n• Enthalpy [kJ/kg] = {h:.2f}\n• Entropy [kJ/Kg.K] = {s:.4f}\n• M [kg/s] = {m:.2f}'.replace(',',' ')
        return text
        

'--------------------- MODELIZAÇAO DOS DIFERENTES COMPONENTES ---------------------'        

#------------------ 1) BOMBA
class Pump:
    def __init__(self, state_in, p_out, n=1, name=''):
        self.name = name
        self.state_in = state_in
        self.n = n
        self.m = state_in.get_m()
        # Calculations for state out
        h_out = state_in.get_H() + state_in.get_v() * ( p_out - state_in.get_P()) / n
        self.state_out = State('P', p_out, 'H', h_out, m =self.m )
        
    def get_state_out(self):
        return self.state_out
    
    def get_work(self):
        return (self.state_out.get_H() - self.state_in.get_H()) * self.m
    
    def get_info(self):
        return {'prop':'W','value':self.get_work()/1000,'unit': 'KW', 'name':self.name}      

#------------------ 2) CALDEIRA
class Boiler:
    def __init__(self, state_in, t_out, n=1, name=''):
        self.name = name
        self.state_in = state_in
        self.n=n
        self.m = state_in.get_m()
        self.state_out = State('T',t_out,'P',state_in.get_P(), m=self.m)
    
    def get_state_out(self):
        return self.state_out
    
    def get_Qh(self):
        return (self.state_out.get_H() - self.state_in.get_H()) * self.m
    
    def get_info(self):
        return {'prop':'Qh','value':self.get_Qh()/1000,'unit': 'KW', 'name':self.name}
               

#------------------ 3) TURBINA
class Turbine:
    def __init__(self, state_in, p_out, n=1, name=''):
        self.name = name
        self.state_in = state_in
        self.n=n
        self.m = state_in.get_m()
        
        h_out_s = State('S',state_in.get_S(),'P',p_out).get_H()
        h_out = state_in.get_H() - n*(state_in.get_H() - h_out_s)
    
        self.state_out = State('H', h_out, 'P', p_out, m=self.m)
    
    def get_state_out(self):
        return self.state_out
    
    def get_work(self):
        return (self.state_in.get_H() - self.state_out.get_H()) * self.m
    
    def get_info(self):
        return {'prop':'W','value':self.get_work()/1000,'unit': 'KW', 'name':self.name}
    
#------------------ 4) CONDENSADOR    
class Condenser:
    def __init__(self,state_in, n=1, Q_out = 0, name=''):
        self.name = name
        self.state_in = state_in
        self.n=n
        self.m = state_in.get_m()
        self.state_out = State('P',state_in.get_P(),'Q',Q_out, m=self.m)
    
    def get_state_out(self):
        return self.state_out

    def get_Ql(self):
        return (self.state_in.get_H() - self.state_out.get_H()) * self.m
    
    def get_info(self):
        return {'prop':'Ql','value':self.get_Ql()/1000,'unit': 'KW', 'name':self.name}

#------------------ 5) MISTURADOR    
class Mixer:
    def __init__(self, states_in_list, name=''):
        self.states_in_list = states_in_list
        self.name = name
        p_out = states_in_list[0].get_P()
        m_out = 0
        h_m_out = 0
        
        for state in states_in_list:
            m_out += state.get_m()
            h_m_out += state.get_m()*state.get_H()
        
        h_out = (h_m_out)/(m_out)        
        self.state_out = State('P',p_out, 'H', h_out, m = m_out )
    
    def get_state_out(self):
        return self.state_out

    def get_info(self):
        return {'prop':'Nao sei','value':0,'unit': 'kJ/Kg', 'name':self.name}
 
 #------------------ 6) PROCESSO    

class Process:
    def __init__(self, state_in, w=None, t_out = 90+273.15, name=''):
        self.state_in = state_in
        self.name = name
        m_in = state_in.get_m()
        
        if w:
            self.w = w
            h_out = state_in.get_H() - w/m_in
            self.state_out = State('P',state_in.get_P(), 'H', h_out, m = m_in )
        else:
            self.state_out = State('P',state_in.get_P(), 'T', t_out, m = m_in )
            self.w = m_in*(state_in.get_H()-self.state_out.get_H())

    
    def get_Q(self):
        return self.w
    
    def get_state_out(self):
        return self.state_out

    def get_info(self):
        return {'prop':'W','value':self.w/1e6,'unit': 'MW','name':self.name}
