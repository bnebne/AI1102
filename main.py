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
LINE_CHANNEL_SECRET = '75ce6e8ea5e559381fa9830575592c74'
LINE_CHANNEL_ACCESS_TOKEN = 'znDynalgVQMv77Ag4Hz0ULgU8GxgkNjXfEPHJIWCve7RkVakYMCbauBZAAoNiGZi5wXZ1t75fgmeUSLB5GiINb9a+/uB82bnB78GhHxHct382fsmYBXkr1bpQ8G/Jc47eq92MH+41/8seuveiIoMsgdB04t89/1O/w1cDnyilFU='
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
        ImageSendMessage( original_content_url='https://addons.cdn.mozilla.net/user-media/addon_icons/824/824288-64.png?modified=1516050890', preview_image_url='https://addons.cdn.mozilla.net/user-media/addon_icons/824/824288-64.png?modified=1516050890'))
     #   TextSendMessage(text=event.message.text))
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
#######