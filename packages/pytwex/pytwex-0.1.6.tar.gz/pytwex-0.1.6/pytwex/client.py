from .utils import *
import aiohttp
import pyuseragents
from loguru import logger
from http.cookies import SimpleCookie


class Client:
    queryId_like = 'lI07N6Otwv1PhnEgXILM7A'
    queryId_retweet = 'ojPdsZsimiJrUGLR1sjUtA'
    queryId_create_tweet = 'SoVnbfCycZ7fERGCwpZkYA'
    queryId_handler_converter = '9zwVLJ48lmVUk8u_Gh9DmA'
    queryId_tweet_parser = 'Uuw5X2n3tuGE_SatnXUqLA'
    queryId_tweet_details = 'VWFGPVAGkZMGRKGe3GFFnA'
    base_url = 'https://twitter.com/i/api/graphql/'

    def __init__(self, auth_token: str, ct0: str = None, proxy: str = None):
        """
        Creating client instance object.
        :param auth_token: Auth token obtained from cookie
        :param ct0: Ct0 param obtained from cookie. NON-REQUIRED! You can obtain it using Client.get_ct0_token() method
        :param proxy: Http proxy for client with format ip:port:log:pass or http://log:pass@ip:port
        """
        self.headers = {
            'authority': 'twitter.com',
            'accept': '*/*',
            'accept-language': 'uk',
            'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
            'content-type': 'application/json',
            'origin': 'https://twitter.com',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': pyuseragents.random(),
            'x-twitter-active-user': 'yes',
            'x-twitter-auth-type': 'OAuth2Session',
            'x-twitter-client-language': 'en',
        }

        self.auth_token = auth_token
        self.ct0 = ct0
        if not self.ct0:
            logger.critical(f"There is no ct0 token for {auth_token} auth token. Please, request .get_ct0_token() method for client.")
        if self.auth_token and self.ct0:
            self.headers["x-csrf-token"] = self.ct0
            self.headers['cookie'] = f'auth_token={self.auth_token}; ct0={self.ct0}'
        self.proxy = self.get_proxy_format(proxy=proxy)
        self.user_name = None

    @staticmethod
    def get_proxy_format(proxy):
        if len(proxy.split(':')) == 4:
            ip, port, login, password = proxy.split(':')
            return f"http://{login}:{password}@{ip}:{port}"
        elif 'http' not in proxy and "@" in proxy:
            return f"http://{proxy}"

    async def make_request(self, path: str, url: str = None, endpoint: str = '', json_data: dict = None,
                           params: dict = None, data: dict = None):
        try:
            json = None
            if not data:
                async with aiohttp.ClientSession() as session:
                    async with session.request(path, url=f"{Client.base_url if not url else url}{endpoint}",
                                               proxy=self.proxy, json=json_data, headers=self.headers,
                                               params=params) as response:
                        json = await response.json()
            elif data:
                async with aiohttp.ClientSession() as session:
                    async with session.request(path, url=f"{Client.base_url if not url else url}{endpoint}",
                                                     proxy=self.proxy, data=data,
                                                     params=params) as response:
                        json = await response.json()
            return json
        except aiohttp.client.InvalidURL:
            logger.error(
                f"Invalid proxy | {self.proxy}. Please, recheck proxy validity or its format")
        except Exception as exc:
            logger.error(f"Unexpected error for @{self.user_name} | {exc}")

    async def make__media_request(self, path: str, url: str = '', endpoint: str = '', json_data: dict = None,
                                  params=None, data: bytes = b''):
        if params is None:
            params = {}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(path, url=f"{Client.base_url if not url else url}{endpoint}",
                                                 proxy=self.proxy,
                                                 params=params, data=data, headers=self.headers) as request:
                    content = await request.read()
                    encoding = request.charset or 'utf-8'
                    decoded_content = content.decode(encoding, errors='ignore')
                    return decoded_content
        except Exception as exc:
            logger.error(f"Unexpected error for @{self.user_name} | {exc}")

    async def get_ct0_token(self):
        randomized_ct = generate_random_ct_for_req()
        self.headers['cookie'] = f'auth_token={self.auth_token}; ct0={randomized_ct}'
        self.headers['x-csrf-token'] = randomized_ct
        async with aiohttp.ClientSession() as session:
            async with session.get('https://twitter.com/i/api/2/oauth2/authorize', headers=self.headers,
                                   proxy=self.proxy) as response:
                if response.status == 403:
                    cookie_jar = SimpleCookie()
                    cookie_jar.load(response.cookies)
                    self.ct0 = cookie_jar.get('ct0').value
                    self.headers["x-csrf-token"] = self.ct0
                    self.headers['cookie'] = f'auth_token={self.auth_token}; ct0={self.ct0}'
                    logger.debug(f"Successfuly setted new ct0 for auth_token: {self.auth_token[:10]}**********")
                    return response.cookies.get('ct0')

    async def update_username(self) -> str:
        """
        Function to getting own account username
        :return: Twitter account username
        """
        try:
            params = {
                'include_mention_filter': 'true',
                'include_nsfw_user_flag': 'true',
                'include_nsfw_admin_flag': 'true',
                'include_ranked_timeline': 'true',
                'include_alt_text_compose': 'true',
                'ext': 'ssoConnections',
                'include_country_code': 'true',
                'include_ext_dm_nsfw_media_filter': 'true',
                'include_ext_sharing_audiospaces_listening_data_with_followers': 'true',
            }
            del self.headers['content-type']
            req = await self.make_request(path='get', url='https://api.twitter.com/1.1/account/settings.json',
                                                    params=params)
            if req.get('screen_name'):
                self.user_name = req['screen_name']
                logger.success(
                    f"Successfully got twitter username for auth_token: *******{self.auth_token[7:-7]}******* | @{req['screen_name']}")
                return req['screen_name']
        except Exception as exc:
            logger.error(f"Couldn't get username for {self.auth_token} | {exc} | Try to recheck your cookie")
