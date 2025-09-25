import requests

def get_json(url: str, params: dict = None, headers: dict = None):
    """
    Faz uma requisição GET e retorna o JSON.
    """
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()

def download_file(url: str, dest_path: str):
    """
    Faz download de um arquivo e salva no caminho especificado.
    """
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(dest_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
