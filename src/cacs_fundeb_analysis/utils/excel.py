import xlrd


def load_sheet_names(file_path: str) -> list[str]:
    """
    Localiza o arquivo do Fundeb e retorna o caminho e a lista de planilhas.
    """
    sheet_names = xlrd.open_workbook(file_path).sheet_names()
    return sheet_names


def filter_sheet_names(
    file_path: str,
    prefix: str = None,
    suffix: str = None,
):
    sheet_names = load_sheet_names(file_path)

    filtered_sheet_names = []
    for name in sheet_names:
        if prefix and name.startswith(prefix):
            filtered_sheet_names.append(name)
        if suffix and name.endswith(suffix):
            filtered_sheet_names.append(name)

    return filtered_sheet_names
