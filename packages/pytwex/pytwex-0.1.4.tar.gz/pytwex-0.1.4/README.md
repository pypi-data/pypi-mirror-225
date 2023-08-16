## Description

Python asynchronous module for interacting with Twitter using ***auth_token*** for **Python 3.10+**

Available methods: 

1. Follow to user
2. Tweet creating
3. Tweet replying
4. Tweet liking
5. Pin tweet
6. Reply to tweet
7. Retweet

## Creating client instance

```
from pytwex.client import Client

### Creating with ct0 token
client = Client(auth_token='YOUR_AUTH_TOKEN',
                ct0='YOUR_CT0_TOKEN',
                proxy='YOUR_PROXY')
                
                
### Creating without ct0 token
async def create_client():

    client = Client(auth_token='YOUR_AUTH_TOKEN',
                    proxy='YOUR_PROXY')
    await client.get_ct0_token()
    
    
### You can update your username after creating client instance
...some async function...
   await client.update_username()
   print(client.user_name)
```

## Follow user example

```
from pytwex.follow import follow

... some async function...
    await follow(
                 client_session=YOUR_CLIENT_OBJECT,
                 follow_user_handler='elonmusk'
                 )
                 
    >>> True or False
```

## Create tweet example

```
from pytwex.create_tweet import create_tweet

... some async function...
    await create_tweet(
                 client_session=YOUR_CLIENT_OBJECT,
                 text='This is my text for tweet', #Non required
                 image_url='http://googletestimage.url/', #Non required
                 tweet_id_for_reply=16911350916896132 #Non required
                 )
                 
    >>> Returns published tweet id, for example 1691135091689611264
```

## Developer

- [Github](https://github.com/flexter1)
- 
  [Telegram](https://t.me/flexter_join)

