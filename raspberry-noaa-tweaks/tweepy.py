# python code to fake tweepy so that raspi-noaa can send to AWS

# copyright Mark McIntyre, 2025

# install this to /home/mark/.local/lib/python3.11/site-packages/tweepy.py

# create a dummy $HOME/.tweepy.conf containing
#  export TWITTER_CONSUMER_API_KEY=notused
#  export TWITTER_CONSUMER_API_KEY_SECRET=notused
#  export TWITTER_ACCESS_TOKEN=notused
#  export TWITTER_ACCESS_TOKEN_SECRET=notused

# make sure push_twitter is enabled in the settings.yml file

import os

__version__ = 'markmac99 special'


class OAuthHandler():
    def __init__(self, token, secret):
        pass

    def set_access_token(self, token, secret):
        return 


class API():
    def __init__(self, auth):
        return
    
    def media_upload(self, image):
        class res():
            def __init__(self, image):
                self.media_id = os.path.split(image)[1]
                return
        return res(image)


class Client():
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        return 
    
    def create_tweet(self, text, media_ids):
        trimloc = text.find('\n\n#NOAA')
        text = text[:trimloc]
        cmd = f'/home/mark/source/pushtoaws/pushaws.sh "{text}" "{media_ids}"'
        print('command is ', cmd)
        os.system(cmd)
        return True
