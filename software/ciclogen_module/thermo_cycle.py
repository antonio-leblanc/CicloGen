from ciclogen_module.thermo_classes import *
import pandas as pd

#############################################################################################
################################## DEFININDO O CICLO EM QUESTAO #############################

class Rankine_cycle:
    def __init__(self):
        pass

    def calculate(self, cycle_p, process_p):
        estados = {}
        componentes = {}

        #------------------ Obtencao dos parâmetros ------------------
        m1=cycle_p['m1']
        
        t1 = cycle_p['t1']
        perda_temperatura = cycle_p['delta_t']
        p1 = cycle_p['p1']
        p3 = cycle_p['p3']
        p5 = cycle_p['p5']
        perda_carga = cycle_p['delta_p']
        f2_10 = cycle_p['f2_10']
        f14 = cycle_p['f14']
        f9 = cycle_p['f9']
        
        cycle_type = cycle_p['cycle_type']

        n_cald = cycle_p['n_cald']

        n_t1 = cycle_p['n_t1']
        n_t2 = cycle_p['n_t2']

        n_b1 = cycle_p['n_b1']
        n_b2 = cycle_p['n_b2']
        
        t_saida_processo = process_p['t_saida_processo']

        #------------------ Calculo das massas ------------------
        
        if cycle_type == 1:  # 2 turbinas
            m2 = m1*f2_10
            m4 = m1-m2
            m3 = m2
            m10 = m3
        else: # Extraçao
            m2 = m1
            m3 = m2
            m10 = m3*f2_10
            m4 = m3-m10

        m14 = m10*f14
        m11 = m10-m14
        
        m7 = m4
        m9 = m7*f9
        m8 = m7-m9

        # ------------------ CALCULOS DO CICLO ------------------
        
        #________ Saida da Caldeira  ________
        estados['E1'] = State('P',p1,'T',t1,m1)

        #__________ Turbina 1 __________
        estados['E2'] = State('P',p1+perda_carga, 'T',t1+perda_temperatura, m2)
        componentes['T1'] = Turbine(estados['E2'],p3, n=n_t1 ,name='Turbina1')
        estados['E3'] = componentes['T1'].get_state_out()
        estados['E10'] = State('P',estados['E3'].get_P(), 'H',estados['E3'].get_H(), m10)

        #__________ Turbina 2 __________
        if cycle_type == 1:
            # Ciclo com 2 turbinas, o ponto 4 é igual ponto 2
            estados['E4'] = State('P',estados['E2'].get_P(), 'H',estados['E2'].get_H(), m4)
        else:
            # Ciclo com extracao o ponto 4 é extracao do ponto 3
            estados['E4'] = State('P',estados['E3'].get_P(), 'H',estados['E3'].get_H(), m4)

        componentes['T2'] = Turbine(estados['E4'],p5, n = n_t2 ,name='Turbina2')
        estados['E5'] = componentes['T2'].get_state_out()

        #__________ Condensador __________
        componentes['Condensador'] = Condenser(estados['E5'], name='Condensador')
        estados['E6'] = componentes['Condensador'].get_state_out()

        #__________ Bomba 1 __________
        componentes['B1'] = Pump(estados['E6'],p3, n = n_b1, name='Bomba1')
        estados['E7'] = componentes['B1'].get_state_out()
        
        #________ Dessuperaquecedor ________
        estados['E9'] = State('P',estados['E7'].get_P(), 'H',estados['E7'].get_H(), m9)
        estados['E11'] = State('P',estados['E10'].get_P(), 'H',estados['E10'].get_H(), m11)

        componentes['Dessup'] = Mixer([estados['E9'],estados['E11']], name='Dessuperaquecedor')
        estados['E12'] = componentes['Dessup'].get_state_out()

        #________ Unidade de Processo ________
        
        componentes['Processo'] = Process(estados['E12'], t_out=t_saida_processo , name='Unidade Processo')
        estados['E13'] = componentes['Processo'].get_state_out()

        #________ Desaerador ________
        estados['E8'] = State('P',estados['E7'].get_P(), 'H',estados['E7'].get_H(), m8)
        estados['E14'] = State('P',estados['E10'].get_P(), 'H',estados['E10'].get_H(), m14)

        componentes['Desaerador'] = Mixer([estados['E8'], estados['E13'], estados['E14'] ], name='Desaerador')
        estados['E15'] = componentes['Desaerador'].get_state_out()

        #________ Bomba 2 ________
        componentes['B2'] = Pump(estados['E15'],p1, n =n_b2, name='Bomba2')
        estados['E16'] = componentes['B2'].get_state_out()

        #________ Fechando o ciclo ________
        componentes['Caldeira'] = Boiler(estados['E16'],t1,n=n_cald, name='Caldeira')
        
        
        self.estados = estados
        self.componentes = componentes
        
        self.cycle_p = cycle_p
        self.process_p = process_p

   
    
    def get_results(self):
        # Calcula os resultados e converte para as unidade apropriadas

        w_outros_equip = self.process_p['potencia_demandada'] /1000                     #[kW]
        vazao_necessaria_processo = self.process_p['vazao_necessaria_processo'] *3.6    #[ton/h]
        vazao_disponivel_processo = self.estados['E13'].get_m()  *3.6                   #[ton/h]
        vazao_vapor_caldeira = self.cycle_p['m1']*3.6                                      #[ton/h]                                     
        m_bag_tot = self.process_p['m_bag_tot']  *3.6                                   #[ton/h]
        capacidade_moagem_h = self.process_p['capacidade_moagem_h'] *3.6                #[ton/h]
        dias_operacao = self.process_p['dias_operacao']                                 #[dias/ano]
        
        mPCI_disp = self.process_p['mPCI_disp']                                         #[W]
        PCI = self.process_p['PCI']                                                     #[kJ/kg]
        n_cald = self.cycle_p['n_cald']                                                 
        n_t1 = self.cycle_p['n_t1']     

        #    Caldeira
        delta_h_cald = self.estados['E1'].get_H() - self.estados['E16'].get_H()        #[kJ/kg]
        vazao_max_disponivel = mPCI_disp/delta_h_cald*n_cald *3.6                      #[t.vapor/h]
        
        Wt1 = self.componentes['T1'].get_work() / 1000                                      #[kW]
        Wt2 = self.componentes['T2'].get_work() / 1000                                      #[kW]
        Wt = Wt1 + Wt2

        Wb = (self.componentes['B1'].get_work() + self.componentes['B2'].get_work()) /1000  #[kW]
        Qp = (self.componentes['Processo'].get_Q()) /1000                                   #[kW]
        Ql = (self.componentes['Condensador'].get_Ql()) /1000                               #[kW]           
        mPCI = (self.componentes['Caldeira'].get_Qh()) /1000                                #[kW]
        
        
        m_bag_cald = (mPCI / PCI) *3.6                        #[ton/h]
        m_bag_exc = m_bag_tot - m_bag_cald                    #[ton/h]
        bag_exc_safra = m_bag_exc*24*dias_operacao            #[ton/safra]

        FUE =  (Wt+Qp) / mPCI          *100
        IPE = mPCI/(Wt/.77 + Qp/.4) * 100
        IGP = Wt / (mPCI - Qp/n_cald)  *100
        RPC = Wt/Qp                    *100
        n_th = (Wt+Qp-Wb-Ql) / mPCI    *100


        w_excedente = Wt - Wb - w_outros_equip
        r_pot_ele_cana = w_excedente/capacidade_moagem_h      #[kWh/ton] #relacao potenciaEcana
        r_bag_vap = m_bag_cald/vazao_vapor_caldeira

        results = {
            'Wt':Wt,
            'Wt1':Wt1,
            'Wt2':Wt2,
            'Wb':Wb,
            'w_outros_equip':w_outros_equip,
            'Qp':Qp,
            'Qh':mPCI,
            'Ql':Ql,
            'n_th' : n_th,       
            'FUE':FUE,
            'IGP' : IGP,
            'IPE':IPE,
            'RPC':RPC,
            'w_excedente' : w_excedente,
            'r_pot_ele_cana':r_pot_ele_cana,
            'r_bag_vap':r_bag_vap,
            'vazao_necessaria_processo':vazao_necessaria_processo,
            'vazao_disponivel_processo':vazao_disponivel_processo,
            'vazao_max_disponivel':vazao_max_disponivel,
            'm_bag_cald':m_bag_cald,
            'm_bag_tot':m_bag_tot,
            'm_bag_exc':m_bag_exc,
            'bag_exc_safra':bag_exc_safra }
        
        return results
    
    def get_state_prop(self,state):
        prop = self.estados[state].get_prop()
        prop['T'] = prop['T'] - 273.15   #[ºC]
        prop['P'] = prop['P'] / 1e5      #[bar]
        prop['H'] = prop['H'] / 1e3      #[kj/kg]
        prop['S'] = prop['S'] / 1e3      #[kj/kgK]
        prop['m'] = prop['m'] * 3.6      #[t/h]
        prop['X'] = prop['X'] *100 if prop['X'] >=0 else '-'   #[%]
        return prop

    def export_results(self):
        T_list = []
        P_list = []
        H_list = []
        S_list = []
        X_list = []
        m_list = []
        fluid_state_list = []
         
        for state_num in range (1,17):
            state = f'E{state_num}'
            info = self.get_state_prop(state)

            T_list.append(info['T'])
            P_list.append(info['P'])
            H_list.append(info['H'])
            S_list.append(info['S'])
            X_list.append(info['X'])
            m_list.append(info['m'])
            fluid_state_list.append(info['fluid_state'])
        
        dic_export = { 
            'Ponto do Ciclo' : list(range (1,17)),
            'Vazão [ton/h]' : m_list,
            'T [ºC]'     : T_list,
            'P [bar]'    : P_list,
            'H [kJ/kg]'  : H_list,
            'S [kJ/kgK]' : S_list,
            'Estado da água' : fluid_state_list,
            'X [%]'      : X_list
        }
            
        df_export = pd.DataFrame(data=dic_export)
        return df_export

