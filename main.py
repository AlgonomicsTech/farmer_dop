import time
from logo import print_ALGONOMICS
from os.path import exists
from dop import *
from config import *
from loguru import logger as log




log.add("logger.log", format="{time:YYYY-MM-DD | HH:mm:ss.SSS} | {level} \t| {function}:{line} - {message}")

def main():

    if exists(path='accounts_data.txt'):
        with open(file='accounts_data.txt', mode='r', encoding='utf-8-sig') as file:
            accounts_list = [row.strip() for row in file]
    else:
        accounts_list = []

    if exists(path='success_reg_accounts.txt'):
        with open(file='success_reg_accounts.txt', mode='r', encoding='utf-8-sig') as file:
            successfully_accounts_list = [row.strip() for row in file]
    else:
        successfully_accounts_list = []

    if exists(path='ref.txt'):
        with open(file='ref.txt', mode='r', encoding='utf-8-sig') as file:
            ref_code_list = [row.strip() for row in file]
    else:
        ref_code_list = []

    print()
    print_ALGONOMICS("ALGONOMICS")
    time.sleep(2)
    print()

    log.success(f'Downloaded successfully {len(accounts_list)} accounts for registration | {len(ref_code_list)} referral codes')
    log.success(
        f'Downloaded successfully {len(successfully_accounts_list)} successfully registered accounts')
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
                    time.sleep(timeout * 3)
                    print()
                except:
                    time.sleep(timeout * 3)
                    continue
            else:
                log.info(f"{email} | already registered")
                log.info("go to the next account")
                time.sleep(2)
                print()
                continue
    elif software_method == 2:
        log.error('In The Process of development...')


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