"""
Módulo de extração de dados do Fundeb a partir do site Tesouro Transparente.
"""

"""
Módulo de ingestão de dados do Fundeb usando Selenium.
"""

import os
from utils.browser import start_chrome_driver, click_element_by_xpath

BASE_URL = "https://www.tesourotransparente.gov.br"


def build_fnde_url(year: int) -> str:
    """
    Constrói a URL da página de download do Fundeb para o ano informado.
    """
    if year != 2022:
        return f"{BASE_URL}/publicacoes/transferencias-ao-fundo-de-manutencao-e-desenvolvimento-da-educacao-basica-fundeb/{year}/114?ano_selecionado={year}"
    return f"{BASE_URL}/publicacoes/transferencias-ao-fundo-de-manutencao-e-desenvolvimento-da-educacao-basica-fundeb/2022/114-2?ano_selecionado=2022"


def download_fnde_data(year: int, download_dir: str = "data/raw/fundeb") -> None:
    """
    Abre o navegador, acessa a página do Fundeb e clica no botão de download do Excel.
    """
    os.makedirs(download_dir, exist_ok=True)

    driver = start_chrome_driver()
    try:
        url = build_fundeb_url(year)
        driver.get(url)

        # Ajustar XPath conforme layout real da página
        if year != 2022:
            xpath_download = '//*[@id="publicacao"]/div/div[2]/section/div[4]/a'
        else:
            xpath_download = '//*[@id="publicacao"]/div/div[2]/section/div[4]/a'

        click_element_by_xpath(driver, xpath_download, wait=10)

    finally:
        driver.quit()
