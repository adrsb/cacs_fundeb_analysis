"""
Módulo de limpeza e transformação de dados do FNDE.
"""

import pandas as pd


def clean_fnde_sheet_data(df: pd.DataFrame) -> pd.DataFrame:
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


def uf_fnde_summary(normal_df: pd.DataFrame, adjust_df: pd.DataFrame) -> pd.DataFrame:
    """
    Gera um resumo dos repasses do FNDE para a UF 'AP', combinando valores líquidos e ajustes.

    Parâmetros:
        normal_df (pd.DataFrame): DataFrame com valores líquidos dos repasses, contendo coluna 'TOTAL'.
        adjust_df (pd.DataFrame): DataFrame com valores de ajustes, contendo coluna 'TOTAL'.

    Retorna:
        pd.DataFrame: DataFrame resumo com colunas:
            - TOTAL_BRUTO_REPASSES
            - TOTAL_AJUSTES
            - TOTAL_LIQUIDO_REPASSES
            - TOTAL_ACUMULADO
    """
    # Valida colunas necessárias
    if "TOTAL" not in normal_df.columns or "TOTAL" not in adjust_df.columns:
        raise ValueError("Ambos os DataFrames devem conter a coluna 'TOTAL'.")

    # Concatena colunas de interesse
    summary = pd.concat([normal_df["TOTAL"], adjust_df["TOTAL"]], axis=1)
    summary.columns = ["TOTAL_LIQUIDO_REPASSES", "TOTAL_AJUSTES"]

    # Calcula acumulado
    summary["TOTAL_ACUMULADO"] = summary["TOTAL_LIQUIDO_REPASSES"].cumsum()

    # Ajusta valor acumulado na linha 'TOTAL' (última linha agregada)
    if "TOTAL" in summary.index:
        # Pega o penúltimo valor do acumulado (último mês)
        penultimo_valor = (
            summary["TOTAL_ACUMULADO"].iloc[-2]
            if len(summary) > 1
            else summary["TOTAL_ACUMULADO"].iloc[0]
        )
        summary.loc["TOTAL", "TOTAL_ACUMULADO"] = penultimo_valor

    # Calcula bruto
    summary["TOTAL_BRUTO_REPASSES"] = (
        summary["TOTAL_LIQUIDO_REPASSES"] - summary["TOTAL_AJUSTES"]
    )

    # Reordena colunas
    summary = summary[
        [
            "TOTAL_BRUTO_REPASSES",
            "TOTAL_AJUSTES",
            "TOTAL_LIQUIDO_REPASSES",
            "TOTAL_ACUMULADO",
        ]
    ]

    return summary
