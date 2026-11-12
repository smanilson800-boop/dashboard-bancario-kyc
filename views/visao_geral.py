import pandas as pd
import streamlit as st
import charts as ch
import config as C
import data as D
import ui
def render(d, ctx):
    if d.empty: ui.vazio(); return
    k = D.kpis(d)
    ui.linha_kpis([
        {"rotulo": "Clientes", "valor": ui.num(k["total"]), "sub": "no perímetro", "cor": C.CORES["navy"]},
        {"rotulo": "Risco Alto", "valor": ui.num(k["risco_alto"]), "sub": f"<b>{ui.pct(k['risco_alto_pct'])}</b>", "cor": C.CORES["vermelho"]},
        {"rotulo": "Expirados", "valor": ui.num(k["expirados"]), "sub": f"<b>{ui.pct(k['expirados_pct'])}</b>", "cor": C.CORES["vermelho"]},
        {"rotulo": "PEP / RCA", "valor": ui.num(k["pep"]), "sub": f"<b>{ui.pct(k['pep_pct'])}</b>", "cor": C.CORES["roxo"]},
    ])
    c1, c2 = st.columns(2)
    with c1, st.container(border=True):
        st.markdown("**Nível de risco**")
        vc = d["Nivel_Risco"].value_counts()
        ui.grafico(ch.donut(vc.index, vc.values, C.COR_RISCO, ordem=C.ORDEM_RISCO, altura=300), chave="vg_r")
    with c2, st.container(border=True):
        st.markdown("**Estado documental**")
        vc = d["Estado_Documento"].value_counts()
        ui.grafico(ch.donut(vc.index, vc.values, C.COR_ESTADO, ordem=C.ORDEM_ESTADO, altura=300), chave="vg_e")
