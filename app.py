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

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    get_message = event.message.text.split()
    
    if get_message[0] == '心理測驗':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text = '愛情三元素測驗請輸入:\n「\nSternberg 你的另一半稱呼\n」\n\n拖延症測驗請輸入:\n「\nProcrastination\n」'))
    if get_message[0] == 'Sternberg':
        if len(get_message) == 10:
            score = [0, 0, 0]
            raw_scores = [''.join(get_message[1:4]), ''.join(get_message[4:7]), ''.join(get_message[7:10])]
            for i in range(3):
                for j in raw_scores[i]:
                    score[i] += int(j)
            love_code = ''.join(['1' if i >= 45 else '0' for i in score])
            love_dic = {'111':['完整的愛', '你們的愛情擁有了所有重要的元素\n祝福與期待你們能維繫這得來不易的愛情'], '110':['浪漫的愛', '如同羅密歐與茱麗葉般充滿浪漫色彩的愛情'], '101':['陪伴的愛', '是老夫老妻、靈魂伴侶呢'], '100':['喜歡', '是朋友間的相互欣賞與喜歡'], '011':['愚昧的愛', '承諾可能是基於短暫的激情\n要思考如何增加親密情感連結'], '010':['癡迷的愛', '你可能是中了一見鍾情的症狀XD'], '001':['空洞的愛', '空空的'], '000':['沒有愛的', '嗚嗚嗚']}
            reply = TextSendMessage(text=f'你們之間是{love_dic[love_code][0]}\n\n{love_dic[love_code][1]}\n\n親密: {score[0]}\n激情: {score[1]}\n承諾: {score[2]}')
            line_bot_api.reply_message(event.reply_token, reply)
        else:
            lover = get_message[1]
            reply = TextSendMessage(text=f'以下有45個陳述句\n請根據陳述句符合的程度回應1-5分\n1分表示非常不符合\n5分表示非常符合\n\n請依照以下格式(依序每15題一行 每5題空一格)回應噢！\n\n「\nSternberg\n33452 32252 35423\n34523 23332 25432\n33542 34523 33314\n」\n\n1.我積極支持{lover}的幸福\n2.我與{lover}有著溫暖的關係\n3.當有需要時，我能夠依靠{lover}\n4.當有需要時，{lover}能夠依靠我\n5.我願意與{lover}分享我的東西及我自己\n6.我從{lover}獲得相當多的情緒支持\n7.我給予{lover}相當多的情緒支持\n8.我與{lover}有良好的溝通\n9.在我生命中，我十分重視{lover}\n10.我感到與{lover}很親近\n11.我與{lover}有著舒服的關係\n12.我覺得我真的了解{lover}\n13.我覺得{lover}真的了解我\n14.我覺得我可以真的信任{lover}\n15.我與{lover}分享很內心深處的個人訊息\n\n16.光是看到{lover}就讓我感到興奮\n17.我發現自己一天中經常想到{lover}\n18.我與{lover}的關係是很浪漫的\n19.我發現{lover}很有吸引力\n20.我把{lover}理想化\n21.我無法想像有另一個人能像{lover}一樣讓我開心\n22.比起其他任何人，我更喜歡與{lover}在一起\n23.對我來說，沒有事情比我與{lover}的關係更重要\n24.我特別喜歡與{lover}肢體接觸\n25.似乎有像『魔法』的東西和我與{lover}的關係有關\n26.我愛慕著{lover}\n27.我無法想像沒有{lover}的生活\n28.我與{lover}的關係是充滿熱情的\n29.當我看浪漫的電影及閱讀浪漫的書時，我會想到{lover}\n30.我對{lover}著迷\n\n31.我知道我在乎{lover}\n32.我承諾維持與{lover}的關係\n33.因為我對{lover}的承諾，我不會讓他人進到我們之間\n34.我對於我與{lover}之間的關係穩定有信心\n35.我不會讓任何事阻礙我對{lover}的承諾\n36.我預期我對{lover}的愛會至死不渝\n37.我對{lover}總是感到強烈的責任感\n38.我對{lover}的承諾是堅定的\n39.我無法想像我與{lover}的關係結束的時刻\n40.我很確定我對{lover}的愛\n41.我覺得我與{lover}的關係是恆久的\n42.我覺得我與{lover}在一起是好的決定\n43.我對{lover}感到責任感\n44.我計畫未來能持續著我與{lover}的關係\n45.即使當面對很難應對{lover}的時刻，我仍維持對於我們關係的承諾')
            line_bot_api.reply_message(event.reply_token, reply)
    if get_message[0] == 'Procrastination':
        if len(get_message) == 5:
            raw_scores = ''.join(get_message[1:])
            revItem = [2, 3, 5, 7, 10, 12, 13, 14, 17, 19]
            score = 0
            for i in range(20):
                if i in revItem:
                    score += 6 - int(raw_scores[i])
                else:
                    score += int(raw_scores[i])
            reply = TextSendMessage(text = f'你的拖延分數是{score}分\n台灣人拖延分數平均數為64.36；標準差為11.65')
            line_bot_api.reply_message(event.reply_token, reply)
        else:
            reply = TextSendMessage(text='一般人會使用以下的陳述句來形容自己\n請判斷您與以下每一個陳述句的符合程度\n1分表示非常不符合\n5分表示非常符合\n\n請依照以下格式依序回應噢！\n\n「\nProcrastination\n31452 13422\n23334 45222\n」\n\n1.我經常在做我幾天前就想做的事情\n2.直到快要交作業前我才會寫它\n3.當我看完圖書館借來的書後，不管是否到期，我都會馬上歸還\n4.每當早上起床時間一到，我幾乎都馬上起床\n5.在我寫完信後，回過個幾天才寄出\n6.我一般都是立刻回撥電話\n7.即使是很簡單的工作，我也很少在幾天內完成\n8.我經常很快速地做出決定\n9.我通常會延遲我必須要做的工作\n10.我經常需要很匆忙地趕作業才得以準時完成它\n11.當準備要外出時，我很少在最後一刻才發現有什麼事情必須去做\n12.在為一些有截止期限的事情做準備時，我經常浪費時間做其他事\n13.我喜歡提前赴約\n14.我經常在作業指派後沒多久就開始做作業\n15.我經常比必須完工的時間更早完成工作\n16.我總是在最後一刻才去買生日禮物或聖誕禮物\n17.即使是必需品，我也經常到最後一刻才買\n18.我經常能完成我一天中計劃好要做的所有事\n19.我一直在說「我明天會做」\n20.在晚上休息之前我通常會先安頓好所有必須做的事情')
            line_bot_api.reply_message(event.reply_token, reply)

