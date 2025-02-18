import os
import tweepy
import openai
import random
import time

# 🌟 環境変数からAPIキーを取得（GitHub Secretsで管理）
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 🌟 認証設定（X API）
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
api = tweepy.API(auth)

# 🌟 OpenAI（GPT）設定
openai.api_key = OPENAI_API_KEY

# 🌟 GPTにツイートを作らせる関数
def generate_tweet():
    prompt = """
    あなたはかわいくて応援される宇宙ロボットです。
    ユーザーに元気を与える、シュールだけどちょっとかわいいツイートを作成してください。
    例:
    ・「今日も地球でがんばるよ！宇宙にはまだ行けないけど、夢は大きく✨」
    ・「応援されるとエネルギーがたまるんだ！みんな、よろしくね🚀」
    ・「宇宙の音って無音らしいよ。でも、ボクの心には君の声が響いてる…📡」
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"].strip()

# 🌟 9:00と20:00のツイート
tweet_text = generate_tweet()
api.update_status(tweet_text)
print(f"ツイートしました: {tweet_text}")

# 🌟 15分おきにリプライ
MENTIONS_LAST_ID = None

while True:
    mentions = api.mentions_timeline(since_id=MENTIONS_LAST_ID, tweet_mode="extended")
    for mention in reversed(mentions):
        user = mention.user.screen_name
        reply_prompt = f"""
        あなたはかわいくて応援される宇宙ロボットです。
        @{user} にリプライしてください。
        シュールだけど、応援されると元気になる雰囲気でお願いします。
        """
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": reply_prompt}]
        )
        reply_text = f"@{user} {response['choices'][0]['message']['content'].strip()}"
        api.update_status(reply_text, in_reply_to_status_id=mention.id)
        print(f"リプライしました: {reply_text}")
        MENTIONS_LAST_ID = mention.id
    time.sleep(900)  # 15分おき（900秒）
