# views/rede_bayesiana.py
import streamlit as st
import pandas as pd
import graphviz
import config as C
import data as D
import ui
import bayes

def render(d: pd.DataFrame, ctx: dict):
    if d.empty:
        ui.vazio()
        return

    ui.secao("Rede Bayesiana de Risco KYC",
             "Inferência probabilística com base em evidências observáveis")

    @st.cache_resource
    def obter_modelo(df_hash, df):
        return bayes.treinar_rede(df)

    hash_dados = f"{len(d)}_{d['Score_Prioridade'].sum()}"
    modelo, dados_treino = obter_modelo(hash_dados, d)

    if modelo is None:
        ui.alerta("Poucos dados para treinar a rede (menos de 50 registos).", C.CORES["ambar"])
        return

    # 1. DAG MELHORADO
    with st.container(border=True):
        st.markdown("**Estrutura da Rede (DAG)**")
        g = graphviz.Digraph(engine='dot') # Motor hierárquico
        g.attr(rankdir="LR", size="8,4", bgcolor="transparent")
        g.attr('node', shape='box', style='rounded,filled', fillcolor='#E7ECF2', 
               color='#0F9D9D', fontname='Helvetica', fontsize='12', margin='0.2')
        g.attr('edge', color='#8A99A8', penwidth='1.5')
        
        # Adicionar o nó alvo com cor diferente
        g.node('Risco_Alvo', fillcolor='#0E2A47', fontcolor='white')
        
        for pai, filho in bayes.ESTRUTURA:
            g.edge(pai, filho)
            
        st.graphviz_chart(g, use_container_width=True)

    # 2. FORMULÁRIO DE EVIDÊNCIAS
    st.markdown("### Definir evidências")
    
    with st.form("form_evidencias"):
        c1, c2, c3 = st.columns(3)
        with c1:
            pep = st.selectbox("PEP / RCA", sorted(dados_treino["PEP_RCA"].unique()))
            pais = st.selectbox("Jurisdição", sorted(dados_treino["Pais_Risco"].unique()))
        with c2:
            tipo = st.selectbox("Tipo de cliente", sorted(dados_treino["Tipo_Cliente"].unique()))
            estado = st.selectbox("Estado documental", sorted(dados_treino["Estado_Documento"].unique()))
        with c3:
            idade = st.selectbox("Segmento de idade", sorted(dados_treino["Segmento_Idade"].unique()))
            tempo = st.selectbox("Antiguidade", sorted(dados_treino["Faixa_Relacionamento"].unique()))

        # O botão de calcular
        submitted = st.form_submit_button("🔮 Calcular Probabilidades", use_container_width=True, type="primary")

    # 3. INFERÊNCIA (Só corre quando o botão é clicado)
    if submitted:
        evidencias = {
            "PEP_RCA": pep,
            "Pais_Risco": pais,
            "Tipo_Cliente": tipo,
            "Estado_Documento": estado,
            "Segmento_Idade": idade,
            "Faixa_Relacionamento": tempo,
        }
        try:
            resultado = bayes.inferir_risco(modelo, evidencias)
            probs = resultado["probabilidades"]

            ui.secao("Resultado da Inferência")
            c1, c2, c3 = st.columns(3)
            for col, nivel in zip([c1, c2, c3], ["Baixo", "Médio", "Alto"]):
                with col:
                    prob = probs.get(nivel, 0) * 100
                    ui.kpi(
                        rotulo=f"Risco {nivel}",
                        valor=ui.pct(prob),
                        cor=C.COR_RISCO.get(nivel, C.CORES["cinza"]),
                    )
            st.markdown(
                ui.pill("Evidências aplicadas", C.CORES["navy"]), unsafe_allow_html=True
            )
            st.write(", ".join(f"**{k}**: {v}" for k, v in evidencias.items()))
            
        except Exception as e:
            st.warning(f"Não foi possível inferir: {e}")