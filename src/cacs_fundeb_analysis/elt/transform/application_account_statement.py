"""
Módulo para ingestão de dados de extratos de aplicações financeiras.
"""

import pandas as pd
import numpy as np


import pandas as pd
import numpy as np


def clean_pdf_applications_account_statemet(df: pd.DataFrame) -> pd.DataFrame:
    """
    Recebe DataFrame bruto de aplicações e retorna no formato padronizado do projeto.
    """
    # Ajusta formato da data para datetime
    from pandas.tseries.offsets import MonthEnd

    df["PERÍODO"] = pd.to_datetime(df["PERÍODO"], format="%y/%m")
    df = df.sort_values(by="PERÍODO")

    # Monta DataFrame padronizado
    df_padrao = pd.DataFrame(
        {
            "DATA": df["PERÍODO"],
            "AG_O": ["0000"] * df.shape[0],
            "LOTE": ["00000"] * df.shape[0],
            "COD_HIST": ["000"] * df.shape[0],
            "HIST": ["RENDIMENTOS"] * df.shape[0],
            "DOC": ["0"] * df.shape[0],
            "VALOR_APP": ["0"] * df.shape[0],
            "VALOR": df["RENDIMENTO"],
            "INF": ["C"] * df.shape[0],
            "SALDO": [np.nan] * df.shape[0],
            "DET_HIST": ["RENDIMENTOS"] * df.shape[0],
        }
    )

    # Ajusta índice para o último dia do mês
    df_padrao.index = pd.to_datetime(df_padrao["DATA"]) + MonthEnd(0)
    df_padrao.drop(columns="DATA", inplace=True)

    # Converte valores para numérico
    df_padrao["VALOR"] = pd.to_numeric(
        df_padrao["VALOR"].astype(str).str.replace(".", "").str.replace(",", ".")
    )

    return df_padrao
