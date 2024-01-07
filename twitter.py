from loguru import logger as log
import asyncio
import random
import aiohttp
from better_automation.twitter.api import TwitterAPI
from config import *

log.add("logger.log", format="{time:YYYY-MM-DD | HH:mm:ss.SSS} | {level} \t| {function}:{line} - {message}")





class TwitterAutomation:
    def __init__(self, auth_token):
        self.auth_token = auth_token
        self.twitter_client = None

    async def setup_client(self):
        async with aiohttp.ClientSession() as session:
            self.twitter_client = TwitterAPI(session=session, auth_token=self.auth_token)

    async def follow_user(self, user_to_follow):
        try:
            user_id = await self.twitter_client.request_user_id(username=user_to_follow)
            await self.twitter_client.follow(user_id=user_id)
            log.success(f'Successfully followed {user_to_follow}')
        except Exception as e:
            log.error(f'Error following {user_to_follow}: {e}')

    async def retweet(self, tweet_id):
        try:
            await self.twitter_client.repost(tweet_id=tweet_id)
            log.info(f'Successfully retweeted {tweet_id}')
        except Exception as e:
            log.error(f'Error retweeting {tweet_id}: {e}')

    async def like_tweet(self, tweet_id):
        try:
            await self.twitter_client.like(tweet_id=tweet_id)
            log.info(f'Successfully liked tweet {tweet_id}')
        except Exception as e:
            log.error(f'Error liking tweet {tweet_id}: {e}')


    async def perform_actions(self, user_to_follow,
                              tweet_id='',
                              comment_text=''):

        async with aiohttp.ClientSession() as session:
            self.twitter_client = TwitterAPI(session=session, auth_token=self.auth_token)

            # Виконуємо дії в межах одного сеансу
            await self.follow_user(user_to_follow)

            # await self.retweet(tweet_id)
            # await self.like_tweet(tweet_id)
            # await self.comment_on_tweet(tweet_id, comment_text)



async def process_token(auth_token):
    user_to_follow = dop_to_follow

    automation = TwitterAutomation(auth_token)
    success = await automation.perform_actions(user_to_follow)
    return success, auth_token


async def main():
    success_tokens = []

    # Читаємо токени з файлу
    with open('twitter_data.txt', 'r') as file:
        tokens = file.read().splitlines()

    # Виконуємо дії для кожного токена
    for token in tokens:
        success, token = await process_token(token)
        if success:
            success_tokens.append(token)

            # Додаємо успішний токен до файлу
            with open('valid_twitter_tokens.txt', 'a') as file:
                file.write(token + '\n')

        # Додаємо рандомну затримку
        await asyncio.sleep(time_break)


if __name__ == '__main__':
    asyncio.run(main())

