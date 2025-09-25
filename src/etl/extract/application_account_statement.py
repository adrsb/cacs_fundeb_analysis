"""
Módulo para ingestão de dados de extratos de aplicações financeiras.
"""

import pandas as pd

from utils.file_paths import list_files_by_prefix_suffix


def extract_manual_applications_account_statement_data(year: int) -> pd.DataFrame:
    """
    Gera manualmente um extrato de rendimentos de aplicações financeiras
    para um determinado ano.

    Parâmetros:
        year (int): Ano de referência (ex.: 2025).

    Retorna:
        pd.DataFrame: Dados no formato padronizado do projeto.
    """
    # Dados manuais de rendimento por mês
    data = [
        (f"01/{year}", 235913.62),
        (f"02/{year}", 457431.56),
        (f"03/{year}", 346857.54),
        (f"04/{year}", 356633.45),
        (f"05/{year}", 309431.29),
        (f"06/{year}", 153722.97),
        (f"07/{year}", 77144.25),
        (f"08/{year}", 57558.73),
        (f"09/{year}", 154945.13),
        (f"10/{year}", 181099.17),
        (f"11/{year}", 243837.01),
        (f"12/{year}", 197406.03),
    ]

    # Cria DataFrame inicial
    applications = pd.DataFrame(data, columns=["PERÍODO", "RENDIMENTO"])

    # Formata período e ordena
    applications["PERÍODO"] = pd.to_datetime(
        applications["PERÍODO"], format="%m/%Y"
    ).dt.strftime("%m/%Y")
    applications = applications.sort_values(by="PERÍODO")

    # Constrói DataFrame no formato padronizado
    applications = pd.DataFrame(
        {
            "DATA": applications["PERÍODO"],
            "AG_O": ["0000"] * applications.shape[0],
            "LOTE": ["00000"] * applications.shape[0],
            "COD_HIST": ["000"] * applications.shape[0],
            "HIST": ["RENDIMENTOS"] * applications.shape[0],
            "DOC": ["0"] * applications.shape[0],
            "VALOR": applications["RENDIMENTO"],
            "INF": ["C"] * applications.shape[0],
            "SALDO": [np.nan] * applications.shape[0],
            "DET_HIST": ["RENDIMENTOS"] * applications.shape[0],
        }
    )

    # Ajusta índice como datetime
    applications.index = pd.to_datetime(applications["DATA"], format="%m/%Y")
    applications.drop(columns="DATA", inplace=True)

    return applications


def extract_pdf_application_account_statement_data(path_file: str) -> pd.Series:
    """
    Lê um único PDF de aplicação financeira e retorna o valor de rendimento.

    Parâmetros:
        path (str): Caminho da pasta onde está o arquivo.
        file (str): Nome do arquivo PDF.

    Retorna:
        pd.Series: Série com período e rendimento extraído.
    """
    import tabula as tb

    df_list = tb.read_pdf(
        input_path=path_file,
        pages="all",
        stream=True,
        area=[0, 0, 842, 595],
        encoding="ISO-8859-1",
    )

    # Extrai o valor da penúltima linha (ajustar conforme layout real)
    valor = df_list[0][-12:-11]["Unnamed: 1"].values

    # Extrai o período do nome do arquivo
    period = path_file.split("\\")[-1][:5]
    return pd.Series({"PERÍODO": period, "RENDIMENTO": valor[0]})


def extract_all_pdf_application_account_statement_data(
    path_base: str, suffix: str
) -> pd.DataFrame:
    """
    Lê todos os PDFs de aplicações financeiras em uma pasta.

    Parâmetros:
        path_base (str): Caminho da pasta contendo os PDFs.
        Sufixo que o arquivo deve ter (ex.: 'Extrato_Conta_Aplicações.pdf').

    Retorna:
        pd.DataFrame: DataFrame com períodos e rendimentos brutos.
    """

    path_list = list_files_by_prefix_suffix(path_base, suffix=suffix)
    if not path_list:
        raise FileNotFoundError(f"Nenhum arquivo PDF encontrado em {path_base}")

    records = []
    for path in path_list:
        income = extract_pdf_application_account_statement_data(path)
        records.append(income)

    df = pd.DataFrame(records)
    df["PERÍODO"] = df["PERÍODO"].str.replace("_", "/")
    return df
