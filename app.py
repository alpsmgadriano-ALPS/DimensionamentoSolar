import streamlit as st
import pandas as pd
import numpy as np
import math
from fpdf import FPDF
from datetime import datetime
import os
# Nova importação para o banco de dados
from streamlit_gsheets import GSheetsConnection

# ==============================================================================
# 1. BANCO DE DADOS COMPLETO (APOLLO)
# ==============================================================================
# ... (MANTENHA TODAS AS LISTAS DE PLACAS, BOMBAS E INVERSORES IGUAIS ANTES) ...
# Para economizar espaço aqui, estou assumindo que as listas DB_PLACAS, 
# DB_BOMBAS_SUBMERSA, etc., continuam no código exatamente como antes.

# --- Módulos Fotovoltaicos ---
DB_PLACAS = [
    {'Modelo': 'Painel 700W', 'P_max': 700.0, 'V_mp': 41.8, 'I_mp': 16.7, 'V_oc': 49.8, 'I_sc': 17.5},
    {'Modelo': 'Painel 620W', 'P_max': 620.0, 'V_mp': 40.8, 'I_mp': 15.2, 'V_oc': 49.1, 'I_sc': 16.0},
    {'Modelo': 'Painel 550W', 'P_max': 550.0, 'V_mp': 41.7, 'I_mp': 14.0, 'V_oc': 49.6, 'I_sc': 14.7},
    {'Modelo': 'Painel 450W', 'P_max': 450.0, 'V_mp': 41.4, 'I_mp': 10.8, 'V_oc': 50.0, 'I_sc': 11.3},
    {'Modelo': 'Painel 340W', 'P_max': 340.0, 'V_mp': 38.7, 'I_mp': 8.8,  'V_oc': 45.2, 'I_sc': 9.2},
]

# --- Bombas Submersas ---
DB_BOMBAS_SUBMERSA = [
    {'CV': 0.5, 'KW': 0.38, 'I_220': 3.6, 'I_380': 2.1},
    {'CV': 0.75, 'KW': 0.56, 'I_220': 4.4, 'I_380': 2.5},
    {'CV': 1.0, 'KW': 0.75, 'I_220': 5.3, 'I_380': 3.1},
    {'CV': 1.5, 'KW': 1.12, 'I_220': 7.1, 'I_380': 4.1},
    {'CV': 2.0, 'KW': 1.5, 'I_220': 9.0, 'I_380': 5.2},
    {'CV': 3.0, 'KW': 2.25, 'I_220': 11.7, 'I_380': 6.7},
    {'CV': 4.0, 'KW': 3.0, 'I_220': 14.8, 'I_380': 8.5},
    {'CV': 5.5, 'KW': 4.12, 'I_220': 18.6, 'I_380': 10.7},
    {'CV': 7.5, 'KW': 5.62, 'I_220': 25.5, 'I_380': 14.7},
    {'CV': 10.0, 'KW': 7.5, 'I_220': 34.7, 'I_380': 19.9},
    {'CV': 11.0, 'KW': 8.25, 'I_220': 34.4, 'I_380': 19.9},
    {'CV': 12.0, 'KW': 9.0, 'I_220': 37.6, 'I_380': 21.7},
    {'CV': 12.5, 'KW': 9.38, 'I_220': 39.1, 'I_380': 22.6},
    {'CV': 13.0, 'KW': 9.75, 'I_220': 44.8, 'I_380': 25.8},
    {'CV': 14.0, 'KW': 10.5, 'I_220': 48.2, 'I_380': 27.8},
    {'CV': 15.0, 'KW': 11.25, 'I_220': 51.6, 'I_380': 29.8},
    {'CV': 20.0, 'KW': 15.0, 'I_220': 62.0, 'I_380': 36.0},
    {'CV': 22.5, 'KW': 16.88, 'I_220': 65.7, 'I_380': 38.3},
    {'CV': 25.0, 'KW': 18.75, 'I_220': 72.0, 'I_380': 42.0},
    {'CV': 27.5, 'KW': 20.62, 'I_220': 78.6, 'I_380': 45.3},
    {'CV': 30.0, 'KW': 22.5, 'I_220': 85.0, 'I_380': 49.0},
    {'CV': 32.5, 'KW': 24.38, 'I_220': 96.7, 'I_380': 54.0},
    {'CV': 35.0, 'KW': 26.25, 'I_220': 102.0, 'I_380': 59.0},
    {'CV': 37.5, 'KW': 28.12, 'I_220': 109.0, 'I_380': 62.5},
    {'CV': 40.0, 'KW': 30.0, 'I_220': 115.0, 'I_380': 66.0},
    {'CV': 45.0, 'KW': 33.75, 'I_220': 132.8, 'I_380': 76.0},
    {'CV': 50.0, 'KW': 37.5, 'I_220': 144.9, 'I_380': 82.9},
    {'CV': 55.0, 'KW': 41.25, 'I_220': 161.0, 'I_380': 92.9},
    {'CV': 60.0, 'KW': 45.0, 'I_220': 174.4, 'I_380': 99.6},
    {'CV': 65.0, 'KW': 48.75, 'I_220': 173.0, 'I_380': 101.0},
    {'CV': 70.0, 'KW': 52.5, 'I_220': 188.0, 'I_380': 109.0},
    {'CV': 75.0, 'KW': 56.25, 'I_220': 219.0, 'I_380': 126.0},
    {'CV': 80.0, 'KW': 60.0, 'I_220': 226.0, 'I_380': 131.0},
    {'CV': 85.0, 'KW': 63.75, 'I_220': 237.0, 'I_380': 137.0},
    {'CV': 90.0, 'KW': 67.5, 'I_220': 249.0, 'I_380': 144.0},
    {'CV': 95.0, 'KW': 71.25, 'I_220': 261.0, 'I_380': 151.0},
    {'CV': 100.0, 'KW': 75.0, 'I_220': 273.0, 'I_380': 158.0},
    {'CV': 105.0, 'KW': 78.75, 'I_220': 302.3, 'I_380': 172.3},
    {'CV': 110.0, 'KW': 82.5, 'I_220': 332.16, 'I_380': 192.0},
    {'CV': 115.0, 'KW': 86.25, 'I_220': 346.0, 'I_380': 200.0},
    {'CV': 120.0, 'KW': 90.0, 'I_220': 359.84, 'I_380': 208.0},
    {'CV': 125.0, 'KW': 93.75, 'I_220': 371.95, 'I_380': 215.0},
    {'CV': 140.0, 'KW': 105.0, 'I_220': 403.09, 'I_380': 233.0},
    {'CV': 150.0, 'KW': 112.5, 'I_220': 429.04, 'I_380': 248.0},
    {'CV': 155.0, 'KW': 116.25, 'I_220': 445.48, 'I_380': 257.5},
    {'CV': 160.0, 'KW': 120.0, 'I_220': 461.91, 'I_380': 267.0},
    {'CV': 165.0, 'KW': 123.75, 'I_220': 479.21, 'I_380': 277.0},
    {'CV': 170.0, 'KW': 127.5, 'I_220': 494.78, 'I_380': 286.0},
    {'CV': 175.0, 'KW': 131.25, 'I_220': 510.35, 'I_380': 295.0},
    {'CV': 180.0, 'KW': 135.0, 'I_220': 523.33, 'I_380': 302.5},
    {'CV': 185.0, 'KW': 138.75, 'I_220': 536.3, 'I_380': 310.0},
    {'CV': 190.0, 'KW': 142.5, 'I_220': 548.93, 'I_380': 317.3},
    {'CV': 195.0, 'KW': 146.25, 'I_220': 561.38, 'I_380': 324.5},
    {'CV': 200.0, 'KW': 150.0, 'I_220': 576.09, 'I_380': 333.0},
    {'CV': 205.0, 'KW': 153.75, 'I_220': 626.26, 'I_380': 362.0},
    {'CV': 210.0, 'KW': 157.5, 'I_220': 640.1, 'I_380': 370.0},
    {'CV': 215.0, 'KW': 161.25, 'I_220': 653.94, 'I_380': 378.0},
    {'CV': 220.0, 'KW': 165.0, 'I_220': 666.05, 'I_380': 385.0},
    {'CV': 225.0, 'KW': 168.75, 'I_220': 679.89, 'I_380': 393.0},
    {'CV': 230.0, 'KW': 172.5, 'I_220': 692.0, 'I_380': 400.0},
    {'CV': 235.0, 'KW': 176.25, 'I_220': 700.65, 'I_380': 405.0},
    {'CV': 240.0, 'KW': 180.0, 'I_220': 709.3, 'I_380': 410.0},
    {'CV': 245.0, 'KW': 183.75, 'I_220': 717.95, 'I_380': 415.0},
    {'CV': 250.0, 'KW': 187.5, 'I_220': 726.6, 'I_380': 420.0},
    {'CV': 255.0, 'KW': 191.25, 'I_220': 715.36, 'I_380': 413.5},
    {'CV': 260.0, 'KW': 195.0, 'I_220': 729.19, 'I_380': 421.5},
    {'CV': 265.0, 'KW': 198.75, 'I_220': 743.9, 'I_380': 430.0},
    {'CV': 270.0, 'KW': 202.5, 'I_220': 757.74, 'I_380': 438.0},
    {'CV': 275.0, 'KW': 206.25, 'I_220': 771.58, 'I_380': 446.0},
    {'CV': 280.0, 'KW': 210.0, 'I_220': 785.42, 'I_380': 454.0},
    {'CV': 285.0, 'KW': 213.75, 'I_220': 794.07, 'I_380': 459.0},
    {'CV': 290.0, 'KW': 217.5, 'I_220': 802.72, 'I_380': 464.0},
    {'CV': 295.0, 'KW': 221.25, 'I_220': 811.37, 'I_380': 469.0},
    {'CV': 300.0, 'KW': 225.0, 'I_220': 820.02, 'I_380': 474.0},
    {'CV': 305.0, 'KW': 228.75, 'I_220': 833.0, 'I_380': 481.5},
    {'CV': 310.0, 'KW': 232.5, 'I_220': 846.84, 'I_380': 489.5},
    {'CV': 315.0, 'KW': 236.25, 'I_220': 859.81, 'I_380': 497.0},
    {'CV': 320.0, 'KW': 240.0, 'I_220': 872.78, 'I_380': 504.5},
    {'CV': 325.0, 'KW': 243.75, 'I_220': 885.76, 'I_380': 512.0},
    {'CV': 330.0, 'KW': 247.5, 'I_220': 899.6, 'I_380': 520.0},
    {'CV': 335.0, 'KW': 251.25, 'I_220': 912.58, 'I_380': 527.5},
    {'CV': 340.0, 'KW': 255.0, 'I_220': 925.55, 'I_380': 535.0},
    {'CV': 345.0, 'KW': 258.75, 'I_220': 938.52, 'I_380': 542.5},
    {'CV': 350.0, 'KW': 262.5, 'I_220': 951.5, 'I_380': 550.0},
    {'CV': 355.0, 'KW': 266.25, 'I_220': 977.45, 'I_380': 565.0},
    {'CV': 360.0, 'KW': 270.0, 'I_220': 1003.4, 'I_380': 580.0},
    {'CV': 365.0, 'KW': 273.75, 'I_220': 1010.32, 'I_380': 584.0},
    {'CV': 370.0, 'KW': 277.5, 'I_220': 1017.24, 'I_380': 588.0},
    {'CV': 375.0, 'KW': 281.25, 'I_220': 1031.94, 'I_380': 596.5},
    {'CV': 380.0, 'KW': 285.0, 'I_220': 1043.19, 'I_380': 603.0},
    {'CV': 385.0, 'KW': 288.75, 'I_220': 1058.76, 'I_380': 612.0},
    {'CV': 390.0, 'KW': 292.5, 'I_220': 1070.0, 'I_380': 618.5},
    {'CV': 395.0, 'KW': 296.25, 'I_220': 1080.38, 'I_380': 624.5},
    {'CV': 400.0, 'KW': 300.0, 'I_220': 1091.63, 'I_380': 631.0}
]

# --- Bombas Periféricas ---
DB_BOMBAS_PERIFERICA = [
    {'CV': 0.16, 'KW': 0.12, 'I_220': 0.93, 'I_380': 0.46},
    {'CV': 0.25, 'KW': 0.18, 'I_220': 1.16, 'I_380': 0.58},
    {'CV': 0.33, 'KW': 0.25, 'I_220': 1.39, 'I_380': 0.69},
    {'CV': 0.5, 'KW': 0.37, 'I_220': 1.85, 'I_380': 0.93},
    {'CV': 0.75, 'KW': 0.55, 'I_220': 2.62, 'I_380': 1.31},
    {'CV': 1.0, 'KW': 0.75, 'I_220': 3.47, 'I_380': 1.74},
    {'CV': 1.5, 'KW': 1.1, 'I_220': 4.86, 'I_380': 2.43},
    {'CV': 2.0, 'KW': 1.5, 'I_220': 6.48, 'I_380': 3.24},
    {'CV': 3.0, 'KW': 2.2, 'I_220': 9.15, 'I_380': 4.57},
    {'CV': 4.0, 'KW': 3.0, 'I_220': 12.51, 'I_380': 6.25},
    {'CV': 5.0, 'KW': 3.7, 'I_220': 14.78, 'I_380': 7.39},
    {'CV': 6.0, 'KW': 4.5, 'I_220': 17.76, 'I_380': 8.88},
    {'CV': 7.5, 'KW': 5.5, 'I_220': 22.51, 'I_380': 11.26},
    {'CV': 10.0, 'KW': 7.5, 'I_220': 28.95, 'I_380': 14.47},
    {'CV': 12.5, 'KW': 9.2, 'I_220': 34.51, 'I_380': 17.25},
    {'CV': 15.0, 'KW': 11.0, 'I_220': 42.61, 'I_380': 21.31},
    {'CV': 20.0, 'KW': 15.0, 'I_220': 57.67, 'I_380': 28.83},
    {'CV': 25.0, 'KW': 18.5, 'I_220': 70.41, 'I_380': 35.2},
    {'CV': 30.0, 'KW': 22.0, 'I_220': 84.77, 'I_380': 42.38},
    {'CV': 40.0, 'KW': 30.0, 'I_220': 114.64, 'I_380': 57.32},
    {'CV': 50.0, 'KW': 37.0, 'I_220': 140.58, 'I_380': 70.29},
    {'CV': 60.0, 'KW': 45.0, 'I_220': 169.99, 'I_380': 85.0},
    {'CV': 75.0, 'KW': 55.0, 'I_220': 200.57, 'I_380': 100.28},
    {'CV': 100.0, 'KW': 75.0, 'I_220': 277.92, 'I_380': 138.96},
    {'CV': 125.0, 'KW': 90.0, 'I_220': 326.56, 'I_380': 163.28},
    {'CV': 150.0, 'KW': 110.0, 'I_220': 396.04, 'I_380': 198.02},
    {'CV': 175.0, 'KW': 132.0, 'I_220': 472.46, 'I_380': 236.23},
    {'CV': 200.0, 'KW': 150.0, 'I_220': 541.94, 'I_380': 270.97},
    {'CV': 250.0, 'KW': 185.0, 'I_220': 660.06, 'I_380': 330.03},
    {'CV': 270.0, 'KW': 200.0, 'I_220': 704.06, 'I_380': 352.03},
    {'CV': 300.0, 'KW': 220.0, 'I_220': 775.86, 'I_380': 387.93},
    {'CV': 350.0, 'KW': 260.0, 'I_220': 917.14, 'I_380': 458.57},
    {'CV': 400.0, 'KW': 300.0, 'I_220': 1046.83, 'I_380': 523.42},
]

# --- Inversores Apollo ---
DB_INVERSORES = [
    # SS2 (220V - Apenas até 2.2kW)
    {'Modelo': 'FU9000SI-0R7G-SS2', 'Potencia_KW': 0.75, 'Corrente_Nominal_A': 7.2,  'Tensao': '220V', 'Max_DC': 400},
    {'Modelo': 'FU9000SI-1R5G-SS2', 'Potencia_KW': 1.5,  'Corrente_Nominal_A': 10.2, 'Tensao': '220V', 'Max_DC': 400},
    {'Modelo': 'FU9000SI-2R2G-SS2', 'Potencia_KW': 2.2,  'Corrente_Nominal_A': 14.0, 'Tensao': '220V', 'Max_DC': 400},
    
    # Série 4 (380V - Usada para 380V e para 220V > 2.2kW)
    {'Modelo': 'FU9000SI-0R7G-4',   'Potencia_KW': 0.75, 'Corrente_Nominal_A': 2.5,  'Tensao': '380V', 'Max_DC': 800},
    {'Modelo': 'FU9000SI-1R5G-4',   'Potencia_KW': 1.5,  'Corrente_Nominal_A': 4.2,  'Tensao': '380V', 'Max_DC': 800},
    {'Modelo': 'FU9000SI-2R2G-4',   'Potencia_KW': 2.2,  'Corrente_Nominal_A': 5.5,  'Tensao': '380V', 'Max_DC': 800},
    {'Modelo': 'FU9000SI-004G-4',   'Potencia_KW': 4.0,  'Corrente_Nominal_A': 9.5,  'Tensao': '380V', 'Max_DC': 800},
    {'Modelo': 'FU9000SI-5R5G-4',   'Potencia_KW': 5.5,  'Corrente_Nominal_A': 14.0, 'Tensao': '380V', 'Max_DC': 800},
    {'Modelo': 'FU9000SI-7R5G-4',   'Potencia_KW': 7.5,  'Corrente_Nominal_A': 18.5, 'Tensao': '380V', 'Max_DC': 800},
    {'Modelo': 'FU9000SI-011G-4',    'Potencia_KW': 11.0, 'Corrente_Nominal_A': 25.0, 'Tensao': '380V', 'Max_DC': 800},
    {'Modelo': 'FU9000SI-015G-4',    'Potencia_KW': 15.0, 'Corrente_Nominal_A': 32.0, 'Tensao': '380V', 'Max_DC': 800},
    {'Modelo': 'FU9000SI-018G-4',    'Potencia_KW': 18.5, 'Corrente_Nominal_A': 38.0, 'Tensao': '380V', 'Max_DC': 800},
    {'Modelo': 'FU9000SI-022G-4',    'Potencia_KW': 22.0, 'Corrente_Nominal_A': 45.0, 'Tensao': '380V', 'Max_DC': 800},
    {'Modelo': 'FU9000SI-030G-4',    'Potencia_KW': 30.0, 'Corrente_Nominal_A': 60.0, 'Tensao': '380V', 'Max_DC': 800},
    {'Modelo': 'FU9000SI-037G-4',    'Potencia_KW': 37.0, 'Corrente_Nominal_A': 75.0, 'Tensao': '380V', 'Max_DC': 800},
    {'Modelo': 'FU9000SI-045G-4',    'Potencia_KW': 45.0, 'Corrente_Nominal_A': 92.0, 'Tensao': '380V', 'Max_DC': 800},
    {'Modelo': 'FU9000SI-055G-4',    'Potencia_KW': 55.0, 'Corrente_Nominal_A': 115.0, 'Tensao': '380V', 'Max_DC': 800},
    {'Modelo': 'FU9000SI-075G-4',    'Potencia_KW': 75.0, 'Corrente_Nominal_A': 150.0, 'Tensao': '380V', 'Max_DC': 800},
    {'Modelo': 'FU9000SI-090G-4',    'Potencia_KW': 90.0, 'Corrente_Nominal_A': 180.0, 'Tensao': '380V', 'Max_DC': 800},
    {'Modelo': 'FU9000SI-110G-4',    'Potencia_KW': 110.0, 'Corrente_Nominal_A': 215.0, 'Tensao': '380V', 'Max_DC': 800},
    {'Modelo': 'FU9000SI-132G-4',    'Potencia_KW': 132.0, 'Corrente_Nominal_A': 260.0, 'Tensao': '380V', 'Max_DC': 800},
    {'Modelo': 'FU9000SI-160G-4',    'Potencia_KW': 160.0, 'Corrente_Nominal_A': 305.0, 'Tensao': '380V', 'Max_DC': 800},
    {'Modelo': 'FU9000SI-185G-4',    'Potencia_KW': 185.0, 'Corrente_Nominal_A': 340.0, 'Tensao': '380V', 'Max_DC': 800},
    {'Modelo': 'FU9000SI-200G-4',    'Potencia_KW': 200.0, 'Corrente_Nominal_A': 380.0, 'Tensao': '380V', 'Max_DC': 800},
    {'Modelo': 'FU9000SI-220G-4',    'Potencia_KW': 220.0, 'Corrente_Nominal_A': 426.0, 'Tensao': '380V', 'Max_DC': 800},
    {'Modelo': 'FU9000SI-250G-4',    'Potencia_KW': 250.0, 'Corrente_Nominal_A': 465.0, 'Tensao': '380V', 'Max_DC': 800},
    {'Modelo': 'FU9000SI-280G-4',    'Potencia_KW': 280.0, 'Corrente_Nominal_A': 520.0, 'Tensao': '380V', 'Max_DC': 800},
    {'Modelo': 'FU9000SI-315G-4',    'Potencia_KW': 315.0, 'Corrente_Nominal_A': 585.0, 'Tensao': '380V', 'Max_DC': 800}
]

df_inversores = pd.DataFrame(DB_INVERSORES)

# ==============================================================================
# 2. CLASSES E FUNÇÕES AUXILIARES
# ==============================================================================

class PropostaPDF(FPDF):
    def header(self):
        if os.path.exists('logo.png'):
            try:
                self.image('logo.png', 10, 8, 40)
            except: pass
        
        self.set_font('Arial', 'B', 15)
        self.cell(45) 
        self.cell(0, 10, 'Relatório de Dimensionamento Solar', 0, 1, 'L')
        self.set_font('Arial', 'I', 10)
        self.cell(45)
        self.cell(0, 5, 'Soluções em Bombeamento Off-Grid - Apollo', 0, 1, 'L')
        self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()} - Gerado por Sistema Apollo', 0, 0, 'C')

    def chapter_title(self, label):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(230, 230, 230)
        self.cell(0, 8, f"  {label}", 0, 1, 'L', 1)
        self.ln(2)

    def chapter_body(self, txt):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 6, txt)
        self.ln()

def calcular_arranjo_otimizado(potencia_necessaria_watts, tensao_sistema, placa_selecionada):
    if tensao_sistema == "220V":
        min_por_string, max_por_string = 7, 9
    else:
        min_por_string, max_por_string = 13, 15
        
    placas_minimas_potencia = math.ceil(potencia_necessaria_watts / placa_selecionada['P_max'])
    melhor_arranjo = None
    menor_sobra_placas = 9999
    
    for num_strings in range(1, 301):
        total_min_tensao = num_strings * min_por_string
        total_max_tensao = num_strings * max_por_string
        total_placas_alvo = max(placas_minimas_potencia, total_min_tensao)
        
        if total_placas_alvo <= total_max_tensao:
            placas_por_string = math.ceil(total_placas_alvo / num_strings)
            total_real = placas_por_string * num_strings
            
            if placas_por_string <= max_por_string:
                sobra = total_real - placas_minimas_potencia
                if sobra < menor_sobra_placas:
                    menor_sobra_placas = sobra
                    melhor_arranjo = {
                        'strings': num_strings,
                        'placas_por_string': placas_por_string,
                        'total_placas': total_real
                    }
                    if sobra == 0: break
    return melhor_arranjo

def gerar_pdf(nome_cliente, tel_cliente, email_cliente, bomba_dados, inversor, arranjo_rec, placa_sel, aviso_adaptacao=False):
    pdf = PropostaPDF()
    pdf.add_page()
    
    # Tratamento de campos vazios para o PDF
    nome = nome_cliente if nome_cliente else "Cliente não identificado"
    tel = tel_cliente if tel_cliente else "-"
    email = email_cliente if email_cliente else "Não informado"

    # 1. Dados do Projeto
    pdf.chapter_title("1. Dados do Cliente e Projeto")
    texto_bomba = (f"Cliente: {nome}\n"
                   f"Telefone: {tel}\n"
                   f"Email: {email}\n"
                   f"Data: {datetime.now().strftime('%d/%m/%Y')}\n\n"
                   f"Tipo de Bomba: {bomba_dados['Tipo']}\n"
                   f"Potência: {bomba_dados['CV']} CV ({bomba_dados['kW']:.2f} kW)\n"
                   f"Tensão: {bomba_dados['Tensao']}\n"
                   f"Corrente Nominal: {bomba_dados['Corrente']} A")
    pdf.chapter_body(texto_bomba)
    
    # 2. Inversor
    pdf.chapter_title("2. Inversor Selecionado (Apollo)")
    texto_inv = (f"Modelo: {inversor['Modelo']}\n"
                 f"Potência Nominal: {inversor['Potencia_KW']} kW\n"
                 f"Corrente Nominal: {inversor['Corrente_Nominal_A']} A\n"
                 f"Tensão Máx DC: {inversor['Max_DC']} V")
    
    if aviso_adaptacao:
        texto_inv += "\n\nNOTA: Inversor da linha 380V selecionado para atender a alta corrente da bomba em 220V. Necessário parametrizar a tensão de saída."
        
    pdf.chapter_body(texto_inv)
    
    # 3. Solar
    pdf.chapter_title("3. Arranjo Fotovoltaico (Recomendado)")
    if arranjo_rec:
        tot = arranjo_rec['total_placas']
        pot_pico = (tot * placa_sel['P_max']) / 1000
        texto_solar = (f"Painel: {placa_sel['Modelo']} ({placa_sel['P_max']}W)\n"
                       f"Configuração: {arranjo_rec['strings']} Strings de {arranjo_rec['placas_por_string']} Placas\n"
                       f"Total de Módulos: {tot} unidades\n"
                       f"Potência Total: {pot_pico:.2f} kWp\n"
                       f"Fator de Dimensionamento: 2.5x Potência da Bomba")
        pdf.chapter_body(texto_solar)
    
    # 4. Materiais
    pdf.chapter_title("4. Resumo de Materiais")
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(100, 8, "Descrição", 1)
    pdf.cell(30, 8, "Qtd", 1, 0, 'C')
    pdf.cell(60, 8, "Detalhe", 1, 1, 'C')
    pdf.set_font('Arial', '', 10)
    
    pdf.cell(100, 8, f"Inversor Apollo {inversor['Modelo']}", 1)
    pdf.cell(30, 8, "1", 1, 0, 'C')
    pdf.cell(60, 8, "Apollo Drive", 1, 1)
    
    if arranjo_rec:
        pdf.cell(100, 8, f"Módulo {placa_sel['Modelo']}", 1)
        pdf.cell(30, 8, f"{arranjo_rec['total_placas']}", 1, 0, 'C')
        pdf.cell(60, 8, f"{placa_sel['P_max']}W", 1, 1)
        
    return pdf.output(dest='S').encode('latin-1')

# ==============================================================================
# 3. INTERFACE STREAMLIT
# ==============================================================================

# --- DATABASE CONNECTION (Google Sheets) ---
# Tenta conectar se as credenciais existirem, senão roda sem banco
conn = None
try:
    if "gsheets" in st.secrets.get("connections", {}):
        from streamlit_gsheets import GSheetsConnection
        conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    pass # Roda apenas localmente sem salvar

def salvar_lead(dados):
    """Salva os dados na planilha se a conexão estiver ativa"""
    if conn:
        try:
            # Lê dados existentes
            df_existente = conn.read()
            # Adiciona nova linha
            df_novo = pd.DataFrame([dados])
            df_final = pd.concat([df_existente, df_novo], ignore_index=True)
            # Atualiza planilha
            conn.update(data=df_final)
        except Exception as e:
            st.error(f"Erro ao salvar no banco de dados: {e}")

st.set_page_config(page_title="Dimensionamento Solar Apollo", layout="wide", page_icon="☀️")

if os.path.exists('logo.png'):
    st.image('logo.png', width=200)

st.title("☀️ Sistema de Dimensionamento Solar - Apollo")
st.markdown("Selecione o modelo da bomba e do painel conforme catálogo.")
st.markdown("---")

# --- 1. SELEÇÃO DA BOMBA ---
st.subheader("1. Seleção da Bomba")
c1, c2, c3, c4 = st.columns(4)

with c1:
    tipo_bomba = st.radio("Tipo de Sistema", ["Submersa", "Superfície / Periférica"])

if tipo_bomba == "Submersa":
    lista_bombas = DB_BOMBAS_SUBMERSA
else:
    lista_bombas = DB_BOMBAS_PERIFERICA

with c2:
    opcoes_potencia = sorted(list(set([b['CV'] for b in lista_bombas])))
    try:
        idx_padrao = opcoes_potencia.index(1.0)
    except ValueError:
        idx_padrao = 0
    potencia_cv = st.selectbox("Modelo da Bomba (CV)", options=opcoes_potencia, index=idx_padrao)

with c3:
    tensao_bomba = st.selectbox("Tensão de Operação", ["220V", "380V"])

bomba_selecionada = next((b for b in lista_bombas if b['CV'] == potencia_cv), None)
corrente_padrao = 0.0
if bomba_selecionada:
    if tensao_bomba == "220V":
        corrente_padrao = bomba_selecionada['I_220']
    else:
        corrente_padrao = bomba_selecionada['I_380']

with c4:
    corrente_bomba = st.number_input("Corrente Nominal (A)", value=corrente_padrao, step=0.1, format="%.2f")

# --- 2. SELEÇÃO DO PAINEL ---
st.divider()
st.subheader("2. Seleção do Painel Solar")
cp1, cp2 = st.columns([1, 3])

with cp1:
    nomes_paineis = [p['Modelo'] for p in DB_PLACAS]
    nome_painel_sel = st.selectbox("Modelo do Painel", options=nomes_paineis)
    painel_sel = next(p for p in DB_PLACAS if p['Modelo'] == nome_painel_sel)

with cp2:
    st.info(f"**Detalhes do Painel:** Pmax: {painel_sel['P_max']}W | Vmp: {painel_sel['V_mp']}V | Imp: {painel_sel['I_mp']}A | Voc: {painel_sel['V_oc']}V")

# --- CÁLCULO ---
if 'calculou' not in st.session_state:
    st.session_state['calculou'] = False

st.divider()

if st.button("🚀 Calcular Dimensionamento", use_container_width=True):
    st.session_state['calculou'] = True

if st.session_state['calculou']:
    
    potencia_bomba_kw = potencia_cv * 0.736
    corrente_com_folga = corrente_bomba * 1.10
    
    # === LÓGICA DE INVERSORES (AJUSTADA) ===
    aviso_adaptacao = False
    
    if tensao_bomba == "220V":
        if potencia_bomba_kw <= 2.2:
            # Até 2.2kW usa linha 220V nativa (SS2)
            df_filtrado = df_inversores[df_inversores['Tensao'] == '220V'].copy()
        else:
            # Acima de 2.2kW usa linha 380V (Série 4) adaptada pela corrente
            df_filtrado = df_inversores[df_inversores['Tensao'] == '380V'].copy()
            aviso_adaptacao = True
    else:
        # 380V padrão
        df_filtrado = df_inversores[df_inversores['Tensao'] == '380V'].copy()
    
    if df_filtrado.empty:
         st.error("Erro no banco de dados de inversores.")
    else:
        # Busca pelo inversor que atende a potência E a corrente
        inversores = df_filtrado[
            (df_filtrado['Potencia_KW'] >= potencia_bomba_kw) &
            (df_filtrado['Corrente_Nominal_A'] >= corrente_com_folga)
        ].sort_values('Potencia_KW')
        
        if inversores.empty:
            st.warning(f"⚠️ Atenção: Nenhum inversor Apollo encontrado para {potencia_cv}CV / {corrente_bomba}A. Verifique se a corrente está correta.")
            inversor_eleito = None
        else:
            inversor_eleito = inversores.iloc[0]
            
            # Cálculo Solar
            pot_min_w = (potencia_bomba_kw * 1000) * 1.5
            pot_rec_w = (potencia_bomba_kw * 1000) * 2.5
            
            arranjo_min = calcular_arranjo_otimizado(pot_min_w, tensao_bomba, painel_sel)
            arranjo_rec = calcular_arranjo_otimizado(pot_rec_w, tensao_bomba, painel_sel)
            
            # --- RESULTADOS ---
            st.success(f"✅ Sistema Apollo Dimensionado!")
            
            col_res1, col_res2 = st.columns(2)
            
            with col_res1:
                st.markdown("### 🔌 Inversor Apollo")
                st.write(f"**Modelo:** {inversor_eleito['Modelo']}")
                st.write(f"**Capacidade:** {inversor_eleito['Potencia_KW']} kW | {inversor_eleito['Corrente_Nominal_A']} A")
                st.caption(f"Considerando folga de 10% ({corrente_com_folga:.2f}A)")
                
                if aviso_adaptacao:
                    st.warning("ℹ️ Inversor 380V selecionado para bomba de alta potência em 220V. Requer parametrização de tensão de saída.")
            
            with col_res2:
                st.markdown("### ☀️ Mínimo (1.5x)")
                if arranjo_min:
                    tot_min = arranjo_min['total_placas']
                    st.write(f"**{tot_min}x Painéis** ({arranjo_min['strings']} strings de {arranjo_min['placas_por_string']})")
                
                st.markdown("### 🌟 Recomendado (2.5x)")
                if arranjo_rec:
                    tot_rec = arranjo_rec['total_placas']
                    st.write(f"**{tot_rec}x Painéis** ({arranjo_rec['strings']} strings de {arranjo_rec['placas_por_string']})")

            # --- LEAD E DOWNLOAD ---
            st.divider()
            st.markdown("### 👤 Dados do Cliente para Proposta")
            
            cc1, cc2, cc3 = st.columns(3)
            with cc1:
                nome_cliente = st.text_input("Nome do Cliente", key="cli_nome")
            with cc2:
                tel_cliente = st.text_input("Telefone", key="cli_tel")
            with cc3:
                email_cliente = st.text_input("Email", key="cli_email")
            
            st.caption("Preencha os dados acima para incluir na proposta.")

            if arranjo_rec:
                dados_bomba_pdf = {'Tipo': tipo_bomba, 'CV': potencia_cv, 'kW': potencia_bomba_kw, 'Tensao': tensao_bomba, 'Corrente': corrente_bomba}
                
                # Gera o PDF usando as variáveis capturadas agora
                pdf_bytes = gerar_pdf(nome_cliente, tel_cliente, email_cliente, dados_bomba_pdf, inversor_eleito, arranjo_rec, painel_sel, aviso_adaptacao)
                
                # Botão de Download que também salva no banco (se configurado)
                btn = st.download_button(
                    label="📄 Baixar Proposta em PDF",
                    data=pdf_bytes,
                    file_name=f"Proposta_Apollo_{nome_cliente.replace(' ','_') if nome_cliente else 'Cliente'}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                
                if btn and conn:
                    # Salva Lead se clicou no botão e tem conexão
                    lead_data = {
                        "Data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Cliente": nome_cliente,
                        "Telefone": tel_cliente,
                        "Email": email_cliente,
                        "Bomba_CV": potencia_cv,
                        "Inversor": inversor_eleito['Modelo'],
                        "Placas": arranjo_rec['total_placas'],
                        "Potencia_Pico_KW": (arranjo_rec['total_placas'] * painel_sel['P_max'])/1000
                    }
                    salvar_lead(lead_data)
