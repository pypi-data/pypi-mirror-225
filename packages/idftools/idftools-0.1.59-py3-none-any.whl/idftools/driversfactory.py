# -*- coding: utf-8 -*-
#coding: utf-8
import sys
sys.path.append("../..")
import io, re, string, os
import time
#import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
import configparser
import sys
import os
# import undetected_chromedriver as uc
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options as OptionsFF
from selenium.webdriver.firefox.service import Service as ServiceFF
import undetected_chromedriver as uc
import datetime

from colorama import Fore, Back, Style
if os.name == 'nt':
    from colorama import just_fix_windows_console
    just_fix_windows_console()

class DriverFactory:
    #HINT: set another dir to chrome:  https://stackoverflow.com/questions/45500606/set-chrome-browser-binary-through-chromedriver-in-python
    '''
    Retorna webdriver
    Parâmetros: chrome, firefox, phantomjs
    '''
    # def create_driver(self, type, headless=False):
    #     self.create_driver(type, headless, None)

    # def create_driver(self, type, headless=False, path_to_download=None, install_extension=None, largura=1440, altura=900):

    def printa(self, tipo='', msg=''):
        msg = msg.replace('\n', '// ').replace('  ', ' ').replace('  ', ' ').replace('  ', ' ').replace('  ', ' ').replace('  ', ' ').replace('  ', ' ')
        agora = datetime.datetime.today().strftime("%Y/%m/%d %H:%M:%S")
        if tipo == 'error':
            print(Fore.RED + f'{agora} | {tipo} | {msg}' + Style.RESET_ALL)
        elif tipo == 'debug':
            print(Fore.MAGENTA + f'{agora} | {tipo} | {msg}' + Style.RESET_ALL)
        elif tipo == 'warning':
            print(Fore.YELLOW + f'{agora} | {tipo} | {msg}' + Style.RESET_ALL)
        elif tipo == 'info':
            print(Fore.CYAN + f'{agora} | {tipo} | {msg}' + Style.RESET_ALL)
        elif tipo == 'critical':
            print(Back.RED + f'{agora} | {tipo} | {msg}' + Style.RESET_ALL)
        else:
            print(f'{agora} | {tipo} | {msg}')

    def create_driver(self, type='chrome', uctype=False, headless=False, path_to_download='TMP', install_extension=None, largura=800, altura=800, kiosk=False, nome_robo_exec='bot', robo_pid_exec='0', logger=None, cert_digital=False, path_cert_digital=None, senha_cert_digital=None, list_url_cert_digital=[], scale_factor=1, set_page_load_timeout=45, implicitly_wait=2, posX=0, posY=0):
        # try:
        path_to_download = os.path.abspath(path_to_download)
        try:
            os.makedirs(path_to_download)
        except:
            pass

        print('\n\n')


        if type == 'chrome' or type == '':
            capabilities = {}

            if uctype:
                print(f'uctype option true')
                chrome_options = uc.ChromeOptions()
            else:
                print(f'uctype option false')


                capabilities['acceptSslCerts'] = True
                capabilities['acceptInsecureCerts'] = True

                chrome_options = Options()

                chrome_options.add_argument('log-level=1')


                chrome_options.add_argument("--ignore-certificate-errors")



                chrome_options.add_argument('--allow-running-insecure-content')


                chrome_options.add_argument('disable-infobars')

                chrome_options.add_argument("--disable-login-animations")
                chrome_options.add_argument("--disable-notifications")
                chrome_options.add_argument("--disable-default-apps")
                chrome_options.add_argument('--ignore-gpu-blocklist')
                chrome_options.add_argument('--disable-gpu-driver-bug-workarounds')
                chrome_options.add_argument('--disable-impl-side-painting')
                chrome_options.add_argument('--disable-accelerated-2d-canvas')
                chrome_options.add_argument('--disable-accelerated-jpeg-decoding')
                chrome_options.add_argument('--test-type=ui')
                chrome_options.add_argument(f'--force-device-scale-factor={scale_factor}')
                chrome_options.add_argument('--dns-prefetch-disable')
                chrome_options.add_argument('--always-authorize-plugins')
                chrome_options.add_argument('--aggressive-cache-discard')
                chrome_options.add_argument('--disable-cache')
                chrome_options.add_argument('--disable-application-cache')
                chrome_options.add_argument('--disable-offline-load-stale-cache')
                chrome_options.add_argument('--disk-cache-size=1000')
                chrome_options.add_argument('--no-proxy-server')
                chrome_options.add_argument("--ignore-certificate-errors")

                prefs = {}
                prefs["download.prompt_for_download"] = False
                prefs["plugins.always_open_pdf_externally"] = True
                prefs["profile.default_content_setting_values.notifications"] = 2
                prefs["profile.password_manager_enabled"] = False
                prefs["credentials_enable_service"] = False
                prefs["download.directory_upgrade"] = True
                prefs['download.default_directory'] = path_to_download
                prefs['download.prompt_for_download'] = False

            chrome_options.add_argument('--disable-dev-shm-usage')  # 3nio
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument(f'--window-position={posX},{posY}')
            chrome_options.add_argument(f'--window-size={largura},{altura}')


            if cert_digital and len(list_url_cert_digital) > 0:
                self.printa('info', 'entrou no cert digital')
                qtde_list_url_cert_digital = len(list_url_cert_digital)

                chrome_options.add_argument("--ssl-client-certificate-file=" + path_cert_digital)
                # chrome_options.add_argument("--ssl-client-certificates-dir=" + path_cert_digital)
                chrome_options.add_argument("--ssl-version-min=tls1.2")
                chrome_options.add_argument("--ssl-client-key-passphrase=" + senha_cert_digital)

                chrome_options.add_experimental_option('prefs', {'required_client_certificate_for_user': path_cert_digital})

                if qtde_list_url_cert_digital > 1:
                    chrome_options.add_argument("--auto-select-certificate-for-urls=" + ",".join(list_url_cert_digital))
                elif qtde_list_url_cert_digital == 1:
                    url_um_cert = list_url_cert_digital[0]
                    chrome_options.add_argument("--auto-select-certificate-for-urls=" + url_um_cert)
                else:
                    # self.logger.error(f'erro ao tentar abrir urls {list_url_cert_digital} com certificado digital')
                    self.printa('error', f'erro ao tentar abrir urls {list_url_cert_digital} com certificado digital')
            else:
                self.printa('info', '                      Iniciando webdriver chrome ')





            if False:
            #if install_extension == True:
                try:
                    list_extensions_to_install = extensions_to_install.split(';')
                    # print(f'create_driver: list_extensions_to_install: {list_extensions_to_install}')
                    qtde_extensions_to_install = len(list_extensions_to_install)
                    while qtde_extensions_to_install > 0:
                        valor_indice = qtde_extensions_to_install - 1
                        # print(f'create_driver: instalando Extensão local {list_extensions_to_install[valor_indice]}')
                        # chrome_options.add_extension('Save-to-Pocket_v3.0.0.11.crx')
                        chrome_options.add_extension(f'{dir_extensions}/{list_extensions_to_install[valor_indice]}')
                        # print(f'create_driver: Instalado! Extensão local {dir_extensions}/{list_extensions_to_install[valor_indice]}')
                        # time.sleep(2)
                        qtde_extensions_to_install -= 1

                except Exception as e:
                    # print(f'create_driver: DEU erro if install_extension: {e}')
                    print('')




            if kiosk == True:
                chrome_options.add_argument("--start-maximized")
                chrome_options.add_argument("--kiosk")  ##esse é muito interessante para colocar no raspberry e na tv




            if headless == True:
                chrome_options.add_argument("headless")
                chrome_options.add_argument('--disable-gpu')


            self.printa('debug', f'                         path_to_download={path_to_download}')



            if uctype:
                print(f'uctype prefs true')

            else:
                print(f'uctype prefs false')
                prefs["safebrowsing.enabled"] = True
                emulation = {"deviceMetrics": {
                    "width": largura,
                    "height": altura,
                    "scale": scale_factor,
                    "pixelRatio": 1 }}
                chrome_options.add_experimental_option("mobileEmulation", emulation)
                chrome_options.add_experimental_option('prefs', prefs)


            try:
                self.printa('debug', f' instalando ChromeDriverManager().install()')
                chromepath = ChromeDriverManager().install()
            except Exception as e:
                errr = str(e)
                self.printa('critical', f' ERRO: ChromeDriverManager().install(): {errr}')
                if str('There is no such driver by url') in str(errr):
                    # print(f'ERRRRRORRRR: {errr}')
                    erro_msg = f'{errr}'.replace('/chromedriver_linux64.zip','').split('/')[-1]
                    raise Exception(f' ERRO ao tentar baixar o chromedriver. \n Por favor atualize seu chrome para a versao mais recente emaior que esta "{erro_msg}". \n ERRO: "{e}"\n\n\n\n\n')




            pathc = os.path.abspath(chromepath)
            self.printa('debug', f'                         chromepath={pathc}')
            try:
                replacement = "akl_roepstdlwoeproslPOweos".encode()
                with io.open(pathc, "r+b") as fh:
                    for line in iter(lambda: fh.readline(), b""):
                        if b"cdc_" in line:
                            fh.seek(-len(line), 1);
                            newline = re.sub(b"cdc_.{22}", replacement, line);
                            fh.write(newline);
                            self.printa('info', "                         linha cdc_ encontrada e alterada com sucesso")
            except Exception as e:
                self.printa('error', f'ERROR: no cdc: {e}')

            try:
                self.printa('info', f'                            criando driver pelo metodo 1')

                if uctype:
                    driver = uc.Chrome(executable_path=f'{pathc}', chrome_options=chrome_options, desired_capabilities=capabilities)  # Optional argument, if not specified will search path.
                else:
                    driver = webdriver.Chrome(executable_path=f'{pathc}', chrome_options=chrome_options, desired_capabilities=capabilities)  # Optional argument, if not specified will search path.

            except Exception as e:
                self.printa('error', f'                               deu erro no metodo 1: {e}')
                try:
                    self.printa('info', f'                            criando driver pelo metodo 2 com service')
                    service = Service(executable_path=pathc, chrome_options=chrome_options, desired_capabilities=capabilities)
                    if uctype:
                        print(f'uctype driver true')
                        driver = uc.Chrome(service=service, options=chrome_options)  # Optional argument, if not specified will search path.
                    else:
                        print(f'uctype driver false')
                        driver = webdriver.Chrome(service=service, options=chrome_options)  # Optional argument, if not specified will search path.
                except Exception as e:
                    self.printa('critical', f'                               deu erro no metodo 2: {e}')
                    raise Exception(f'Agora lascou, deu erro tambem no metodo service')

            self.printa('info', f'                      CRIADO driver: {driver}')

            driver.set_page_load_timeout(set_page_load_timeout)
            driver.implicitly_wait(implicitly_wait)

            # driver = uc.drivera

            # driver.get('https://supervisao.com.vc/')

            # time.sleep(1)

            # driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options, desired_capabilities=capabilities)  # Optional argument, if not specified will search path.

            # print('create_driver: chrome 0010 carregado driver')
            # try:
            #     print('\n\n\n------\n-------\nchrome position window: ini')
            #
            #     # driver.Manage().Window.Position = new System.Drawing.Point(2000, 1)
            #     # driver.Manage().Window.Maximize();
            #
            #     # time.sleep(2)
            #     # driver.set_window_position(300, 0)
            #     # time.sleep(2)
            #     # # driver.maximize_window()
            #     # time.sleep(2)
            #     # driver.set_window_position(-1200, 0)
            #     # time.sleep(2)
            #     # #driver.maximize_window()
            #     # # time.sleep(2)
            #     # # driver.set_window_position(100, 100)
            #     # # time.sleep(2)
            #     # driver.set_window_size(largura, altura)
            #     print('chrome position window: fim\n------\n-------\n\n\n')
            #     time.sleep(2)
            # except Exception as e:
            #     print(f'\n\n\n------\n-------\n\n\nerro chrome position window: {e}')
            #     time.sleep(20)

            #print('chrome 010')
            try:
                # print('create_driver: chrome 0011a vai tentar if headless == True')
                if False:
                    if headless == True:
                        # print('create_driver: chrome 0011b dentro if headless == True')
                        # print('create_driver: chrome 011 headless true')
                        driver.command_executor._commands["send_command"] = (
                            "POST",
                            '/session/$sessionId/chromium/send_command')
                        params = {
                            'cmd': 'Page.setDownloadBehavior',
                            'params': {
                                'behavior': 'allow',
                                'downloadPath': path_to_download
                            }
                        }
                        driver.execute("send_command", params)
                # print('create_driver: chrome 0011c saiu if headless == True')


                # print('create_driver: chrome 012')
            except Exception as e:
                # print(f'create_driver: erro no if headless == True POST - {e}')
                print('\n\n')

            # print('create_driver: chrome 0013 vai para return driver')



            return driver

        elif type == 'firefox':
            capabilities = {}
            options = OptionsFF()

            # capabilities = DesiredCapabilities.FIREFOX.copy()
            capabilities["marionette"] = True  # para usar o protocolo Marionette
            capabilities["log.level"] = "trace"  # para definir o nível de log
            capabilities["moz:firefoxOptions"] = {}  # para definir opções específicas do Firefox


            # options.add_extension("/home/user/my_extension.xpi")  # para adicionar uma extensão
            # options.profile = "/home/user/my_profile"  # para usar um perfil existente


            if headless == True:
                options.add_argument("--headless")
                # capabilities["moz:firefoxOptions"]["args"] = ["--headless"]

            # firefoxpath = config['drivers']['firefox_path']



            # options.set_preference("browser.download.dir", "/home/user/Downloads")

            options.set_preference("browser.download.dir", path_to_download)
            # options.merge_capabilities(capabilities)

            firefoxpath = GeckoDriverManager().install()
            pathc = os.path.abspath(firefoxpath)
            self.printa('debug', f'                         firefoxpath={pathc}')
            self.printa('debug', f'                         path_to_download={path_to_download}')



            try:

                self.printa('info', f'                            criando driver firefox pelo metodo 1')
                # driver = webdriver.Chrome(executable_path=f'{pathc}', chrome_options=chrome_options, desired_capabilities=capabilities)  # Optional argument, if not specified will search path.
                driver = webdriver.Firefox(pathc, desired_capabilities=capabilities, options=options)
            except Exception as e:
                self.printa('error', f'                              firefox deu erro no metodo 1: {e}')
                try:
                    self.printa('info', f'                            criando driver firefox pelo metodo 2 com service')
                    # service = Service(executable_path=pathc, chrome_options=chrome_options, desired_capabilities=capabilities)
                    # driver = webdriver.Chrome(service=service, options=chrome_options)  # Optional argument, if not specified will search path.

                    # service = ServiceFF(executable_path=pathc, desired_capabilities=capabilities)
                    service = ServiceFF(executable_path=pathc)
                    driver = webdriver.Firefox(service=service, options=options)

                except Exception as e:
                    self.printa('critical', f'                              firefox deu erro no metodo 2: {e}')
                    raise Exception(f'firefox: Agora lascou, deu erro tambem no metodo service: {e}')

            self.printa('info', f'                      CRIADO firefox driver: {driver}')

            # driver = webdriver.Firefox(pathc)
            # driver.set_page_scale_factor(scale_factor)
            driver.set_window_size(largura, altura)
            driver.set_window_position(posX, posY)
            driver.execute_script(f"document.body.style.zoom = '{scale_factor}'")
            return driver

        elif type == 'phantomjs':
            # phantomjspath = config['drivers']['phantomjs_path']
            phantomjspath = ''
            driver = webdriver.PhantomJS(phantomjspath)
            return driver

        # except Exception as e:
        #     print(f'       create_driver: DEU erro ao criar driver {e}')
        #     print('')
