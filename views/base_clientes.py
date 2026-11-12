import pandas as pd
import streamlit as st
import config as C
import data as D
import ui
def render(d, ctx):
    if d.empty: ui.vazio(); return
    ui.secao("Explorador")
    cols = ["ID_Cliente", "Tipo_Cliente", "Pais_PT", "Nivel_Risco", "Estado_Documento", "Score_Prioridade"]
    ui.tabela(d[cols].head(100), altura=400)
