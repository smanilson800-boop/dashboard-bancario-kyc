# bayes.py
import pandas as pd
from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.parameter_estimator import DiscreteMLE
from pgmpy.inference import VariableElimination

ESTRUTURA = [
    ("PEP_RCA", "Risco_Alvo"),
    ("Pais_Risco", "Risco_Alvo"),
    ("Tipo_Cliente", "Risco_Alvo"),
    ("Estado_Documento", "Risco_Alvo"),
    ("Segmento_Idade", "Risco_Alvo"),
    ("Faixa_Relacionamento", "Risco_Alvo"),
]

def preparar_dados(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    def classificar_pais(row):
        if row.get("FATF", False): return "FATF"
        if row.get("Offshore", False): return "Offshore"
        return "Normal"
    d["Pais_Risco"] = d.apply(classificar_pais, axis=1)
    d["Risco_Alvo"] = d["Nivel_Risco"].astype(str)
    
    colunas = [
        "PEP_RCA", "Pais_Risco", "Tipo_Cliente", "Estado_Documento",
        "Segmento_Idade", "Faixa_Relacionamento", "Risco_Alvo",
    ]
    d_limpo = d[colunas].dropna().copy()
    
    # A CORREÇÃO CRÍTICA: O pgmpy precisa de 'category' e não 'string'
    for col in d_limpo.columns:
        d_limpo[col] = d_limpo[col].astype('category')
        
    return d_limpo

def treinar_rede(df: pd.DataFrame):
    dados = preparar_dados(df)
    if len(dados) < 50: 
        return None, dados
    
    modelo = DiscreteBayesianNetwork(ESTRUTURA)
    modelo.fit(dados, estimator=DiscreteMLE())
    return modelo, dados

def inferir_risco(modelo, evidencias: dict) -> dict:
    infer = VariableElimination(modelo)
    resultado = infer.query(variables=["Risco_Alvo"], evidence=evidencias)
    return {
        "probabilidades": dict(zip(resultado.state_names["Risco_Alvo"], resultado.values)),
        "factor": resultado,
    }
    