#!/usr/bin/env python

TWITCH_HOST = "irc.chat.twitch.tv"         # This is Twitchs IRC server
TWITCH_PORT = 6697                         # Twitchs IRC server listens on port 6767
TWITCH_NICK = "USERNAME OF YOUR TWITCH BOT"            # Twitch username your using for your bot
TWITCH_PASS = "OAUTH TOKEN TO LOGIN"          # Twitch OAuth token from https://twitchapps.com/tmi/
TWITCH_PREFIX = "!"

DEBUG = 1
TWITCH_RATE = (20/30) # messages per seccond
CHANNEL_NAME = ["USERNAME OF THE CHANNEL"]

CLIENT_ID = "GET FROM DEV REPO"         # https://dev.twitch.tv/console/apps/
CLIENT_SECRET = "GET FROM DEV REPO" # https://dev.twitch.tv/console/apps/
CLIENT_REFRESH_TOKEN = "GET FROM DEV REPO" # See instuction bellow
CLIENT_ACCESS_TOKEN = "GET FROM DEV REPO"

#RUN IN BROWSER (change CLIENT_ID and CLIENT SECRET)
#https://id.twitch.tv/oauth2/authorize?response_type=code&client_id=CLIENT_ID&redirect_uri=http://localhost&scope=clips:edit
#Take the code from url response and get the refresh token from terminal (change CLIENT_ID, CLIENT_SECRET, CODE)
#curl -X POST -k -i 'https://id.twitch.tv/oauth2/token?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&code=CODE&grant_type=authorization_code&redirect_uri=http://localhost'

#id dxbzyezewd3czlc810g27y4nltszzf
#secret 38sbsxxdshgq4llqll77uu0v06gjp9
#token bearer

#https://id.twitch.tv/oauth2/authorize?response_type=code&client_id=dxbzyezewd3czlc810g27y4nltszzf&client_secret=38sbsxxdshgq4llqll77uu0v06gjp9&redirect_uri=http://localhost&scope=clips:edit