import random
import string
import time
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from config import *
from loguru import logger as log
from selenium.webdriver.common.keys import Keys


log.add("logger.log", format="{time:YYYY-MM-DD | HH:mm:ss.SSS} | {level} \t| {function}:{line} - {message}")


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


def twitter_not_use(lodin_twitter):
    with open('passed_testnet.txt', 'r') as file:
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



def testnet(EMAIL, mm_mnemonic, dop_mnemonic, twitter_lodin, twiter_password):

    ua = UserAgent()

    # Вибір випадкових позицій
    random_user_agent = ua.random

    mm_mnemonic = mm_mnemonic.split()

    dop_password = generate_password()
    mm_password = generate_password()


    chrome_options = Options()
    chrome_options.add_argument(f'user-agent={random_user_agent}')
    chrome_options.add_extension('MetaMask_Chrome.crx')
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    driver.get(url_testnet_dop)

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

        driver.switch_to.window(driver.window_handles[0])
        time.sleep(time_break)
        log.info(f"{EMAIL} | switch | to window DOP")

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


        #----------------------------------------------------------------------------------------------------------------- switch to window MM

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


        scroll_height = 10 * 37.7952755906

        # Виконуємо скролінг на вказану висоту
        driver.execute_script(f"window.scrollBy(0, {scroll_height});")
        time.sleep(time_break)
        log.info(f"{EMAIL} | scroll на {scroll_height} pixel | DOP")

        log.success(dop_password)



        driver.find_element('xpath',
                           '//*[@id="left-tabs-example-tabpane-earn"]/section/div[3]/div[1]/div[2]/div/div/button').click()     # auth Twitter step 1
        time.sleep(time_break)
        log.info(f"{EMAIL} | click | auth twitter step 1 | DOP")

        log.info(f"counter of open windows | {len(driver.window_handles)}")

# ------------------------------------------------------------------------------------------------------- switch to window TWITTER
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(time_break)
        log.info(f"{EMAIL} | switch | to window TWITTER")

        driver.find_element('xpath',
                            '//*[@id="username_or_email"]').send_keys(
            twitter_lodin)  # enter  login TWITTER
        time.sleep(time_break)
        log.info(f"{EMAIL} | input | login | TWITTER")

        driver.find_element('xpath',
                            '//*[@id="password"]').send_keys(
            twiter_password)  # enter password TWITTER
        time.sleep(time_break)
        log.info(f"{EMAIL} | input | password | TWITTER")

        driver.find_element('xpath',
                            '//*[@id="allow"]').click()  # submit Twitter
        time.sleep(time_break)
        log.info(f"{EMAIL} | click | submit | TWITTER")

        log.debug('Press Enter to continue...')
        input()
#
#         driver.find_element('xpath',
#                             '//*[@id="allow"]').click()  # confirm auth Twitter
#         time.sleep(time_break)
#         log.info(f"{EMAIL} | click | confirm auth Twitter | TWITTER")
#
#         # ------------------------------------------------------------------------------------------------------- switch to window DOP
#
#         driver.switch_to.window(driver.window_handles[0])
#         time.sleep(time_break)
#         log.info(f"{EMAIL} | switch | to window DOP")
#
#
#         driver.find_element('xpath',
#                                 '//*[@id="left-tabs-example-tabpane-earn"]/section/div[3]/div[1]/div[2]/div/button[2]').click()  # follow dop_org
#         time.sleep(time_break)
#         log.info(f"{EMAIL} | click | follow dop_org | DOP")
#
#
#         # ------------------------------------------------------------------------------------------------------- switch to window TWITTER
#
#         # driver.switch_to.window(driver.window_handles[-1])
#         # time.sleep(time_break)
#         # log.info(f"{EMAIL} | switch | to window TWITTER")
#         #
#         # driver.find_element('xpath',
#         #                     '//*[@id="allow"]').click()  # auth Twitter step 3
#         # time.sleep(time_break)
#         # log.info(f"{EMAIL} | click | auth twitter step 3 | Twitter")
#
#
#         # ------------------------------------------------------------------------------------------------------- switch to window TWITTER
#
#         driver.switch_to.window(driver.window_handles[-1])
#         time.sleep(time_break)
#         log.info(f"{EMAIL} | switch | to window TWITTER")
#
#         driver.find_element('xpath',
#                             '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[3]/div[1]/div').click()  # follow Twitter
#         time.sleep(time_break)
#         log.info(f"{EMAIL} | click | follow dop_org | Twitter")
#
#
#         # ------------------------------------------------------------------------------------------------------- switch to window DOP
#
#         driver.switch_to.window(driver.window_handles[0])
#         time.sleep(time_break)
#         log.info(f"{EMAIL} | switch | to window DOP")
#
#         driver.find_element('xpath',
#                             '/html/body/div[3]/div/div/div/div[2]/div/label"]').click()  # I agree checkbox
#         time.sleep(time_break)
#         log.info(f"{EMAIL} | click | I agree checkbox  | DOP")
#
#         driver.find_element('xpath',
#                             '/html/body/div[3]/div/div/div/button').click()  # Done checkbox
#         time.sleep(time_break)
#         log.info(f"{EMAIL} | click | done checkbox | DOP")

        # driver.find_element('xpath',
        #                     '//*[@id="left-tabs-example-tabpane-earn"]/section/div[3]/div[2]/div[2]/button').click()  # claim step 2
        # time.sleep(timeout)
        # log.info(f"{EMAIL} | click | claim step 2 | DOP")
        #
        # driver.find_element('xpath',
        #                     '//*[@id="left-tabs-example-tabpane-earn"]/section/div[3]/div[3]/div[2]/button').click()  # claim step 3
        # time.sleep(timeout)
        # log.info(f"{EMAIL} | click | claim step 3 | DOP")
        #
        # # ----------------------------------------------------------------------------------------------------------------- switch to window MM
        #
        # driver.switch_to.window(driver.window_handles[-1])
        # time.sleep(time_break)
        # log.info(f"{EMAIL} | switch | to window MM")
        #
        # driver.find_element('xpath',
        #                     '//*[@id="app-content"]/div/div/div/div[3]/div[3]/footer/button[2]').click()  # confirm in MM
        # time.sleep(time_break*5)
        # log.info(f"{EMAIL} | click | confirm step 3 | MM")
        #
        # # ------------------------------------------------------------------------------------------------------- switch to window DOP
        #
        # driver.switch_to.window(driver.window_handles[0])
        # time.sleep(time_break)
        # log.info(f"{EMAIL} | switch | to window DOP")
        #
        # driver.find_element('xpath',
        #                     '//*[@id="left-tabs-example-tabpane-earn"]/section/div[3]/div[4]/div[2]/button').click()  # claim step 4
        # time.sleep(timeout)
        # log.info(f"{EMAIL} | click | claim step 4 | DOP")
        #
        # # ----------------------------------------------------------------------------------------------------------------- switch to window MM
        #
        # driver.switch_to.window(driver.window_handles[-1])
        # time.sleep(time_break)
        # log.info(f"{EMAIL} | switch | to window MM")
        #
        # driver.find_element('xpath',
        #                     '//*[@id="app-content"]/div/div/div/div[3]/div[3]/footer/button[2]').click()  # confirm in MM step 4
        # time.sleep(time_break * 5)
        # log.info(f"{EMAIL} | click | confirm step 4 | MM")
        #
        # # ------------------------------------------------------------------------------------------------------- switch to window DOP
        #
        # driver.switch_to.window(driver.window_handles[0])
        # time.sleep(time_break)
        # log.info(f"{EMAIL} | switch | to window DOP")

        # driver.find_element('xpath',
        #                     '//*[@id="left-tabs-example-tabpane-earn"]/section/div[3]/div[5]/div[2]/button').click()  # step 5
        # time.sleep(time_break)
        # log.info(f"{EMAIL} | click | step 5 | DOP")
        #
        #
        # driver.find_element('xpath',
        #                     '//*[@id="left-tabs-example-tabpane-deposit"]/section/section/form/div[1]/div[2]/div/img').click()  # step 5 - choice coin
        # time.sleep(time_break)
        # log.info(f"{EMAIL} | click | step 5 - select coin | DOP")
        #
        # #---
        #
        # driver.find_element('xpath',
        #                     '/html/body/div[3]/div/div/div[2]/div[2]/div[1]').click()  # step 5 - choice USTD
        # time.sleep(time_break)
        # log.info(f"{EMAIL} | click | step 5 - select USTD | DOP")
        #
        #
        # amount_usdt = random.randint(7000, 10000)
        # log.info(amount_usdt)
        # driver.find_element('xpath',
        #                     '//*[@id="left-tabs-example-tabpane-deposit"]/section/section/form/div[2]/input').send_keys(
        #     amount_usdt)
        # time.sleep(time_break)
        #
        # driver.find_element('xpath',
        #                     '//*[@id="left-tabs-example-tabpane-deposit"]/section/section/form/button').click()  # step 5 - encrypt
        # time.sleep(time_break)
        # log.info(f"{EMAIL} | click | step 5 - encrypt {amount_usdt} usdt | DOP")
        #
        # driver.find_element('xpath',
        #                     '/html/body/div[3]/div/div/div[2]/div[3]/button[2]').click()  # step 5 - confirm
        # time.sleep(time_break)
        # log.info(f"{EMAIL} | click | step 5 - confirm {amount_usdt} usdt | DOP")
        #
        # # ----------------------------------------------------------------------------------------------------------------- switch to window MM
        #
        # driver.switch_to.window(driver.window_handles[-1])
        # time.sleep(timeout)
        # log.info(f"{EMAIL} | switch | to window MM")
        #
        #
        # driver.find_element('xpath',
        #                     '//*[@id="app-content"]/div/div/div/div[9]/footer/button[2]').click()  # confirm-1 in MM step 5
        # time.sleep(timeout)         #//*[@id="app-content"]/div/div/div/div[3]/div[3]/footer/button[2]
        #
        # log.info(f"{EMAIL} | click | confirm-1 step 5 | MM")
        #
        #
        # driver.find_element('xpath',
        #                     '//*[@id="app-content"]/div/div/div/div[10]/footer/button[2]').click()  # confirm-2 in MM step 5
        # time.sleep(timeout)
        # log.info(f"{EMAIL} | click | confirm-2 step 5 | MM")
        #
        # log.debug('Press Enter to continue...')
        # input()
        #
        #
        # driver.find_element('xpath',
        #                     '//*[@id="app-content"]/div/div/div/div[3]/div[3]/footer/button[2]').click()  # confirm-3 in MM step 5
        # time.sleep(timeout * 2)
        # log.info(f"{EMAIL} | click | confirm-3 step 5 | MM")
        #
        # log.debug('Press Enter to continue...')
        # input()
        #
        # # ------------------------------------------------------------------------------------------------------- switch to window DOP
        #
        # driver.switch_to.window(driver.window_handles[0])
        # time.sleep(time_break)
        # log.info(f"{EMAIL} | switch | to window DOP")
        #
        # driver.find_element('xpath',
        #                     '/html/body/div[3]/div/div/div/div[2]/button[1]').click()  # step 5 - close
        # time.sleep(timeout)
        # log.info(f"{EMAIL} | click | step 5 - close | DOP")
        #
        # driver.find_element('xpath',
        #                     '/html/body/div[3]/div/div/div/div[2]/button[1]').click()  # step 5 - okey
        # time.sleep(timeout)
        # log.info(f"{EMAIL} | click | step 5 - okey | DOP")

        amount_usdt = 100

        # driver.find_element('xpath',
        #                     '//*[@id="left-tabs-example-tabpane-earn"]/section/div[3]/div[6]/div[2]/button').click()  # step 6 - get started
        # time.sleep(time_break)
        # log.info(f"{EMAIL} | click | step 6 - get started | DOP")
        #
        # dop_test_adress = '0x130c318bef3a60f05541955003b2baa1d691335f'
        #
        # driver.find_element('xpath',
        #                     '//*[@id="left-tabs-example-tabpane-transfer"]/section/section/form/div[1]/input').send_keys(
        #     dop_test_adress)
        # time.sleep(time_break)
        # log.info(f"{EMAIL} | input | {dop_test_adress} | DOP")
        #
        #
        # driver.find_element('xpath',
        #                     '//*[@id="left-tabs-example-tabpane-transfer"]/section/section/form/div[2]/div').click()  # step 6 - select token
        # time.sleep(time_break)
        # log.info(f"{EMAIL} | click | step 6 - select token | DOP")
        #
        # driver.find_element('xpath',
        #                     '/html/body/div[3]/div/div/div[2]/div[2]/div[1]').click()  # step 6 - select token USDT
        # time.sleep(time_break)
        # log.info(f"{EMAIL} | click | step 6 - select token USDT | DOP")
        #
        # amount_usdt_2 = random.randint(10, amount_usdt // 2)
        # driver.find_element('xpath',
        #                     '//*[@id="left-tabs-example-tabpane-transfer"]/section/section/form/div[3]/input').send_keys(
        #     amount_usdt_2)  #
        # time.sleep(time_break)
        #
        # driver.find_element('xpath',
        #                     '//*[@id="left-tabs-example-tabpane-transfer"]/section/section/form/button').click()  # step 6 - send submit
        # time.sleep(time_break)
        # log.info(f"{EMAIL} | click | step 6 - send submit {amount_usdt_2} USDT | DOP")
        #
        # log.debug('Press Enter to continue...')
        # input()
        #
        #
        # driver.find_element('xpath',
        #                     '//*[@id="left-tabs-example-tabpane-transfer"]/section/section/form/button').click()  # step 6 - send confirm
        # time.sleep(timeout)
        # log.info(f"{EMAIL} | click | step 6 - send confirm {amount_usdt_2} USDT | DOP")
        #
        #
        #
        # # ----------------------------------------------------------------------------------------------------------------- switch to window MM
        #
        # driver.switch_to.window(driver.window_handles[-1])
        # time.sleep(time_break)
        # log.info(f"{EMAIL} | switch | to window MM")
        #
        # driver.find_element('xpath',
        #                     '//*[@id="app-content"]/div/div/div/div[9]/footer/button[2]').click()  # confirm-1 in MM step 5
        # time.sleep(timeout)
        # log.info(f"{EMAIL} | click | confirm-1 step 5 | MM")
        #
        # driver.find_element('xpath',
        #                     '//*[@id="app-content"]/div/div/div/div[10]/footer/button[2]').click()  # confirm-2 in MM step 5
        # time.sleep(timeout * 2)
        # log.info(f"{EMAIL} | click | confirm-2 step 5 | MM")
        #
        # driver.find_element('xpath',
        #                     '//*[@id="app-content"]/div/div/div/div[3]/div[3]/footer/button[2]').click()  # confirm-3 in MM step 5
        # time.sleep(timeout * 2)
        # log.info(f"{EMAIL} | click | confirm-3 step 5 | MM")
        #
        # # ------------------------------------------------------------------------------------------------------- switch to window DOP
        #
        # driver.switch_to.window(driver.window_handles[0])
        # time.sleep(time_break)
        # log.info(f"{EMAIL} | switch | to window DOP")
        #
        # driver.find_element('xpath',
        #                     '/html/body/div[3]/div/div/div/div[2]/button[1]').click()  # step 6 - close
        # time.sleep(time_break)
        # log.info(f"{EMAIL} | click | step 6 - close | DOP")
        #
        # driver.find_element('xpath',
        #                     '/html/body/div[3]/div/div/div/div[2]/button').click()  # step 6 - ok
        # time.sleep(time_break)
        # log.info(f"{EMAIL} | click | step 6 - ok | DOP")
        #
        # driver.find_element('xpath',
        #                     '//*[@id="left-tabs-example-tabpane-earn"]/section/div[3]/div[7]/div[2]/button').click()  # step 7 - get started
        # time.sleep(time_break)
        # log.info(f"{EMAIL} | click | step 7 - get started | DOP")
        #
        # driver.find_element('xpath',
        #                     '//*[@id="left-tabs-example-tabpane-withdraw"]/section/section/form/div[2]/div/img').click()  # step 7 - select token
        # time.sleep(time_break)
        # log.info(f"{EMAIL} | click | step 7 - select token | DOP")
        #
        # driver.find_element('xpath',
        #                     '/html/body/div[3]/div/div/div[2]/div[2]/div[1]').click()  # step 7 - select token USDT
        # time.sleep(time_break)
        # log.info(f"{EMAIL} | click | step 7 - select token USDT | DOP")
        #
        # amount_usdt_3 = random.randint(100, amount_usdt-amount_usdt_2)
        # driver.find_element('xpath',
        #                     '//*[@id="left-tabs-example-tabpane-withdraw"]/section/section/form/div[3]/input').send_keys(
        #     amount_usdt_3)  # input amount
        # time.sleep(time_break)
        #
        # driver.find_element('xpath',
        #                     '//*[@id="left-tabs-example-tabpane-withdraw"]/section/section/form/div[4]/input').send_keys(
        #     dop_password)  # input password
        # time.sleep(time_break)
        #
        # driver.find_element('xpath',
        #                     '//*[@id="left-tabs-example-tabpane-withdraw"]/section/section/form/button').click()  # step 7 - decrypt
        # time.sleep(time_break)
        # log.info(f"{EMAIL} | click | step 7 - decrypt {amount_usdt_3} USDT | DOP")
        #
        # driver.find_element('xpath',
        #                     '//*[@id="left-tabs-example-tabpane-withdraw"]/section/section/form/button').click()  # step 7 - decrypt confirm
        # time.sleep(time_break*3)
        # log.info(f"{EMAIL} | click | decrypt confirm {amount_usdt_3} USDT | DOP")
        #
        # # ----------------------------------------------------------------------------------------------------------------- switch to window MM
        #
        # driver.switch_to.window(driver.window_handles[-1])
        # time.sleep(time_break)
        # log.info(f"{EMAIL} | switch | to window MM")
        #
        # driver.find_element('xpath',
        #                     '//*[@id="app-content"]/div/div/div/div[3]/div[3]/footer/button[2]').click()  # confirm-1 in MM step 7
        # time.sleep(timeout)
        # log.info(f"{EMAIL} | click | confirm-1 step 7 | MM")
        #
        # # ------------------------------------------------------------------------------------------------------- switch to window DOP
        #
        # driver.switch_to.window(driver.window_handles[0])
        # time.sleep(time_break)
        # log.info(f"{EMAIL} | switch | to window DOP")
        #
        # driver.find_element('xpath',
        #                     '/html/body/div[3]/div/div/div/div[2]/button[1]').click()  # step 7 - close
        # time.sleep(time_break)
        # log.info(f"{EMAIL} | click | step 7 - close | DOP")
        #
        # driver.find_element('xpath',
        #                     '/html/body/div[3]/div/div/div/button').click()  # step 7 - done
        # time.sleep(time_break)
        # log.info(f"{EMAIL} | click | step 7 - done | DOP")

        save_data_passed_testnet(email, dop_mnemonic, mm_mnemonic, twitter_lodin)
        log.success(f'{email} | testnet passed successfully')

        return True

    except Exception as e:
        log.error(f'{EMAIL}| Failed Registered | {str(e)}')
    finally:
        driver.quit()



email = 'mverituvid@gmail.com'
dop_mnemonic = 'tool bleak live unique skate profit elephant cup legend merit learn extend'
mm_mnemonic = 'catch sting delay book torch legal purity copy swallow kid coach soft'


with open(file='twitter_data.txt', mode='r', encoding='utf-8-sig') as file:
    twitter_accounts_list = [row.strip() for row in file]

for account_data in twitter_accounts_list:
    twitter_lodin, twiter_password = account_data.split(':')
    if testnet(email, mm_mnemonic, dop_mnemonic, twitter_lodin, twiter_password):
        log.success("step with twitter passes successfully")
        log.info("go to the next account")
        time.sleep(timeout)
        log.debug('Press Enter to continue...')
        input()
        break
    else:
        log.error("account twitter frozen")
        log.info("go to the next twitter account")
        time.sleep(timeout)
        continue