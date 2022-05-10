import numpy as np

import re
import tweepy
from janome.tokenizer import Tokenizer

p = re.compile("[ぁ-んァ-ン一-龥]+")

# 認証に必要なキーとトークン
API_KEY = ''
API_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''

# APIでどのidから検索するか
MAX_ID = 0

# 検索の繰り返し, APIの規定では15分に180回したら怒られる
REPEAT = 20

# APIの認証
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

current_id = MAX_ID
num = 2001

t = Tokenizer()

f = open("words_9_14.txt", "w")
f1 = open("tweet_9_14.txt", "w")

for repeat in range(REPEAT):

    # キーワードからツイートを取得
    api = tweepy.API(auth)
    if current_id == 0:
        tweets = api.search(q=['#教師のバトン -RT'], count=100)
    else:
        tweets = api.search(q=['#教師のバトン -RT'], count=100, max_id=current_id - 1)

    for tweet in tweets:
        words = ""
        for tok in t.tokenize(tweet.text):
            pos = tok.part_of_speech.split(",")
            if "名詞" in pos and p.fullmatch(tok.surface) and not tok.surface == "バトン" and not tok.surface == "教師":
                words += tok.surface
                words += " "

        # current_idの更新
        current_id = tweet.id

        # ファイルへの書き込み
        f1.write(str(num))
        num += 1
        f1.write(tweet.text)
        f.write(words[0:-1])
        f1.write("\n")
        if num < 0:
            f.write("\t1\n")
        else:
            f.write("\t0\n")
f1.close()
f.close()
