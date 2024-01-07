import requests

#auth_token = "790e504f26f77fca9e6451c4f93477608a755d61"

headers = {
    'authority': 'rewards-api.dop.org',
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-type': 'application/json',
    'origin': 'https://doptest.dop.org',
    'referer': 'https://doptest.dop.org/',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69',
    #'Authorization': f'Bearer {auth_token}'
}

response = requests.post('https://rewards-api.dop.org/rewards/auth/twitter/reverse', headers=headers)
print(response.json())
{'oauth_token': '9wd8UQAAAAABrL1LAAABjNmC5hg', 'oauth_token_secret': 'cyfdigf2HxaReycnbrSx2ksahi7PwNEu', 'oauth_callback_confirmed': 'true'}