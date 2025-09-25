"""
Módulo para ingestão de relatórios contábeis e orçamentários.
"""

# src/dsuv/etl/extract.py
from pathlib import Path

import pandas as pd


def extract_accounting_data(path: str | Path, bi: str = "1") -> pd.DataFrame:
    """
    Extrai dados brutos de planilha Excel.
    """
    path = Path(path)
    df = pd.read_excel(path, sheet_name="Planilha 1", skiprows=4)
    return df
