from __future__ import annotations

from . import (
    base_clientes, geografia, kyc_documentos, metodologia,
    perfil_clientes, qualidade_dados, risco_aml, visao_geral,
    rede_bayesiana  # <-- Nova página adicionada aqui
)

PAGINAS = [
    ("Visão Geral", "🏦", visao_geral, "Resumo executivo"),
    ("Risco & AML/CFT", "🛡️", risco_aml, "Risco e PEP"),
    ("KYC & Documentação", "📄", kyc_documentos, "Validade documental"),
    ("Perfil de Clientes", "👥", perfil_clientes, "Demografia"),
    ("Geografia & Diáspora", "🌍", geografia, "Distribuição territorial"),
    ("Qualidade de Dados", "🧪", qualidade_dados, "Regras de validação"),
    ("Base de Clientes", "📋", base_clientes, "Explorador e ficha"),
    ("Rede Bayesiana", "🧠", rede_bayesiana, "Inferência probabilística de risco"), # <-- Nova página adicionada aqui
    ("Metodologia & Fontes", "📚", metodologia, "Dicionário e limites"),
]

__all__ = ["PAGINAS"] + [m.__name__.split(".")[-1] for _, _, m, _ in PAGINAS]
