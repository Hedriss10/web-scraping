import requests as r
from bs4 import BeautifulSoup as bf
import locale
from models import FundoImobiliario
from models import Estrategia

from tabulate import *

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


def trata_porcentagem(porcentagem_str):
    return locale.atof(porcentagem_str.split('%')[0])


def trata_decimal(decimal_str):
    # 'R$ 5.000,50'
    return locale.atof(decimal_str)


'''
Passando o dict para navigatoHeaders, mudando á propria headers para não da error de escrita!!
'''
navigatorHeaders = {"User-Agent": 'Mozilla/6.0'}

requestOne = r.get('https://www.fundamentus.com.br/fii_resultado.php', headers=navigatorHeaders)

soupText = bf(requestOne.text, 'html.parser')

linesSoup = soupText.find(id='tabelaResultado').find('tbody').find_all('tr')

##print(soupText.td(id='tabelaResultado').find_all('tr'))

resultado = []

estrategia = Estrategia(
    cotacao_atual_minima=50.0,
    dividiend_yield_minimo=5,
    p_pv_minimo=0.70,
    valor_mercado_minimo=20000000,
    liquedez_minima=50000,
    qt_minima_imoveis=5,
    maxima_vacancia_media=10
)

for linha in linesSoup:
    dados_money = linha.find_all('td')
    codigo = dados_money[0].text
    segmento = dados_money[1].text
    cotacao = trata_decimal(dados_money[2].text)
    ffo_yield = trata_porcentagem(dados_money[3].text)
    dividendo_yield = trata_porcentagem(dados_money[4].text)
    p_pv = trata_decimal(dados_money[5].text)
    valor_mercado = trata_decimal(dados_money[6].text)
    liquidez = trata_decimal(dados_money[7].text)
    qt_imoveis = int(dados_money[8].text)
    preco_m2 = trata_decimal(dados_money[9].text)
    aluguel_m2 = trata_decimal(dados_money[10].text)
    cap_rate = trata_porcentagem(dados_money[11].text)
    vacancia_media = trata_porcentagem(dados_money[12].text)


    fundo_imobiliario = FundoImobiliario(
        codigo, segmento, cotacao, ffo_yield, dividendo_yield, p_pv, valor_mercado, liquidez,
        qt_imoveis, preco_m2, aluguel_m2,
        cap_rate, vacancia_media
    )

    if estrategia.aplicate_estrategia(fundo_imobiliario):
        resultado.append(fundo_imobiliario)


title = ["CÓDIGO", "SEGMENTO", "COTAÇÃO ATUAL", "DIVIDENDO VIELO"]

tabela = []


for elemento in resultado:
    tabela.append([
        elemento.codigo, elemento.segmento, locale.currency(elemento.cotacao_atual),
        f'{locale.str(elemento.dividendo_yield)} %'
    ])

print(tabulate(tabela, headers=title, showindex='always', tablefmt="fancy_grid"))