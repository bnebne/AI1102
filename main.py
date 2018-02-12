#coding=utf-8

import logging
import time

from flask import Flask,request , abort
import requests
from linebot import (LineBotApi , WebhookHandler)

from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (
MessageEvent,
TextMessage ,
TextSendMessage,
CarouselTemplate,
URITemplateAction,
TemplateSendMessage,
CarouselColmn
)

BACKEND_SERVUCE = "http://35.229.156.92:7705"

app = Flask(__name__)

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
    if len(event.message.text.lower())<=2:
        line_bot_echo(event)
    else:
        line_bot_car_suggestion_process(event)
def line_bot_car_suggestion_process(event):
    user_info = event.source.user_id
    profile = line_bot_api.get_profile(event.source.user_id)
    display_name = profile.display_name

    time_log = time.strftime("%Y-%m-%d %H:%M:%S")
    json_data = {'data':{'message_raw': event.message.text.replace('n',' '),
                         'user_data':{'user_id': user_info,
                                      'time_log':time_log,
                                      'display_name':display_name}}}
    headers = {'Content-Type': "application/json"}
    url = BACKEND_SERVUCE + "/api/v1/car-suggestion"
    try:
        result = requests.post(url = url, json = json_data ,headers = headers)
        result.encoding = "utf-8"
        result = result.json()
        line_bot_car_suggestion_response(event,result)
    except Exception as exc:
        logging.exception("Connect to backend sever %s error: %s" , url ,exc)
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text = "連線中斷，請重新嘗試一次"))
def line_bot_car_suggestion_response(event,result):
    status = result.get("status")
    if status is None or status != "ok" :
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text = "抱歉無法找到適合您的商品～\n請更加詳細描述您的購買需求！"))
        return
    columns_data = []
    for p in result["products"]:
        image_url = p["photo"]
        title = p['name']
        price = '價格: %s - %s 萬' % (str(p["min_price"]),str(p["max_price"]))
        action_intro = URITemplateAction(label ='詳細資料', uri = p['introduction'])
        carousel_obj = CarouselColmn(thumbnail_image_url = image_url,
                                     title= title,
                                     text = price,
                                     actions=[action_intro])
        columns_data.append(carousel_obj)
        if len(columns_data) >= 10:
            break
    message = TemplateSendMessage(alt_text = "您的推薦結果", template=CarouselTemplate(columns=columns_data,
                                                                                     imageSize='contain'))
    line_bot_api.reply_message(event.reply_token ,message)

def line_bot_echo(event):
    line_bot_api.reply_message(
        event.reply_token ,
        TextSendMessage(text=event.text)
    )

if __name__ == "__main__":
    app.run()

