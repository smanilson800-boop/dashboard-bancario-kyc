from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "clientes_banco_real.csv"

APP_TITULO = "Painel de Controlo Bancário"
APP_SUBTITULO = "KYC · Risco de Clientes · Compliance AML/CFT"
BANCO_NOME = "Instituição Financeira · Cabo Verde"

CORES = {
    "navy": "#0E2A47", "navy_claro": "#1B4B73", "teal": "#0F9D9D",
    "azul": "#2E6FDB", "azul_claro": "#7FA8E8", "cinza": "#8A99A8",
    "cinza_claro": "#E7ECF2", "fundo": "#F4F7FB", "texto": "#14243A",
    "verde": "#1F9D6B", "ambar": "#E39A2B", "vermelho": "#D6455D", "roxo": "#7A5AF8",
}
ORDEM_RISCO = ["Baixo", "Médio", "Alto"]
COR_RISCO = {"Baixo": CORES["verde"], "Médio": CORES["ambar"], "Alto": CORES["vermelho"]}
ORDEM_ESTADO = ["Expirado", "Crítico", "A Vencer", "Válido", "Sem Data"]
COR_ESTADO = {
    "Expirado": CORES["vermelho"], "Crítico": "#F0713F",
    "A Vencer": CORES["ambar"], "Válido": CORES["verde"], "Sem Data": CORES["cinza"],
}
ORDEM_TIPO_CLIENTE = ["Residente", "Não Residente", "Emigrante", "Pessoa Coletiva"]
COR_TIPO_CLIENTE = {
    "Residente": CORES["azul"], "Não Residente": CORES["teal"],
    "Emigrante": CORES["roxo"], "Pessoa Coletiva": CORES["cinza"],
}
COR_PRIORIDADE = {
    "Crítica": CORES["vermelho"], "Alta": "#F0713F",
    "Média": CORES["ambar"], "Baixa": CORES["verde"],
}
ORDEM_PRIORIDADE = ["Crítica", "Alta", "Média", "Baixa"]
SEQ_AZUIS = ["#0E2A47", "#1B4B73", "#2E6FDB", "#5C93E8", "#9FC2F2", "#D3E3FA"]
SEQ_TEAL = ["#065F5F", "#0F9D9D", "#4FC3C3", "#9BDADA"]

DIAS_CRITICO = 30
JANELA_ALERTA_PADRAO = 90
ANOS_VALIDADE_SUSPEITA = 2050

PESOS_PADRAO = {
    "doc_expirado": 40, "doc_critico": 30, "doc_a_vencer": 18, "doc_sem_data": 35,
    "risco_alto": 20, "risco_medio": 10, "pep": 15, "nao_residente": 8,
    "jurisdicao_risco": 12, "inconsistencia": 7,
}
ROTULOS_PESOS = {
    "doc_expirado": "Documento expirado", "doc_critico": "Documento vence ≤ 30 dias",
    "doc_a_vencer": "Documento vence na janela de alerta", "doc_sem_data": "Sem data de validade",
    "risco_alto": "Nível de risco Alto", "risco_medio": "Nível de risco Médio",
    "pep": "PEP / RCA", "nao_residente": "Não residente / emigrante",
    "jurisdicao_risco": "Jurisdição de risco reforçado", "inconsistencia": "Inconsistência de dados",
}
LIMIARES_PRIORIDADE = [(70, "Crítica"), (50, "Alta"), (30, "Média"), (0, "Baixa")]

FATF_CALL_FOR_ACTION = ["Democratic People's Republic of Korea", "Iran", "Myanmar"]
FATF_INCREASED_MONITORING = [
    "Angola", "Bolivia", "Bosnia and Herzegovina", "Cameroon", "Haiti", "Iraq",
    "Kenya", "Kuwait", "Lao People's Democratic Republic", "Lebanon", "Nepal",
    "Papua New Guinea", "South Sudan", "Syria", "Venezuela", "Vietnam",
    "Virgin Islands (UK)", "Yemen",
]
OFFSHORE_INTERNO = ["Macau", "Mauritius", "Bahrain", "Luxembourg"]
JURISDICOES_RISCO = set(FATF_CALL_FOR_ACTION + FATF_INCREASED_MONITORING + OFFSHORE_INTERNO)

ISO3 = {
    "Albania": "ALB", "Angola": "AGO", "Australia": "AUS", "Bahrain": "BHR", "Belgium": "BEL",
    "Benin": "BEN", "Brazil": "BRA", "Cabo Verde": "CPV", "Canada": "CAN",
    "Congo Democratic Republic": "COD", "Djibouti": "DJI", "Equatorial Guinea": "GNQ",
    "Estonia": "EST", "France": "FRA", "Gambia, The": "GMB", "Ghana": "GHA", "Guinea": "GIN",
    "Guinea-Bissau": "GNB", "Hungary": "HUN", "Iceland": "ISL", "Ireland": "IRL",
    "Italy": "ITA", "Japan": "JPN", "Luxembourg": "LUX", "Macau": "MAC", "Mauritius": "MUS",
    "Morocco": "MAR", "Mozambique": "MOZ", "Netherlands": "NLD", "New Zealand": "NZL",
    "Nigeria": "NGA", "Norway": "NOR", "Pakistan": "PAK", "Peoples Republic Of China": "CHN",
    "Portugal": "PRT", "Rwanda": "RWA", "Saudi Arabia": "SAU", "Senegal": "SEN",
    "Sierra Leone": "SLE", "Slovenia": "SVN", "Spain": "ESP", "Sweden": "SWE",
    "Switzerland": "CHE", "Tunisia": "TUN", "Uganda": "UGA", "United Kingdom": "GBR",
    "United States Of America": "USA", "West Germany": "DEU", "Zambia": "ZMB",
}
PAIS_PT = {
    "Albania": "Albânia", "Angola": "Angola", "Australia": "Austrália", "Bahrain": "Bahrein",
    "Belgium": "Bélgica", "Benin": "Benim", "Brazil": "Brasil", "Cabo Verde": "Cabo Verde",
    "Canada": "Canadá", "Congo Democratic Republic": "RD Congo", "Djibouti": "Djibuti",
    "Equatorial Guinea": "Guiné Equatorial", "Estonia": "Estónia", "France": "França",
    "Gambia, The": "Gâmbia", "Ghana": "Gana", "Guinea": "Guiné", "Guinea-Bissau": "Guiné-Bissau",
    "Hungary": "Hungria", "Iceland": "Islândia", "Ireland": "Irlanda", "Italy": "Itália",
    "Japan": "Japão", "Luxembourg": "Luxemburgo", "Macau": "Macau", "Mauritius": "Maurícia",
    "Morocco": "Marrocos", "Mozambique": "Moçambique", "Netherlands": "Países Baixos",
    "New Zealand": "Nova Zelândia", "Nigeria": "Nigéria", "Norway": "Noruega",
    "Pakistan": "Paquistão", "Peoples Republic Of China": "China", "Portugal": "Portugal",
    "Rwanda": "Ruanda", "Saudi Arabia": "Arábia Saudita", "Senegal": "Senegal",
    "Sierra Leone": "Serra Leoa", "Slovenia": "Eslovénia", "Spain": "Espanha",
    "Sweden": "Suécia", "Switzerland": "Suíça", "Tunisia": "Tunísia", "Uganda": "Uganda",
    "United Kingdom": "Reino Unido", "United States Of America": "Estados Unidos",
    "West Germany": "Alemanha", "Zambia": "Zâmbia",
}
REGRAS_QUALIDADE = {
    "sem_datas": ("Datas em falta", "Alta", "Data de validade e/ou de emissão ausente."),
    "validade_sentinela": ("Validade irrealista (sentinela)", "Média", "Ano de validade ≥ 2050."),
    "emissao_futura": ("Emissão no futuro", "Alta", "Data de emissão posterior à referência."),
    "status_desatualizado": ("Estado do documento desatualizado", "Alta", "Estado não corresponde à validade."),
    "pep_risco_baixo": ("PEP sem risco Alto", "Alta", "PEP classificado como risco Baixo/Médio."),
    "pj_com_perfil_pessoal": ("Pessoa coletiva com idade/sexo", "Média", "PJ com atributos de pessoa singular."),
    "emigrante_residente": ("Emigrante marcado residente", "Média", "Emigrante com condição de residente = Sim."),
    "residencia_pais_divergente": ("Residência vs. país divergente", "Média", "Condição incompatível com país."),
    "nr_flag_divergente": ("Flag não residente divergente", "Baixa", "Flag não cobre emigrantes/PJ."),
    "doc_pj_inadequado": ("Documento inadequado ao tipo", "Média", "PJ com documento de pessoa singular."),
}
DOCS_PESSOA_SINGULAR = ["BI (Identity Card)", "CNI (BI Nacional)", "Passaporte", "Certidão Nascimento"]
DOCS_PESSOA_COLETIVA = ["Certidão Comercial", "Certidão Nome Empresarial"]
SEGMENTOS_IDADE = [17, 25, 35, 50, 65, 200]
LABELS_IDADE = ["18–25", "26–35", "36–50", "51–65", "66+"]
SEGMENTOS_TEMPO = [-1, 2, 5, 10, 20, 100]
LABELS_TEMPO = ["0–2 anos", "3–5 anos", "6–10 anos", "11–20 anos", "21+ anos"]
