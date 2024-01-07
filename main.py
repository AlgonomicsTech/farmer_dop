import time
from logo import print_ALGONOMICS
from os.path import exists
from dop import *
from config import *
from passing_testnet import *
from loguru import logger as log


log.add("logger.log", format="{time:YYYY-MM-DD | HH:mm:ss.SSS} | {level} \t| {function}:{line} - {message}")

def main():

    if exists(path='accounts.txt'):
        with open(file='accounts.txt', mode='r', encoding='utf-8-sig') as file:
            accounts_list = [row.strip() for row in file]
    else:
        accounts_list = []

    if exists(path='passed_testnet.txt'):
        with open(file='passed_testnet.txt', mode='r', encoding='utf-8-sig') as file:
            accounts_list_passed_testnet = [row.strip() for row in file]
    else:
        accounts_list_passed_testnet = []

    if exists(path='twitter_data.txt'):
        with open(file='twitter_data.txt', mode='r', encoding='utf-8-sig') as file:
            accounts_twitter_list = [row.strip() for row in file]
    else:
        accounts_twitter_list = []

    if exists(path='success_reg_accounts.txt'):
        with open(file='success_reg_accounts.txt', mode='r', encoding='utf-8-sig') as file:
            success_reg_accounts = [row.strip() for row in file]
    else:
        success_reg_accounts = []

    if exists(path='ref.txt'):
        with open(file='ref.txt', mode='r', encoding='utf-8-sig') as file:
            ref_code_list = [row.strip() for row in file]
    else:
        ref_code_list = []

    print()
    print_ALGONOMICS("ALGONOMICS")
    time.sleep(2)
    print()

    log.success(f'Downloaded successfully {len(accounts_list)} accounts for registration | {len(accounts_twitter_list)} twitter accounts | {len(ref_code_list)} referral codes')
    log.success(
        f'Downloaded successfully {len(success_reg_accounts)} successfully registered accounts | {len(accounts_list_passed_testnet)} successfully passing testnet')
    log.info('💰 DONATION EVM ADDRESS: 0x4A080654795e526801954493BD0D712609d0ccEF')
    time.sleep(2)

    software_method = int(input('\n1. Account registration\n'
                                '2. Passing the testnet\n'
                                'Make your choice:\n'))
    print()

    if software_method == 1:
        for account in accounts_list:
            email, mnemonic = account.split(':')
            if is_account_registered(email):
                try:
                    auto_reg(email, mnemonic)
                    time.sleep(timeout)
                    print()
                except:
                    time.sleep(timeout)
                    continue
            else:
                log.info(f"{email} | already registered")
                log.info("go to the next account")
                time.sleep(2)
                print()
                continue

            log.info("go to the next account")

    elif software_method == 2:
        twitter_index = 0  # Індекс останнього використаного Twitter-акаунту

        for dot_accounts in success_reg_accounts:
            _, dop_mnemonic, _, email, mm_mnemonic, _ = dot_accounts.split(":")
            if is_account_registered_2(email):
                passed = 0
                while passed != 1:
                    for i in range(twitter_index, len(accounts_twitter_list)):
                        twitter_account = accounts_twitter_list[i]
                        twitter_login, twitter_password = twitter_account.split(":")
                        if twitter_not_use(twitter_login):
                            try:
                                testnet(email, mm_mnemonic, dop_mnemonic, twitter_login, twitter_password)
                                log.success("all steps passes successfully")
                                log.info("go to the next account")
                                time.sleep(timeout)
                                passed = 1
                                twitter_index = i + 1
                                break
                            except Exception as err:
                                log.error(f"{email} when passing {err}")
                                log.info("repeat process of passing")
                                time.sleep(timeout)
                                continue

                        else:
                            log.error(f"{twitter_login} already used in DOP")
                            log.info("go to the next twitter")
                            continue
                    else:
                        passed = 1
                        log.error("plase add new twitter accounts")
            else:
                log.error(f"{email} not registered in DOP")
                log.info("go to the next account")
                time.sleep(2)
                continue



    else:
        log.error("Unknown method, choose 1 or 2!")

    time.sleep(time_break)
    print()
    log.success('Work completed successfully')

    time.sleep(time_break)
    log.debug('Press Enter to exit...')
    input()


if __name__ == '__main__':
    main()