"""
Módulo de ingestão de dados do FNDE.
"""

from sys import prefix
import pandas as pd
from typing import Optional


def load_fnde_sheet_data(
    file_path: str,
    sheet_name: str,
    adjust: bool = False,
) -> pd.DataFrame:
    """
    Lê uma planilha específica do arquivo Excel do FNDE e retorna um DataFrame bruto dos valores líquidos.

    Parâmetros:
        file_path (str): Caminho completo do arquivo Excel.
        sheet_name (str): Nome da planilha a ser lida. Padrão: "E_TOTAL".
        skiprows (int, opcional): Número de linhas a serem puladas no início. Padrão: 7.
        index_col (str, opcional): Coluna a ser usada como índice. Padrão: "UF".

    Retorna:
        pd.DataFrame: DataFrame com os dados brutos da planilha.
                      Retorna DataFrame vazio se ocorrer erro na leitura.
    """
    skiprows = 46 if adjust else 7
    try:
        df = pd.read_excel(
            io=file_path,
            sheet_name=sheet_name,
            skiprows=skiprows,
            index_col="UF",
            nrows=38,
        )
        return df
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {file_path}")
    except ValueError as e:
        print(f"Erro ao ler a planilha '{sheet_name}' em {file_path}: {e}")
    except Exception as e:
        print(f"Erro inesperado ao carregar dados do FNDE: {e}")

    return pd.DataFrame()


def load_all_fnde_sheet_data(
    file_path: str, state_level: str, uf: str, adjust: bool = False, year: int = 2025
) -> pd.DataFrame:
    from utils.excel import filter_sheet_names
    from processing.public_transfers import (
        clean_fnde_sheet_data,
        filter_uf_fnde_sheet_data,
    )

    uf = uf.upper()
    state_level = state_level.upper()
    filtered_sheet_names = filter_sheet_names(file_path, state_level)
    filtered_sheet_names_copy = filtered_sheet_names.copy()
    for name in filtered_sheet_names_copy:
        if name in [
            f"{state_level}_Tot1_U",
            f"{state_level}_Tot2_E",
            f"{state_level}_TOTAL",
        ]:
            filtered_sheet_names.remove(name)

    df_base = pd.DataFrame(columns=["MÊS"])
    for name in filtered_sheet_names:
        raw_df_new = load_fnde_sheet_data(file_path, name, adjust)
        clean_df_new = clean_fnde_sheet_data(raw_df_new)
        filtered_df_new = filter_uf_fnde_sheet_data(
            clean_df_new, name, uf, adjusts=adjust, year=year
        )
        df_base = pd.merge(df_base, filtered_df_new, on="MÊS", how="outer")
    # Adição de Totalização
    df_base.set_index("MÊS", inplace=True)
    df_base["TOTAL"] = df_base.sum(axis=1)
    df_base.loc["TOTAL", :] = df_base.sum(axis=0)
    return df_base
