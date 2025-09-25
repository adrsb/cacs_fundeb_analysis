import os
import pandas as pd


def save_dataframe_to_excel(
    df: pd.DataFrame, file_name: str, folder: str, index: bool = True
) -> str:
    """
    Salva um DataFrame como arquivo Excel na estrutura do projeto.

    Parâmetros:
        df (pd.DataFrame): DataFrame a ser salvo.
        file_name (str): Nome do arquivo (ex.: 'extratos_consolidados.xlsx').
        folder (str, opcional): Pasta onde o arquivo será salvo. Padrão: 'data/output'.
        index (bool, opcional): Se True, inclui o índice do DataFrame no arquivo.

    Retorna:
        str: Caminho completo do arquivo salvo.
    """
    # Garante que a pasta exista
    os.makedirs(folder, exist_ok=True)

    # Monta o caminho completo
    file_path = os.path.join(folder, file_name)

    # Salva como Excel
    df.to_excel(file_path, index=index)

    return file_path
