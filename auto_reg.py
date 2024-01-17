import random
import string
import time
import zipfile
import os
from datetime import datetime
from seleniumwire import webdriver
import pyperclip
from fake_useragent import UserAgent
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

log.add("logger.log", format="{time:YYYY-MM-DD | HH:mm:ss.SSS} | {level} \t| {line}:{function} | {message}")


def choose_random(file_name):
    try:
        with open(file_name, 'r') as file:
            codes = [code.strip() for code in file.readlines()]
        return random.choice(codes) if codes else ''
    except FileNotFoundError:
        return ''


def save_data_account(secret_key_dop, seed_prase_dop, password_dop, email_address, mnemonic_mm, password_mm, proxy):
    file_path = 'data/success_reg_accounts.txt'
    data_line = f"{secret_key_dop}:{seed_prase_dop}:{password_dop}:{email_address}:{mnemonic_mm}:{password_mm}:{proxy}:0\n"

    with open(file_path, 'a') as file:
        file.write(data_line)
    log.info(f"{email_address} | data save in {file_path}")


def save_data_ref_code(email, ref_code, count_referrals=0):
    file_path = 'data/ref.txt'
    data_line = f"{email}:{ref_code}:{count_referrals}\n"

    with open(file_path, 'a') as file:
        file.write(data_line)
    log.info(f"{email} | data save in {file_path}")


def is_account_registered_dop(email_address):
    with open('data/success_reg_accounts.txt', 'r') as file:
        for line in file:
            if email_address in line.split(':')[3]:
                return False
    return True


def generate_password(length=8):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(length))
    return password


def select_referral_code(filename="data/ref.txt"):
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


def update_referral_data(selected_referral, filename='data/ref.txt'):
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


def proxy_not_use(proxy):
    with open('data/success_reg_accounts.txt', 'r') as file:
        for line in file:
            if proxy in line.split(':')[-2]:
                return False
    return True


def check_proxy(proxy):
    proxy_options = {
        "proxy": {
            "https": proxy
        }
    }

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    test_driver = webdriver.Chrome(options=chrome_options,
                                   seleniumwire_options=proxy_options)
    test_driver.get("https://2ip.ua/ua/")

    proxy = proxy.split("@")[1].split(":")[0]

    if "Визначити свою IP адресу | 2IP.ua" in test_driver.title:
        log.info(f"{proxy} | proxy is working")
        test_driver.quit()
        return True
    else:
        log.error(f"{proxy} | proxy is NOT working")
        test_driver.quit()
        return False


def auto_reg_and_step8(EMAIL, MNEMONIC, PROXY):
    ua = UserAgent()
    random_user_agent = ua.random

    MNEMONIC = MNEMONIC.split()
    dop_password = generate_password()
    mm_password = generate_password()

    # if not check_proxy(proxy):
    #     return None

    # time.sleep(time_break*2)
    # proxy_options = {
    #     "proxy": {
    #         "https": proxy
    #     }
    # }

    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument(f'user-agent={random_user_agent}')
    chrome_options.add_extension('MetaMask_Chrome.crx')
    driver = webdriver.Chrome(options=chrome_options)  # seleniumwire_options=proxy_options

    driver.maximize_window()

    time.sleep(time_break)
    proxy = PROXY.split("@")[1].split(":")[0]
    ref = select_referral_code('data/ref.txt')  # "FDtPJDz"
    driver.get(url_main_dop + ref)

    driver.implicitly_wait(10)
    time.sleep(time_break)

    driver.switch_to.window(driver.window_handles[1])
    time.sleep(timeout)
    driver.refresh()

    try:
        # METAMASK
        driver.find_element('xpath', agree_to_tos).click()
        time.sleep(time_break)
        log.info(f"{EMAIL} | click | agree to TOS | MM")

        driver.find_element('xpath', import_mm).click()
        time.sleep(time_break)
        log.info(f"{EMAIL} | click  | import | MM")

        driver.find_element('xpath', no_thanks).click()
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

        driver.find_element('xpath', confirm_mm).click()
        time.sleep(time_break)
        log.info(f"{EMAIL} | click | mnemonic confirm | MM")

        driver.find_element('xpath', input_password_mm).send_keys(mm_password)
        driver.find_element('xpath', input_password_twice_mm).send_keys(mm_password)
        time.sleep(time_break)
        log.info(f"{EMAIL} | input | password 2 | MM")

        driver.find_element('xpath', i_understand_mm).click()
        time.sleep(time_break // 2)
        log.info(f"{EMAIL} | click | I understand | MM")

        driver.find_element('xpath',
                            import_my_wallet).click()
        time.sleep(time_break * 2)
        log.info(f"{EMAIL} | click | import my wallet | MM)")

        driver.find_element('xpath', got_it).click()  # got it
        time.sleep(time_break // 2)
        log.info(f"{EMAIL} | click | got it MM")

        driver.find_element('xpath', next_page).click()
        time.sleep(time_break // 2)
        log.info(f"{EMAIL} | click | next page | MM")

        driver.find_element('xpath', done_mm).click()  # done
        time.sleep(time_break // 2)
        log.info(f"{EMAIL} | click | done | MM")

        driver.find_element('xpath', close_mm).click()  # close
        time.sleep(time_break // 2)
        log.info(f"{EMAIL} | click | close| MM")

        # DOP
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(time_break)
        log.info(f"{EMAIL} | switch | to window DOP")

        driver.find_element('xpath', i_understand_dop).click()

        time.sleep(time_break)
        log.info(f"{EMAIL} | click | I understand | DOP)")

        driver.find_element('xpath',
                            input_email).send_keys(EMAIL)
        time.sleep(time_break)
        log.info(f"{EMAIL} | input | email | DOP")

        driver.find_element('xpath', continue_dop).click()
        time.sleep(time_break)
        log.info(f"{EMAIL} | click | continue | DOP")

        driver.find_element('xpath', create_new_wallet).click()
        time.sleep(time_break)
        log.info(f"{EMAIL} | click | create new wallet | DOP")

        driver.find_element('xpath', input_password_dop).send_keys(dop_password)
        time.sleep(time_break)

        driver.find_element('xpath',input_password_twice_dop).send_keys(dop_password)
        time.sleep(time_break)
        log.info(f"{EMAIL} | input | 2 password | DOP")

        driver.find_element('xpath', confirm_dop).click()
        time.sleep(time_break * 2)
        log.info(f"{EMAIL} | click | I confirm | DOP")

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(time_break * 2)
        log.info(f"{EMAIL} | scroll | DOP")

        driver.find_element('xpath', copy_pharase).click()
        driver.implicitly_wait(time_break)
        time.sleep(time_break)
        log.info(f"{EMAIL} | click | copy phrase | DOP")

        driver.find_element('xpath', verify).click()
        driver.implicitly_wait(time_break)
        log.info(f"{EMAIL} | click | verify | DOP")
        time.sleep(time_break)

        copied_phrase = pyperclip.paste()
        seed_phrase = copied_phrase.split()

        log.info(f"{EMAIL} | click | verify phase 12 words | DOP")
        for word in seed_phrase:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//button[contains(., '{word}')]"))).click()
            time.sleep(time_break)

        driver.find_element('xpath',
                            verify_confirm).click()
        time.sleep(time_break)
        log.info(f"{EMAIL} | click | verify confirm | DOP")

        driver.find_element('xpath', verify_continue).click()
        time.sleep(time_break)
        log.info(f"{EMAIL} | click | verify continue | DOP")

        driver.find_element('xpath',
                            copy_secret_key).click()
        time.sleep(time_break)
        log.info(f"{EMAIL} | click | copy secret key | DOP")

        secret_key = pyperclip.paste()

        driver.find_element('xpath', done_dop).click()
        time.sleep(time_break)
        log.info(f"{EMAIL} | click | done | DOP")

        proxy = proxy.split(":")[0]
        save_data_account(secret_key, ' '.join(seed_phrase), dop_password, EMAIL, ' '.join(MNEMONIC), mm_password,
                          proxy)

        time.sleep(time_break)

        driver.find_element('xpath',
                            unlock_wallet).send_keys(dop_password)
        time.sleep(time_break)
        log.info(f"{EMAIL} | input | password | DOP")

        driver.find_element('xpath',
                            input_password_dop_unlock).click()
        time.sleep(time_break)
        log.info(f"{EMAIL} | click | password confirm | DOP")

        driver.find_element('xpath',start).click()
        time.sleep(time_break)
        log.info(f"{EMAIL} | click | start testnet | DOP")

        driver.find_element('xpath', connect_mm).click()
        time.sleep(time_break)
        log.info(f"{EMAIL} | click | connect MM | DOP")

        # METAMASK
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(time_break)
        log.info(f"{EMAIL} | switch | to window MM")

        driver.find_element('xpath',
                            confirm_in_mm).click()
        time.sleep(time_break)
        log.info(f"{EMAIL} | click | confirm | MM")

        driver.find_element('xpath',
                            connect_final).click()
        time.sleep(time_break)
        log.info(f"{EMAIL} | click | connect final | MM")

        driver.find_element('xpath',
                            switch_network_on_cepolia).click()
        time.sleep(time_break)
        log.info(f"{EMAIL} | click | switch network on cepolia | MM")

        # DOP
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
