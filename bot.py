import random
import tweepy  # X API用ライブラリ
import anthropic  # Claude API用ライブラリ
from dotenv import load_dotenv
import os

# 環境変数をロード
load_dotenv()

# X (Twitter) API 認証
client = tweepy.Client(
    consumer_key=os.getenv("X_CONSUMER_KEY"),
    consumer_secret=os.getenv("X_CONSUMER_SECRET"),
    access_token=os.getenv("X_ACCESS_TOKEN"),
    access_token_secret=os.getenv("X_ACCESS_TOKEN_SECRET")
)

# Claude API 認証
anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Claudeでツイートを生成
def generate_tweet():
    response = anthropic_client.messages.create(
        model="claude-3",  # Claudeの最新モデル（Claude 3に適宜変更）
        max_tokens=100,
        messages=[{"role": "user", "content": "ポンコツな宇宙ロボットがつぶやくような面白い一言を作って"}]
    )
    return response.content[0].text  # Claudeのレスポンスからテキストを取得

# ツイートを投稿
tweet_text = generate_tweet()
client.create_tweet(text=tweet_text)

print("ツイートしました:", tweet_text)
