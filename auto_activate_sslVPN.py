import time, os, os.path, traceback
from getpass import getpass
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

def authorizationData():
    os.system('cls||clear')
    
    print(f'[{datetime.now().strftime("%d/%m/%Y в %H:%M:%S")}] [INFO] Для смены логина или пароля необходимо удалить файл auth.txt или удалить данные из него\n'
            f'[{datetime.now().strftime("%d/%m/%Y в %H:%M:%S")}] [ATTENTION!] При закрытии консоли выполнение скрипта остановится')
    
    authFile = 'auth.txt'
    currentDir = os.getcwd()
    try:
        fileList = os.listdir(currentDir)
        if authFile in fileList:
            checkIsEmpty = os.stat(f'{currentDir}/{authFile}').st_size == 0
            if checkIsEmpty == True:
                createAuthorizationData()
            else:
                with open(authFile, 'r') as openFile:
                    lines = openFile.readlines()
                    LOGIN = lines[0].replace(' ','')
                    PASSWORD = lines[1].replace(' ', '')
                    openFile.close()
        else:
            createAuthorizationData()
    except Exception as e:
        print(f'[ОШИБКА] {traceback.format_exc()}')
    finally:
        autoLogin(PASSWORD, LOGIN)
        
def createAuthorizationData():
    
    LOGIN = input(f'[{datetime.now().strftime("%d/%m/%Y в %H:%M:%S")}] [INPUT] Введите логин: ')
    PASSWORD = getpass(f'[{datetime.now().strftime("%d/%m/%Y в %H:%M:%S")}] [INPUT] Введите пароль: ')
    
    with open('auth.txt', 'w') as newFile:
        newFile.write(f'{LOGIN}\n{PASSWORD}')
        newFile.close()
        
    authorizationData()

    
def autoLogin(PASSWORD, LOGIN):
    
    options=Options()
    options.set_preference('security.tls.version.min', 1)
    driver = webdriver.Firefox(options=options)
    
    try:
        driver.get('https://10.10.10.60/')
    except:
        try: 
            driver.quit()
        except:
            pass
        autoLogin(PASSWORD, LOGIN)
    finally:
        try:
            user_name = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'username'))
            )
        finally:
            user_name.send_keys(LOGIN)
            print(f'[{datetime.now().strftime("%d/%m/%Y в %H:%M:%S")}] [INFO] Логин введен успешно!')
            try:
                password = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.NAME, 'pwd'))
                )
            finally:
                password.send_keys(PASSWORD)
                ssl_login = driver.find_element('name', 'LoginSSL')
                ssl_login.click()
        
    start_script_again = datetime.now() + timedelta(hours=14)
    
    print(f'[{datetime.now().strftime("%d/%m/%Y в %H:%M:%S")}] [INFO] Скрипт будет запущен автоматически {start_script_again.strftime("%d/%m/%Y в %H:%M")}')
    
    extensionLogin(driver, PASSWORD, LOGIN)
        

def extensionLogin(driver, PASSWORD, LOGIN):
    
    while True:
        
        time.sleep(50400)

        try:
            _logout = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, '_logout'))
            )
        except:
            driver.quit()
            autoLogin(PASSWORD, LOGIN)
        finally:
            _logout.click()
            autoLogin(PASSWORD, LOGIN, driver)
        
    
if __name__ == '__main__':
    authorizationData()