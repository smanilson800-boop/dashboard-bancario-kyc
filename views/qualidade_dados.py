import pandas as pd
import streamlit as st
import charts as ch
import config as C
import data as D
import ui
def render(d, ctx):
    if d.empty: ui.vazio(); return
    regras = []
    for r, (rot, sev, desc) in C.REGRAS_QUALIDADE.items():
        n = int(d[f"flag_{r}"].sum())
        if n > 0: regras.append({"Regra": rot, "Ocorrências": n})
    if regras:
        with st.container(border=True):
            st.markdown("**Ocorrências por regra**")
            ui.grafico(ch.barras_h(pd.DataFrame(regras), "Regra", "Ocorrências", cor=C.CORES["ambar"], altura=300), chave="qd_r")
    else:
        ui.alerta("✅ Sem inconsistências no perímetro.", C.CORES["verde"], "#F3FBF7")
