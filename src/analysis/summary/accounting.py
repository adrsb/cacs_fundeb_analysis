import pandas as pd

# Constantes para evitar repetição
BUDGET_COLUMNS = [
    "Dotação Inicial",
    "Dotação Atualizada",
    "Despesas Empenhadas",
    "Despesas Liquidadas",
    "Despesas do Exercício Pagas",
    "Despesas Pagas RAP",
    "Restos a Pagar do Exercício",
    "RAP do Exercício Processados",
    "RAP do Exercício Não Processados",
]

FINAL_COLUMNS = [
    "Ordem",
    "Fase Orçamentária",
    "Despesas com Remuneração dos Profissionais da Educação Básica",
    "Outras Despesas",
    "TOTAL",
]

CUSTOM_INDEX = [0, 1, 2, 3, 4, 5, 6, 6.1, 6.2]


def budget_summary(accounting_data: pd.DataFrame) -> pd.DataFrame:
    """
    Gera um resumo orçamentário a partir dos dados contábeis.

    Parameters
    ----------
    accounting_data : pd.DataFrame
        DataFrame contendo as colunas necessárias para o cálculo
        (ver BUDGET_COLUMNS).

    Returns
    -------
    pd.DataFrame
        DataFrame resumido com fases orçamentárias e totais.
    """

    # Cria tabela dinâmica com totais
    budget_summary = accounting_data.pivot_table(
        values=BUDGET_COLUMNS,
        index="Classificação",
        aggfunc="sum",
        margins=True,
        margins_name="TOTAL",
    )

    # Reorganiza colunas e transpõe
    budget_summary = budget_summary[BUDGET_COLUMNS].T.reset_index()

    # Define índice customizado
    budget_summary.index = CUSTOM_INDEX

    # Reseta índice e renomeia colunas finais
    budget_summary = budget_summary.reset_index()
    budget_summary.columns = FINAL_COLUMNS

    return budget_summary


# Constantes de colunas
SUMMARY_VALUES = [
    "Dotação Atualizada",
    "Despesas Empenhadas",
    "Despesas Liquidadas",
    "Despesas do Exercício Pagas",
    "Despesas Pagas RAP",
    "Restos a Pagar do Exercício",
    "RAP do Exercício Processados",
    "RAP do Exercício Não Processados",
]

SUMMARY_INDEX = ["Classificação", "Natureza"]


def accounting_summary(accounting_data: pd.DataFrame) -> pd.DataFrame:
    """
    Gera uma tabela dinâmica (pivot table) com o resumo das despesas contábeis.

    Args:
        accounting_data (pd.DataFrame): DataFrame já transformado contendo
            colunas de valores e classificações.

    Returns:
        pd.DataFrame: DataFrame resumo com totais agregados por classificação e natureza.
    """
    summary = (
        pd.pivot_table(
            data=accounting_data,
            values=SUMMARY_VALUES,
            index=SUMMARY_INDEX,
            aggfunc="sum",
            margins=True,
            margins_name="TOTAL",
        )
        .reset_index()
        .loc[:, SUMMARY_INDEX + SUMMARY_VALUES]  # garante ordem das colunas
    )
    return summary
