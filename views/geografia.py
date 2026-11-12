import pandas as pd
import streamlit as st
import charts as ch
import config as C
import data as D
import ui
def render(d, ctx):
    if d.empty: ui.vazio(); return
    st.markdown("**Mapa de clientes**")
    with st.container(border=True):
        g = d.groupby(["Pais_Residencia", "Pais_PT", "ISO3"], observed=True, dropna=False).size().reset_index(name="n")
        ui.grafico(ch.mapa_mundi(g.dropna(subset=["ISO3"]), altura=400), chave="geo_m")
