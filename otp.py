from dop import *
from config import *
import imaplib
import email
import re
import time
import logging as log


def get_otp(email_address, password, imap_server):
    try:
        # Підключення до поштового сервера
        mail = imaplib.IMAP4_SSL('imap.' + imap_server)
        mail.login(email_address, password)
        mail.select("inbox")
        time.sleep(timeout)
        for _ in range(5):
            status, messages = mail.search(None, '(FROM "info@x.com")')
            messages = messages[0].split()

            if not messages:
                log.error(f"{email_address} | email with OTP code not found")
                time.sleep(time_break)  # Затримка перед наступною спробою
                continue

            for mail_id in reversed(messages):  # Перевірка повідомлень з кінця
                _, msg_data = mail.fetch(mail_id, "(RFC822)")
                msg = email.message_from_bytes(msg_data[0][1])

                for part in msg.walk():
                    if part.get_content_type() == "text/html":
                        html_content = part.get_payload(decode=True).decode('utf-8')

                        #print("Повний вміст листа:", html_content)
                        verification_code_match = re.search(r'\<td align=\"left\" class=\"h1\"[^\>]*\>(\w+)', html_content)
                        verification_code = verification_code_match.group(1) if verification_code_match else None

                        if verification_code:
                            log.info(f"{email_address} | {verification_code}")
                            return verification_code

            log.error(f"{email_address} | OTP code not found in the current batch of emails")
            time.sleep(timeout)

        # Якщо OTP код так і не знайдено
        raise ValueError("Email with OTP code not found after 15 attempts")

    except Exception as err:
        log.error(f"{email_address} | error getting OTP | {err}")
    finally:
        mail.logout()

    return None


