from cogen_module.thermo_classes import *

#############################################################################################
################################## DEFININDO O CICLO EM QUESTAO #############################

class Rankine_cycle:
    def __init__(self):
        pass

    def calculate(self, cycle_p, components_p, process_p):
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

        n_b1 = components_p['n_b1']
        n_b2 = components_p['n_b2']
        n_t1 = components_p['n_t1']
        n_t2 = components_p['n_t2']
        
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
        estados['E10'] = State('P',estados['E3'].get_P(), 'H',estados['E3'].get_H(), m10)
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
        componentes['Caldeira'] = Boiler(estados['E16'],t1, name='Caldeira')
        self.estados = estados
        self.componentes = componentes

        # ------------------- Calculos para resultados ----------------
        self.w_outros_equip = process_p['potencia_demandada']
        self.vazao_necessaria_processo = process_p['vazao_necessaria_processo']
        energia_disponivel = process_p['energia_disponivel']
        
        delta_h = estados['E1'].get_H() - estados['E16'].get_H()
        self.vazao_max_disponivel = energia_disponivel/delta_h

        self.vazao_disponivel_processo = m11+m9




    
    
    def get_results(self):
        results = {}
        results['Wb'] = self.componentes['B1'].get_work() + self.componentes['B2'].get_work()
        results['Wt'] = self.componentes['T1'].get_work() + self.componentes['T2'].get_work()
        results['Qp'] = self.componentes['Processo'].get_Q()
        results['Qh'] = self.componentes['Caldeira'].get_Qh()
        results['Ql'] = self.componentes['Condensador'].get_Ql()
        
        results['w_outros_equip'] = self.w_outros_equip
        results['w_excedente'] = results['Wt']-results['Wb']-results['w_outros_equip']

        results['n_th'] = (results['Wt']-results['Wb']+results['Qp'])/results['Qh']
        
        results['vazao_necessaria_processo'] = self.vazao_necessaria_processo
        results['vazao_disponivel_processo'] = self.vazao_disponivel_processo
        results['vazao_max_disponivel'] = self.vazao_max_disponivel
        return results
    
    
    def get_state_info(self,state):
        return self.estados[state].get_info()
    
    def get_component_info(self,component):
        return self.componentes[component].get_info()

