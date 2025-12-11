#copyright mark McIntyre, 2025

# simple tester for the fake tweepy

import tweepy

CONSUMER_KEY = 'hello'
CONSUMER_SECRET = 'there'
ACCESS_TOKEN_KEY = 'my'
ACCESS_TOKEN_SECRET = 'old friend'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
client = tweepy.Client(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET, access_token=ACCESS_TOKEN_KEY, access_token_secret=ACCESS_TOKEN_SECRET)

annotation = 'this is a test' + '\n\n#NOAA #NOAA15 #NOAA18 #NOAA19 #MeteorM2_3 #MeteorM2_4 #weather #weathersats #APT #LRPT #wxtoimg #MeteorDemod #rtlsdr #gpredict #raspberrypi #RN2 #ISS'
image_list = ['/srv/images/METEOR-M2-4-20251211-041433-equidistant_67_composite.jpg',
    '/srv/images/METEOR-M2-4-20251211-041433-equidistant_67.jpg',
    '/srv/images/METEOR-M2-4-20251211-041433-equidistant_67_rain_composite.jpg']

client.create_tweet(text=annotation, media_ids=image_list)
