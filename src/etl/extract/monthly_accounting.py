from pathlib import Path

import pandas as pd

from utils.file_paths import list_files_by_prefix_suffix


def extract_excel_monthly_accounting_data(
    base_dir: str | Path, bi: int = 1
) -> pd.DataFrame:
    """
    Extrai dados brutos de planilha Excel.
    """
    # Encontra path do arquivo
    file_path = list_files_by_prefix_suffix(
        base_dir,
        prefix="Demonstrativo da Execução Financeira por Mês",
        suffix=f"{bi}B.xls",
    )[0]
    # Leitura
    monthly_accounting_data = pd.read_excel(
        io=file_path, sheet_name="Planilha 1", skiprows=4
    )
    return monthly_accounting_data
