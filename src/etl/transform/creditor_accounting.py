"""
Módulo para ingestão de relatórios contábeis e orçamentários.
"""

# src/dsuv/etl/transform.py
import pandas as pd
import numpy as np


NATUREZA_FOLHA = [
    "319004 - Contratação por Tempo Determinado ",
    "319011 - Vencimentos e Vantagens Fixas - Pessoal Civil",
    "319013 - Obrigações Patronais",
    "319016 - Outras Despesas Variáveis - Pessoal Civil",
    "319094 - Indenizações e Restituições Trabalhistas ",
    "319113 - Obrigações Patronais",
]

NATUREZA_OUTRAS = [
    "339046 - Auxílio-Alimentação",
    "339039 - Outros Serviços de Terceiros - Pessoa Jurídica ",
    "449052 - Equipamentos e Material Permanente ",
    "335041 - Contribuições ",
]


def transform_creditor_accounting_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforma dados contábeis brutos em dados limpos e enriquecidos.
    """
    df = df.iloc[2:-17].copy()

    # Preenchimento de valores ausentes
    cols_ffill = [
        "Unidade Gestora / Unidade Orçamentária / Ação",
        "Natureza",
        "Fonte",
        "Nota de Empenho",
        "Nota de Liquidação",
    ]
    for col in cols_ffill:
        df[col] = df[col].ffill()

    # Filtragem
    mask_invalid = (
        (df["Dotação Inicial"] == 0.0)
        & (df["Dotação Atualizada"] == 0.0)
        & (df["Despesas Empenhadas"] == 0.0)
        & (df["Despesas Liquidadas"] == 0.0)
        & (df["Despesas do Exercício Pagas"] == 0.0)
        & (df["Despesas Pagas RAP"] == 0.0)
    )
    df = df.loc[~mask_invalid].copy()

    # Colunas derivadas
    df["Restos a Pagar do Exercício"] = (
        df["Despesas Empenhadas"] - df["Despesas do Exercício Pagas"]
    )
    df["RAP do Exercício Processados"] = (
        df["Despesas Liquidadas"] - df["Despesas do Exercício Pagas"]
    )
    df["RAP do Exercício Não Processados"] = (
        df["Despesas Empenhadas"] - df["Despesas Liquidadas"]
    )

    # Classificação
    df["Classificação"] = np.nan
    df.loc[df["Natureza"].isin(NATUREZA_FOLHA), "Classificação"] = (
        "Despesas com Remuneração dos Profissionais da Educação Básica"
    )
    df.loc[df["Natureza"].isin(NATUREZA_OUTRAS), "Classificação"] = "Outras Despesas"

    # Ajustes finais
    df["Despesas Pagas RAP"] = df["Despesas Pagas RAP"].astype("float64")
    df.loc[df["Credor"] == " - - - ", "Credor"] = np.nan
    df["Credor"] = df["Credor"].ffill()

    return df
