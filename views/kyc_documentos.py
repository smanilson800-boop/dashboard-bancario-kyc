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
        {"rotulo": "Conformidade", "valor": ui.pct(100 - k["expirados_pct"]), "cor": C.CORES["verde"]},
        {"rotulo": "Críticos ≤ 30d", "valor": ui.num(k["criticos"]), "cor": "#F0713F"},
        {"rotulo": "A vencer", "valor": ui.num(k["a_vencer"]), "cor": C.CORES["ambar"]},
    ])
    c1, c2 = st.columns(2)
    with c1, st.container(border=True):
        st.markdown("**Situação do documento**")
        vc = d["Estado_Documento"].value_counts().reindex(C.ORDEM_ESTADO).fillna(0)
        tab = pd.DataFrame({"Estado": vc.index, "n": vc.values.astype(int)})
        ui.grafico(ch.barras_v(tab, "Estado", "n", escala_cor=C.COR_ESTADO, ordem=C.ORDEM_ESTADO, altura=300), chave="ky_p")
    with c2, st.container(border=True):
        st.markdown("**Documentos expirados (antiguidade)**")
        exp = d[d["Estado_Documento"].eq("Expirado")].copy()
        if not exp.empty:
            exp["Atraso"] = -exp["Dias_Para_Vencer"]
            ui.grafico(ch.histograma(exp["Atraso"], cor=C.CORES["vermelho"], altura=300), chave="ky_a")
