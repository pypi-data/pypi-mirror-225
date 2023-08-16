from .client import Client

from loguru import logger


async def get_tweet_details(client_session: Client, tweet_id: str | int) -> list[dict]:
    tweet_details = []
    try:
        param_str = '{"focalTweetId":"' + str(tweet_id) + '","with_rux_injections":false,"includePromotedContent":true,"withCommunity":true,"withQuickPromoteEligibilityTweetFields":true,"withBirdwatchNotes":true,"withVoice":true,"withV2Timeline":true}'

        params = {
            'variables': param_str,
            'features': '{"rweb_lists_timeline_redesign_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"tweetypie_unmention_optimization_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_enhance_cards_enabled":false}',
        }
        req = await client_session.make_request(path='get', endpoint=Client.queryId_tweet_details + "/TweetDetail", params=params)
        if req.get('data'):
            tweet_data = req['data']['threaded_conversation_with_injections_v2']['instructions'][0]['entries']
            tweet_owner_id = tweet_data[0]['content']['itemContent']['tweet_results']['result']['legacy']['user_id_str']
            try:
                tweet = tweet_data[1]
                entryId = tweet['entryId']
                in_reply_to_user_id_str = tweet['content']['items'][0]['item'].get('itemContent').get('tweet_results').get(
                    'result').get('legacy').get('in_reply_to_user_id_str')
                in_reply_to_status_id_str = tweet['content']['items'][0]['item'].get('itemContent').get('tweet_results').get('result').get('legacy').get('in_reply_to_status_id_str')
                if entryId.find('conversationthread') != -1 and (in_reply_to_status_id_str and in_reply_to_user_id_str) and int(in_reply_to_status_id_str) == int(tweet_id) and int(in_reply_to_user_id_str) == int(tweet_owner_id):
                    tweet_items = tweet['content']['items']
                    for item in tweet_items:
                        try:
                            in_reply_to_status_id_str = item['item']['itemContent']['tweet_results']['result']['legacy'].get('in_reply_to_status_id_str')
                            user_id = item['item']['itemContent']['tweet_results']['result']['legacy']['user_id_str']

                            if int(tweet_owner_id) == int(user_id) and int(in_reply_to_status_id_str) == int(tweet_id):
                                tweet_id = item['item']['itemContent']['tweet_results']['result'].get('rest_id')
                                text = item['item']['itemContent']['tweet_results']['result']['legacy']['full_text']
                                if item.get('item').get('itemContent').get('tweet_results').get('result').get('legacy').get('extended_entities'):
                                    media_url = item['item']['itemContent']['tweet_results']['result']['legacy']['extended_entities']['media'][0]['media_url_https']
                                else:
                                    media_url = None
                                tweet_details.append({'text': text, 'media_url': media_url})
                        except KeyError:
                            pass
            except IndexError:
                pass
    except Exception as exc:
        logger.error(f"Unexpected error for @{client_session.proxy} | {exc}")
    finally:
        return tweet_details
