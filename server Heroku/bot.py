import requests
from firebase import firebase

TOKEN = "303253879:AAGlGdiEJhIO933iVpJg2-tiRJwhpqC4o6g"
db = firebase.FirebaseApplication("https://jkdev-news.firebaseio.com/")


class Bot:
    url = ""

    def __init__(self, token):
        self.url = "https://api.telegram.org/bot%s/" % token

    def sendmessage(self, chat_id, text):
        url = self.url + "sendMessage?chat_id=%s&text=%s" % (chat_id, text)
        requests.get(url)

    def getKeyboard(self, chat_id, text, js):
        url = self.url + "sendMessage?chat_id=%s&text=%s&reply_markup=%s" % (chat_id, text, js)
        requests.post(url)


bot = Bot(TOKEN)


class Chat:
    chat_id = ""

    def __init__(self, chat_id):
        self.chat_id = chat_id

    def sendmessage(self, text):
        bot.sendmessage(self.chat_id, text)

    def getKeyBoard(self, text, js):
        bot.getKeyboard(self.chat_id, text, js)


class Message:
    chat_id = ""
    text = ""

    def __init__(self, requestJson):
        self.chat_id = requestJson["message"]["chat"]["id"]
        self.text = requestJson["message"]["text"]


class ChatInfo:
    chat_id = ""
    login = ""

    def __init__(self, chat_id, login):
        self.chat_id = chat_id
        self.login = login

    def update(self):
        db.post("/ChatInfo/CHAT" + self.chat_id, self.login)

    @staticmethod
    def getlogin(chat_id):
        d = db.get("/ChatInfo", "CHAT"+str(chat_id))
        if d is not None:
            for i in d.values():
                return i
        return

