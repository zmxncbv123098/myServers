# This Python file uses the following encoding: utf-8


import os
from bottle import run, route, request, get, post, static_file, redirect
import requests
from firebase import firebase
from UsersDB import UsersDB
import json
from bot import bot, Chat, Message, ChatInfo
from Functions import *

UNVERIFIED_USERS = []


class User:
    login = ""
    pwd = ""
    mail = ""
    telegram = ""
    chat_id = ""
    subscriptions = {}

    def __init__(self, login, pwd, mail, telegram, subscriptions):
        self.login = login
        self.pwd = pwd
        self.mail = mail
        self.telegram = telegram
        self.subscriptions = subscriptions

    @staticmethod
    def get_from_auth(login):
        d = db.get(AUTH_TABLE_ADR, login)
        try:
            for i in d.values():
                return i
        except:
            return None

    @staticmethod
    def login_exists(login):
        res = User.get_from_auth(login) is not None
        return res

    def exists(self):
        print(self.login)
        return User.login_exists(self.login)

    @staticmethod
    def get(login):

        def evolve(subs):
            for s in SOURCES:
                if s not in subs:
                    subs[s] = []

        d = User.get_from_auth(login)
        return User(d['login'],
                    d['pwd'],
                    d.get('mail', None),
                    d.get('telegram', None),
                    evolve(d.get('subscriptions', {})))

    @staticmethod
    def register(user):
        if not user.exists():
            db.post(AUTH_TABLE_ADR + "/" + user.login, user.__dict__)
            print(user.__dict__)
            return status_message(200, 'Registration success')
        return status_message(406, 'Username already taken')

    @staticmethod
    def delete(login):
        user = User.get(login)
        if user.exists():
            db.delete(AUTH_TABLE_ADR, login)

    def update(self):
        User.delete(self.login)
        User.register(self)

    def add_subscription(self, source, subscription):
        if not isinstance(self.subscriptions, dict):
            self.subscriptions = {}

        if source not in self.subscriptions.keys():
            print("NOT IN KEYS!")
            self.subscriptions[source] = []

        print(self.subscriptions)
        self.subscriptions[source].append(subscription)

        self.update()

    def delete_subscriptions(self, source, *subscriptions):
        for sub in subscriptions:
            subs = self.subscriptions.get(source, None)
            if subs is not None:
                if sub in subs:
                    subs.remove(sub)
                else:
                    return status_message(404, "Subscription not found")
            else:
                return status_message(404, "Source not found")
        self.update()


@post('/')
def hello():
    global chat
    TOKEN = "303253879:AAGlGdiEJhIO933iVpJg2-tiRJwhpqC4o6g"

    requests.get('https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=ok' % (TOKEN, chat.chat_id))
    print(request.json)
    msg = Message(request.json)
    chat = Chat(msg.chat_id)

    if msg.chat_id in UNVERIFIED_USERS:

        login = msg.text
        try:
            user = User.get(login)
            user.chat_id = chat.chat_id
            user.update()
            UNVERIFIED_USERS.remove(msg.chat_id)
            chat.sendmessage("Вы добавлены в рассылку!")
        except:
            chat.sendmessage("No such user!!")
            msg.text = '/start'

    if msg.text == '/start':
        chat.sendmessage("Введите Ваш логин:")
        UNVERIFIED_USERS.append(msg.chat_id)

    elif msg.text == 'VK':
        text = "Parser result for VK"
        login = ChatInfo.getlogin(msg.chat_id)
        user = User.get(login)
        subs = user.subscriptions
        if subs is not None:
            chat.sendmessage(str(subs))
        else:
            chat.sendmessage("Ваши подписки")

        json_keyboard = json.dumps({'keyboard': [["VK"], ["Instagram"]],
                                    'one_time_keyboard': False,
                                    'resize_keyboard': True})
        bot.getKeyboard(msg.chat_id, text, json_keyboard)

    elif msg.text == 'Instagram':
        text = "Parser result for Instagram"

        json_keyboard = json.dumps({'keyboard': [["VK"], ["Instagram"]],
                                    'one_time_keyboard': False,
                                    'resize_keyboard': True})

        bot.getKeyboard(msg.chat_id, text, json_keyboard)

    else:
        json_keyboard = json.dumps({'keyboard': [["VK"], ["Instagram"]],
                                    'one_time_keyboard': False,
                                    'resize_keyboard': True})

        bot.getKeyboard(msg.chat_id, "Choose source!", json_keyboard)
        print(request.json)


@route('/test/<url>')
def index(url):
    url_id = ShortUrlToId(url)
    a = UsersDB()
    final_url = a.fetch('SELECT destination FROM links WHERE id=\'%s\'' % url_id)[0][0]
    return redirect(final_url)


@route('/addUrl')
def addUrl():
    url = request.query['url']
    a = UsersDB()
    add_url_to_links(url)
    res = IdToShortUrl(a.fetch('SELECT id FROM links WHERE destination=\'%s\'' % url)[0][0])
    return res


@route('/showUrl')
def show():
    a = UsersDB()
    b = show_all_urls_in_links()
    return b

@route('/result')



@route('/mmc')
def show():

    return '''
<!DOCTYPE HTML>
<html>
 <head>
  <meta charset="utf-8">
  <title></title>
 </head>
 <body>

 <form name="test" action="showUrl">
  <p><b>Choose your exam:</b><Br>
   <input type="radio" name="browser" value="ie"> KET<Br>
   <input type="radio" name="browser" value="opera"> PET<Br>
   <input type="radio" name="browser" value="firefox"> FCE<Br>
   <input type="radio" name="browser" value="firefox"> CAE<Br>
  </p>

  <p><b>Score:</b><br>
   <input type="text" size="40">
  </p>

  <p><input type="submit" value="Отправить">
   <input type="reset" value="Очистить"></p>
 </form>

 </body>
</html>

    '''


run(host='0.0.0.0', port=os.environ.get('PORT', 5000), quiet=False)
