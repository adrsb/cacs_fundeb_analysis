# SYSTEM IMPORTS
import pandas as pd

# PROPRIETIES IMPORTS
from src.cacs_fundeb_analysis.elt.load.application_account_statement import (
    load_all_pdf_application_account_statement,
    load_manual_applications_account_statement,
)
from src.cacs_fundeb_analysis.elt.transform.application_account_statement import (
    clean_pdf_applications_account_statemet,
)
from src.cacs_fundeb_analysis.elt.load.current_account_statement import (
    load_all_excel_banks_current_account,
    load_all_pdf_current_account_statement,
)
from src.cacs_fundeb_analysis.elt.transform.current_account_statement import (
    clean_pdf_current_account_statement,
)
from src.cacs_fundeb_analysis.elt.transform.bank_statement import (
    bank_statement_consolidation,
)
from src.cacs_fundeb_analysis.utils.io import save_dataframe_to_excel


def run_bank_statement_pipeline(
    opening_balance: float,
    year: int,
    base_dir: str = "..\\data",
    current_account_statement_suffix: str = "Extrato_Conta_Corrente.pdf",
    application_account_statement_suffix: str = "Extrato_Conta_Aplicações.pdf",
) -> pd.DataFrame:
    """
    Lê, limpa, consolida e exporta em excel os extratos da conta corrente e da conta de aplicações.

    Parâmetros:
        opening_balance (float): Saldo inicial a ser inserido no extrato consolidado.
        year (int): Ano de referência para o saldo inicial.
        base_dir (str, opcional): Diretório base onde estão os arquivos brutos.
        current_account_statement_suffix (str, opcional): Sufixo do nome do arquivo da conta corrente (ex.: 'Extrato_Conta_Corrente.xls').
        application_account_statement_suffix (str, opcional): Sufixo do arquivo da conta de aplicações (ex.: 'Extrato_Conta_aplicações.xls').

    Retorna:
        pd.DataFrame: DataFrame consolidado com todas as transações e saldo acumulado.
    """
    # 1. Leitura dos dados brutos
    raw_current_account_statement = load_all_pdf_current_account_statement(
        base_dir, current_account_statement_suffix
    )
    raw_application_account_statement = load_all_pdf_application_account_statement(
        base_dir, application_account_statement_suffix
    )

    # 2. Salvar dados brutos em interin/
    save_dataframe_to_excel(
        df=raw_current_account_statement,
        file_name="extrato_conta_corrente_bruto.xlsx",
        folder=base_dir + "\\interin\\",
    )
    save_dataframe_to_excel(
        df=raw_application_account_statement,
        file_name="extrato_conta_aplicação_bruto.xlsx",
        folder=base_dir + "\\interin\\",
    )

    # 3. Limpeza e padronização
    clean_current_account_statement = clean_pdf_current_account_statement(
        raw_current_account_statement
    )
    clean_application_account_statement = clean_pdf_applications_account_statemet(
        raw_application_account_statement
    )

    # 4. Salva dados limpos em processed/
    save_dataframe_to_excel(
        df=clean_current_account_statement,
        file_name="extrato_conta_corrente_limpo.xlsx",
        folder=base_dir + "\\processed\\",
    )
    save_dataframe_to_excel(
        df=clean_application_account_statement,
        file_name="extrato_conta_aplicação_limpo.xlsx",
        folder=base_dir + "\\processed\\",
    )

    # 5. Consolidação
    bank_statement = bank_statement_consolidation(
        clean_application_account_statement,
        clean_current_account_statement,
        opening_balance,
        year,
    )
    # 6. Exportação do arquivo final para output/
    save_dataframe_to_excel(
        df=bank_statement,
        file_name="extrato_bancário.xlsx",
        folder=base_dir + "\\output\\files",
    )

    return bank_statement
