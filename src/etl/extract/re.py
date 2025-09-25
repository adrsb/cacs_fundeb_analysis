from pathlib import Path

import pandas as pd

from src.etl.transform.re import transform_excel_re_data
from src.utils.file_paths import list_files_by_prefix_suffix


def extract_excel_re_data(
    file_path: str, sheet_name: str = "Planilha 1", skiprows: int = 7
) -> pd.DataFrame:
    """
    Lê um arquivo de RE em Excel bruto.

    Parâmetros:
        file_path (str): Caminho completo do arquivo Excel.
        sheet_name (str): Nome da aba a ser lida.
        skiprows (int): Número de linhas iniciais a ignorar.

    Retorna:
        pd.DataFrame: DataFrame bruto.
    """
    file = Path(file_path)
    if not file.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

    return pd.read_excel(file, sheet_name=sheet_name, skiprows=skiprows)


def extract_all_excel_res_data(base_dir: str, prefix: str = "2025RE") -> pd.DataFrame:
    """
    Consolida todos os relatórios Excel de um diretório em um único DataFrame.

    Parâmetros:
        path (str): Caminho para o diretório contendo os arquivos Excel.

    Retorna:
        pd.DataFrame: DataFrame consolidado com coluna 'RE' indicando a origem.
    """
    base_path = Path(base_dir)
    if not base_path.exists() or not base_path.is_dir():
        raise FileNotFoundError(f"Diretório inválido: {base_dir}")

    excel_files = list_files_by_prefix_suffix(base_dir, prefix=prefix)

    if not excel_files:
        raise FileNotFoundError(f"Nenhum arquivo Excel encontrado em {base_dir}")

    dfs = []
    keys = []

    for file in excel_files:
        file_path = Path(file)
        raw_df = extract_excel_re_data(file)
        clean_df = transform_excel_re_data(raw_df)
        dfs.append(clean_df)
        keys.append(file_path.stem)

    consolidated_df = pd.concat(dfs, axis=0, keys=keys)
    consolidated_df = consolidated_df.reset_index(level=0).rename(
        columns={"level_0": "RE"}
    )

    return consolidated_df
