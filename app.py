import requests
import tweepy
import json, time
class Spotify:
    def GetNowPlayingMusic(self):
        end_point = "https://api.spotify.com/v1/me/player/currently-playing"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer Token"
        }
        params = (
            ('market', 'ES'),
        )
        response = requests.get(end_point, headers=headers, params=params)
        return response.json()
        
    
class Twitter:
    def __init__(self, consumer_key, consumer_secret, access_key, access_secret):
        self.consumer_key, self.consumer_secret = consumer_key, consumer_secret
        self.access_key, self.access_secret     = access_key, access_secret
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_key, access_secret)
        self.api = tweepy.API(self.auth)
    
    def PostNowPlayingMusic(self, json):
        # 汚いので改善します。
        print(json)
        tweet_text = "Now Playing #Spotify \nMusic Name: %s \nArtist Name: %s %s" \
                        % (json['item']['name'],
                            json['item']['artists'][0]["name"],
                            json['item']['artists'][0]['external_urls']['spotify']
                        )
        self.api.update_status(tweet_text)

if __name__ == "__main__":
    # 汚いので改善します。とりあえず動ける形にしました。
    num = 1
    twitter = Twitter(consumer_key, consumer_secret, access_key, access_secret)
    now_play = Spotify().GetNowPlayingMusic()
    first_music_name = now_play['item']['name']
    twitter.PostNowPlayingMusic(now_play)
    while 1:
        # 見てられない
        if num == 1:
            time.sleep(0.1)
            now_play = Spotify().GetNowPlayingMusic()
            if first_music_name == now_play['item']['name']:
                pass
            else:
                twitter.PostNowPlayingMusic(now_play)
                num = num + 1
        else:
            print("Sleep...")
            time.sleep(now_play['item']['duration_ms'] / 1000.0 + 0.01)
            now_play = Spotify().GetNowPlayingMusic()
            twitter.PostNowPlayingMusic(now_play)