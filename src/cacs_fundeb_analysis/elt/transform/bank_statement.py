"""
Módulo de consolidação de extratos bancários (conta corrente + conta de aplicações).
"""

import pandas as pd


def bank_statement_consolidation(
    application_account_statement: pd.DataFrame,
    current_account_statement: pd.DataFrame,
    opening_balance: float,
    year: int,
) -> pd.DataFrame:
    """
    Consolida os extratos da conta corrente e da conta de aplicações em um único DataFrame.

    Parâmetros:
        application_account_statement (pd.Dataframe): Dataframe da conta de aplicações.
        current_account_statement (pd.Dataframe): Dataframe da conta corrente.
        year (int): Ano de referência para o saldo inicial.
        opening_balance (float): Saldo inicial a ser inserido no extrato consolidado.

    Retorna:
        pd.DataFrame: DataFrame consolidado com todas as transações e saldo acumulado.
    """
    # Consolida os extratos
    extracts_consolidation_data = pd.concat(
        [current_account_statement, application_account_statement]
    )

    # Adiciona saldo inicial
    saldo_inicial_data = pd.DataFrame(
        {"HIST": ["SALDO INICIAL"], "VALOR": [opening_balance]},
        index=pd.to_datetime([f"{year - 1}-12-31"]),
    )
    extracts_consolidation_data = pd.concat(
        [extracts_consolidation_data, saldo_inicial_data]
    )

    # Ordena por data e calcula saldo acumulado
    extracts_consolidation_data = extracts_consolidation_data.sort_index()
    extracts_consolidation_data["SALDO"] = extracts_consolidation_data["VALOR"].cumsum()

    return extracts_consolidation_data
