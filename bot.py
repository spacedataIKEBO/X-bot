import os
import tweepy
import anthropic  # Claude API用ライブラリ

# Claude API 認証
anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Twitter API の認証
client = tweepy.Client(
    consumer_key=os.getenv("TWITTER_API_KEY"),
    consumer_secret=os.getenv("TWITTER_API_SECRET"),
    access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.getenv("TWITTER_ACCESS_SECRET")
)

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
