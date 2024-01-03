import random
import time
import zipfile
import os
from datetime import datetime

import pyperclip
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from config import *
from xpath import *
from loguru import logger as log
from selenium.webdriver.common.keys import Keys


ref = 'H6jgeh5'
log.add("logger.log", format="{time:YYYY-MM-DD | HH:mm:ss.SSS} | {level} \t| {function}:{line} - {message}")

MNEMONIC = 'fault mouse weird peasant wasp enroll vote black spend sugar dice senior'.split(' ')
PASSWORD = '11111111'
PASSWORD2 = 'Qzmp2023'
EMAIL = 'jobpfrosjc@rambler.ru'


def choose_random(file_name):
    try:
        with open(file_name, 'r') as file:
            codes = [code.strip() for code in file.readlines()]
        return random.choice(codes) if codes else ''
    except FileNotFoundError:
        return ''


def save_data(secret_key_dop, seed_prase_dop, password_dop, email_address, mnemonic_mm, password_mm='11111111'):

    file_path = 'success_reg_accounts.txt'
    data_line = f"{secret_key_dop}:{seed_prase_dop}:{password_dop}:{email_address}:{mnemonic_mm}:{password_mm}\n"

    with open(file_path, 'a') as file:
        file.write(data_line)
    log.info(f"{email_address} | data save in {file_path}")



def auto_reg():

    chrome_options = Options()
    chrome_options.add_extension('MetaMask_Chrome.crx')
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    driver.get(url_main_dop + ref)

    driver.implicitly_wait(10)
    time.sleep(time_break)

    driver.switch_to.window(driver.window_handles[1])
    time.sleep(time_break)

    try:

        driver.find_element('xpath',
                            '/html/body/div[1]/div/div[2]/div/div/div/ul/li[1]/div/input').click()  # agree to TOS
        time.sleep(time_break)
        log.info(f"{EMAIL} | click | agree to TOS | MM")

        driver.find_element('xpath', '/html/body/div[1]/div/div[2]/div/div/div/ul/li[3]/button').click()  # import
        time.sleep(time_break)
        log.info(f"{EMAIL} | click  | import | MM")

        driver.find_element('xpath', '/html/body/div[1]/div/div[2]/div/div/div/div/button[2]').click()  # no thanks
        time.sleep(time_break)
        log.info(f"{EMAIL} | click | no thanks | MM")

        for i in range(3): driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.TAB)  # locate mnemonic box
        for word in MNEMONIC:
            driver.switch_to.active_element.send_keys(word)
            for i in range(2): driver.find_element(By.CSS_SELECTOR, 'body').send_keys(
                Keys.TAB)  # switch to next textbox
            time.sleep(time_break)
        log.info(f"{EMAIL} | input | mnemonic | MM")
        time.sleep(time_break)

        driver.find_element('xpath', '/html/body/div[1]/div/div[2]/div/div/div/div[4]/div/button').click()  # confirm
        time.sleep(time_break)
        log.info(f"{EMAIL} | click | mnemonic confirm | MM")

        driver.find_element('xpath',
                            '/html/body/div[1]/div/div[2]/div/div/div/div[2]/form/div[1]/label/input').send_keys(
            PASSWORD)  # enter password
        driver.find_element('xpath',
                            '/html/body/div[1]/div/div[2]/div/div/div/div[2]/form/div[2]/label/input').send_keys(
            PASSWORD)  # enter password twice
        time.sleep(time_break)
        log.info(f"{EMAIL} | input | 2 password | MM")

        driver.find_element('xpath',
                            '/html/body/div[1]/div/div[2]/div/div/div/div[2]/form/div[3]/label/input').click()  # I understand
        time.sleep(time_break // 2)
        log.info(f"{EMAIL} | click | I understand | MM")

        driver.find_element('xpath',
                            '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/button').click()  # import my wallet
        time.sleep(time_break // 2)
        log.info(f"{EMAIL} | click | import my wallet | MM)")

        driver.find_element('xpath', '/html/body/div[1]/div/div[2]/div/div/div/div[2]/button').click()  # got it
        time.sleep(time_break // 2)
        log.info(f"{EMAIL} | click | got it MM")

        driver.find_element('xpath', '/html/body/div[1]/div/div[2]/div/div/div/div[2]/button').click()  # next page
        time.sleep(time_break // 2)
        log.info(f"{EMAIL} | click | next page | MM")

        driver.find_element('xpath', '/html/body/div[1]/div/div[2]/div/div/div/div[2]/button').click()  # done
        time.sleep(time_break // 2)
        log.info(f"{EMAIL} | click | done | MM")

        driver.find_element('xpath', '/html/body/div[2]/div/div/section/div[1]/div/button/span').click()  # close
        time.sleep(time_break // 2)
        log.info(f"{EMAIL} | click | close| MM")

        # --------------------------------------------------------------------------------------------------------------------- switch to window DOP

        driver.switch_to.window(driver.window_handles[0])
        time.sleep(time_break)
        log.info(f"{EMAIL} | switch | to window DOP")

        driver.find_element('xpath',
                            '/html/body/div[3]/div/div/div[2]/form/div[1]/div/label').click()  # I understand
        time.sleep(time_break)
        log.info(f"{EMAIL} | click | I understand | DOP)")

        driver.find_element('xpath',
                            '/html/body/div[3]/div/div/div[2]/form/div[2]/input').send_keys(
            EMAIL)  # enter email twice
        time.sleep(time_break)
        log.info(f"{EMAIL} | input | email | DOP")

        driver.find_element('xpath', '/html/body/div[3]/div/div/div[2]/form/button').click() # continue
        time.sleep(time_break)
        log.info(f"{EMAIL} | click | continue | DOP")

        driver.find_element('xpath', '//*[@id="root"]/section[2]/div/div[2]/div[1]/a/button').click() # create new wallet
        time.sleep(time_break)
        log.info(f"{EMAIL} | click | create new wallet | DOP")

        driver.find_element('xpath',
                            '//*[@id="root"]/section[2]/div/div/form/div/div[1]/input').send_keys(
            PASSWORD2)  # enter password
        time.sleep(time_break)

        driver.find_element('xpath',
                            '//*[@id="root"]/section[2]/div/div/form/div/div[2]/input').send_keys(
            PASSWORD2)  # enter password twice
        time.sleep(time_break)
        log.info(f"{EMAIL} | input | 2 password | DOP")

        driver.find_element('xpath',
                            '//*[@id="root"]/section[2]/div/div/form/div/button').click()  # I confirm
        time.sleep(time_break*2)
        log.info(f"{EMAIL} | click | I confirm | DOP")

        driver.find_element('xpath',
                            '//*[@id="root"]/section[2]/div/div/div[2]/div[3]/button/p').click()  # copy phrase
        driver.implicitly_wait(time_break)
        time.sleep(time_break)
        log.info(f"{EMAIL} | click | copy phrase | DOP")

        driver.find_element('xpath',
                            '//*[@id="root"]/section[2]/div/div/div[2]/div[3]/a/button').click() # verify
        driver.implicitly_wait(time_break)
        log.info(f"{EMAIL} | click | verify | DOP")
        time.sleep(time_break)

        copied_phrase = pyperclip.paste()
        log.info(f'seed phrase | {copied_phrase}')
        seed_phrase = copied_phrase.split()

        log.info(f"{EMAIL} | click | verify phase 12 words | DOP")
        for word in seed_phrase:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//button[contains(., '{word}')]"))).click() # check phase
            time.sleep(time_break)

        driver.find_element('xpath',
                            '//*[@id="root"]/section[2]/div/div/div[2]/div[2]/button').click()  # verify confirm
        time.sleep(time_break)
        log.info(f"{EMAIL} | click | verify confirm | DOP")

        driver.find_element('xpath',
                            '//*[@id="root"]/section[2]/div/div/div[3]/button').click()  # verify continue
        time.sleep(time_break)
        log.info(f"{EMAIL} | click | verify continue | DOP")

        driver.find_element('xpath',
                            '/html/body/div[3]/div/div/div/h6/p/img').click()  # copy secret key
        time.sleep(time_break)
        log.info(f"{EMAIL} | click | copy secret key | DOP")

        secret_key = pyperclip.paste()
        log.info(f'secret key | {secret_key}')

        driver.find_element('xpath',
                            '/html/body/div[3]/div/div/div/div[2]/button').click()  # done
        time.sleep(time_break)
        log.info(f"{EMAIL} | click | done | DOP")

        save_data(secret_key, seed_phrase, PASSWORD2, EMAIL, MNEMONIC)
        log.success('Created account in DOP successfully!')
        print()

        driver.find_element('xpath',
                            '//*[@id="root"]/section[2]/div/div/form/div/div/input').send_keys(
            PASSWORD2)  # input password login
        time.sleep(time_break)
        log.info(f"{EMAIL} | input | password | DOP")

        driver.find_element('xpath',
                            '//*[@id="root"]/section[2]/div/div/form/div/button').click()  # key confirm
        time.sleep(time_break)
        log.info(f"{EMAIL} | click | password confirm | DOP")

        driver.find_element('xpath',
                            '/html/body/div[5]/div/div/div[2]/button').click()  # start
        time.sleep(time_break)
        log.info(f"{EMAIL} | click | start testnet | DOP")

        driver.find_element('xpath',
                            '/html/body/div[3]/div/div/div/div[2]/button').click()  # connect MM
        time.sleep(time_break)
        log.info(f"{EMAIL} | click | connect MM | DOP")

        log.info(f"list of open windows | {driver.window_handles}")

        # ----------------------------------------------------------------------------------------------------------------- switch to window MM

        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(time_break)
        log.info(f"{EMAIL} | switch | to window MM")

        driver.find_element('xpath',
                            '//*[@id="app-content"]/div/div/div/div[3]/div[2]/footer/button[2]').click()  # confirm in MM
        time.sleep(time_break)
        log.info(f"{EMAIL} | click | confirm | MM")

        driver.find_element('xpath',
                            '//*[@id="app-content"]/div/div/div/div[3]/div[2]/footer/button[2]').click()  # connect final MM
        time.sleep(time_break)
        log.info(f"{EMAIL} | click | connect final | MM")

        driver.find_element('xpath',
                            '//*[@id="app-content"]/div/div/div/div[2]/div/button[2]').click()  # switch network on cepolia
        time.sleep(time_break)
        log.info(f"{EMAIL} | click | switch network on cepolia | MM")

        log.debug('Press Enter to exit...')
        input()

        return True

    except Exception as e:
        log.error(f'     | {str(e)}')
    finally:
        driver.quit()


auto_reg()
