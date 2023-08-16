from .client import Client

from loguru import logger


async def retweet(client_session: Client, tweet_id: str | int) -> str:
    """
    Function for retweeting post
    :param client_session: Required client session object
    :param tweet_id: Tweet ID for retweeting
    :return: Retweeted tweet url
    """
    try:
        json_data = {
            'variables': {
                'tweet_id': str(tweet_id),
            },
            'queryId': Client.queryId_retweet,
        }
        req: dict = await client_session.make_request(path='post', endpoint=Client.queryId_retweet + "/CreateRetweet", json_data=json_data)
        if req.get('data') != {} and req.get('data').get('create_retweet').get('retweet_results').get('result').get('rest_id'):
            rest_id = req.get('data').get('create_retweet').get('retweet_results').get('result').get('rest_id')
            logger.success(f"Twitter: {client_session.user_name} | Successfully retweeted | https://twitter.com/{client_session.user_name}/status/{rest_id}")
            tweet_link = f"https://twitter.com/{client_session.user_name}/status/{rest_id}"
            return tweet_link
        elif 'errors' in req:
            logger.error(f"Twitter: {client_session.proxy} | Could'nt retweet | {req['errors'][0]['message']}")
    except Exception as exc:
        logger.error(f"Unexpected error for @{client_session.proxy} | {exc}")
