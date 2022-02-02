from financas.financas import WebScrapper
import financas.financas as val
import time

#dont show logs
import logging
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium import webdriver

LOGGER.setLevel(logging.WARNING)


with WebScrapper() as bot:
    bot.land_first_page()
    bot.add_login()
    bot.clicar_emitir()
    bot.dados_recibo()
    bot.adquirente()
    bot.emitir_recibo()

   
