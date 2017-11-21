import tweepy
import re
import urllib
import os
import codecs
import time

consumer_key = "4TmRDKaXwj9itwTnbMNzal7SG"
consumer_secret = "GsFN7mrWfjCS8EWqDVdcUuHvW0Qnc9r6qcYz6VlTDCBwlsevNx"
access_key = "915244569800798211-pUeGgPRt97USaMWdV9tuIRYRDx1GG6W"
access_secret = "RfvLqEsm0gWMKsSVjd5zZXSuNLaNdpr7fEa3JeT09YVem"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

path = "./img/"

def Downloadimg(tweet_data,username):
    if not os.path.exists(path + username):
        os.mkdir(path + username )
    savename = tweet_data
    filename = re.sub(r'https?://[a-zA-Z0-9.-]*/[a-zA-Z0-9.-]*/',"",savename)
    img = urllib.request.urlopen(savename).read()
    with open(path + username + "/" + filename, mode="wb") as f:
        f.write(img)
    print("保存しました:" + savename)
    tweet_data = ""

def DownloadVideo(tweet_data,username):
    if not os.path.exists(path + username):
        os.mkdir(path + username )
    url = tweet_data
    file_name = re.sub(r'https?://[a-zA-Z0-9.-]*/[a-zA-Z0-9.-]*/',"",url)
    res = urllib.request.urlopen(url).read()
    with open(file_name, 'wb') as f:
        f.write(res)
    print("保存しました:" + savename)
    tweet_data = ""

class MyStreamListener(tweepy.StreamListener):
    def on_connect(self):
        print("接続しました")
        return

    def on_disconnect(self, notice):
        print('切断されました:' + str(notice.code))
        return

    def on_status(self, status):
        print("ユーザーID:" + status.user.screen_name)
        try:
            if status._json["extended_entities"]["media"][0]["media_url_https"] != []:
                for jpg_data in status._json["extended_entities"]['media']:
                    print("画像がありました:" + jpg_data["media_url"])
                    tweet_data = jpg_data["media_url"]
                    if status._json["retweeted_status"]["user"]["screen_name"] != []:
                        username = status._json["retweeted_status"]["user"]["screen_name"]
                    else:
                        print(status._json)
                        username = status.user.screen_name
                    Downloadimg(tweet_data,username)
        except KeyError:
            if status._json["entities"]["urls"] == []:
                print("画像が含まれていないツイートです")
            if status._json["extended_entities"]["media"][0]["video_info"] == "video/mp4":
                print("動画、またはgifファイルです。")
                tweet_data = urllib.parse.urlparse =    status._json["extended_entities"]["media"][0]['video_info']["url"]
                print(tweet_data)
                username = status.user.screen_name
                DownloadVideo(tweet_data,username)
        except UnicodeEncodeError:
            data = (status._json).encode('cp932', "ignore")
            encodedata = data.decode('cp932')
            print(encodedata)

    def on_error(self, status_code):
        print("エラーが発生しました:" + str(status_code))
        return True

    def on_limit(self, track):
        print("API制限のため切断されました")
        return

    def disconnect(self,notice):
        print("接続が中断しました")
        return

if __name__ == "__main__":
    myStreamListener = MyStreamListener()
    stream = tweepy.Stream(auth = api.auth, listener=MyStreamListener())
    while True:
        try:
            stream.userstream()
        except:
            time.sleep(60)
            stream = tweepy.Stream(auth = api.auth, listener=MyStreamListener())