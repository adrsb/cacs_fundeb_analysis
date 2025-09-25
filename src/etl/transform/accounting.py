"""
Módulo para ingestão de relatórios contábeis e orçamentários.
"""

# src/dsuv/etl/transform.py
import pandas as pd
import numpy as np


def transform_accounting_data(df: pd.DataFrame) -> pd.DataFrame:
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
    # ... (listas de natureza e regras de classificação aqui)

    # Ajustes finais
    df["Despesas Pagas RAP"] = df["Despesas Pagas RAP"].astype("float64")
    df.loc[df["Credor"] == " - - - ", "Credor"] = np.nan
    df["Credor"] = df["Credor"].ffill()

    return df
