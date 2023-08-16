from .client import Client

from loguru import logger


async def like(client_session: Client, tweet_id: str | int) -> bool:
    """
    Function for post liking
    :param client_session: Required client session object
    :param tweet_id: Tweet ID for liking
    :return: True if successfully liked else False
    """
    try:
        json_data = {
            'variables': {
                'tweet_id': str(tweet_id),
            },
            'queryId': Client.queryId_like,
        }
        req = await client_session.make_request(path='post', endpoint=Client.queryId_like + "/FavoriteTweet", json_data=json_data)
        if 'errors' in req:
            logger.error(f"Twitter: {client_session.user_name} | Could'nt like tweet | {req['errors'][0]['message']}")
            return False
        elif 'data' in req and req['data']['favorite_tweet'] == 'Done':
            logger.success(f"Twitter: {client_session.user_name} | Successfully liked tweet")
            return True
    except Exception as exc:
        logger.error(f"Unexpected error for {client_session.proxy} | {exc}")
    return False
