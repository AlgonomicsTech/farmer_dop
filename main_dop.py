import random
import time
import zipfile
import os

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

MNEMONIC = 'jeans letter able dog erase conduct oblige update feature dumb sleep blanket'.split(' ')
PASSWORD = '11111111'
PASSWORD2 = 'Qzmp2023'
EMAIL = 'hCnn1eu4O2wt@rambler.ru:f7xxyyc4GhlO@1'


def choose_random(file_name):
    try:
        with open(file_name, 'r') as file:
            codes = [code.strip() for code in file.readlines()]
        return random.choice(codes) if codes else ''
    except FileNotFoundError:
        return ''





def auto_reg():
    try:

        chrome_options = Options()
        chrome_options.add_extension('MetaMask_Chrome.crx')
        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()

        driver.get(url_main_dop + ref)

        driver.implicitly_wait(10)
        time.sleep(time_break)

        driver.switch_to.window(driver.window_handles[1])
        time.sleep(time_break)

        # fix "Message: unknown error: Runtime.callFunctionOn threw exception: Error: LavaMoat"
        # solution: https://github.com/LavaMoat/LavaMoat/pull/360#issuecomment-1547271080
        driver.find_element('xpath',
                            '/html/body/div[1]/div/div[2]/div/div/div/ul/li[1]/div/input').click()  # agree to TOS
        time.sleep(time_break)
        driver.find_element('xpath', '/html/body/div[1]/div/div[2]/div/div/div/ul/li[3]/button').click()  # import
        time.sleep(time_break)
        driver.find_element('xpath', '/html/body/div[1]/div/div[2]/div/div/div/div/button[2]').click()  # no thanks
        time.sleep(time_break)
        for i in range(3): driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.TAB)  # locate mnemonic box
        for word in MNEMONIC:
            driver.switch_to.active_element.send_keys(word)  # input each mnemonic to current textbox
            for i in range(2): driver.find_element(By.CSS_SELECTOR, 'body').send_keys(
                Keys.TAB)  # switch to next textbox
            time.sleep(1)
        time.sleep(time_break)

        driver.find_element('xpath', '/html/body/div[1]/div/div[2]/div/div/div/div[4]/div/button').click()  # confirm
        time.sleep(0.5)

        driver.find_element('xpath',
                            '/html/body/div[1]/div/div[2]/div/div/div/div[2]/form/div[1]/label/input').send_keys(
            PASSWORD)  # enter password
        driver.find_element('xpath',
                            '/html/body/div[1]/div/div[2]/div/div/div/div[2]/form/div[2]/label/input').send_keys(
            PASSWORD)  # enter password twice
        time.sleep(time_break)
        driver.find_element('xpath',
                            '/html/body/div[1]/div/div[2]/div/div/div/div[2]/form/div[3]/label/input').click()  # I understand


        driver.find_element('xpath',
                            '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/button').click()  # import my wallet
        driver.find_element('xpath', '/html/body/div[1]/div/div[2]/div/div/div/div[2]/button').click()  # got it
        driver.find_element('xpath', '/html/body/div[1]/div/div[2]/div/div/div/div[2]/button').click()  # next page
        driver.find_element('xpath', '/html/body/div[1]/div/div[2]/div/div/div/div[2]/button').click()  # done

        time.sleep(time_break)
        driver.find_element('xpath', '/html/body/div[2]/div/div/section/div[1]/div/button/span').click()  # close

        driver.switch_to.window(driver.window_handles[0])
        time.sleep(time_break)


        driver.find_element('xpath',
                            '/html/body/div[3]/div/div/div[2]/form/div[1]/div/label').click()  # I understand
        time.sleep(time_break)

        driver.find_element('xpath',
                            '/html/body/div[3]/div/div/div[2]/form/div[2]/input').send_keys(
            EMAIL)  # enter email twice

        time.sleep(time_break)

        driver.find_element('xpath', '/html/body/div[3]/div/div/div[2]/form/button').click() # continue
        time.sleep(time_break)

        driver.find_element('xpath', '//*[@id="root"]/section[2]/div/div[2]/div[1]/a/button').click() # create new wallet

        time.sleep(time_break)
        driver.find_element('xpath',
                            '//*[@id="root"]/section[2]/div/div/form/div/div[1]/input').send_keys(
            PASSWORD2)  # enter password

        time.sleep(time_break)
        driver.find_element('xpath',
                            '//*[@id="root"]/section[2]/div/div/form/div/div[2]/input').send_keys(
            PASSWORD2)  # enter password twice
        time.sleep(time_break)

        driver.find_element('xpath',
                            '//*[@id="root"]/section[2]/div/div/form/div/button').click()  # I confifm
        time.sleep(time_break)

        log.debug('Press Enter to exit...0')
        input()

        driver.find_element('xpath',
                            '//*[@id="root"]/section[2]/div/div/div[2]/div[3]/button/p').click()  # copy prase
        driver.implicitly_wait(time_break)

        log.debug('Press Enter to exit...1')
        input()

        driver.find_element('xpath',
                            '//*[@id="root"]/section[2]/div/div/div[2]/div[3]/a/button').click() # verify
        driver.implicitly_wait(time_break)

        # Використання pyperclip для отримання тексту з буфера обміну
        copied_url = pyperclip.paste()
        seed_phrase = copied_url.split()
        log.info(f'seed_prase | {seed_phrase}')


        log.debug('Press Enter to exit...1')
        input()

        for word in seed_phrase:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//button[contains(., '{word}')]"))).click() # check phase
            time.sleep(time_break)

        driver.find_element('xpath',
                            '//*[@id="root"]/section[2]/div/div/div[2]/div[2]/button').click()  # verify confirm
        time.sleep(time_break)

        driver.find_element('xpath',
                            '//*[@id="root"]/section[2]/div/div/div[3]/button').click()  # verify continue
        time.sleep(time_break)

        driver.find_element('xpath',
                            '/html/body/div[3]/div/div/div/h6/p/img').click()  # copy secret key
        time.sleep(time_break)

        # ----------------------------------------------------save secret key

        driver.find_element('xpath',
                            '/html/body/div[3]/div/div/div/div[2]/button').click()  # done
        time.sleep(time_break)

        driver.find_element('xpath',
                            '//*[@id="root"]/section[2]/div/div/form/div/div/input').send_keys(
            PASSWORD2)  # enter password 222
        time.sleep(time_break)

        driver.find_element('xpath',
                            '//*[@id="root"]/section[2]/div/div/form/div/button').click()  # key confirm
        time.sleep(time_break)

        driver.find_element('xpath',
                            '/html/body/div[5]/div/div/div[2]/button').click()  # start
        time.sleep(time_break)

        driver.find_element('xpath',
                            '/html/body/div[3]/div/div/div/div[2]/button').click()  # connect MM
        time.sleep(time_break)

        log.info(driver.window_handles)

        log.debug('Press Enter to exit...')
        input()

    except Exception as e:
        log.error(f'     | {str(e)}')
    finally:
        driver.quit()


auto_reg()
