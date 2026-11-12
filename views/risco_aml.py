import pandas as pd
import streamlit as st
import charts as ch
import config as C
import data as D
import ui
def render(d, ctx):
    if d.empty: ui.vazio(); return
    ui.secao("Matriz de risco")
    c1, c2 = st.columns([1, 1])
    with c1, st.container(border=True):
        dim = st.selectbox("Cruzar com", ["Tipo_Cliente", "Atividade_Economica", "Pais_PT"], key="ra_dim")
        t = D.cruzar(d, dim, "Nivel_Risco", normalizar=True).reindex(columns=C.ORDEM_RISCO).fillna(0)
        ui.grafico(ch.heatmap(t, altura=300, percent=True), chave="ra_h")
    with c2, st.container(border=True):
        st.markdown("**Fatores de prioridade**")
        fat = D.contributors_prioridade(d, ctx["pesos"])
        ui.grafico(ch.barras_h(fat, "Fator", "Clientes", cor=C.CORES["navy_claro"], altura=300), chave="ra_f")
    ui.secao("Fila de intervenção")
    cols = ["ID_Cliente", "Score_Prioridade", "Nivel_Risco", "PEP_RCA", "Estado_Documento", "Alerta_Principal"]
    ui.tabela(d.sort_values("Score_Prioridade", ascending=False).head(20)[cols], altura=300)
