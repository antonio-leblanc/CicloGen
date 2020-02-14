

#  ------------------ Ciclo Genérico ------------------------

generic_cycle_inputs = { 
    't1': 320,
    'delta_t':0 ,
    'p1': 22,
    'p3': 2.5,
    'p5': 0.08,
    'delta_p': 0,
    'm1': 240,
    'f2_10': 69.2,
    'f14': 3.3,
    'f9': 10,
    'n_cald': 85 ,
    'n_t1': 55,
    'n_t2': 70,
    'n_b1': 45,
    'n_b2': 45 
    }

generic_process_inputs = {
    'm_cana_hora':500,
    'dias_operacao':200,
    'fracao_bagaco_cana':25,
    'pci_bagaco':7500,
    'consumo_vapor':335,
    't_saida_processo':90,
    'demanda_mecanica_equip':15,
    'demanda_eletrica_equip':12.5
}

#  ------------------ DOURADOS ------------------------

dourados_cycle_inputs = { 
    't1': '400',
    'delta_t': '0',
    'p1': '43',
    'p3': '2.5',
    'p5': '0.08',
    'delta_p': '0',
    'm1': '220',
    'f2_10': '82.27',
    'f14': '3.3',
    'f9': '0',
    'n_cald': 77 ,
    'n_t1': 84.4,
    'n_t2': 84.4,
    'n_b1': '75',
    'n_b2': '75' 
    }

dourados_process_inputs = {
    'm_cana_hora':416.66,
    'dias_operacao':225,
    'fracao_bagaco_cana':24.73 ,
    'pci_bagaco':7736,
    'consumo_vapor':420,
    't_saida_processo':127.4,
    'demanda_mecanica_equip':15,
    'demanda_eletrica_equip':12.5
}

#  ------------------ passolongo ------------------------

passolongo_cycle_inputs = { 
    't1': 530,
    'delta_t': '0',
    'p1': 68.6,
    'p3': 2.45,
    'p5': 0.07,
    'delta_p': '0',
    'm1': 160,
    'f2_10': 82.55,
    'f14': 3.55,
    'f9': 9.3,
    'n_cald': 78 ,
    'n_t1': 84,
    'n_t2': 86,
    'n_b1': 75,
    'n_b2': 75 
    }

passolongo_process_inputs = {
    'm_cana_hora':286,
    'dias_operacao':240,
    'fracao_bagaco_cana':28.5,
    'pci_bagaco':7990,
    'consumo_vapor':454,
    't_saida_processo':124.7,
    'demanda_mecanica_equip':15,
    'demanda_eletrica_equip':12
}

# ------------ ESCOLHA DOS DADOS USADOS PARA INICIAR O CICLO ----------------

cycle_inputs = generic_cycle_inputs
process_inputs = generic_process_inputs