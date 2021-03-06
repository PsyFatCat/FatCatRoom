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
    
    if get_message[0][0] == '#':
        Hastags = ['#心理學', '#心理學應用', '#科學', '#心靈雞湯', '#哀傷', '#悲傷五階段', '#fivestagesofgrief', '#rip', '#心理肥宅貓', '#psyfatcat', '#心理學', '#心靈雞湯', '#心理韌性', '#心靈成長', '#心理學', '#判決', '#兒童法案', '#自我認同', '#認同危機', '#成長痛', '#Erikson', '#棉花糖實驗', '#自制力', '#延宕滿足', '#成功語錄', '#心理學', '#先別急著吃棉花糖', '#棉花糖系列', '#棉花糖實驗', '#自制力', '#延宕滿足', '#成功語錄', '#心理學', '#先別急著吃棉花糖', '#量化分析', '#棉花糖系列', '#心理學', '#先別急著吃棉花糖', '#創造力', '#自制力', '#延宕滿足', '#心理學', '#積極傾聽', '#社會支持', '#諮商', '#陪伴', '#心理學', '#污名化', '#精神疾患', '#歧視', '#社會關懷', '#與疾病共存', '#思覺失調', '#憂鬱', '#身心科', '#精神醫學', '#服務', '#成長', '#心靈雞湯', '#聖誕節', '#吸引力', '#社會心理學', '#行為學', '#reinforce', '#人本', '#自我拓展理論', '#交往關係', '#渣男', '#承諾', '#分手', '#感情', '#愛情心理學', '#戀愛', '#心理學', '#脫單', '#告白', '#上課時間', '#睡眠不足', '#學習成效', '#填鴨式教育', '#專注力', '#持續性注意力', '#注意力測驗', '#教育心理學', '#分配時間', '#專注時間', '#學習時間', '#重質不重量', '#經濟學', '#邊際效應', '#心理學', '#教育', '#國中', '#高中', '#上課', '#放學', '#學習', '#議題', '#刷存在感', '#單純曝光效果', '#連我阿嬤都會', '#社會心理學', '#好感度', '#意識', '#習慣', '#habituation', '#無聊', '#boredom', '#反向控制', '#防衛機制', '#合理化', '#否認）來抵銷自己對物的喜好', '#歸因', '#attribution', '#熟悉', '#familiarity', '#熟悉度', '#吸引力', '#神不知鬼不覺', '#心理學', '#感情', '#愛情', '#脫單', '#告白', '#追求', '#語錄', '#外表吸引力', '#吸引力', '#第一印象', '#月暈效應', '#看臉時代', '#大眾臉', '#對稱臉', '#臉上性別差異', '#演化', '#健康', '#生育能力', '#適者生存', '#族群繁衍', '#脫魯', '#修圖', '#交友軟體', '#化妝', '#微整形', '#乾乾淨淨', '#健健康康', '#魅力', '#感情', '#愛情', '#科普', '#脫單', '#科學', '#心理學', '#帥哥', '#正妹', '#抽獎文', '#文末抽獎', '#文末抽Clubhouse邀請碼', '#FB', '#IG', '#Clubhouse', '#疫情', '#iPhone', '#心理學', '#認知失調', '#改變行為', '#改變想法', '#邀請碼', '#抽獎', '#拖延症', '#拖延', '#心理測驗', '#信效度', '#自我保護', '#評價性', '#自我設限', '#Self-Handicap', '#自我價值', '#自尊', '#面對挑戰', '#成長', '#惰性', '#具象化', '#明確', '#截止時間了', '#惡魔小鞭鞭', '#心理學', '#科學', '#肥宅', '#耍廢', '#自我約束', '#拖延症', '#拖延', '#心理測驗', '#Dcard', '#IG', '#PTT', '#Other', '#台灣', '#香港', '#美國', '#中華民國', '#金城武', '#ANOVA', '#變異數分析', '#相關', '#統計', '#信度', '#效度', '#穩定性', '#因素分析', '#先拖再說', '#時間管理', '#死到臨頭', '#慢', '#心理學', '#科學', '#量化', '#資料分析', '#懶惰', '#耍廢', '#台灣', '#鮭魚', '#心理學', '#自我認同', '#特質', '#改名', '#自我接納', '#人格', '#自我', '#運勢', '#心理學家', '#心理浴場', '#鮭魚之亂', '#社會', '#時事', '#評論', '#心理學', '#孤獨', '#存在', '#存在主義', '#心理諮商', '#心理治療', '#精神', '#意義', '#語錄', '#心情', '#憂鬱', '#焦慮', '#成長', '#歐文亞隆', '#創傷', '#trauma', '#DSM-5', '#創傷後壓力症候群', '#PTSD', '#侵入性反應', '#迴避反應', '#認知與情緒的負向轉變', '#生理警覺度改變', '#心理學', '#臨床', '#諮商', '#心理師', '#字典', '#太魯閣', '#身心科', '#精神科', '#心理治療', '#創傷後成長', '#PTG', '#創傷', '#新的契機', '#人際關係轉變', '#力量湧現', '#對生命的欣賞', '#心靈成長', '#生活目標', '#自我認同', '#生活哲學', '#認知反芻', '#rumination', '#憂鬱症', '#書寫', '#敘說', '#梳理', '#放棄', '#陪伴', '#聆聽', '#心理浴場', '#心理學', '#三級警戒', '#疫情', '#防疫新生活', '#隔離', '#檢疫來防止疫情擴散', '#遠距教學', '#居家辦公', '#憂鬱', '#焦慮', '#情緒低落', '#易怒', '#害怕', '#緊張', '#難過', '#罪惡感', '#困惑', '#睡眠品質不佳', '#創傷後壓力症', '#畏避人群', '#酒精依賴', '#1925', '#衛生福利部', '#臺灣社交距離', '#臺灣加油', '#心理學', '#防疫', '#新冠肺炎', '#covid_19', '#主導色', '#心理測驗', '#心理學家', '#音樂心理測驗', '#體液學說', '#心理健康', '#現代醫學之父', '#信效度', '#心理學', '#人格', '#性格', '#科學', '#實事求是', '#偵探', '#科普', '#曉', '#鼬', '#confession', '#告白', '#電影', '#心理學', '#校園霸凌', '#私刑正義', '#親職教育', '#精神疾病', '#自體心理學', '#Kohut', '#自戀型人格', '#心理學家', '#自體', '#self', '#誇大自體', '#自我欣賞', '#羞愧', '#憤怒', '#自戀', '#心理學', '#客體關係', '#影評', '#成長', '#電影推薦', '#畢馬龍效應', '#吸引力法則', '#心靈雞湯', '#科學', '#心理學', '#社會心理學', '#自證預言', '#客體關係', '#投射認同', '#投射', '#projection', '#誘發', '#provocation', '#回應', '#response', '#認同', '#identification', '#神話', '#故事', '#Pygmalion', '#Galatea', '#Aphrodite', '#成功', '#信念', '#執著', '#秘密', '#教育', '#網路公審', '#公審', '#網路霸凌', '#心理歷程', '#仇恨言論', '#基模', '#schema', '#知識結構', '#意識形態', '#匿名性', '#隔空互動', '#娛樂性', '#非語言線索', '#罪惡感', '#認知失調', '#mindset', '#心理學', '#同理心', '#心情', '#政大', '#自殺', '#抽獎', '#抽獎文', '#文末抽獎', '#line貼圖', '#貼圖', '#表情符號', '#非語言線索', '#nonverbal_cue', '#語言線索', '#沒事', '#XD', '#環南市場', '#政治', '#心理學', '#陳時中', '#柯文哲', '#林昶佐', '#林勝東', '#評估', '#appraisal', '#因應', '#coping', '#問題焦點', '#情緒焦點', '#萬華', '#艋舺', '#疫情', '#防疫', '#covid_19', '#壓力', '#因應', '#先安內而後攘外', '#領域展開', '#早起早睡', '#心如止水', '#自我肯定', '#心理學', '#認知心理學', '#指考', '#指考戰士', '#高中', '#大學', '#考試', '#考試加油', '#生活', '#讀書', '#努力', '#認真', '#成長', '#心理學', '#憂鬱', '#憂鬱症', '#重鬱症', '#抑鬱症', '#情緒', '#心情', '#臨床心理', '#心理', '#心理師', '#身心科', '#精神科', '#心理疾病', '#病因', '#病程', '#治療', '#心理治療', '#認知治療', '#阿滴', '#youtube', '#youtuber', '#depression', '#majordepressivedisorder', '#mdd', '#psychology', '#clinical', '#psychiatry', '#psychopathology', '#psychotherapy', '#正向性格', '#動機', '#信心', '#專注', '#社會支持', '#奧運', '#東京奧運', '#東奧', '#台灣', '#台灣加油', '#中華隊', '#選手', '#加油', '#集氣', '#金牌', '#銀牌', '#銅牌', '#心理學', '#心理韌性', '#運動', '#olympics', '#tokyo2020', '#psychology', '#resilience', '#taiwan', '#chinesetaipei', '#台湾です', '#每看必輸', '#沒看就贏', '#鍋貼', '#紅內褲', '#迷信', '#儀式', '#心理學', '#行為學', '#制約', '#操作制約', '#史金納', '#增強', '#懲罰', '#奧運', '#東京奧運', '#東奧', '#台灣', '#台灣加油', '#中華隊', '#加油', '#集氣', '#olympics', '#tokyo2020', '#psychology', '#taiwan', '#chinesetaipei', '#conditioning', '#skinner', '#心理學', '#心理', '#父親節', '#父愛', '#紀錄片', '#愛', '#貼心', '#同理', '#照顧', '#母嬰關係', '#psychology', '#father', '#fathersday', '#caring', '#love', '#empathy', '#心理學', '#心理', '#單純曝光效果', '#科普', '#統計', '#心理統計', '#卡方', '#檢定', '#假設', '#科學', '#量化', '#刷存在', '#存在感', '#R', '#程式', '#code', '#社會心理學', '#認知心理學', '#發展心理學', '#性格心理學', '#知覺心理學', '#生理心理學', '#變態心理學', '#心理統計', '#心理測驗', '#心理實驗', '#心理系', '#心理學', '#心理師', '#臨床', '#諮商', '#科學', '#讀心術', '#指考', '#學測', '#考大學', '#轉學考', '#選系', '#選校', '#心理學', '#犯罪學', '#犯罪心理學', '#罪犯側寫', '#暴力', '#犯罪', '#偵查', '#偵探', '#犯罪現場', '#受害者', '#邏輯', '#歸納法', '#演繹法', '#科學', '#psychology', '#criminal', '#offender', '#profiling', '#心理學', '#認知', '#歸因', '#焦慮', '#疫苗', '#AZ', '#莫德納', '#BNT', '#高端', '#疫情', '#covid_19', '#安慰劑', '#反安慰劑', '#CDC', '#抽獎', '#心理', '#心情', '#psychology', '#vaccine', '#moderna', '#肺炎', '#心理學', '#創傷', '#童年', '#逆境', '#虐待', '#暴力', '#家暴', '#酒癮', '#藥癮', '#忽略', '#健康', '#預防', '#心情', '#情緒', '#感情', '#家人', '#成長', '#長大', '#psychology', '#mentalhealth', '#抽獎', '#心情', '#回顧', '#生日', '#週年', '#帶空嚨嚨回家', '#抽獎', '#心情', '#未來', '#生日', '#週年', '#帶水獺君回家', '#心理學', '#疫苗', '#COVID_19', '#暈針', '#制約', '#焦慮', '#焦慮症', '#畏懼症', '#害怕', '#恐懼', '#臨床心理', '#心理治療', '#行為治療', '#暴露', '#放鬆', '#打針恐懼症', '#psychology', '#anxiety', '#mental_health', '#needle_phobia', '#phobia', '#心理學', '#笑話', '#佛洛依德', '#本我', '#自我', '#超我', '#不一致化解', '#認知心理學', '#幽默', '#薩泰爾', '#博恩', '#老k', '#龍龍', '#文本', '#段子', '#炎上', '#諸葛亮', '#馬謖', '#誰守得住街亭', '#psychology', '#humor', '#str', '#freud', '#心理學', '#科學', '#統計', '#丁特', '#遊戲橘子', '#天堂m', '#機率', '#二項分配', '#數學', '#轉蛋法', '#dinter', '#psychology', '#statistics', '#probability', '#心理學', '#肥宅貓心理測驗', '#心理測驗', '#拖延症', '#拖延症心理測驗', '#肥宅貓', '#line', '#linebot', '#聊天機器人', '#熬夜', '#工作', '#功課', '#做不完', '#宅貓心理室']
        if get_message[0] in Hastags:
            hi = '''為什麼你不難過 https://www.instagram.com/p/CFbwv6gMAow/ #心理學 #心理學應用 #科學 #心靈雞湯 #哀傷 #悲傷五階段 #fivestagesofgrief #rip #心理肥宅貓 #psyfatcat
            ---
            跌倒之後 https://www.instagram.com/p/CF2KyzrFhTY/ #心理學 #心靈雞湯 #心理韌性 #心靈成長
            ---
            成長痛-心理學看電影 https://www.instagram.com/p/CGfUpfoFjOM/ #心理學 #判決 #兒童法案 #自我認同 #認同危機 #成長痛 #Erikson
            ---
            何時才能吃棉花糖-Part_I-經典實驗介紹 https://www.instagram.com/p/CHDGkcalata/ #棉花糖實驗 #自制力 #延宕滿足 #成功語錄 #心理學 #先別急著吃棉花糖 #棉花糖系列
            ---
            何時才能吃棉花糖-Part_II-量化研究的白話文翻譯 https://www.instagram.com/p/CHSrYW-FaM6/ #棉花糖實驗 #自制力 #延宕滿足 #成功語錄 #心理學 #先別急著吃棉花糖 #量化分析 #棉花糖系列
            ---
            何時才能吃棉花糖-Part_III-質化結論的再讀 https://www.instagram.com/p/CHmsTHBFX7k/ #心理學 #先別急著吃棉花糖 #創造力 #自制力 #延宕滿足
            ---
            讓我做你的後盾 https://www.instagram.com/p/CIOPezclQlS/ #心理學 #積極傾聽 #社會支持 #諮商 #陪伴
            ---
            精神疾病的污名 https://www.instagram.com/p/CIucntXF19x/ #心理學 #污名化 #精神疾患 #歧視 #社會關懷 #與疾病共存 #思覺失調 #憂鬱 #身心科 #精神醫學 #服務 #成長 #心靈雞湯
            ---
            脱魯指南-Part_I-大二聖誕節前 https://www.instagram.com/p/CJMGtfZlsHM/ #聖誕節 #吸引力 #社會心理學 #行為學 #reinforce #人本 #自我拓展理論 #交往關係 #渣男 #承諾 #分手 #感情 #愛情心理學 #戀愛 #心理學 #脫單 #告白
            ---
            國高中上課時間更改 https://www.instagram.com/p/CJ0C0r1l0Vz/ #上課時間 #睡眠不足 #學習成效 #填鴨式教育 #專注力 #持續性注意力 #注意力測驗 #教育心理學 #分配時間 #專注時間 #學習時間 #重質不重量 #經濟學 #邊際效應 #心理學 #教育 #國中 #高中 #上課 #放學 #學習 #議題
            ---
            脱魯指南-Part_II-一招讓對方愛上你 https://www.instagram.com/p/CKFvVWTl2TK/ #刷存在感 #單純曝光效果 #連我阿嬤都會 #社會心理學 #好感度 #意識 #習慣 #habituation #無聊 #boredom #反向控制 #防衛機制 #合理化 #否認 #歸因 #attribution #熟悉 #familiarity #熟悉度 #吸引力 #神不知鬼不覺 #心理學 #感情 #愛情 #脫單 #告白 #追求 #語錄
            ---
            脱魯指南-Part_III-外表重要嗎 https://www.instagram.com/p/CKp-sJOltij/ #外表吸引力 #吸引力 #第一印象 #月暈效應 #看臉時代 #大眾臉 #對稱臉 #臉上性別差異 #演化 #健康 #生育能力 #適者生存 #族群繁衍 #脫魯 #修圖 #交友軟體 #化妝 #微整形 #乾乾淨淨 #健健康康 #魅力 #感情 #愛情 #科普 #脫單 #科學 #心理學 #帥哥 #正妹
            ---
            Clubhouse在紅什麼 https://www.instagram.com/p/CLEAAXMldwy/ #抽獎文 #文末抽獎 #文末抽Clubhouse邀請碼 #FB #IG #Clubhouse #疫情 #iPhone #心理學 #認知失調 #改變行為 #改變想法 #邀請碼 #抽獎
            ---
            拖延心理測驗 https://www.instagram.com/p/CL0tsmasepr/ #拖延症 #拖延 #心理測驗 #信效度 #自我保護 #評價性 #自我設限 #Self-Handicap #自我價值 #自尊 #面對挑戰 #成長 #惰性 #具象化 #明確 #截止時間了 #惡魔小鞭鞭 #心理學 #科學 #肥宅 #耍廢 #自我約束
            ---
            拖延症心理測驗分析 https://www.instagram.com/p/CMZ87C3sIk3/ #拖延症 #拖延 #心理測驗 #Dcard #IG #PTT #Other #台灣 #香港 #美國 #中華民國 #金城武 #ANOVA #變異數分析 #相關 #統計 #信度 #效度 #穩定性 #因素分析 #先拖再說 #時間管理 #死到臨頭 #慢 #心理學 #科學 #量化 #資料分析 #懶惰 #耍廢
            ---
            你的名字比你想像的重要-鮭魚之亂 https://www.instagram.com/p/CMrSrZZMOr2/ #台灣 #鮭魚 #心理學 #自我認同 #特質 #改名 #自我接納 #人格 #自我 #運勢 #心理學家 #心理浴場 #鮭魚之亂 #社會 #時事 #評論
            ---
            如何孤獨 https://www.instagram.com/p/CM9yJJrM_RI/ #心理學 #孤獨 #存在 #存在主義 #心理諮商 #心理治療 #精神 #意義 #語錄 #心情 #憂鬱 #焦慮 #成長 #歐文亞隆
            ---
            創傷後壓力症候群 https://www.instagram.com/p/CNh7GlTMGnB/ #創傷 #trauma #DSM-5 #創傷後壓力症候群 #PTSD #侵入性反應 #迴避反應 #認知與情緒的負向轉變 #生理警覺度改變 #心理學 #臨床 #諮商 #心理師 #字典 #太魯閣 #身心科 #精神科 #心理治療
            ---
            痛苦與成長 https://www.instagram.com/p/COURNt2sSte/ #創傷後成長 #PTG #創傷 #新的契機 #人際關係轉變 #力量湧現 #對生命的欣賞 #心靈成長 #生活目標 #自我認同 #生活哲學 #認知反芻 #rumination #憂鬱症 #書寫 #敘說 #梳理 #放棄 #陪伴 #聆聽 #心理浴場 #心理學
            ---
            防疫心理戰 https://www.instagram.com/p/CO7hta0MIm6/ #三級警戒 #疫情 #防疫新生活 #隔離 #檢疫來防止疫情擴散 #遠距教學 #居家辦公 #憂鬱 #焦慮 #情緒低落 #易怒 #害怕 #緊張 #難過 #罪惡感 #困惑 #睡眠品質不佳 #創傷後壓力症 #畏避人群 #酒精依賴 #1925 #衛生福利部 #臺灣社交距離 #臺灣加油 #心理學 #防疫 #新冠肺炎 #covid_19
            ---
            你的主導色不是你的主導色-主導色心理測驗 https://www.instagram.com/p/CPc92hJsIIm/ #主導色 #心理測驗 #心理學家 #音樂心理測驗 #體液學說 #心理健康 #現代醫學之父 #信效度 #心理學 #人格 #性格 #科學 #實事求是 #偵探 #科普 #曉 #鼬
            ---
            告白-心理學看電影 https://www.instagram.com/p/CQA_9CSM1xU/ #confession #告白 #電影 #心理學 #校園霸凌 #私刑正義 #親職教育 #精神疾病 #自體心理學 #Kohut #自戀型人格 #心理學家 #自體 #self #誇大自體 #自我欣賞 #羞愧 #憤怒 #自戀 #心理學 #客體關係 #影評 #成長 #電影推薦
            ---
            畢馬龍效應 https://www.instagram.com/p/CQTznBfMCqK/ #畢馬龍效應 #吸引力法則 #心靈雞湯 #科學 #心理學 #社會心理學 #自證預言 #客體關係 #投射認同 #投射 #projection #誘發 #provocation #回應 #response #認同 #identification #神話 #故事 #Pygmalion #Galatea #Aphrodite #成功 #信念 #執著 #秘密 #教育
            ---
            大公審時代下的自省 https://www.instagram.com/p/CQnIYMWscBb/ #網路公審 #公審 #網路霸凌 #心理歷程 #仇恨言論 #基模 #schema #知識結構 #意識形態 #匿名性 #隔空互動 #娛樂性 #非語言線索 #罪惡感 #認知失調 #mindset #心理學 #同理心 #心情 #政大 #自殺
            ---
            傳貼圖很敷衍嗎 https://www.instagram.com/p/CQ3AzwnMoro/ #抽獎 #抽獎文 #文末抽獎 #line貼圖 #貼圖 #表情符號 #非語言線索 #nonverbal_cue #語言線索 #沒事 #XD
            ---
            同理練習-環南市場篇 https://www.instagram.com/p/CRLyOYMMJn9/ #環南市場 #政治 #心理學 #陳時中 #柯文哲 #林昶佐 #林勝東 #評估 #appraisal #因應 #coping #問題焦點 #情緒焦點 #萬華 #艋舺 #疫情 #防疫 #covid_19 #壓力 #因應
            ---
            給指考戰士的考前一週建議 https://www.instagram.com/p/CRaymm1sABL/ #先安內而後攘外 #領域展開 #早起早睡 #心如止水 #自我肯定 #心理學 #認知心理學 #指考 #指考戰士 #高中 #大學 #考試 #考試加油 #生活 #讀書 #努力 #認真 #成長
            ---
            什麼是憂鬱症 https://www.instagram.com/p/CRvNNKQsUHX/ #心理學 #憂鬱 #憂鬱症 #重鬱症 #抑鬱症 #情緒 #心情 #臨床心理 #心理 #心理師 #身心科 #精神科 #心理疾病 #病因 #病程 #治療 #心理治療 #認知治療 #阿滴 #youtube #youtuber #depression #majordepressivedisorder #mdd #psychology #clinical #psychiatry #psychopathology #psychotherapy
            ---
            奧運心理學 https://www.instagram.com/p/CR_EpNCHE-u/ #正向性格 #動機 #信心 #專注 #社會支持 #奧運 #東京奧運 #東奧 #台灣 #台灣加油 #中華隊 #選手 #加油 #集氣 #金牌 #銀牌 #銅牌 #心理學 #心理韌性 #運動 #olympics #tokyo2020 #psychology #resilience #taiwan #chinesetaipei #台湾です
            ---
            為什麼我看比賽就會輸 https://www.instagram.com/p/CSByUSZHdKt/ #每看必輸 #沒看就贏 #鍋貼 #紅內褲 #迷信 #儀式 #心理學 #行為學 #制約 #操作制約 #史金納 #增強 #懲罰 #奧運 #東京奧運 #東奧 #台灣 #台灣加油 #中華隊 #加油 #集氣 #olympics #tokyo2020 #psychology #taiwan #chinesetaipei #conditioning #skinner
            ---
            父親節快樂 https://www.instagram.com/p/CST9QGBpN3u/ #心理學 #心理 #父親節 #父愛 #紀錄片 #愛 #貼心 #同理 #照顧 #母嬰關係 #psychology #father #fathersday #caring #love #empathy
            ---
            量化科學的心理學應用-單純曝光效果驗證 https://www.instagram.com/p/CSls9EJnBMD/ #心理學 #心理 #單純曝光效果 #科普 #統計 #心理統計 #卡方 #檢定 #假設 #科學 #量化 #刷存在 #存在感 #R #程式 #code
            ---
            心理系在幹嘛 https://www.instagram.com/p/CStMzzyHyYY/ #社會心理學 #認知心理學 #發展心理學 #性格心理學 #知覺心理學 #生理心理學 #變態心理學 #心理統計 #心理測驗 #心理實驗 #心理系 #心理學 #心理師 #臨床 #諮商 #科學 #讀心術 #指考 #學測 #考大學 #轉學考 #選系 #選校
            ---
            閣樓裡的側寫師-什麼是罪犯側寫 https://www.instagram.com/p/CTHMUeRHVd8/ #心理學 #犯罪學 #犯罪心理學 #罪犯側寫 #暴力 #犯罪 #偵查 #偵探 #犯罪現場 #受害者 #邏輯 #歸納法 #演繹法 #科學 #側寫師 #閣樓裡的側寫師 #psychology #criminal #offender #profiling
            ---
            疫苗心理學-心理副作用 https://www.instagram.com/p/CTZvNCipUtl/ #心理學 #認知 #歸因 #焦慮 #疫苗 #AZ #莫德納 #BNT #高端 #疫情 #covid_19 #安慰劑 #反安慰劑 #CDC #抽獎 #心理 #心情 #psychology #vaccine #moderna #肺炎
            ---
            童年創傷-長大後的身心適應 https://www.instagram.com/p/CT9NwacpRGz/ #心理學 #創傷 #童年 #逆境 #虐待 #暴力 #家暴 #酒癮 #藥癮 #忽略 #健康 #預防 #心情 #情緒 #感情 #家人 #成長 #長大 #psychology #mentalhealth
            ---
            20210922-年度回顧 https://www.instagram.com/p/CURinOAJjnX/ #抽獎 #心情 #回顧 #生日 #週年 #帶空嚨嚨回家
            ---
            20210922-未來展望 https://www.instagram.com/p/CURizFupQvX/ #抽獎 #心情 #未來 #生日 #週年 #帶水獺君回家
            ---
            暈針 https://www.instagram.com/p/CUh9I94JJiQ/ #心理學 #疫苗 #COVID_19 #暈針 #制約 #焦慮 #焦慮症 #畏懼症 #害怕 #恐懼 #臨床心理 #心理治療 #行為治療 #暴露 #放鬆 #打針恐懼症 #psychology #anxiety #mental_health #needle_phobia #phobia
            ---
            笑話文本分析 https://www.instagram.com/p/CUzeubmJVhv/ #心理學 #笑話 #佛洛依德 #本我 #自我 #超我 #不一致化解 #認知心理學 #幽默 #薩泰爾 #博恩 #老k #龍龍 #文本 #段子 #炎上 #諸葛亮 #馬謖 #誰守得住街亭 #psychology #humor #str #freud
            ---
            宅貓統計教室-遊戲橘子欺騙玩家? https://www.instagram.com/p/CVIgQj_pdL9/ #心理學 #科學 #統計 #丁特 #遊戲橘子 #天堂m #機率 #二項分配 #數學 #轉蛋法 #dinter #psychology #statistics #probability
            ---
            宅貓機器人-拖延症心理測驗 https://www.instagram.com/p/CWcfwxBLGP7/ #心理學 #肥宅貓心理測驗 #心理測驗 #拖延症 #拖延症心理測驗 #肥宅貓 #line #linebot #聊天機器人 #熬夜 #工作 #功課 #做不完 #宅貓心理室
            ---
            閣樓裡的側寫師-心理病態 https://www.instagram.com/p/CXN5CBbJVMU/ #反社會型人格 #反社會人格 #反社會 #心理病態 #心理變態 #心理學 #犯罪學 #犯罪心理學 #罪犯側寫 #暴力 #犯罪 #犯罪 #科學 #側寫師 #閣樓裡的側寫師 #psychopathy #sociopath #psychopath #psychology #criminal #offender #profiling
            ---
            閣樓裡的側寫師-反社會型人格 https://www.instagram.com/p/CXiFerxJx3F/ #反社會型人格 #反社會人格 #反社會 #心理病態 #心理變態 #心理學 #犯罪學 #犯罪心理學 #罪犯側寫 #暴力 #犯罪 #犯罪 #科學 #側寫師 #閣樓裡的側寫師 #psychopathy #sociopath #psychopath #psychology #criminal #offender #profiling
            ---
            脫魯指南-Part_IV-聖誕節一起去看恐怖電影吧 https://www.instagram.com/p/CXvAvglLDib/ #聖誕節 #脫單 #脫魯指南 #心理學 #社會心理學 #戀愛心理學 #戀愛 #愛情 #感情 #吸引力 #心動 #恐怖電影 #錯誤歸因 #錯覺 #吊橋實驗 #情緒 #身體激發 #psychology #attribution'''
            hi2 = hi.split('---')
            ArtDict = {i.split()[0]:i.split()[1:] for i in hi2}
            TextArt = f'想看看 {get_message[0][1:]} 相關的文章?\n'
            for key, value in ArtDict.items():
                if get_message[0] in value:
                    TextArt += f'\n{key}\n{value[0]}\n'
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text = TextArt))
        else:
            reply = TextSendMessage(text=f'目前心理肥宅貓沒有關於 {get_message[0][1:]} 的文章，趕快去ig私訊宅貓你想看的文章！')
            line_bot_api.reply_message(event.reply_token, reply)
    if get_message[0] == '心理測驗':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text = '拖延症測驗請輸入:\nProcrastination\n\n心理病態特質測驗請輸入：\nPsychopathy\n\n性成癮測驗請輸入：\nSexualAddiction\n\n(請注意大小寫噢！)'))
    if get_message[0] == 'SexualAddiction':
        if len(get_message) == 3:
            raw_score = sum([int(i) for i in ''.join(get_message[1:])])
            if raw_score < 23:
                result_text = f'你的得分是{raw_score}\n結果顯示你沒有性成癮噢，恭喜XD'
            else:
                result_text = f'你的得分是{raw_score}\n結果顯示你可能有性成癮><\n\n不過實際狀況仍須依專業臨床工作者的評估噢！'
            reply = TextSendMessage(text = result_text + '\n\n\n馬上前往了解更多心理學知識: https://www.instagram.com/')
            line_bot_api.reply_message(event.reply_token, reply)
        else:
            reply = TextSendMessage(text = '請判斷您與以下每一個陳述句的相似程度\n1分，表示不像我\n2分，表示一點點像我\n3分，表示部分像我\n4分，表示非常像我\n\n請依照以下格式依序回應噢！\n-\n\nSexualAddiction\n13112 41124\n\n-\n1.我的性慾阻礙到了我的人際關係\n2.我的性行為及對性的想法造成我生活上的困擾\n3.我對性愛的渴望打亂了我的日常生活\n4.我有時候會因為我的性行為造成我違背承諾或失責\n5.我有時候會性飢渴到無法控制自己\n6.我發現我在工作時也會想到性\n7.我對性的想法與感受比對我自己本身還強烈\n8.我必須很努力的去控制我對性的想法及行為\n9.我比我希望的還要多地去想到性\n10.對我來說很難找到一個像我一樣想性愛的性伴侶')
            line_bot_api.reply_message(event.reply_token, reply)
    if get_message[0] == 'Psychopathy':
        if len(get_message) == 5:
            raw_score = [int(i) for i in ''.join(get_message[1:])]
            fac_score = [0, 0, 0, 0, 0]
            fac_criteria = [0, 6, 6, 7.5, 7.5]
            fac_item = [1, 1, 3, 1, 1, 2, 2, 2, 3, 4, 0, 4, 3, 3, 3, 2, 0, 4, 4, 4]
            fac_domain = ['', '「人際關係」', '「情感」', '「生活風格」', '「反社會」']
            for i, j in zip(raw_score, fac_item):
                fac_score[j] += i
            if sum(fac_score) < 30:
                result_text = '結果顯示你沒有心理病態特質噢，恭喜XD'
            else:
                fac_text = []
                for i in range(1,5):
                    if fac_score[i] >= fac_criteria[i]:
                        fac_text.append(fac_domain[i])
                if fac_text:
                    result_text = '結果顯示你可能有心理病態特質><\n\n你的心理病態特質出現在'+', '.join(fac_text)+'面向上\n\n不過實際狀況仍須依專業臨床工作者的評估噢！'
                else:
                    result_text = '結果顯示你可能有心理病態特質><\n\n不過實際狀況仍須依專業臨床工作者的評估噢！'
            reply = TextSendMessage(text = result_text + '\n\n\n馬上前往了解更多心理病態知識: https://www.instagram.com/p/CXN5CBbJVMU/')
            line_bot_api.reply_message(event.reply_token, reply)
        else:
            reply = TextSendMessage(text = '請判斷您與以下每一個陳述句的符合程度\n0分，表示不符合\n1分，表示部分符合\n2分，表示符合\n\n請依照以下格式依序回應噢！\n-\n\nPsychopathy\n22222 11220\n12212 22102\n\n-\n1.我是能言善道、會做表面功夫、且常被認為是有魅力的人\n2.我有十分良好的自我價值感，甚至有些自戀\n3.我容易感到無聊，常需要追求刺激\n4.我慣性說謊或喜歡欺騙別人\n5.我是一個奸巧且會操弄別人以獲取好處的人\n6.我很少對於我不好的行為感到後悔或罪惡\n7.我看似能表達強烈情緒，但實際上我內心沒有太大的情緒感受\n8.我是冷酷且缺乏同理心的人\n9.我雖然能自己賺錢生活，但傾向仰賴他人經濟支持而生活\n10.我很難控制自己的行為\n11.我的性生活很淫亂\n12.我小時候就常有違規的行為（如，偷竊、欺瞞、...）\n13.我缺乏實際且長遠的目標規劃\n14.我是衝動的\n15.我是不負責任的\n16.我常無法或不願為自己的行為負責\n17.我有過許多短期的伴侶關係（結婚或具承諾的親密關係）\n18.我有青少年的犯罪紀錄\n19.我曾被撤銷假釋（假釋中故意再犯）\n20.我的犯罪類型十分多樣')
            line_bot_api.reply_message(event.reply_token, reply)
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
            raw_score = ''.join(get_message[1:])
            revItem = [2, 3, 5, 7, 10, 12, 13, 14, 17, 19]
            tran_score = [6-int(raw_score[i]) if i in revItem else int(raw_score[i]) for i in range(20)]
            fac_score = [0, 0, 0, 0, 0]
            fac_dic = {1:[21.04942, 5.011986], 2:[12.67442, 2.655944], 3:[8.97093, 2.657137], 4:[12.38372, 2.94227]}
            fac_item = [0, 1, 4, 4, 3, 2, 0, 2, 0, 1, 4, 1, 4, 1, 1, 3, 3, 2, 1, 2]
            for i, j in zip(tran_score, fac_item):
                fac_score[j] += i
            fac_T = [round(((fac_score[i] - fac_dic[i][0])/fac_dic[i][1]) * 10 + 50, 2) for i in range(1, 5)]
            dic_per = {20:0.01, 21:0.01, 22:0.01, 23:0.02, 24:0.03, 25:0.04, 26:0.05, 27:0.07, 28:0.09, 29:0.12, 30:0.16, 31:0.21, 32:0.27, 33:0.35, 34:0.45, 35:0.57, 36:0.73, 37:0.92, 38:1.15, 39:1.43, 40:1.77, 41:2.18, 42:2.66, 43:3.23, 44:3.89, 45:4.66, 46:5.55, 47:6.57, 48:7.73, 49:9.03, 50:10.49, 51:12.12, 52:13.92, 53:15.89, 54:18.03, 55:20.35, 56:22.83, 57:25.48, 58:28.28, 59:31.22, 60:34.29, 61:37.46, 62:40.72, 63:44.04, 64:47.41, 65:50.8, 66:54.18, 67:57.53, 68:60.83, 69:64.05, 70:67.17, 71:70.18, 72:73.05, 73:75.78, 74:78.36, 75:80.76, 76:83, 77:85.06, 78:86.95, 79:88.67, 80:90.21, 81:91.6, 82:92.84, 83:93.93, 84:94.88, 85:95.71, 86:96.43, 87:97.05, 88:97.58, 89:98.02, 90:98.39, 91:98.71, 92:98.96, 93:99.18, 94:99.35, 95:99.49, 96:99.6, 97:99.69, 98:99.76, 99:99.82, 100:99.86}
            reply = TextSendMessage(text = f'你的拖延分數是「{sum(fac_score)}」分\n你比 {dic_per[sum(fac_score)]}% 的台灣人還要會拖\n\n細項分析:\n就是愛拖(T分數): {fac_T[0]}\n時間管理困難(T分數): {fac_T[1]}\n死到臨頭型(T分數): {fac_T[2]}\n動作慢(T分數): {fac_T[3]}\n\nP.S. T分數平均為50，標準差為10，如果超過50分表示比平均高，高過越多就越需留意噢XD\n\n延伸閱讀:\n拖延心理學: https://www.instagram.com/p/CL0tsmasepr/\n台灣人拖延調查分析: https://www.instagram.com/p/CMZ87C3sIk3/')
            line_bot_api.reply_message(event.reply_token, reply)
        else:
            reply = TextSendMessage(text='一般人會使用以下的陳述句來形容自己\n請判斷您與以下每一個陳述句的符合程度\n1分表示非常不符合\n5分表示非常符合\n\n請依照以下格式依序回應噢！\n-\n\n\nProcrastination\n31452 13422\n23334 45222\n\n\n-\n1.我經常在做我幾天前就想做的事情\n2.直到快要交作業前我才會寫它\n3.當我看完圖書館借來的書後，不管是否到期，我都會馬上歸還\n4.每當早上起床時間一到，我幾乎都馬上起床\n5.在我寫完信後，回過個幾天才寄出\n6.我一般都是立刻回撥電話\n7.即使是很簡單的工作，我也很少在幾天內完成\n8.我經常很快速地做出決定\n9.我通常會延遲我必須要做的工作\n10.我經常需要很匆忙地趕作業才得以準時完成它\n11.當準備要外出時，我很少在最後一刻才發現有什麼事情必須去做\n12.在為一些有截止期限的事情做準備時，我經常浪費時間做其他事\n13.我喜歡提前赴約\n14.我經常在作業指派後沒多久就開始做作業\n15.我經常比必須完工的時間更早完成工作\n16.我總是在最後一刻才去買生日禮物或聖誕禮物\n17.即使是必需品，我也經常到最後一刻才買\n18.我經常能完成我一天中計劃好要做的所有事\n19.我一直在說「我明天會做」\n20.在晚上休息之前我通常會先安頓好所有必須做的事情')
            line_bot_api.reply_message(event.reply_token, reply)

