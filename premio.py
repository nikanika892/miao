# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1s1tEkxhwqJ61qFeVpREmseqwJhfr4Ii5
"""

import pandas as pd
import ipywidgets as widgets
from IPython.display import display, clear_output

# Caricamento dei dati dai file Excel
def load_data():
    job_data = pd.read_excel('/content/Tempi Target 2025.xlsx', sheet_name='TM_010525')
    job_pregiati = pd.read_excel('/content/Tempi Target 2025.xlsx', sheet_name='job pregiati')
    return job_data, job_pregiati

job_data, job_pregiati = load_data()

# Lista di jobtype per il menu a tendina
jobtype_list = job_data['JOBTYPE'].unique().tolist()

# Funzione per ottenere il tempo target e il fattore di pregiatezza
def get_job_details(jobtype):
    try:
        row = job_data[job_data['JOBTYPE'] == jobtype].iloc[0]
        tempo_target = row['Peso=TM Ore  \'25']
        if jobtype in job_pregiati['Jobtype'].values:
            fattore = job_pregiati[job_pregiati['Jobtype'] == jobtype]['Fattore di Pregiatezza'].values[0]
        else:
            fattore = 0
        return tempo_target, fattore
    except IndexError:
        return 0, 0

# Interfaccia utente con widget
output = widgets.Output()
jobtype_inputs = []
quantita_inputs = []

# Funzione per aggiornare i menu a tendina
def aggiorna_jobtype_inputs(change):
    num_jobtype = int(num_jobtype_input.value)
    global jobtype_inputs, quantita_inputs
    jobtype_inputs = [widgets.Dropdown(options=jobtype_list, description=f'Jobtype {i+1}') for i in range(num_jobtype)]
    quantita_inputs = [widgets.IntText(description=f'Quantità {i+1}') for i in range(num_jobtype)]
    clear_output()
    display(giorni_input, ferie_input, permessi_input, formazione_input, num_jobtype_input)
    for jt, qt in zip(jobtype_inputs, quantita_inputs):
        display(jt, qt)
    display(calcola_button, output)

# Widget per inserimento dati
giorni_input = widgets.IntText(description='Giorni Lavorativi')
ferie_input = widgets.FloatText(description='Ore Ferie')
permessi_input = widgets.FloatText(description='Ore Permessi')
formazione_input = widgets.FloatText(description='Ore Formazione')
num_jobtype_input = widgets.IntText(description='Numero Jobtype')
num_jobtype_input.observe(aggiorna_jobtype_inputs, names='value')

calcola_button = widgets.Button(description='Calcola Premio')
calcola_button.on_click(calcola_premio)

# Visualizzazione widget iniziale
display(giorni_input, ferie_input, permessi_input, formazione_input, num_jobtype_input)
display(calcola_button, output)