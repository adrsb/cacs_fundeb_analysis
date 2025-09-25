"""
Módulo para ingestão de dados de extratos bancários da conta corrente.
"""

import os

import pandas as pd


def load_pdf_current_account_statement(
    path: str, column_areas: list[int] | None = None
) -> pd.DataFrame:
    """
    Lê um PDF de extrato bancário e retorna o DataFrame bruto.

    Parâmetros:
        path (str): Caminho para a pasta onde o arquivo está.
        column_areas (list): Lista python com as posições, em pontos, das colunas no PDF.

    Retorna:
        pd.DataFrame: Dados brutos extraídos do PDF.
    """
    import tabula as tb

    if column_areas is None:
        column_areas = [177, 222, 244, 260, 380, 458, 511, 522, 595]
    df_list = tb.read_pdf(
        input_path=path,
        pages="all",
        stream=True,
        area=[0, 0, 842, 595],
        columns=column_areas,
        multiple_tables=False,
        pandas_options={
            "names": [
                "DATA",
                "AG_O",
                "LOTE",
                "COD_HIST",
                "HIST",
                "DOC",
                "VALOR",
                "INF",
                "SALDO",
            ]
        },
        encoding="ISO-8859-1",
    )
    result = df_list[0]
    if not isinstance(result, pd.DataFrame):
        raise ValueError("Falha ao extrair DataFrame do PDF")
    return result  # Retorna DataFrame bruto


def load_all_pdf_current_account_statement(path_base: str, suffix: str) -> pd.DataFrame:
    """
    Lê todos os arquivos PDF de extratos bancários da conta corrente em uma pasta.

    Parâmetros:
        path_base (str): Caminho da pasta contendo os PDFs.
        suffix (str): Sufixo que o arquivo deve ter (ex.: 'Extrato_Conta_Corrente.pdf').

    Retorna:
        pd.DataFrame: Dados concatenados de todos os PDFs.
    """
    from utils.file_paths import list_files_by_prefix_suffix

    path_list = list_files_by_prefix_suffix(path_base, suffix=suffix)
    area_columns = [
        [177, 222, 244, 260, 380, 458, 511, 522, 595],  # fev/mar/abr
        [176, 225, 250, 269, 398, 451, 511.8, 519.4, 595],  # jan
    ]

    dfs = []
    for path in path_list:
        try:
            df = load_pdf_current_account_statement(
                path=path, column_areas=area_columns[0]
            )
        except Exception:
            df = load_pdf_current_account_statement(
                path=path, column_areas=area_columns[1]
            )
        dfs.append(df)

    if not dfs:
        raise FileNotFoundError(f"Nenhum arquivo PDF encontrado em {path}")

    return pd.concat(dfs, axis=0)


def load_excel_bank_current_account(file_path: str) -> pd.DataFrame:
    """
    Lê um único arquivo Excel de extrato bancário e retorna um DataFrame bruto.
    """
    df = pd.read_excel(
        io=file_path,
        sheet_name="Extrato",
        skiprows=2,
        index_col="Data",
        verbose=False,
        thousands=".",
        decimal=",",
    )
    return df


def load_all_excel_banks_current_account(folder_path: str) -> pd.DataFrame:
    """
    Lê todos os arquivos .xlsx de uma pasta usando load_excel_bank e concatena.
    """
    list_dfs = []
    for file in os.listdir(folder_path):
        if file.lower().endswith(".xlsx"):
            df = load_excel_bank(os.path.join(folder_path, file))
            list_dfs.append(df)

    if not list_dfs:
        raise FileNotFoundError(f"Nenhum arquivo .xlsx encontrado em {folder_path}")

    return pd.concat(list_dfs, axis="rows")
