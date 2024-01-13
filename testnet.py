import random
import string
import time

import pyperclip
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.common import NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from config import *
from solver_captcha import solve_recaptcha
from otp import get_otp
from loguru import logger as log
from selenium.webdriver.common.keys import Keys
import base64
import json



log.add("logger.log", format="{time:YYYY-MM-DD | HH:mm:ss.SSS} | {level} \t| {line}:{function} | {message}")


def encrypto_cookies(cookies):
    decoded_bytes = base64.b64decode(cookies)
    return decoded_bytes.decode('utf-8')

def choose_random(file_name):
    try:
        with open(file_name, 'r') as file:
            codes = [code.strip() for code in file.readlines()]
        return random.choice(codes) if codes else ''
    except FileNotFoundError:
        return ''


def is_account_registered_2(email_address):
    with open('success_reg_accounts.txt', 'r') as file:
        for line in file:
            if email_address in line.split(':')[3]:
                return True
    return False

def is_account_passed_testnet(email_address):
    with open('passed_testnet.txt', 'r') as file:
        for line in file:
            if email_address in line.split(':')[0]:
                return False
    return True


def twitter_not_use(lodin_twitter):
    with open('passed_testnet.txt', 'r') as file:
        for line in file:
            if lodin_twitter in line.split(':')[-1]:
                return False
    return True


def is_twitter_frozen(lodin_twitter):
    with open('frozen_twitter_accounts.txt', 'r') as file:
        for line in file:
            if lodin_twitter in line.split(':')[-1]:
                return False
    return True


def generate_password(length=8):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(length))
    return password


def save_data_passed_testnet(email_address, seed_phrase_dop, mnemonic_mm, twitter_login):
    file_path = 'passed_testnet.txt'
    data_line = f"{email_address}:{seed_phrase_dop}:{mnemonic_mm}:{twitter_login}\n"

    with open(file_path, 'a') as file:
        file.write(data_line)
    log.info(f"{email_address} | data save in {file_path}")


def save_data_frozen_twitter(twitter_login):
    file_path = 'frozen_twitter_accounts.txt'
    data_line = f"{twitter_login}\n"

    with open(file_path, 'a') as file:
        file.write(data_line)
    log.info(f"{twitter_login} | data save in {file_path}")


def save_data_ref_code(email, ref_code, count_referrals=0):

    file_path = 'ref.txt'
    data_line = f"{email}:{ref_code}:{count_referrals}\n"

    with open(file_path, 'a') as file:
        file.write(data_line)
    log.success(f"{email} | save {ref_code}")


def save_progress(email, number):
    updated_lines = []
    found = False

    with open("success_reg_accounts.txt", 'r') as file:
        lines = file.readlines()

    for line in lines:
        parts = line.strip().split(':')
        if len(parts) > 3 and parts[3] == email:
            found = True
            parts[-1] = str(number)  # Заміна останнього елемента на нове число
            line = ':'.join(parts) + '\n'
        updated_lines.append(line)

    if found:
        with open("success_reg_accounts.txt", 'w') as file:
            file.writelines(updated_lines)
        return True
    else:
        return False

def update_step_progress(email):
    with open("success_reg_accounts.txt", 'r') as file:
        lines = file.readlines()

    for line in lines:
        parts = line.strip().split(':')
        if len(parts) > 3 and parts[3] == email:
            return int(parts[-1])

    log.error(f"{email} | not found")
    return None


def copy_ref_code(driver, EMAIL):
    time.sleep(time_break)
    log.info(f"{EMAIL} | click | step 7 - done | DOP")

    driver.find_element('xpath',
                        '//*[@id="left-tabs-example-tabpane-earn"]/section/div[3]/div[8]/div[2]/div[1]/div[1]/div/p/h6/img').click()  # copy ref code

    time.sleep(time_break)
    log.info(f"{EMAIL} | click | copy ref code | DOT")

    driver.implicitly_wait(time_break)
    time.sleep(time_break)

    ref_code = pyperclip.paste().split('=')[1]
    log.info(f'ref code | {ref_code}')

    save_data_ref_code(EMAIL, ref_code)
    save_progress(EMAIL, 7)



def main_step(driver, EMAIL, mm_mnemonic, dop_mnemonic):

    mm_mnemonic = mm_mnemonic.split()
    global dop_password
    dop_password = generate_password()
    mm_password = generate_password()

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
    for word in mm_mnemonic:
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
        mm_password)  # enter password
    driver.find_element('xpath',
                        '/html/body/div[1]/div/div[2]/div/div/div/div[2]/form/div[2]/label/input').send_keys(
        mm_password)  # enter password twice
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
    # Відкриття нової вкладки з вказаним URL
    driver.execute_script(f"window.open('{url_testnet_dop}', '_blank');")
    # Переключення на нову вкладку
    driver.switch_to.window(driver.window_handles[-1])
    driver.find_element('xpath', '//*[@id="root"]/section[2]/div/div[2]/form/div[1]/div/label').click()  # I agree
    time.sleep(time_break)
    log.info(f"{EMAIL} | click | I agree | DOP")
    driver.find_element('xpath',
                        '//*[@id="root"]/section[2]/div/div[2]/form/div[2]/input').send_keys(
        EMAIL)  # enter email twice
    time.sleep(time_break)
    log.info(f"{EMAIL} | input | email | DOP")
    driver.find_element('xpath', '//*[@id="root"]/section[2]/div/div[2]/form/button').click()  # continue
    time.sleep(time_break)
    log.info(f"{EMAIL} | click | continue | DOP")
    driver.find_element('xpath',
                        '//*[@id="root"]/section[2]/div/div[2]/div[2]/a/button').click()  # import wallet
    time.sleep(time_break)
    log.info(f"{EMAIL} | click | import wallet | DOP)")
    driver.find_element('xpath',
                        '//*[@id="root"]/section[2]/div/div/form/div/div[1]/input').send_keys(
        dop_mnemonic)  # enter seed phrase
    time.sleep(time_break)
    log.info(f"{EMAIL} | input | seed phrase | DOP")
    driver.find_element('xpath',
                        '//*[@id="root"]/section[2]/div/div/form/div/div[3]/input').send_keys(
        dop_password)  # enter password
    time.sleep(time_break)
    driver.find_element('xpath',
                        '//*[@id="root"]/section[2]/div/div/form/div/div[4]/input').send_keys(
        dop_password)  # enter password twice
    time.sleep(time_break)
    log.info(f"{EMAIL} | input | 2 password | DOP")
    driver.find_element('xpath', '//*[@id="root"]/section[2]/div/div/form/div/button').click()  # submit
    time.sleep(time_break)
    log.info(f"{EMAIL} | click | submit | DOP")
    driver.find_element('xpath',
                        '//*[@id="root"]/section[2]/div/div/form/div/div/input').send_keys(
        dop_password)  # enter password login
    time.sleep(time_break)
    log.info(f"{EMAIL} | input | login | DOP")
    driver.find_element('xpath', '//*[@id="root"]/section[2]/div/div/form/div/button').click()  # unlock
    time.sleep(time_break)
    log.info(f"{EMAIL} | click | unlock | DOP")
    driver.find_element('xpath', '/html/body/div[5]/div/div/div[2]/button').click()  # start
    time.sleep(time_break)
    log.info(f"{EMAIL} | click | start | DOP")
    driver.find_element('xpath', '/html/body/div[3]/div/div/div/div[2]/button').click()  # Connect MM
    time.sleep(time_break)
    log.info(f"{EMAIL} | click | Connect MM| DOP")
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

    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(time_break)
    log.info(f"{EMAIL} | switch | to window DOP")

    log.success(dop_password)



def step1(driver, EMAIL):
    scroll_height = 10 * 37.7952755906

    # Виконуємо скролінг на вказану висоту
    driver.execute_script(f"window.scrollBy(0, {scroll_height});")
    time.sleep(time_break)
    log.info(f"{EMAIL} | scroll {int(scroll_height)} pixel | DOP")

    driver.find_element('xpath',
                        '//*[@id="left-tabs-example-tabpane-earn"]/section/div[3]/div[1]/div[2]/div/div/button').click()  # auth Twitter step 1
    time.sleep(time_break)
    log.info(f"{EMAIL} | click | auth twitter | DOP")

    log.info(f"counter of open windows | {len(driver.window_handles)}")

    # ------------------------------------------------------------------------------------------------------- switch to window TWITTER
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(time_break)
    log.info(f"{EMAIL} | switch | to window TWITTER")

    driver.find_element('xpath',
                        '//*[@id="allow"]').click()  # auth Twitter
    time.sleep(time_break)
    log.info(f"{EMAIL} | click | auth Twitter | TWITTER")

    # ------------------------------------------------------------------------------------------------------- switch to window DOP

    driver.switch_to.window(driver.window_handles[2])
    time.sleep(time_break)
    log.info(f"{EMAIL} | switch | to window DOP")



    driver.find_element('xpath',
                        '//*[@id="left-tabs-example-tabpane-earn"]/section/div[3]/div[1]/div[2]/div/button[2]').click()  # follow dop_org
    time.sleep(time_break)
    log.info(f"{EMAIL} | click | follow dop_org | DOP")

    # ------------------------------------------------------------------------------------------------------- switch to window TWITTER

    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(time_break)
    log.info(f"{EMAIL} | switch | to window TWITTER")
    driver.find_element('xpath',
                        '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[3]/div[1]/div').click()  # follow Twitter
    time.sleep(time_break)
    log.info(f"{EMAIL} | click | follow @dop_org | Twitter")

    # ------------------------------------------------------------------------------------------------------- switch to window DOP

    driver.close()

    driver.switch_to.window(driver.window_handles[2])
    time.sleep(time_break)
    log.info(f"{EMAIL} | switch | to window DOP")

    log.debug('Solve the captcha and press enter to continue..')
    input()
    save_progress(EMAIL, 1)



def step2(driver, EMAIL):

    scroll_height = 10 * 37.7952755906

    # Виконуємо скролінг на вказану висоту
    driver.execute_script(f"window.scrollBy(0, {scroll_height});")
    time.sleep(time_break)
    log.info(f"{EMAIL} | scroll на {int(scroll_height)} pixel | DOP")

    driver.find_element('xpath',
                        '//*[@id="left-tabs-example-tabpane-earn"]/section/div[3]/div[2]/div[2]/button').click()  # claim step 2
    time.sleep(timeout)
    log.info(f"{EMAIL} | click | claim | DOP")

    save_progress(EMAIL, 2)


def step3(driver, EMAIL):
    driver.find_element('xpath',
                        '//*[@id="left-tabs-example-tabpane-earn"]/section/div[3]/div[3]/div[2]/button').click()  # claim step 3
    time.sleep(timeout)
    log.info(f"{EMAIL} | click | claim | DOP")

    # ----------------------------------------------------------------------------------------------------------------- switch to window MM

    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(time_break)
    log.info(f"{EMAIL} | switch | to window MM")

    driver.find_element('xpath',
                        '//*[@id="app-content"]/div/div/div/div[3]/div[3]/footer/button[2]').click()  # confirm in MM
    time.sleep(timeout)
    log.info(f"{EMAIL} | click | confirm | MM")

    # ------------------------------------------------------------------------------------------------------- switch to window DOP

    save_progress(EMAIL, 3)

    driver.switch_to.window(driver.window_handles[2])
    time.sleep(timeout)
    log.info(f"{EMAIL} | switch | to window DOP")


def step4(driver, EMAIL):
    driver.find_element('xpath',
                        '//*[@id="left-tabs-example-tabpane-earn"]/section/div[3]/div[4]/div[2]/button').click()  # claim step 4
    time.sleep(timeout)
    log.info(f"{EMAIL} | click | claim | DOP")

    # ----------------------------------------------------------------------------------------------------------------- switch to window MM

    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(timeout)
    log.info(f"{EMAIL} | switch | to window MM")

    driver.find_element('xpath',
                        '//*[@id="app-content"]/div/div/div/div[3]/div[3]/footer/button[2]').click()  # confirm in MM step 4
    time.sleep(timeout)
    log.info(f"{EMAIL} | click | confirm | MM")

    # ------------------------------------------------------------------------------------------------------- switch to window DOP

    save_progress(EMAIL, 4)

    driver.switch_to.window(driver.window_handles[2])
    time.sleep(time_break)
    log.info(f"{EMAIL} | switch | to window DOP")


def step5(driver, EMAIL):
    driver.find_element('xpath',
                        '//*[@id="left-tabs-example-tabpane-earn"]/section/div[3]/div[5]/div[2]/button').click()  # step 5
    time.sleep(time_break)
    log.info(f"{EMAIL} | click | get started | DOP")


    driver.find_element('xpath',
                        '//*[@id="left-tabs-example-tabpane-deposit"]/section/section/form/div[1]/div[2]/div/img').click()  # step 5 - choice coin
    time.sleep(time_break)
    log.info(f"{EMAIL} | click | select coin | DOP")

    driver.find_element('xpath',
                        '/html/body/div[3]/div/div/div[2]/div[2]/div[1]').click()  # step 5 - choice USTD
    time.sleep(time_break)
    log.info(f"{EMAIL} | click | select USTD | DOP")

    amount_usdt = random.randint(7000, 10000)
    log.info(amount_usdt)
    driver.find_element('xpath',
                        '//*[@id="left-tabs-example-tabpane-deposit"]/section/section/form/div[2]/input').send_keys(
        amount_usdt)
    time.sleep(time_break)
    log.info(f"{EMAIL} | input | {amount_usdt} USDT")

    driver.find_element('xpath',
                        '//*[@id="left-tabs-example-tabpane-deposit"]/section/section/form/button').click()  # step 5 - encrypt
    time.sleep(time_break)
    log.info(f"{EMAIL} | click | encrypt {amount_usdt} usdt | DOP")

    driver.find_element('xpath',
                        '/html/body/div[3]/div/div/div[2]/div[3]/button[2]').click()  # step 5 - confirm
    time.sleep(time_break)
    log.info(f"{EMAIL} | click | confirm {amount_usdt} usdt | DOP")

    # ----------------------------------------------------------------------------------------------------------------- switch to window MM

    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(timeout)
    log.info(f"{EMAIL} | switch | to window MM")


    driver.find_element('xpath',
                        '//*[@id="app-content"]/div/div/div/div[9]/footer/button[2]').click()  # confirm-1 in MM step 5
    time.sleep(timeout)

    log.info(f"{EMAIL} | click | confirm-1 | MM")


    driver.find_element('xpath',
                        '//*[@id="app-content"]/div/div/div/div[10]/footer/button[2]').click()  # confirm-2 in MM step 5
    time.sleep(timeout)
    log.info(f"{EMAIL} | click | confirm-2 | MM")


    time.sleep(timeout * 2)

    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(timeout)
    log.info(f"{EMAIL} | switch | to window MM")

    time.sleep(timeout * 2)

    driver.find_element('xpath',
                        '//*[@id="app-content"]/div/div/div/div[3]/div[3]/footer/button[2]').click()  # confirm-3 in MM step 5
    time.sleep(timeout*2)
    log.info(f"{EMAIL} | click | confirm-3 | MM")



    # ------------------------------------------------------------------------------------------------------- switch to window DOP

    driver.switch_to.window(driver.window_handles[2])
    time.sleep(time_break)
    log.info(f"{EMAIL} | switch | to window DOP")

    save_progress(EMAIL, 5)

    driver.find_element('xpath',
                        '/html/body/div[3]/div/div/div/div[2]/button[1]').click()  # step 5 - close
    time.sleep(time_break)
    log.info(f"{EMAIL} | click | close | DOP")

    driver.find_element('xpath',
                        '/html/body/div[7]/div/div/div/div[2]/button').click()  # step 5 - okey
    time.sleep(time_break)
    log.info(f"{EMAIL} | click | okey | DOP")


def step6(driver, EMAIL):

    driver.find_element('xpath',
                        '//*[@id="left-tabs-example-tabpane-earn"]/section/div[3]/div[6]/div[2]/button').click()  # step 6 - get started
    time.sleep(time_break)
    log.info(f"{EMAIL} | click | get started | DOP")

    dop_test_adress = '0x130c318bef3a60f05541955003b2baa1d691335f'

    driver.find_element('xpath',
                        '//*[@id="left-tabs-example-tabpane-transfer"]/section/section/form/div[1]/input').send_keys(
        dop_test_adress)
    time.sleep(time_break)
    log.info(f"{EMAIL} | input | {dop_test_adress} | DOP")


    driver.find_element('xpath',
                        '//*[@id="left-tabs-example-tabpane-transfer"]/section/section/form/div[2]/div').click()  # step 6 - select token
    time.sleep(time_break)
    log.info(f"{EMAIL} | click | select token | DOP")

    driver.find_element('xpath',
                        '/html/body/div[3]/div/div/div[2]/div[2]/div[1]').click()  # step 6 - select token USDT
    time.sleep(time_break)
    log.info(f"{EMAIL} | click | select token USDT | DOP")

    amount_usdt = random.randint(1, 3000)
    driver.find_element('xpath',
                        '//*[@id="left-tabs-example-tabpane-transfer"]/section/section/form/div[3]/input').send_keys(
        amount_usdt)
    time.sleep(time_break)
    log.info(f"{EMAIL} | input | {amount_usdt} USDT")

    driver.find_element('xpath',
                        '//*[@id="left-tabs-example-tabpane-transfer"]/section/section/form/button').click()  # step 6 - send submit
    time.sleep(time_break)
    log.info(f"{EMAIL} | click | send submit {amount_usdt} USDT | DOP")

    driver.find_element('xpath',
                        '/html/body/div[3]/div/div/div[2]/div[3]/button[2]').click()  # step 6 - send confirm
    time.sleep(timeout)
    log.info(f"{EMAIL} | click | send confirm {amount_usdt} USDT | DOP")


    # ----------------------------------------------------------------------------------------------------------------- switch to window MM

    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(time_break)
    log.info(f"{EMAIL} | switch | to window MM")

    driver.find_element('xpath',
                        '//*[@id="app-content"]/div/div/div/div[9]/footer/button[2]').click()  # confirm-1 in MM step 6
    time.sleep(timeout)
    log.info(f"{EMAIL} | click | confirm-1 | MM")

    driver.find_element('xpath',
                        '//*[@id="app-content"]/div/div/div/div[10]/footer/button[2]').click()  # confirm-2 in MM step 6
    time.sleep(timeout)
    log.info(f"{EMAIL} | click | confirm-2 | MM")
    time.sleep(timeout * 2)

    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(timeout)
    log.info(f"{EMAIL} | switch | to window MM")
    time.sleep(timeout * 2)

    driver.find_element('xpath',
                        '//*[@id="app-content"]/div/div/div/div[3]/div[3]/footer/button[2]').click()  # confirm-3 in MM step 6
    time.sleep(timeout * 2)
    log.info(f"{EMAIL} | click | confirm-3 | MM")

    # -----------------------------------------------------------------------switch to window DOP

    driver.switch_to.window(driver.window_handles[2])
    time.sleep(time_break)
    log.info(f"{EMAIL} | switch | to window DOP")

    save_progress(EMAIL, 6)

    driver.find_element('xpath',
                        '/html/body/div[3]/div/div/div/div[2]/button[1]').click()  # step 6 - close
    time.sleep(time_break)
    log.info(f"{EMAIL} | click | close | DOP")

    driver.find_element('xpath',
                        '/html/body/div[3]/div/div/div/div[2]/button').click()  # step 6 - ok
    time.sleep(time_break)
    log.info(f"{EMAIL} | click | okey | DOP")



def step7(driver, EMAIL):
    driver.find_element('xpath',
                        '//*[@id="left-tabs-example-tabpane-earn"]/section/div[3]/div[7]/div[2]/button').click()  # step 7 - get started
    time.sleep(time_break)
    log.info(f"{EMAIL} | click | get started | DOP")

    driver.find_element('xpath',
                        '//*[@id="left-tabs-example-tabpane-withdraw"]/section/section/form/div[2]/div/img').click()  # step 7 - select token
    time.sleep(time_break)
    log.info(f"{EMAIL} | click | select token | DOP")

    driver.find_element('xpath',
                        '/html/body/div[3]/div/div/div[2]/div[2]/div[1]').click()  # step 7 - select token USDT
    time.sleep(time_break)
    log.info(f"{EMAIL} | click | select token USDT | DOP")

    amount_usdt = random.randint(1, 3000)
    driver.find_element('xpath',
                        '//*[@id="left-tabs-example-tabpane-withdraw"]/section/section/form/div[3]/input').send_keys(
        amount_usdt)  # input amount
    time.sleep(time_break)
    log.info(f"{EMAIL} | input | {amount_usdt} | DOP")

    driver.find_element('xpath',
                        '//*[@id="left-tabs-example-tabpane-withdraw"]/section/section/form/div[4]/input').send_keys(
        dop_password)  # input password
    log.success(dop_password)
    time.sleep(time_break)
    log.info(f"{EMAIL} | input | {dop_password} | DOP")

    driver.find_element('xpath',
                        '//*[@id="left-tabs-example-tabpane-withdraw"]/section/section/form/button').click()  # step 7 - decrypt
    time.sleep(time_break)
    log.info(f"{EMAIL} | click | decrypt {amount_usdt} USDT | DOP")

    driver.find_element('xpath',
                        '/html/body/div[3]/div/div/div[2]/div[2]/button[2]').click()  # step 7 - decrypt confirm
    time.sleep(time_break * 3)
    log.info(f"{EMAIL} | click | decrypt confirm {amount_usdt} USDT | DOP")

    # ----------------------------------------------------------------------------------------------------------------- switch to window MM

    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(time_break)
    log.info(f"{EMAIL} | switch | to window MM")

    driver.find_element('xpath',
                        '//*[@id="app-content"]/div/div/div/div[3]/div[3]/footer/button[2]').click()  # confirm-1 in MM step 7
    time.sleep(timeout)
    log.info(f"{EMAIL} | click | confirm | MM")

    # ------------------------------------------------------------------------------------------------------- switch to window DOP

    driver.switch_to.window(driver.window_handles[2])
    time.sleep(timeout*3)
    log.info(f"{EMAIL} | switch | to window DOP")

    driver.find_element('xpath',
                        '/html/body/div[3]/div/div/div/div[2]/button[1]').click()  # step 7 - close
    time.sleep(time_break)
    log.info(f"{EMAIL} | click | close | DOP")

    driver.find_element('xpath',
                        '/html/body/div[3]/div/div/div/button').click()  # step 7 - done
    time.sleep(time_break)
    log.info(f"{EMAIL} | click | done | DOP")




def refresh(driver):
    driver.switch_to.window(driver.window_handles[2])
    time.sleep(time_break)
    log.info(f" REFRESH | switch | to window DOP")
    driver.back()
    time.sleep(time_break*3)
    driver.forward()


def finish(driver, EMAIL, dop_mnemonic, mm_mnemonic, twitter_lodin, question):
    if question:
        log.debug('Save account data as a successfully passed testnet? (yes - 1/no - 0):\n')
        passing = int(input())
        if passing:

            save_data_passed_testnet(EMAIL, dop_mnemonic, mm_mnemonic, twitter_lodin)
            log.success(f'{EMAIL} | testnet passed successfully')
            time.sleep(time_break)
            print()
            print()

            copy_ref_code(driver, EMAIL)

    driver.quit()


def run_step(step, driver, EMAIL, dop_mnemonic, mm_mnemonic, twitter_login, question, attempt_number=0):
    global count_attempt
    try:
        step(driver, EMAIL)
    except WebDriverException:
        if attempt_number < count_attempt:
            time.sleep(time_break*2)
            print()
            log.info(f"{step.__name__} | refresh the page and repeat {step.__name__}")
            refresh(driver)
            time.sleep(time_break)
            attempt_number += 1
            run_step(step, driver, EMAIL, dop_mnemonic, mm_mnemonic, twitter_login, question, attempt_number)
        else:
            log.error(f"{step.__name__} | the limit of attempts has been exceeded")
            log.debug("Do you want to retry this step? (yes - 1/no - 0):\n")
            response = int(input())
            if response:
                attempt_number = 0
                run_step(step, driver, EMAIL, dop_mnemonic, mm_mnemonic, twitter_login, question, attempt_number)
            else:
                step_progress = int(str(step.__name__)[-1])
                save_progress(EMAIL, step_progress)
                log.info(f"SKIPP | {step.__name__} | moving to the next step.")
                print()


def run_testnet(EMAIL, mm_mnemonic, dop_mnemonic, twitter_login, cookies, step_progress):
    step_progress = int(step_progress)
    question = False

    decoded_cookies = encrypto_cookies(cookies)
    cookies_dict = json.loads(decoded_cookies)
    ua = UserAgent()
    random_user_agent = ua.random
    chrome_options = Options()
    chrome_options.add_argument(f'user-agent={random_user_agent}')
    chrome_options.add_extension('MetaMask_Chrome.crx')
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.get("https://twitter.com")

    for cookie in cookies_dict:
        if 'sameSite' in cookie:
            if cookie['sameSite'] not in ["Strict", "Lax", "None"]:
                cookie['sameSite'] = "Lax"
        driver.add_cookie(cookie)

    driver.refresh()
    time.sleep(time_break)
    driver.implicitly_wait(10)
    time.sleep(time_break)
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(time_break)

    try:
        main_step(driver, EMAIL, mm_mnemonic, dop_mnemonic)
        log.info(f'{EMAIL} | current start step | {step_progress}')

        if step_progress < 1:
            run_step(step1, driver, EMAIL, dop_mnemonic, mm_mnemonic, twitter_login, question)
            question = True
            step_progress = update_step_progress(EMAIL)
            print()

        if step_progress < 2:
            run_step(step2, driver, EMAIL, dop_mnemonic, mm_mnemonic, twitter_login, question)
            time.sleep(time_break * 2)
            step_progress = update_step_progress(EMAIL)
            print()

        if step_progress < 3:
            run_step(step3, driver, EMAIL, dop_mnemonic, mm_mnemonic, twitter_login, question)
            time.sleep(time_break * 2)
            step_progress = update_step_progress(EMAIL)
            print()

        if step_progress < 4:
            run_step(step4, driver, EMAIL, dop_mnemonic, mm_mnemonic, twitter_login, question)
            time.sleep(time_break * 2)
            step_progress = update_step_progress(EMAIL)
            print()

        if step_progress < 5:
            run_step(step5, driver, EMAIL, dop_mnemonic, mm_mnemonic, twitter_login, question)
            time.sleep(time_break * 2)
            step_progress = update_step_progress(EMAIL)
            print()

        if step_progress < 6:
            run_step(step6, driver, EMAIL, dop_mnemonic, mm_mnemonic, twitter_login, question)
            time.sleep(time_break * 2)
            step_progress = update_step_progress(EMAIL)
            print()

        if step_progress < 7:
            run_step(step7, driver, EMAIL, dop_mnemonic, mm_mnemonic, twitter_login, question)
            time.sleep(time_break * 2)
            step_progress = update_step_progress(EMAIL)
            print()

        if step_progress == 7:
            copy_ref_code(driver, EMAIL)
            save_data_passed_testnet(EMAIL, dop_mnemonic, mm_mnemonic, twitter_login)
            log.success(f'{EMAIL} | testnet passed successfully')

    except Exception as err:
        log.error(f"run testnet | {err}")
        input()
        finish(driver, EMAIL, dop_mnemonic, mm_mnemonic, twitter_login, question)
