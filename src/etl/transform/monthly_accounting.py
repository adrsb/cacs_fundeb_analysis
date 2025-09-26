import pandas as pd


def transform_monthly_accounting_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Trata dados brutos de planilha Excel.
    """
    # Remove valores nulos da coluna "OB"
    df = df.dropna(subset="OB")

    # Preenche valores ausente de acordo com o primeiro registro anterior
    df = df.ffill()
    return df
