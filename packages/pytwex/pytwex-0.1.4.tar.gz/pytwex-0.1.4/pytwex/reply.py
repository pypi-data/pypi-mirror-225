from .client import Client

from loguru import logger


async def reply(client_session: Client, tweet_id: str | int, text: str) -> str:
    """
    Function for replying to tweet
    :param client_session: Required client session object
    :param tweet_id: Tweet ID for replying
    :param text: Text for replying
    :return: Replied tweet link
    """
    try:
        json_data = {
        'variables': {
            'tweet_text': text,
            'reply': {
                'in_reply_to_tweet_id': str(tweet_id),
                'exclude_reply_user_ids': [],
            },
            'dark_request': False,
            'media': {
                'media_entities': [],
                'possibly_sensitive': False,
            },
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
            'tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled': True,
            'responsive_web_graphql_skip_user_profile_image_extensions_enabled': False,
            'responsive_web_graphql_timeline_navigation_enabled': True,
            'responsive_web_enhance_cards_enabled': False,
            'responsive_web_media_download_video_enabled': False,
            'responsive_web_twitter_article_tweet_consumption_enabled': False
        },
        'queryId': Client.queryId_create_tweet,
    }
        req: dict = await client_session.make_request(path='post', endpoint=Client.queryId_create_tweet + "/CreateTweet",
                                                      json_data=json_data)
        if req.get('data'):
            rest_id = req.get('data').get('create_tweet').get('tweet_results').get('result').get('rest_id')
            logger.success(f"Twitter: {client_session.user_name} | Successfully replied | https://twitter.com/{client_session.user_name}/status/{rest_id}")
            tweet_link = f"https://twitter.com/{client_session.user_name}/status/{rest_id}"
            return tweet_link
        elif req.get('errors'):
            logger.error(f"Twitter: {client_session.proxy} | Could'nt reply | {req['errors'][0]['message']}")
    except Exception as exc:
        logger.error(f"Unexpected error for @{client_session.proxy} | {exc}")
