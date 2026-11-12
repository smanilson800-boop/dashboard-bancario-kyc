from __future__ import annotations
import datetime as dt
import pandas as pd
import streamlit as st
import config as C

COLUNAS_DATA = ["Data_Validade", "Data_Emissao"]
COLUNAS_NUM = ["Idade", "Tempo_Relacionamento"]

@st.cache_data(show_spinner="A carregar a base de clientes...")
def carregar_bruto(caminho: str) -> pd.DataFrame:
    df = pd.read_csv(caminho, encoding="utf-8-sig", dtype=str)
    df.columns = [c.strip() for c in df.columns]
    for col in COLUNAS_DATA:
        df[col] = pd.to_datetime(df[col], errors="coerce")
    for col in COLUNAS_NUM:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    for col in df.columns:
        if df[col].dtype == object or str(df[col].dtype) == "str":
            df[col] = df[col].astype("string").str.strip()
    return df

def enriquecer(df: pd.DataFrame, data_ref: dt.date, janela: int = C.JANELA_ALERTA_PADRAO, jurisdicoes: set[str] | None = None) -> pd.DataFrame:
    jurisdicoes = C.JURISDICOES_RISCO if jurisdicoes is None else set(jurisdicoes)
    d = df.copy()
    ref = pd.Timestamp(data_ref)
    d["Dias_Para_Vencer"] = (d["Data_Validade"] - ref).dt.days
    dias = d["Dias_Para_Vencer"]
    d["Estado_Documento"] = pd.Series("Sem Data", index=d.index, dtype="string")
    d.loc[dias.notna(), "Estado_Documento"] = "Válido"
    d.loc[dias.notna() & (dias <= janela), "Estado_Documento"] = "A Vencer"
    d.loc[dias.notna() & (dias <= C.DIAS_CRITICO), "Estado_Documento"] = "Crítico"
    d.loc[dias.notna() & (dias < 0), "Estado_Documento"] = "Expirado"
    est90 = pd.Series("Sem Data", index=d.index, dtype="string")
    est90[dias.notna()] = "Válido"
    est90[dias.notna() & (dias <= 90)] = "Quase Expirando"
    est90[dias.notna() & (dias < 0)] = "Expirado"
    d["Estado_90d"] = est90
    d["Mes_Vencimento"] = d["Data_Validade"].dt.to_period("M").astype("string")
    d["Ano_Vencimento"] = d["Data_Validade"].dt.year
    d["Segmento_Idade"] = pd.cut(d["Idade"], bins=C.SEGMENTOS_IDADE, labels=C.LABELS_IDADE).astype("string")
    d["Faixa_Relacionamento"] = pd.cut(d["Tempo_Relacionamento"], bins=C.SEGMENTOS_TEMPO, labels=C.LABELS_TEMPO).astype("string")
    d["Pais_PT"] = d["Pais_Residencia"].map(C.PAIS_PT).fillna(d["Pais_Residencia"])
    d["ISO3"] = d["Pais_Residencia"].map(C.ISO3)
    d["Continente"] = d["Pais_Residencia"].map(_continente).fillna("Outro")
    d["Eh_PEP"] = d["PEP_RCA"].eq("Sim")
    d["Eh_Nao_Residente"] = d["Tipo_Cliente"].isin(["Não Residente", "Emigrante"]) | d["Condicao_Residente"].eq("Não")
    d["Eh_Pessoa_Coletiva"] = d["Tipo_Cliente"].eq("Pessoa Coletiva")
    d["Eh_Risco_Alto"] = d["Nivel_Risco"].eq("Alto")
    d["Jurisdicao_Risco"] = d["Pais_Residencia"].isin(jurisdicoes)
    d["FATF"] = d["Pais_Residencia"].isin(C.FATF_CALL_FOR_ACTION + C.FATF_INCREASED_MONITORING)
    d["Offshore"] = d["Pais_Residencia"].isin(C.OFFSHORE_INTERNO)
    for col in ["Eh_PEP", "Eh_Nao_Residente", "Eh_Pessoa_Coletiva", "Eh_Risco_Alto", "Jurisdicao_Risco", "FATF", "Offshore"]:
        d[col] = d[col].to_numpy(dtype=bool)
    f = pd.DataFrame(index=d.index)
    f["sem_datas"] = d["Data_Validade"].isna() | d["Data_Emissao"].isna()
    f["validade_sentinela"] = d["Ano_Vencimento"].ge(C.ANOS_VALIDADE_SUSPEITA).fillna(False)
    f["emissao_futura"] = d["Data_Emissao"].gt(ref).fillna(False)
    f["status_desatualizado"] = d["Status_Documento"].ne(d["Estado_90d"]) & d["Data_Validade"].notna()
    f["pep_risco_baixo"] = d["Eh_PEP"] & ~d["Eh_Risco_Alto"]
    f["pj_com_perfil_pessoal"] = d["Eh_Pessoa_Coletiva"] & (d["Idade"].notna() | d["Sexo"].notna())
    f["emigrante_residente"] = d["Tipo_Cliente"].eq("Emigrante") & d["Condicao_Residente"].eq("Sim")
    f["residencia_pais_divergente"] = (d["Condicao_Residente"].eq("Sim") & d["Pais_Residencia"].ne("Cabo Verde")) | (d["Condicao_Residente"].eq("Não") & d["Pais_Residencia"].eq("Cabo Verde"))
    f["nr_flag_divergente"] = d["Cliente_Nao_Residente"].eq("Não") & d["Condicao_Residente"].eq("Não")
    f["doc_pj_inadequado"] = (d["Eh_Pessoa_Coletiva"] & d["Tipo_Documento"].isin(C.DOCS_PESSOA_SINGULAR)) | (~d["Eh_Pessoa_Coletiva"] & d["Tipo_Documento"].isin(C.DOCS_PESSOA_COLETIVA))
    f = pd.DataFrame(f.to_numpy(dtype=bool), index=d.index, columns=[f"flag_{c}" for c in f.columns])
    d = pd.concat([d, f], axis=1)
    d["N_Flags"] = f.sum(axis=1)
    partes = pd.Series("", index=d.index, dtype="string")
    for col in f.columns:
        rotulo = C.REGRAS_QUALIDADE[col[len("flag_"):]][0]
        partes = partes + f[col].map({True: rotulo + "; ", False: ""})
    d["Flags"] = partes.str.rstrip("; ").astype("string")
    d["Tem_Inconsistencia"] = d["N_Flags"].gt(0)
    d["Alerta_Principal"] = _alerta_principal(d)
    return d

def _alerta_principal(d: pd.DataFrame) -> pd.Series:
    alerta = pd.Series("Sem alerta", index=d.index, dtype="string")
    alerta[d["Estado_Documento"].eq("A Vencer")] = "Documento a vencer"
    alerta[d["flag_sem_datas"]] = "Documentação sem datas"
    alerta[d["flag_emissao_futura"]] = "Data de emissão no futuro"
    alerta[d["flag_pep_risco_baixo"]] = "PEP sem risco Alto"
    alerta[d["Estado_Documento"].eq("Crítico")] = "Documento vence ≤ 30 dias"
    alerta[d["Estado_Documento"].eq("Expirado")] = "Documento expirado"
    alerta[d["Estado_Documento"].eq("Expirado") & d["Eh_Risco_Alto"]] = "Expirado + risco Alto"
    alerta[d["Estado_Documento"].eq("Expirado") & d["Eh_PEP"]] = "Expirado + PEP"
    return alerta

def indice_prioridade(d: pd.DataFrame, pesos: dict[str, int]) -> pd.DataFrame:
    d = d.copy()
    estado = d["Estado_Documento"]
    score = pd.Series(0.0, index=d.index)
    score += pesos["doc_expirado"] * estado.eq("Expirado").astype(int)
    score += pesos["doc_critico"] * estado.eq("Crítico").astype(int)
    score += pesos["doc_a_vencer"] * estado.eq("A Vencer").astype(int)
    score += pesos["doc_sem_data"] * estado.eq("Sem Data").astype(int)
    score += pesos["risco_alto"] * d["Eh_Risco_Alto"].astype(int)
    score += pesos["risco_medio"] * d["Nivel_Risco"].eq("Médio").astype(int)
    score += pesos["pep"] * d["Eh_PEP"].astype(int)
    score += pesos["nao_residente"] * d["Eh_Nao_Residente"].astype(int)
    score += pesos["jurisdicao_risco"] * d["Jurisdicao_Risco"].astype(int)
    score += pesos["inconsistencia"] * d["Tem_Inconsistencia"].astype(int)
    
    d["Score_Prioridade"] = score.clip(upper=100).round(1)
    classe = pd.Series("Baixa", index=d.index, dtype="string")
    for limiar, nome in sorted(C.LIMIARES_PRIORIDADE):
        classe[d["Score_Prioridade"] >= limiar] = nome
    d["Classe_Prioridade"] = classe
    return d

def contributors_prioridade(d: pd.DataFrame, pesos: dict[str, int]) -> pd.DataFrame:
    estado = d["Estado_Documento"]
    fatores = {
        "doc_expirado": estado.eq("Expirado"), "doc_critico": estado.eq("Crítico"),
        "doc_a_vencer": estado.eq("A Vencer"), "doc_sem_data": estado.eq("Sem Data"),
        "risco_alto": d["Eh_Risco_Alto"], "risco_medio": d["Nivel_Risco"].eq("Médio"),
        "pep": d["Eh_PEP"], "nao_residente": d["Eh_Nao_Residente"],
        "jurisdicao_risco": d["Jurisdicao_Risco"], "inconsistencia": d["Tem_Inconsistencia"],
    }
    linhas = [{"Fator": C.ROTULOS_PESOS[k], "Clientes": int(m.sum()), "Peso": pesos[k]} for k, m in fatores.items()]
    out = pd.DataFrame(linhas)
    return out[out["Clientes"] > 0].sort_values("Clientes", ascending=False)

def aplicar_filtros(d: pd.DataFrame, flt: dict) -> pd.DataFrame:
    m = pd.Series(True, index=d.index)
    for coluna, chave in [
        ("Tipo_Cliente", "tipo_cliente"), ("Nivel_Risco", "risco"), ("Tipo_Conta", "tipo_conta"),
        ("Pais_PT", "pais"), ("Nacionalidade_Primaria", "nacionalidade"), ("Sexo", "sexo"),
        ("Estado_Documento", "estado"), ("Tipo_Documento", "tipo_documento"), ("Atividade_Economica", "atividade"),
    ]:
        valores = flt.get(chave)
        if valores:
            m &= d[coluna].isin(valores)
    if flt.get("pep") and flt["pep"] != "Todos":
        m &= d["PEP_RCA"].eq(flt["pep"])
    if flt.get("apenas_inconsistentes"):
        m &= d["Tem_Inconsistencia"]
    if flt.get("idade"):
        m &= d["Idade"].between(*flt["idade"])
    if flt.get("tempo"):
        m &= d["Tempo_Relacionamento"].between(*flt["tempo"])
    if flt.get("pesquisa"):
        termo = flt["pesquisa"].strip().lower()
        if termo:
            alvo = d["ID_Cliente"].astype("string").str.lower() + " " + d["Pais_PT"].astype("string").str.lower() + " " + d["Nacionalidade_Primaria"].astype("string").str.lower() + " " + d["Atividade_Economica"].astype("string").str.lower()
            m &= alvo.str.contains(termo, na=False, regex=False)
    return d[m]

def kpis(d: pd.DataFrame) -> dict:
    n = len(d)
    if n == 0:
        return {k: 0 for k in ["total", "risco_alto", "risco_alto_pct", "expirados", "expirados_pct", "criticos", "a_vencer", "sem_data", "pep", "pep_pct", "nao_residentes", "nao_residentes_pct", "idade_media", "tempo_medio", "inconsistentes", "inconsistentes_pct", "prioridade_critica", "jurisdicao_risco"]}
    estado = d["Estado_Documento"]
    return {
        "total": n, "risco_alto": int(d["Eh_Risco_Alto"].sum()), "risco_alto_pct": 100 * d["Eh_Risco_Alto"].mean(),
        "expirados": int(estado.eq("Expirado").sum()), "expirados_pct": 100 * estado.eq("Expirado").mean(),
        "criticos": int(estado.eq("Crítico").sum()), "a_vencer": int(estado.eq("A Vencer").sum()),
        "sem_data": int(estado.eq("Sem Data").sum()), "pep": int(d["Eh_PEP"].sum()),
        "pep_pct": 100 * d["Eh_PEP"].mean(), "nao_residentes": int(d["Eh_Nao_Residente"].sum()),
        "nao_residentes_pct": 100 * d["Eh_Nao_Residente"].mean(), "idade_media": float(d["Idade"].mean()),
        "tempo_medio": float(d["Tempo_Relacionamento"].mean()), "inconsistentes": int(d["Tem_Inconsistencia"].sum()),
        "inconsistentes_pct": 100 * d["Tem_Inconsistencia"].mean(),
        "prioridade_critica": int(d["Classe_Prioridade"].eq("Crítica").sum()) if "Classe_Prioridade" in d else 0,
        "jurisdicao_risco": int(d["Jurisdicao_Risco"].sum()),
    }

def cruzar(d: pd.DataFrame, linhas: str, colunas: str, normalizar: bool = False) -> pd.DataFrame:
    t = pd.crosstab(d[linhas], d[colunas])
    if normalizar:
        t = (t.div(t.sum(axis=1).replace(0, pd.NA), axis=0) * 100).round(1)
    return t

def _continente(pais: str) -> str:
    europa = {"Albania", "Belgium", "Estonia", "France", "Hungary", "Iceland", "Ireland", "Italy", "Luxembourg", "Netherlands", "Norway", "Portugal", "Slovenia", "Spain", "Sweden", "Switzerland", "United Kingdom", "West Germany"}
    africa = {"Angola", "Benin", "Cabo Verde", "Congo Democratic Republic", "Djibouti", "Equatorial Guinea", "Gambia, The", "Ghana", "Guinea", "Guinea-Bissau", "Morocco", "Mozambique", "Nigeria", "Rwanda", "Senegal", "Sierra Leone", "Tunisia", "Uganda", "Zambia"}
    america = {"Brazil", "Canada", "United States Of America"}
    asia = {"Bahrain", "Japan", "Macau", "Pakistan", "Peoples Republic Of China", "Saudi Arabia"}
    oceania = {"Australia", "New Zealand"}
    if pais in europa: return "Europa"
    if pais in africa: return "África"
    if pais in america: return "Américas"
    if pais in asia: return "Ásia"
    if pais in oceania: return "Oceania"
    return "Outro"
