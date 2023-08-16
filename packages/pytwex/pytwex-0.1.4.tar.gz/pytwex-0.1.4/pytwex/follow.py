from .client import Client

from loguru import logger


async def handler_to_id(client_session: Client, follow_user_handler: str):
    param_str = f'{{"screen_name":"{follow_user_handler}"}}'
    params = {
        'variables': param_str,
    }
    req = await client_session.make_request(path='get',
        endpoint=Client.queryId_handler_converter + '/ProfileSpotlightsQuery',
        params=params,
    )
    if req.get('data'):
        user_id = str(req['data']['user_result_by_screen_name']['result']['rest_id'])
        return user_id
    elif req.get('errors'):
        logger.error(f"Unexpected error for @{client_session.user_name} | {req['errors'][0]['message']}")


async def follow(client_session: Client, follow_user_handler: str) -> bool:
    """
    Function for following user using its handler. For example, if you want to follow https://twitter.com/elonmusk,
    you should write elonmusk

    :param client_session: Required client session object
    :param follow_user_handler: User handler without @
    :return: True if successfully followed else False
    """
    try:
        user_id = await handler_to_id(client_session=client_session, follow_user_handler=follow_user_handler)
        data = {
            'include_profile_interstitial_type': '1',
            'include_blocking': '1',
            'include_blocked_by': '1',
            'include_followed_by': '1',
            'include_want_retweets': '1',
            'include_mute_edge': '1',
            'include_can_dm': '1',
            'include_can_media_tag': '1',
            'include_ext_has_nft_avatar': '1',
            'include_ext_is_blue_verified': '1',
            'include_ext_verified_type': '1',
            'include_ext_profile_image_shape': '1',
            'skip_status': '1',
            'user_id': user_id,
        }
        req = await client_session.make_request(path='post', url="https://twitter.com/i/api/1.1/friendships/create.json", endpoint='', params=data)
        if 'id' in req:
            logger.success(f"Twitter: {client_session.user_name} | Successfully followed to @{follow_user_handler}")
            return True
        elif 'errors' in req:
            logger.error(f"Twitter: {client_session.proxy} | Could'nt follow to @{follow_user_handler} | {req['errors'][0]['message']}")
            return False
    except Exception as exc:
        logger.error(f"Unexpected error for @{client_session.proxy} | {exc}")
    return False

