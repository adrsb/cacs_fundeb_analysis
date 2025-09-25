import pandas as pd


def list_res_canceled(res_relation_data: pd.DataFrame) -> pd.DataFrame:
    """
    Filtra apenas os registros cancelados em uma relação de RES.

    Parâmetros:
        res_relation_data (pd.DataFrame): DataFrame contendo a relação de RES,
            com a coluna 'CANCELAMENTO'.

    Retorna:
        pd.DataFrame: DataFrame apenas com registros cancelados.
    """
    if "CANCELAMENTO" not in res_relation_data.columns:
        raise KeyError("A coluna 'CANCELAMENTO' não foi encontrada no DataFrame.")

    canceled_df = res_relation_data.loc[
        res_relation_data["CANCELAMENTO"].notna()
    ].copy()
    canceled_df.loc["TOTAL", "VALOR"] = canceled_df["VALOR"].sum()
    return canceled_df
