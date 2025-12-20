# Raspberry NOAA v2 Tweaks

I wanted to push data to my website (hosted on AWS). Raspi-noaa-v2 doesn't contain any functionality to do this so i decided to 'suborn' the push-to-twitter capability. 

`scripts/push_processors/push_twitter.sh` calls a python module `post_to_twitter.py` which makes use of the Tweepy library to push files to twitter. However, I realised that i could create my own version of tweepy that did what i wanted.

I therefore created `tweepy.py` which sits in the local site-packages folder `.local/lib/python3.11/site-packages`, dummies out the Tweepy objects and functions, and then calls a bash script `pushaws.sh`. This script syncs the local image folder `/srv/images` to my S3 location and builds a javascript table thats pushed to my website for inclusion in a page in Wordpress. 

Note: Enabling push-to-twitter in the raspi-noaa config automatically installs tweepy so i then had to rename the tweepy folder in `.local/lib/python3.11/site-packages`. Otherwise this would get imported instead of my custom version. 