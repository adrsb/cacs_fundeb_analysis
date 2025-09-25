from pathlib import Path
import pandas as pd


def load_excel_re(
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
