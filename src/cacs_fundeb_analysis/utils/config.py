import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
env_path = Path(__file__).resolve().parents[2] / ".env"
if env_path.exists():
    load_dotenv(env_path)

def get_config(key: str, default=None):
    """
    Retorna o valor de uma configuração a partir das variáveis de ambiente.
    """
    return os.getenv(key, default)
