# src/processing/reports/clean_report.py

import pandas as pd


def transform_excel_re_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica regras de limpeza e padronização em um DataFrame de relatório.

    Parâmetros:
        df (pd.DataFrame): DataFrame bruto.

    Retorna:
        pd.DataFrame: DataFrame limpo.
    """
    df = df.dropna(subset=["Valor"])
    df = df.drop(columns=["Unnamed: 1"], errors="ignore")

    if "Cancelamento" not in df.columns:
        df["Cancelamento"] = pd.NA

    df.loc[df["Cancelamento"] == "***********", "Cancelamento"] = pd.NA
    df.columns = [
        "OB",
        "TIPO",
        "CNPJ/CPF",
        "FAVORECIDO",
        "C/C_ORIGEM",
        "BANCO",
        "AG",
        "C/C",
        "VALOR",
        "CANCELAMENTO",
    ]
    return df



