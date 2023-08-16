from aiohttp import ClientSession
from .client import Client

from loguru import logger


async def pin_tweet(client_session: Client, tweet_id: str | int) -> bool:
    """
    Function for tweet pinning
    :param client_session: Required client session object
    :param tweet_id: Tweet ID for pinning
    :return: True if successfully pinned else False
    """
    try:
        data = {
            'tweet_mode': 'extended',
            'id': str(tweet_id),
        }
        async with ClientSession() as session:
            headers = client_session.headers
            headers['content-type'] = 'application/x-www-form-urlencoded'
            async with session.post('https://api.twitter.com/1.1/account/pin_tweet.json', headers=headers,
                                    proxy=client_session.proxy, data=data) as response:
                req = await response.json()
        if 'errors' in req:
            logger.error(f"Twitter: {client_session.proxy} | Could'nt pin tweet | {req['errors'][0]['message']}")
            return False
        elif 'pinned_tweets' in req:
            logger.success(f"Twitter: {client_session.user_name} | Successfully pinned tweet https://twitter.com/{client_session.user_name}/status/{tweet_id}")
            return True
    except Exception as exc:
        logger.error(f"Unexpected error for @{client_session.proxy} | {exc}")