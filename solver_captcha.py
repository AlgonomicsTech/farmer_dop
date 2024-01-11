from dop import *
from anticaptchaofficial.recaptchav2proxyless import *
import time

# Вирішуємо каптчу
def solve_recaptcha(count_try_solve=0):
    log.info('Captcha found - trying to solve..')

    solver = recaptchaV2Proxyless()
    solver.set_verbose(1)
    solver.set_key(anticaptcha_api_key)
    solver.set_website_url(url_testnet_dop)
    solver.set_website_key(data_sitekey)
    solver.set_soft_id(0)

    g_response = solver.solve_and_return_solution()
    if g_response != 0:
        time.sleep(2)
        log.info(f"Captcha solved successfully!")
        return g_response
    else:
        log.error(f"Captcha resolution error | {solver.error_code}!")
        log.info("I am trying to solve the captcha again")
        count_try_solve += 1
        if count_try_solve < 5:
            return solve_recaptcha(count_try_solve)
        else:
            log.error("All attempts to solve the captcha ended in error")
            return None



# # Вирішуємо каптчу
# def solve_recaptcha(count_try_solve=0):
#     log.info('Captcha found - trying to solve..')
#
#     solver = recaptchaV3Proxyless()
#     solver.set_verbose(1)
#     solver.set_key(anticaptcha_api_key)
#     solver.set_website_url(url_testnet_dop)
#     solver.set_website_key(data_sitekey)
#     solver.set_page_action(home_page)
#     solver.set_min_score(0.9)
#     solver.set_soft_id(0)
#
#     g_response = solver.solve_and_return_solution()
#     if g_response != 0:
#         time.sleep(2)
#         log.info(f"Captcha solved successfully!")
#         return g_response
#     else:
#         log.error(f"Captcha resolution error | {solver.error_code}!")
#         log.info("I am trying to solve the captcha again")
#         count_try_solve += 1
#         if count_try_solve < 5:
#             # Повертайте результат рекурсивного виклику
#             return solve_recaptcha(count_try_solve)
#         else:
#             log.error("All attempts to solve the captcha ended in error")
#             return None
