import time
from logo import print_ALGONOMICS
from os.path import exists
from auto_reg import *
from config import *
from testnet import *
from creator_wallets import create_wallet
from loguru import logger as log


log.add("logger.log", format="{time:YYYY-MM-DD | HH:mm:ss.SSS} | {level} \t| {line}:{function} | {message}")

def main():

    if exists(path='data/accounts.txt'):
        with open(file='data/accounts.txt', mode='r', encoding='utf-8-sig') as file:
            accounts_list = [row.strip() for row in file]
    else:
        accounts_list = []

    if exists(path='data/passed_testnet.txt'):
        with open(file='data/passed_testnet.txt', mode='r', encoding='utf-8-sig') as file:
            accounts_list_passed_testnet = [row.strip() for row in file]
    else:
        accounts_list_passed_testnet = []

    if exists(path='data/twitter_data.txt'):
        with open(file='data/twitter_data.txt', mode='r', encoding='utf-8-sig') as file:
            accounts_twitter_list = [row.strip() for row in file]
    else:
        accounts_twitter_list = []

    if exists(path='data/success_reg_accounts.txt'):
        with open(file='data/success_reg_accounts.txt', mode='r', encoding='utf-8-sig') as file:
            success_reg_accounts = [row.strip() for row in file]
    else:
        success_reg_accounts = []

    if exists(path='data/ref.txt'):
        with open(file='data/ref.txt', mode='r', encoding='utf-8-sig') as file:
            ref_code_list = [row.strip() for row in file]
    else:
        ref_code_list = []

    if exists(path='data/proxy.txt'):
        with open(file='data/proxy.txt', mode='r', encoding='utf-8-sig') as file:
            proxy_list = [row.strip() for row in file]
    else:
        proxy_list = []

    print()
    print_ALGONOMICS("ALGONOMICS")
    time.sleep(2)
    print()

    log.success(f'Downloaded successfully {len(accounts_list)} accounts for registration | {len(accounts_twitter_list)} twitter accounts | {len(ref_code_list)} referral codes')
    log.success(
        f'Downloaded successfully {len(success_reg_accounts)} successfully registered accounts | {len(accounts_list_passed_testnet)} successfully passing testnet | {len(proxy_list)} proxy')
    log.info('💰 DONATION EVM ADDRESS: 0x4A080654795e526801954493BD0D712609d0ccEF')
    time.sleep(2)

    software_method = int(input('\n1. Account registration\n'
                                '2. Passing the testnet\n'
                                '3. Create the wallets\n'
                                'Make your choice:\n'))
    print()

    if software_method == 1:
        proxy_index = 0
        for account in accounts_list:
            email, mnemonic = account.split(':')
            if is_account_registered_dop(email):
                use_proxy = 0
                while use_proxy != 1:
                    for i in range(proxy_index, len(proxy_list)):
                        PROXY = proxy_list[i]

                        try:
                            auto_reg_and_step8(email, mnemonic, PROXY)
                            time.sleep(2)
                            log.info("go to the next account")
                            time.sleep(timeout // 2)
                            print()
                            use_proxy = 1
                            proxy_index = i + 1
                            break
                        except:
                            time.sleep(timeout)
                            continue

            else:
                log.info(f"{email} | already registered")
                log.info("go to the next account...")
                time.sleep(2)
                print()
                continue

            log.info("go to the next account..")

    elif software_method == 2:
        twitter_index = 0

        for dot_accounts in success_reg_accounts:
            _, dop_mnemonic, _, email, mm_mnemonic, _, ip, step_progress = dot_accounts.split(":")

            proxy = f"https://{login_proxy}:{password_proxy}@{ip}:{port_proxy}"

            if is_account_registered_2(email):
                if is_account_passed_testnet(email):
                    passed = 0
                    while passed != 1:
                        for i in range(twitter_index, len(accounts_twitter_list)):
                            twitter_account = accounts_twitter_list[i]
                            twitter_login, _, _, _, _, _, cookies = twitter_account.split(":")
                            if twitter_not_use(twitter_login):
                                log.info(f"{twitter_login} | current twitter account")

                                try:
                                    run_testnet(email, mm_mnemonic, dop_mnemonic, twitter_login, cookies, step_progress, proxy)
                                    time.sleep(2)
                                    log.info("go to the next account")
                                    time.sleep(timeout//2)
                                    print()
                                    passed = 1
                                    twitter_index = i + 1
                                    break
                                except Exception as err:
                                    log.error(f"{email} when passing {err}")
                                    log.info("repeat process of passing")
                                    time.sleep(timeout)
                                    continue

                            else:
                                log.info(f"{twitter_login} already used in DOP | or frozen")
                                log.info("go to the next twitter")
                                time.sleep(1)
                                print()
                                continue
                        else:
                            passed = 1
                            log.error("plase add new twitter accounts")
                else:
                    log.info(f"{email} already used in DOP")
                    log.info("go to the next account")
                    time.sleep(1)
                    print()
                    continue


            else:
                log.error(f"{email} not registered in DOP")
                log.info("go to the next account")
                time.sleep(2)
                continue

    elif software_method == 3:
        try:
            amount_wallets = int(input('\nHow many wallets do you need to make?\n'))
            for _ in range(amount_wallets):
                create_wallet()
        except Exception as err:
            log.error(f"Try first and enter the whole number | {err}")

    else:
        log.error("Unknown method, choose 1, 2 or 3!")

    time.sleep(time_break)
    print()
    log.success('Work completed successfully')

    time.sleep(time_break)

    log.debug('Press Enter to exit...')
    input()


if __name__ == '__main__':
    main()