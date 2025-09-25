"""
Módulo de limpeza e transformação de dados do FNDE.
"""

import pandas as pd


def transform_fnde_sheet_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove linhas com índice nulo de um DataFrame do FNDE.

    Parâmetros:
        df (pd.DataFrame): DataFrame bruto lido da planilha do FNDE.
        sheet_name (str): Nome da planilha de origem, usado para nomear as colunas.

    Retorna:
        pd.DataFrame: DataFrame sem linhas cujo índice seja NaN.
    """
    if df is None or df.empty:
        return pd.DataFrame()

    # Remove linhas com índice nulo
    df_clean = df.loc[~df.index.isna()]

    # Remove linhas de totais
    df_clean = df_clean.drop("TOTAL", axis=1)

    # Remove coluna 'ESTADOS'
    df_clean = df_clean.drop(labels="ESTADOS", axis=1)

    return df_clean


def filter_uf_fnde_sheet_data(
    df: pd.DataFrame,
    sheet_name: str,
    uf: str = "AP",
    adjusts: bool = False,
    year: int = 2025,
) -> pd.DataFrame:
    """
    Filtra os dados do FNDE para a UF 'AP', remove a coluna 'ESTADOS',
    transpõe o DataFrame e renomeia as colunas com base no nome da planilha.

    Parâmetros:
        df (pd.DataFrame): DataFrame bruto lido da planilha do FNDE.


    Retorna:
        pd.DataFrame: DataFrame transposto, filtrado e com colunas renomeadas.
    """
    uf = uf.upper()
    if uf not in df.index:
        raise ValueError(f"UF {uf} não encontrada no DataFrame.")

    # Filtra apenas a UF 'AP'
    df_filtered = df.loc[uf]

    # Resetar indices da tabela
    df_filtered = df_filtered.reset_index()

    # Renomeação das colunas
    if adjusts:
        df_filtered.columns = ["MÊS", f"{sheet_name}_AJUSTES"]
    else:
        df_filtered.columns = ["MÊS", f"{sheet_name}"]

    # Transformar mês em valores numéricos
    months = {
        "JANEIRO": "1",
        "FEVEREIRO": "2",
        "MARÇO": "3",
        "ABRIL": "4",
        "MAIO": "5",
        "JUNHO": "6",
        "JULHO": "7",
        "AGOSTO": "8",
        "SETEMBRO": "9",
        "OUTUBRO": "10",
        "NOVEMBRO": "11",
        "DEZEMBRO": "12",
    }
    df_filtered["MÊS"] = df_filtered["MÊS"].map(months)
    df_filtered["MÊS"] = df_filtered["MÊS"] + f"/{year}"
    df_filtered["MÊS"] = pd.to_datetime(
        df_filtered["MÊS"], format=f"%m/%Y"
    ).dt.strftime(f"%m/%Y")
    df_filtered.set_index("MÊS", inplace=True)

    return df_filtered
