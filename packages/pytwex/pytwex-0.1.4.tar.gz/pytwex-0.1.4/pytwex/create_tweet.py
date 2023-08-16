from .client import Client
from .get_media_id import media_converter

from loguru import logger


async def create_tweet(client_session: Client, text: str = "", image_url: str = None, tweet_id_for_reply: str | int = None) -> int:
    """
    Function for tweet creating
    :param client_session: Required client session object
    :param text: Optional text for tweet
    :param image_url: Image's url for post
    :param tweet_id_for_reply: Tweet ID if you need to reply to tweet
    :return: Created tweet id
    """
    try:
        json_data = {
            'variables': {
                'tweet_text': text if text else "",
                'dark_request': False,
                'media': {
                    'media_entities': [],
                    'possibly_sensitive': False},
                'semantic_annotation_ids': [],
            },
            'features': {
                'tweetypie_unmention_optimization_enabled': True,
                'responsive_web_edit_tweet_api_enabled': True,
                'graphql_is_translatable_rweb_tweet_is_translatable_enabled': True,
                'view_counts_everywhere_api_enabled': True,
                'longform_notetweets_consumption_enabled': True,
                'tweet_awards_web_tipping_enabled': False,
                'longform_notetweets_rich_text_read_enabled': True,
                'longform_notetweets_inline_media_enabled': True,
                'responsive_web_graphql_exclude_directive_enabled': True,
                'verified_phone_label_enabled': False,
                'freedom_of_speech_not_reach_fetch_enabled': True,
                'standardized_nudges_misinfo': True,
                'tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled': False,
                'responsive_web_graphql_skip_user_profile_image_extensions_enabled': False,
                'responsive_web_graphql_timeline_navigation_enabled': True,
                'responsive_web_enhance_cards_enabled': False,
                'responsive_web_twitter_article_tweet_consumption_enabled': False,
                'responsive_web_media_download_video_enabled': False
            },
            'queryId': Client.queryId_create_tweet,
        }
        if tweet_id_for_reply:
            json_data['variables']['reply'] = {
            'in_reply_to_tweet_id': str(tweet_id_for_reply),
            'exclude_reply_user_ids': [],
        }
        if image_url:
            json_data['variables']['media'] = {
            'media_entities': [
                {
                    'media_id': await media_converter(client_session=client_session, media_url=image_url),
                    'tagged_users': [],
                },
            ],
            'possibly_sensitive': False,
        }
        req: dict = await client_session.make_request(path='post', endpoint=Client.queryId_create_tweet + "/CreateTweet", json_data=json_data)
        if req.get('data') and req.get('data').get('create_tweet').get('tweet_results').get('result'):
            tweet_id = req['data']['create_tweet']['tweet_results']['result']['rest_id']
            screen_name =req['data']['create_tweet']['tweet_results']['result']['core']['user_results']['result']['legacy']['screen_name']
            logger.success(f"Twitter: {client_session.user_name} | Successfully posted new tweet | Url: https://twitter.com/{screen_name}/status/{tweet_id}")
            return int(tweet_id)
        elif req.get('errors'):
            logger.error(f"Twitter: {client_session.proxy} | Couldn't post new tweet | {req.get('errors')[0].get('message')}")
            return False
    except Exception as exc:
        logger.error(f"Unexpected error for @{client_session.proxy} | {exc}")
    return False
