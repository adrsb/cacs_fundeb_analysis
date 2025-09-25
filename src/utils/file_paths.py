"""
Funções para gerenciar caminhos de arquivos no projeto.
"""

import os
from typing import List, Optional


def list_all_file_paths(base_path: str) -> List[str]:
    """
    Percorre recursivamente todos os diretórios dentro de base_path
    e retorna uma lista com os caminhos completos de todos os arquivos encontrados.

    Parâmetros:
        base_path (str): Caminho do diretório base.

    Retorna:
        List[str]: Lista com caminhos completos dos arquivos.
    """
    all_files = []
    for root, _, files in os.walk(base_path):
        for file in files:
            full_path = os.path.join(root, file)
            all_files.append(full_path)
    return all_files


def list_all_file_names(base_path: str) -> List[str]:
    """
    Percorre recursivamente todos os diretórios dentro de base_path
    e retorna uma lista com os caminhos completos de todos os arquivos encontrados.

    Parâmetros:
        base_path (str): Caminho do diretório base.

    Retorna:
        List[str]: Lista com caminhos completos dos arquivos.
    """
    all_files = []
    for root, _, files in os.walk(base_path):
        for file in files:
            all_files.append(file)
    return all_files


def list_files_by_prefix_suffix(
    base_path: str, prefix: Optional[str] = None, suffix: Optional[str] = None
) -> List[str]:
    """
    Percorre recursivamente todos os diretórios dentro de base_path
    e retorna os caminhos completos dos arquivos que atendem aos filtros
    de prefixo e/ou sufixo.

    Parâmetros:
        base_path (str): Caminho do diretório base.
        prefix (str, opcional): Prefixo que o arquivo deve ter (ex.: '2025_01').
        suffix (str, opcional): Sufixo que o arquivo deve ter (ex.: 'Extrato_Conta_Corrente.pdf').

    Retorna:
        List[str]: Lista com caminhos completos dos arquivos filtrados.
    """

    paths = list_all_file_paths(base_path)
    matched_files = []

    for path in paths:
        filename = path.split("\\")[-1]  # pega apenas o nome do arquivo
        if prefix and not filename.startswith(prefix):
            continue
        if suffix and not filename.endswith(suffix):
            continue
        matched_files.append(path)

    return matched_files
