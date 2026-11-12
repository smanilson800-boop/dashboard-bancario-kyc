from __future__ import annotations
import datetime as dt
import pandas as pd
import streamlit as st
import config as C
import data as D
import ui
import views

st.set_page_config(page_title=C.APP_TITULO, page_icon="🏦", layout="wide", initial_sidebar_state="expanded")
ui.injetar_css()

with st.sidebar:
    st.markdown("## 🏦 Painel Bancário")
    st.caption(C.APP_SUBTITULO)
    st.markdown("---")
    with st.expander("📂 Fonte de dados", expanded=False):
        upload = st.file_uploader("Carregar outro CSV", type=["csv"])
    try:
        bruto = D.carregar_bruto(upload if upload else str(C.DATA_PATH))
    except FileNotFoundError:
        st.error(f"CSV não encontrado em `{C.DATA_PATH}`. Coloca o ficheiro em `data/`.")
        st.stop()

    st.markdown("### ⚙️ Parâmetros")
    data_ref = st.date_input("Data de referência", value=dt.date(2026, 11, 12), key="p_ref")
    janela = st.select_slider("Janela «a vencer» (dias)", options=[30, 60, 90, 120, 180, 365], value=C.JANELA_ALERTA_PADRAO, key="p_janela")

    st.markdown("### 🎯 Filtros")
    filtros = {}
    def _multi(coluna: str, chave: str, rotulo: str):
        opcoes = sorted(bruto[coluna].dropna().astype(str).unique().tolist())
        return st.multiselect(rotulo, opcoes, default=[], key=chave)
    filtros["tipo_cliente"] = _multi("Tipo_Cliente", "f_tipo", "Tipo de cliente")
    filtros["risco"] = _multi("Nivel_Risco", "f_risco", "Nível de risco")
    filtros["estado"] = st.multiselect("Estado documental", C.ORDEM_ESTADO, default=[], key="f_estado")
    filtros["tipo_conta"] = _multi("Tipo_Conta", "f_conta", "Tipo de conta")
    filtros["pais"] = _multi("Pais_Residencia", "f_pais", "País de residência")
    filtros["nacionalidade"] = _multi("Nacionalidade_Primaria", "f_nac", "Nacionalidade")
    filtros["sexo"] = _multi("Sexo", "f_sexo", "Sexo")
    filtros["tipo_documento"] = _multi("Tipo_Documento", "f_doc", "Tipo de documento")
    filtros["atividade"] = _multi("Atividade_Economica", "f_ativ", "Atividade económica")
    filtros["pep"] = st.radio("PEP / RCA", ["Todos", "Sim", "Não"], horizontal=True, key="f_pep")
    filtros["apenas_inconsistentes"] = st.toggle("Só registos com inconsistências", value=False, key="f_inc")
    filtros["pesquisa"] = st.text_input("🔎 Pesquisa livre", key="f_pesq")

    with st.expander("⚖️ Modelo de prioridade (pesos)", expanded=False):
        pesos = {}
        for chave, valor in C.PESOS_PADRAO.items():
            pesos[chave] = st.slider(C.ROTULOS_PESOS[chave], 0, 50, valor, 1, key=f"w_{chave}")

    st.markdown("---")
    rotulos = [f"{ico}  {nome}" for nome, ico, _, _ in views.PAGINAS]
    escolha = st.radio("Página", rotulos, label_visibility="collapsed", key="nav")

base = D.enriquecer(bruto, data_ref, janela)
base = D.indice_prioridade(base, pesos)
d = D.aplicar_filtros(base, filtros)

ctx = {"bruto": bruto, "base": base, "data_ref": data_ref, "janela": janela, "pesos": pesos, "filtros": filtros}
n_ativos = sum(bool(v) for chave, v in filtros.items() if not (chave == "pep" and v == "Todos"))
nome_pagina = escolha.split("  ", 1)[-1].strip()
ui.cabecalho(nome_pagina, C.APP_SUBTITULO, chips=[f"{len(d):,} clientes no perímetro".replace(",", " "), f"Data ref.: {ui.data_br(data_ref)}", f"Janela: {janela} dias", f"{n_ativos} filtro(s) ativo(s)" if n_ativos else "Sem filtros ativos"])
modulo = next(m for nome, ico, m, _ in views.PAGINAS if nome == nome_pagina)
modulo.render(d, ctx)
