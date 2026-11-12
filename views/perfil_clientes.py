import pandas as pd
import streamlit as st
import charts as ch
import config as C
import data as D
import ui
def render(d, ctx):
    if d.empty: ui.vazio(); return
    c1, c2 = st.columns(2)
    with c1, st.container(border=True):
        st.markdown("**Pirâmide etária**")
        pir = d.groupby(["Segmento_Idade", "Sexo"], observed=True).size().reset_index(name="n")
        ui.grafico(ch.piramide(pir, altura=300), chave="pc_p")
    with c2, st.container(border=True):
        st.markdown("**Distribuição de idades**")
        ui.grafico(ch.histograma(d["Idade"], cor=C.CORES["azul"], altura=300), chave="pc_h")
