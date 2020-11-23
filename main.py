from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

YOUR_CHANNEL_ACCESS_TOKEN = '/P5MDiQkNityjRVMLvhJ0L2sk00dNVuPnL946BYHVvt4Pz/y+8XJ2z8kOEKudBsL5nWs8XgTV1PwJ4m7eWulGVzTabmLMN8eiCXORe96jEmXuzvK7c2WVnWiiGJQhQlnHBpdQBRELzIIeBL5wFbVmAdB04t89/1O/w1cDnyilFU='
YOUR_CHANNEL_SECRET = '955d8b8c54ec7094760955682f5e5b2a'


app = Flask(__name__)
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


@app.route("/callback", methods=['POST'])
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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()