import random
import string
import time
import zipfile
import os
from datetime import datetime

import pyperclip
from fake_useragent import UserAgent
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


# ref = 'FDtPJDz'

log.add("logger.log", format="{time:YYYY-MM-DD | HH:mm:ss.SSS} | {level} \t| {function}:{line} - {message}")


def choose_random(file_name):
    try:
        with open(file_name, 'r') as file:
            codes = [code.strip() for code in file.readlines()]
        return random.choice(codes) if codes else ''
    except FileNotFoundError:
        return ''


def save_data_account(secret_key_dop, seed_prase_dop, password_dop, email_address, mnemonic_mm, password_mm):

    file_path = 'success_reg_accounts.txt'
    data_line = f"{secret_key_dop}:{seed_prase_dop}:{password_dop}:{email_address}:{mnemonic_mm}:{password_mm}:0\n"

    with open(file_path, 'a') as file:
        file.write(data_line)
    log.info(f"{email_address} | data save in {file_path}")


def save_data_ref_code(email, ref_code, count_referrals=0):

    file_path = 'ref.txt'
    data_line = f"{email}:{ref_code}:{count_referrals}\n"

    with open(file_path, 'a') as file:
        file.write(data_line)
    log.info(f"{email} | data save in {file_path}")


def is_account_registered_dop(email_address):
    with open('success_reg_accounts.txt', 'r') as file:
        for line in file:
            if email_address in line.split(':')[3]:
                return False
    return True


def generate_password(length=8):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(length))
    return password


def select_referral_code(filename="ref.txt"):

    with open(filename, 'r') as file:
        lines = file.readlines()

    referrals = [line.strip().split(':') for line in lines]

    more_than_0_less_than_3 = [ref for ref in referrals if ref[2].isdigit() and 0 < int(ref[2]) < 3]
    equal_to_0 = [ref for ref in referrals if ref[2].isdigit() and int(ref[2]) == 0]

    if more_than_0_less_than_3:
        selected_referral = random.choice(more_than_0_less_than_3)[1]
    elif equal_to_0:
        selected_referral = random.choice(equal_to_0)[1]
    else:
        selected_referral = random.choice(referrals)[1]

    log.info(f"select | ref code {selected_referral} | random")
    return selected_referral

def update_referral_data(selected_referral, filename='ref.txt'):
    with open(filename, 'r') as file:
        lines = file.readlines()

    referrals = [line.strip().split(':') for line in lines]

    for ref in referrals:
        if ref[1] == selected_referral:
            ref[2] = str(int(ref[2]) + 1)
            break

    updated_lines = [':'.join(ref) for ref in referrals]
    with open(filename, 'w') as file:
        file.write('\n'.join(updated_lines))

    log.info(f'{selected_referral} | update | referral +1')



def auto_reg(EMAIL, MNEMONIC):

    ua = UserAgent()

    # Вибір випадкових позицій
    random_user_agent = ua.random

    MNEMONIC = MNEMONIC.split()
    dop_password = generate_password()
    mm_password = generate_password()

    chrome_options = Options()
    chrome_options.add_argument(f'user-agent={random_user_agent}')
    chrome_options.add_extension('MetaMask_Chrome.crx')
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    time.sleep(time_break)
    ref = select_referral_code('ref.txt')
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

        driver.switch_to.window(driver.window_handles[0])
        time.sleep(time_break)
        log.info(f"{EMAIL} | switch | to window DOP")


        driver.find_element('xpath',
                            '//*[@id="root"]/section[2]/div/div[2]/form/div[1]/div/label').click()  # I understand


        time.sleep(time_break)
        log.info(f"{EMAIL} | click | I understand | DOP)")

        driver.find_element('xpath',
                            '//*[@id="root"]/section[2]/div/div[2]/form/div[2]/input').send_keys(
            EMAIL)  # enter email twice
        time.sleep(time_break)
        log.info(f"{EMAIL} | input | email | DOP")

        driver.find_element('xpath', '//*[@id="root"]/section[2]/div/div[2]/form/button').click() # continue
        time.sleep(time_break)
        log.info(f"{EMAIL} | click | continue | DOP")


        driver.find_element('xpath', '//*[@id="root"]/section[2]/div/div[2]/div[1]/a/button').click() # create new wallet
        time.sleep(time_break)
        log.info(f"{EMAIL} | click | create new wallet | DOP")

        driver.find_element('xpath',
                            '//*[@id="root"]/section[2]/div/div/form/div/div[1]/input').send_keys(
            dop_password)  # enter password
        time.sleep(time_break)

        driver.find_element('xpath',
                            '//*[@id="root"]/section[2]/div/div/form/div/div[2]/input').send_keys(
            dop_password)  # enter password twice
        time.sleep(time_break)
        log.info(f"{EMAIL} | input | 2 password | DOP")

        driver.find_element('xpath',
                            '//*[@id="root"]/section[2]/div/div/form/div/button').click()  # I confirm
        time.sleep(time_break*2)
        log.info(f"{EMAIL} | click | I confirm | DOP")

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(time_break * 2)
        log.info(f"{EMAIL} | scroll | DOP")

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

        driver.find_element('xpath',
                            '/html/body/div[3]/div/div/div/div[2]/button').click()  # done
        time.sleep(time_break)
        log.info(f"{EMAIL} | click | done | DOP")

        save_data_account(secret_key, ' '.join(seed_phrase), dop_password, EMAIL, ' '.join(MNEMONIC), mm_password)
        time.sleep(time_break)


        driver.find_element('xpath',
                            '//*[@id="root"]/section[2]/div/div/form/div/div/input').send_keys(
            dop_password)  # input password login
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

        log.info(f"counter of open windows | {len(driver.window_handles)}")

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

        # --------------------------------------------------------------------------------------------------------------------- switch to window DOP

        driver.switch_to.window(driver.window_handles[0])
        time.sleep(time_break)
        log.info(f"{EMAIL} | switch | to window DOP")


        update_referral_data(selected_referral=ref)

        log.success('Created account in DOP successfully!')
        time.sleep(time_break)
        print()
        print()

        return True

    except Exception as e:
        log.error(f'{EMAIL}| Failed Registered | {str(e)}')
    finally:
        driver.quit()


