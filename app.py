import os
from datetime import datetime

from flask import Flask, abort, request

# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))


@app.route("/", methods=["GET", "POST"])
def callback():

    if request.method == "GET":
        return "Hello Heroku"
    if request.method == "POST":
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)

        return "OK"

intimacy, passion, commitment = 0
lover = ''
sternberg = ''

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    get_message = event.message.text
    
    if (get_message == '心理測驗') & (sternberg == ''):
    	sternberg = 'intimacy'
        reply = TextSendMessage(text = '你愛的人是誰?(請輸入名字或暱稱)')
        line_bot_api.reply_message(event.reply_token, reply)
    elif sternberg == 'intimacy':
        lover = get_message
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text = f'你愛{lover}'))
        sternberg == ''
    else:
        reply = TextSendMessage(text=f"{get_message}")
        line_bot_api.reply_message(event.reply_token, reply)
