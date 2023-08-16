from .client import Client
from aiohttp import ClientSession
import requests
import json

from loguru import logger


async def media_converter(client_session: Client, media_url: str = None) -> str:
    """
    Function for uploading Image_URL to twitter for posting it in future
    :param client_session: Required client session object
    :param media_url: Url to image
    :return: Media_id uploaded to twitter. This uses for create_tweet() method
    """
    try:
        if media_url:
            logger.info(f"Getting media id for @{client_session.user_name}...")
            bytes_media = requests.get(url=media_url).content
            len_media = len(bytes_media)

            #1 req
            params = {
                'command': 'INIT',
                'total_bytes': len_media,
                'media_type': 'image/jpeg',
                'media_category': 'tweet_image',
            }
            req1: dict = await client_session.make_request(path='post', url='https://upload.twitter.com/i/media/upload.json', params=params)
            media_id_string = str(req1.get('media_id_string'))
            if media_id_string:
                #2 req
                params = {
                    'command': 'APPEND',
                    'media_id': media_id_string,
                    'segment_index': '0',
                }
                req2 = await client_session.make__media_request(path='options', url='https://upload.twitter.com/i/media/upload.json', params=params)

                #3 req
                client_session.headers['content-type'] = 'multipart/form-data; boundary=----WebKitFormBoundaryCGqmEUMuU9BgPiZm'
                data = b'------WebKitFormBoundaryCGqmEUMuU9BgPiZm\r\nContent-Disposition: form-data; name="media"; filename="blob"\r\nContent-Type: application/octet-stream\r\n\r\n'
                data += b'' + bytes_media
                data += b'\r\n------WebKitFormBoundaryCGqmEUMuU9BgPiZm--'
                async with ClientSession() as session:
                    async with session.post('https://upload.twitter.com/i/media/upload.json', headers=client_session.headers, params=params, data=data, proxy=client_session.proxy) as response:
                        pass
                #req4
                params = {
                    'command': 'FINALIZE',
                    'media_id': media_id_string,
                }
                req4 = await client_session.make__media_request(path='post', url='https://upload.twitter.com/i/media/upload.json', params=params)
                client_session.headers['content-type'] = 'application/json'
                if json.loads(req4).get('media_id_string'):
                    logger.info(f"Successfully got media id for {client_session.user_name}")
                    return json.loads(req4).get('media_id_string')
                else:
                    logger.error(f"Couldn't get media id for @{client_session.user_name} | {req4}")
    except Exception as exc:
        logger.error(f"Unexpected error for @{client_session.user_name} | {exc}")
