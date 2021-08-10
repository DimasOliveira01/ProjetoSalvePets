from selenium import webdriver

def before_all(context):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    context.browser = webdriver.Chrome(chrome_options=chrome_options)


# tutorial para rodar os testes automatizados

# instalar o behave e o selenium
# no terminal, digitar: pip install behave e pip install selenium
# baixar o chromedriver na máquina (Link: https://sites.google.com/chromium.org/driver/)
# instalar o chromedriver e configurá-lo no path da máquina
# ir até a pasta features (no Windows, usar o comando cd '.\Projeto\SalvePets\features\')
# rodar o comando behave
