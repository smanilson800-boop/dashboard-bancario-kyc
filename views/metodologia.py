import streamlit as st
import config as C
import ui
def render(d, ctx):
    ui.secao("Sobre o Dashboard")
    ui.alerta("Dashboard construído para análise de KYC e Compliance (AML/CFT).", C.CORES["navy"], "#F5F9FF")
    st.markdown("**Arquitetura:** `app.py` (UI) + `data.py` (Motor) + `charts.py` (Gráficos) + `config.py` (Regras).")
