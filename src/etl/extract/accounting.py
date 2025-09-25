"""
Módulo para ingestão de relatórios contábeis e orçamentários.
"""

# src/dsuv/etl/extract.py
from pathlib import Path

import pandas as pd

from utils.file_paths import list_files_by_prefix_suffix


def extract_excel_accounting_data(base_dir: str | Path, bi: int = 1) -> pd.DataFrame:
    """
    Extrai dados brutos de planilha Excel.
    """
    file_path = list_files_by_prefix_suffix(
        base_dir, prefix="Demonstrativo da Execução Financeira", suffix=f"{bi}B.xls"
    )[0]
    df = pd.read_excel(file_path, sheet_name="Planilha 1", skiprows=4)
    return df
