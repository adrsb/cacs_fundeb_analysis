# src/processing/reports/clean_report.py
from pathlib import Path

import pandas as pd

from pathlib import Path
import pandas as pd
from data.loading.re import load_excel_re
from utils.file_paths import list_files_by_prefix_suffix


def clean_excel_re(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica regras de limpeza e padronização em um DataFrame de relatório.

    Parâmetros:
        df (pd.DataFrame): DataFrame bruto.

    Retorna:
        pd.DataFrame: DataFrame limpo.
    """
    df = df.dropna(subset=["Valor"])
    df = df.drop(columns=["Unnamed: 1"], errors="ignore")

    if "Cancelamento" not in df.columns:
        df["Cancelamento"] = pd.NA

    df.loc[df["Cancelamento"] == "***********", "Cancelamento"] = pd.NA
    df.columns = [
        "OB",
        "TIPO",
        "CNPJ/CPF",
        "FAVORECIDO",
        "C/C_ORIGEM",
        "BANCO",
        "AG",
        "C/C",
        "VALOR",
        "CANCELAMENTO",
    ]
    return df


def load_all_excel_res(base_dir: str, prefix: str = "2025RE") -> pd.DataFrame:
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
        raw_df = load_excel_re(file)
        clean_df = clean_excel_re(raw_df)
        dfs.append(clean_df)
        keys.append(file_path.stem)

    consolidated_df = pd.concat(dfs, axis=0, keys=keys)
    consolidated_df = consolidated_df.reset_index(level=0).rename(
        columns={"level_0": "RE"}
    )

    return consolidated_df


def filter_canceled_res_relation(res_relation_data: pd.DataFrame) -> pd.DataFrame:
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
