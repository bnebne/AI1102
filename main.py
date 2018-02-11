from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,ImageSendMessage
)

app = Flask(__name__)

# Replace by your channel secret and access token from Line Developers console -> Channel settings.
LINE_CHANNEL_SECRET = 'e9d5b7f1223e54b57a458d4c82eff1fc'
LINE_CHANNEL_ACCESS_TOKEN = 'h6rGRksS2ZRJl4xFvfv2tDrBiAwTVUEPMtczNSy8cwe6yLbJ87wleDMyhIIF6+lwsDCR1XMBf8MCqDjegzEzKxyiF1hBOrkgZAIxoBQKlq55fSRnVtQx2F7XNgzhpBbXqcZcWbwjFFpXj0Uia4F12wdB04t89/1O/w1cDnyilFU='
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


@app.route("/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # Replace the text by what you want to say
    line_bot_api.reply_message(
        event.reply_token,
         TextSendMessage(text=reply(event.message.text)))
def reply(text):
    if text == "剪刀":
        return "石頭"
    elif text == "石頭":
        return "布"
    elif text == "布":
        return "剪刀"
    else:
        return "Hello world"

if __name__ == "__main__":
    app.run()