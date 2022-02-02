import os
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import financas.constants as const

class WebScrapper(webdriver.Chrome):
    def __init__(self, driver_path = r"D:\SeleniumDrivers"):
        self.driver_path = driver_path
        os.environ['PATH'] += self.driver_path
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])


        super(WebScrapper, self).__init__(chrome_options=options)
        #wait until the element of the website is ready
        self.implicitly_wait(15)
        self.maximize_window()

    #automaticaly close the browser
    # def __exit__(self, exc_type, exc_val, exc_tb):
    #     if self.teardown:
    #         self.quit()

    #lands the bot in the base url defined in the constants
    def land_first_page(self):
        self.get(const.BASE_URL)

    #Login in
    def add_login(self):
        #Número contribuinte
        username_login_value = input("Qual é número de contribuinte? ")
        username_login = self.find_element_by_id('username')
        username_login.send_keys(username_login_value)
        #password
        password_login_value = input("Qual é a password de acesso? ")
        password_login = self.find_element_by_id('password-nif')
        password_login.send_keys(password_login_value)

        login_btn = self.find_element_by_id('sbmtLogin').click()

    #clicar em emitir
    def clicar_emitir(self):
        emitir_btn = self.find_element_by_xpath('/html/body/div/main/div/div[2]/div/section/div/section/div/div/div[1]/div[3]/a').click()
        fatura_btn = self.find_element_by_xpath('/html/body/div/main/div/div[2]/div/section/div/section/div/div/div[1]/a/h4').click()

    def dados_recibo(self):
        data_prestacao_value = input("Qual a data de prestação de serviço (YYYY-MM-DD): ")
        data_prestacao = self.find_element_by_xpath('/html/body/div/main/div/div[2]/div/section/div/div/emitir-app/emitir-form/div[1]/div[2]/div/div/dados-de-operacao/div/div[3]/div[2]/div[1]/lf-date/div/div[1]/input')
        data_prestacao.send_keys(data_prestacao_value)
        fatura_recibo = Select(self.find_element_by_xpath('/html/body/div/main/div/div[2]/div/section/div/div/emitir-app/emitir-form/div[1]/div[2]/div/div/dados-de-operacao/div/div[3]/div[2]/div[2]/lf-dropdown/div/select'))
        fatura_recibo.select_by_visible_text('Fatura-Recibo')

    def adquirente(self):
        selecionar_aquirente = input("Quer usar os dados de uma empresa já guardada? (Sim/Não) ")
        selecionar_aquirente = selecionar_aquirente.upper()

        if selecionar_aquirente == "SIM":
            empresas = const.empresas
            i = 1
            print("Qual dos adquirentes quer utilizar: ")
            for empresa in empresas:
                print(f" {i} - {empresa}")
                i = i + 1

            adquirente = int(input("Escolha o número: "))
            adquirente = adquirente - 1 #Necessário fazer o ajuste do indice
            empresa = list(const.empresas.values())[adquirente]
            
            #nome da empresa
            nome_empresa = empresa.get('Nome da Empresa')
            nome_empresa_input = self.find_element_by_xpath('/html/body/div/main/div/div[2]/div/section/div/div/emitir-app/emitir-form/div[1]/div[2]/div/dados-adquirente/div/div[2]/div[2]/div/lf-text/div/input')
            nome_empresa_input.send_keys(nome_empresa)
            
            #nif da empresa
            nif_empresa = empresa.get('Nif')
            nif_empresa_input = self.find_element_by_xpath('/html/body/div/main/div/div[2]/div/section/div/div/emitir-app/emitir-form/div[1]/div[2]/div/dados-adquirente/div/div[2]/div[1]/div[3]/lf-nif/div/input')
            nif_empresa_input.send_keys(nif_empresa)
            
            #morada da empresa
            morada_empresa = empresa.get('Morada')
            morada_empresa_input = self.find_element_by_xpath('/html/body/div/main/div/div[2]/div/section/div/div/emitir-app/emitir-form/div[1]/div[2]/div/dados-adquirente/div/div[2]/div[3]/div/lf-text/div/input')
            morada_empresa_input.send_keys(morada_empresa)

            #importância a título de
            radio_escolher_tipo = self.find_element_by_xpath('/html/body/div/main/div/div[2]/div/section/div/div/emitir-app/emitir-form/div[1]/div[2]/div/dados-transmissao/div/div[2]/div[1]/pf-radio/div/div[1]/label/input').click()

            #descrição
            descricao_recibo = empresa.get('Descrição')
            descricao_recibo_input = self.find_element_by_xpath('/html/body/div/main/div/div[2]/div/section/div/div/emitir-app/emitir-form/div[1]/div[2]/div/dados-transmissao/div/div[2]/div[2]/div/textarea')
            descricao_recibo_input.send_keys(descricao_recibo)

            #regime de IVA
            regime_iva = Select(self.find_element_by_xpath('/html/body/div/main/div/div[2]/div/section/div/div/emitir-app/emitir-form/div[1]/div[2]/div/dados-transmissao/div/div[2]/div[6]/div/div[1]/lf-dropdown/div/select'))  
            regime_iva.select_by_visible_text('IVA - regime de isenção [art.º 53.º]')

            #base de incidencia em IRS
            base_incidencia_irs = Select(self.find_element_by_xpath('/html/body/div/main/div/div[2]/div/section/div/div/emitir-app/emitir-form/div[1]/div[2]/div/dados-transmissao/div/div[2]/div[7]/div[1]/div/lf-dropdown/div/select'))  
            base_incidencia_irs.select_by_visible_text(r'Sobre 100% - art. 101.º, n.ºs 1 e 9, do CIRS')

            #retencao na fonte irs
            fonte_irs = Select(self.find_element_by_xpath('/html/body/div/main/div/div[2]/div/section/div/div/emitir-app/emitir-form/div[1]/div[2]/div/dados-transmissao/div/div[2]/div[7]/div[2]/div[1]/lf-dropdown/div/select'))  
            fonte_irs.select_by_visible_text(r'À taxa de 25% - art. 101.º, n.º1, do CIRS')

            #valor base
            valor_base = empresa.get('Valor Base')
            valor_base_input = self.find_element_by_xpath('/html/body/div/main/div/div[2]/div/section/div/div/emitir-app/emitir-form/div[1]/div[2]/div/dados-transmissao/div/div[2]/div[4]/div/div/div/input') 
            valor_base_input.send_keys(valor_base)

    def emitir_recibo(self):
        confirmar = input("Confirma a emissao do recibo?(Sim/Nao) ")
        confirmar = confirmar.upper()
        if confirmar == 'SIM':
            btn_confirmar = self.find_element_by_xpath('/html/body/div/main/div/div[2]/div/section/div/div/emitir-app/emitir-form/div[1]/div[1]/div[1]/div[1]/div[3]/button').click()
            btn_confirm_2 = self.find_element_by_xpath('/html/body/div[1]/main/div/div[2]/div/section/div/div/emitir-app/emitir-form/div[2]/div/div/div[3]/button[2]').click()
        else:
            self.quit()



        






            





        

      




