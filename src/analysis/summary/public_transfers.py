import pandas as pd


def uf_fnde_table_summary(
    normal_df: pd.DataFrame, adjust_df: pd.DataFrame
) -> pd.DataFrame:
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
