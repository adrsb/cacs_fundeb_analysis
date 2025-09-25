"""
Módulo para limpeza e transformação de dados de extratos bancários da conta corrente.
"""

import pandas as pd


def clean_pdf_current_account_statement(df: pd.DataFrame) -> pd.DataFrame:
    """
    Recebe DataFrame bruto e aplica limpeza e transformação.

    Parâmetros:
        df (pd.DataFrame): DataFrame bruto retornado pela ingestão.

    Retorna:
        pd.DataFrame: Dados tratados e prontos para análise.
    """
    # Filtra linhas relevantes
    df = df.loc[(df.INF == "C") | (df.INF == "D")]

    # Conversão de VALORES
    df.VALOR

    # Ajusta coluna de detalhes
    df.loc[df.DATA.isna(), "DET_HIST"] = df.loc[df.DATA.isna(), "HIST"]
    df.DET_HIST = df.DET_HIST.shift(-1)
    df = df.loc[~df.DATA.isna()]

    # Ajusta datas e valores
    df.index = pd.to_datetime(df.DATA, dayfirst=True)
    df.drop(columns="DATA", inplace=True)

    df.VALOR = df.VALOR.str.replace(".", "").str.replace(",", ".").astype(float)
    df = df.loc[df.HIST != "Saldo Anterior"]
    df.VALOR = df.apply(
        lambda row: row.VALOR * -1 if row.INF == "D" else row.VALOR, axis=1
    )

    # Coluna de aplicações
    df["VALOR_APP"] = df.apply(
        lambda row: row.VALOR
        if row.HIST in ["BB-APLIC C.PRZ-APL.AUT", "Resgate Automático"]
        else 0,
        axis=1,
    )
    df.VALOR = df.apply(
        lambda row: 0
        if row.HIST in ["BB-APLIC C.PRZ-APL.AUT", "Resgate Automático"]
        else row.VALOR,
        axis=1,
    )

    # Reorganiza colunas
    df = df[
        [
            "AG_O",
            "DOC",
            "LOTE",
            "COD_HIST",
            "HIST",
            "VALOR_APP",
            "VALOR",
            "INF",
            "SALDO",
            "DET_HIST",
        ]
    ]
    df.SALDO = 0

    return df
