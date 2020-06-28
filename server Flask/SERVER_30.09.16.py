import flask
from flask import request

app = flask.Flask(__name__)


class Country:
    name = ""
    capital = ""
    gcd = 0
    head = None
    next = None

    def __init__(self, name, capital, gcd):
        self.name = name
        self.capital = capital
        self.gcd = gcd

    def election(self, name):
        self.head = name

    def change_GCD(self, newGcd):
        self.gcd = newGcd

    def show(self):
        print('Country - ' + self.name + ',', end=' ')
        print('Capital - ' + self.capital + ',', end=' ')
        print('GCD is ' + str(self.gcd) + ',', end=" ")
        if self.head is not None:
            print("Leader - " + self.head)
        else:
            print('No Leader')

    def show_next(self):
        self.next.show()

    def set_next(m, n):
        m.next = n
        n.next = m

    def return_(self):
        x = str(self.name) + ' ' + str(self.capital) + ' ' + str(self.gcd) + ' ' + str(self.head) + '\n'
        x += str(self.next.name) + ' ' + str(self.next.capital) + ' ' + str(self.next.gcd) + ' ' + str(
            self.next.head) + '\n'
        return x


def hash_(a):
    hash_end = 0

    for pos in range(len(a)):
        hash_end += ord(a[pos]) * (30 ** pos)

    return hash_end % 50000


@app.route("/GetHash")  # Получаем хеш из параметра 'str', [GET]
def url():
    a = flask.request.args.get("str")

    x = hash_(a)

    return '<!DOCTYPE HTML><p>RESULT =  %s</p>' % x  # возвращать можно только строку


@app.route("/postHello", methods=['POST'])  # С помощью cmd отправляем POST запрост и возвращаем хеш
def hello_post():
    get_param_from_post = flask.request.form['str']
    my_hash = hash_(get_param_from_post)

    print(get_param_from_post)

    return "\n Hash = %s \n" % str(my_hash)


@app.route("/solve")  # Решаем Задачи из контеста-3
def backpack():
    task = flask.request.args.get("task")
    data = flask.request.args.get("data")
    if task == 'backpack':  # РЮКЗАК
        data = data.split(',')
        for i in range(len(data)):
            data[i] = int(data[i])

        kolvo = data[0]
        ves = data[1]
        mid = (len(data) + 2) / 2
        weight = data[2:int(mid)]
        cost = data[int(mid):]
        weight.insert(0, 0)
        cost.insert(0, 0)

        mas = []
        for i in range(kolvo + 1):
            mas.append([0] * (ves + 1))

        for n in range(1, kolvo + 1):
            for m in range(ves + 1):
                mas[n][m] = mas[n - 1][m]
                if m >= weight[n] and mas[n - 1][m - weight[n]] + cost[n] > mas[n][m]:
                    mas[n][m] = mas[n - 1][m - weight[n]] + cost[n]

        return "Your result is: %s" % str(mas[kolvo][ves])
    elif task == 'min_backpack':  # МИНИМУМ ПРЕДМЕТОВ
        data = data.split(',')
        for i in range(len(data)):
            data[i] = int(data[i])

        n = data[0]
        m = data[1]
        mass = data[2:]

        a = [0] * 100000

        for i in range(n):
            for j in range(m, 0, -1):
                if a[j] != 0:
                    if a[j + mass[i]] != 0:
                        a[j + mass[i]] = min(a[j + mass[i]], 1 + a[j])
                    else:
                        a[j + mass[i]] = a[j] + 1

            a[mass[i]] = 1

        return "Your result is: %s" % str(a[m])

    else:
        return "WRONG PARAM"


@app.route('/index')  # Возврыщает HTML
def index():
    user = {'nickname': 'Misha'}
    return '''
<html>

    <head>
      <title>Home Page</title>
    </head>

    <body>
        <img src='https://cdn3.iconfinder.com/data/icons/seo-and-marketing-1-10/97/25-512.png'>
    </body>

</html>
'''


@app.route('/search')  # Ищет страну, method = [GET]
def search():
    name = flask.request.args.get('query')
    print(name)
    result = ''
    usa = Country('USA', 'Washington', 16)
    eng = Country('England', 'London', 2)
    rus = Country('Russia', 'Moscow', 20)
    fra = Country('France', 'Paris', 10)

    usa.election('TRUMP')
    rus.election('PUTIN')
    eng.election('Elizabeth I')

    Country.set_next(rus, usa)
    dic = {usa.name: usa, rus.name: rus, eng.name: eng, fra.name: fra}

    if name in dic:
        dic[name].show()
        if dic[name].next is not None:
            dic[name].next.show()
        else:
            print("No opponent in The 2018 FIFA World Cup")
    else:
        print("No such country in Data Base")

    return 'Done'


@app.route('/election', methods=['POST'])
def election():
    usa = Country('USA', 'Washington', 16)
    eng = Country('England', 'London', 2)
    rus = Country('Russia', 'Moscow', 20)
    fra = Country('France', 'Paris', 10)

    name = flask.request.form['name']
    head = flask.request.form['head']

    dic = {usa.name: usa, rus.name: rus, eng.name: eng, fra.name: fra}

    print(dic[name].head)

    dic[name].election(head)

    return dic[name].name + '\n' + dic[name].head + '\n'


@app.route('/next', methods=['POST'])
def nextVisitor():
    home = flask.request.form['home']
    visitor = flask.request.form['visitor']

    usa = Country('USA', 'Washington', 16)
    eng = Country('England', 'London', 2)
    rus = Country('Russia', 'Moscow', 20)
    fra = Country('France', 'Paris', 10)

    dic = {usa.name: usa, rus.name: rus, eng.name: eng, fra.name: fra}

    Country.set_next(dic[home], dic[visitor])
    print(home)
    dic[home].show(), dic[home].show_next()

    print(visitor)
    dic[visitor].show(), dic[visitor].show_next()

    m = dic[home].return_()
    return m


@app.route("/mmc")  # Получаем хеш из параметра 'str', [GET]
def test():
    return '''<html>
 <head>
  <meta charset="utf-8">
  <title></title>
 </head>
 <body>

 <form action="result" method="POST">

    <select name="mmm">
    <option>KETListening</option>
    <option>KETReading</option>
    <option>KETSpeaking</option>
    <option>PETListening</option>
    <option>PETReading</option>
    <option>PETWriting</option>
    <option>PETSpeaking</option>
    <option>FCEListening</option>
    <option>FCEReading</option>
    <option>FCEUseOfEnglish</option>
    <option>FCEWriting</option>
    <option>FCESpeaking</option>
    <option>CAEListening</option>
    <option>CAEReading</option>
    <option>CAEUseOfEnglish</option>
    <option>CAEWriting</option>
    <option>CAESpeaking</option>
    </select>
  <p><b>Score:</b><br>
   <input type="text" name="test" size="40">
  </p>

  <p><input type="submit" value="Отправить"></p>
 </form>

 </body>
</html>'''


@app.route("/result", methods=['POST'])
def res():
    r = request.form['test']
    q = request.form['mmm']
    return flask.redirect('%s?score=%s' % (q, r))


@app.route("/KETListening")
def test1():
    KETListening = [['25', '150'], ['24', '145'],
                    ['23', '140'], ['22', '135'], ['21', '130'], ['20', '127'], ['19', '125'], ['18', '123'],
                    ['17', '120'],
                    ['16', '116'], ['15', '112'], ['14', '108'], ['13', '104'], ['12', '102'], ['11', '100'],
                    ['10', '96'],
                    ['9', '92'], ['8', '88'], ['7', '85'], ['6', '82']]
    a = flask.request.args.get("score")
    num = "NOT FOUND"
    for i in KETListening:
        if a in i:
            num = i[1]
    return num


@app.route("/KETReading")
def test2():
    a = flask.request.args.get("score")
    KETReading = [['60', '150'], ['59', '148'], ['58', '146'],
                  ['57', '144'], ['56', '142'], ['55', '140'], ['54', '137'], ['53', '135'], ['52', '133'],
                  ['51', '131'],
                  ['50', '130'], ['49', '129'], ['48', '128'], ['47', '127'], ['46', '126'], ['45', '125'],
                  ['44', '124'],
                  ['43', '123'], ['42', '122'], ['41', '121'], ['40', '120'], ['39', '119'], ['38', '118'],
                  ['37', '117'],
                  ['36', '116'], ['35', '115'], ['34', '114'], ['33', '113'], ['32', '112'], ['31', '111'],
                  ['30', '110'],
                  ['29', '108'], ['28', '106'], ['27', '104'], ['26', '102'], ['25', '100'], ['24', '98'], ['23', '96'],
                  ['22', '94'], ['21', '92'], ['20', '90'], ['19', '89'], ['18', '88'], ['17', '86'], ['16', '85'],
                  ['15', '84'],
                  ['14', '83'], ['13', '82']]

    num = "NOT FOUND"
    for i in KETReading:
        if a in i:
            num = i[1]
    return num


@app.route("/KETSpeaking")
def test3():
    a = flask.request.args.get("score")
    KETSpeaking = [['45', '150'], ['44', '148'], ['43', '145'], ['42', '142'], ['41', '140'], ['40', '139'],
                   ['39', '138'],
                   ['38', '137'],
                   ['37', '135'], ['36', '134'], ['35', '132'], ['34', '131'], ['33', '129'], ['32', '128'],
                   ['31', '126'],
                   ['30', '125'], ['29', '123'], ['28', '122'], ['27', '120'], ['26', '119'], ['25', '117'],
                   ['24', '115'],
                   ['23', '112'], ['22', '109'], ['21', '106'], ['20', '104'], ['19', '102'], ['18', '100'],
                   ['17', '98'],
                   ['16', '96'], ['15', '94'], ['14', '90'], ['13', '88'], ['12', '86'], ['11', '84'], ['10', '82']]
    num = "NOT FOUND"
    for i in KETSpeaking:
        if a in i:
            num = i[1]
    return num


@app.route("/PETListening")
def test4():
    a = flask.request.args.get("score")
    PETListening = [['25', '170'],
                    ['24', '165'],
                    ['23', '160'], ['22', '158'], ['21', '154'], ['20', '150'], ['19', '145'], ['18', '140'],
                    ['17', '139'],
                    ['16', '138'], ['15', '136'], ['14', '132'], ['13', '128'], ['12', '124'], ['11', '120'],
                    ['10', '118'],
                    ['9', '114'], ['8', '110'], ['7', '106'], ['6', '104'], ['5', '102']]
    num = "NOT FOUND"
    for i in PETListening:
        if a in i:
            num = i[1]
    return num


@app.route("/PETReading")
def test5():
    a = flask.request.args.get("score")
    PETReading = [['35', '170'], ['34', '167'], ['33', '163'],
                  ['32', '160'], ['31', '158'], ['30', '156'], ['29', '153'], ['28', '149'], ['27', '146'],
                  ['26', '143'],
                  ['25', '140'], ['24', '138'], ['23', '136'], ['22', '134'], ['21', '131'], ['20', '129'],
                  ['19', '127'],
                  ['18', '125'], ['17', '123'], ['16', '121'], ['15', '120'], ['14', '118'], ['13', '117'],
                  ['12', '115'],
                  ['11', '112'], ['10', '110'], ['9', '107'], ['8', '104'], ['7', '102']]
    num = "NOT FOUND"
    for i in PETReading:
        if a in i:
            num = i[1]
    return num


@app.route("/PETWriting")
def test6():
    a = flask.request.args.get("score")
    PETWriting = [['25', '170'], ['24', '165'], ['23', '160'],
                  ['22', '157'], ['21', '155'], ['20', '152'], ['19', '148'], ['18', '144'], ['17', '140'],
                  ['16', '137'],
                  ['15', '135'], ['14', '132'], ['13', '128'], ['12', '124'], ['11', '120'], ['10', '116'],
                  ['9', '110'],
                  ['8', '107'], ['7', '104'], ['6', '102']]
    num = "NOT FOUND"
    for i in PETWriting:
        if a in i:
            num = i[1]
    return num


@app.route("/PETSpeaking")
def test7():
    a = flask.request.args.get("score")
    PETSpeaking = [['30', '170'], ['29', '167'], ['28', '163'],
                   ['27', '160'], ['26', '158'], ['25', '156'], ['24', '154'], ['23', '152'], ['22', '150'],
                   ['21', '147'],
                   ['20', '145'], ['19', '142'], ['18', '140'], ['17', '137'], ['16', '135'], ['15', '133'],
                   ['14', '129'],
                   ['13', '126'], ['12', '120'], ['11', '117'], ['10', '113'], ['9', '109'], ['8', '105'], ['7', '102']]
    num = "NOT FOUND"
    for i in PETSpeaking:
        if a in i:
            num = i[1]
    return num


@app.route("/FCEListening")
def test8():
    a = flask.request.args.get("score")
    FCEListening = [['30', '190'], ['29', '187'],
                    ['28', '183'], ['27', '180'], ['26', '178'], ['25', '176'], ['24', '175'], ['23', '173'],
                    ['22', '171'],
                    ['21', '169'], ['20', '167'], ['19', '164'], ['18', '160'], ['17', '159'], ['16', '157'],
                    ['15', '153'],
                    ['14', '149'], ['13', '144'], ['12', '140'], ['11', '138'], ['10', '133'], ['9', '127'],
                    ['8', '122']]
    num = "NOT FOUND"
    for i in FCEListening:
        if a in i:
            num = i[1]
    return num


@app.route("/FCEReading")
def test9():
    a = flask.request.args.get("score")
    FCEReading = [['42', '190'],
                  ['41', '188'],
                  ['40', '186'], ['39', '184'], ['38', '182'], ['37', '180'], ['36', '179'], ['35', '178'],
                  ['34', '176'],
                  ['33', '174'], ['32', '172'], ['31', '171'], ['30', '170'], ['29', '168'], ['28', '166'],
                  ['27', '164'],
                  ['26', '162'], ['25', '161'], ['24', '160'], ['23', '158'], ['22', '155'], ['21', '153'],
                  ['20', '150'],
                  ['19', '147'], ['18', '145'], ['17', '142'], ['16', '140'], ['15', '136'], ['14', '133'],
                  ['13', '130'],
                  ['12', '127'], ['11', '125'], ['10', '122']]
    num = "NOT FOUND"
    for i in FCEReading:
        if a in i:
            num = i[1]
    return num


@app.route("/FCEUseOfEnglish")
def test10():
    a = flask.request.args.get("score")
    FCEUseOfEnglish = [['28', '190'], ['27', '188'], ['26', '185'],
                       ['25', '183'], ['24', '180'], ['23', '177'], ['22', '174'], ['21', '170'], ['20', '166'],
                       ['19', '163'],
                       ['18', '160'], ['17', '158'], ['16', '156'], ['15', '153'], ['14', '150'], ['13', '146'],
                       ['12', '143'],
                       ['11', '140'], ['10', '137'], ['9', '133'], ['8', '127'], ['7', '122']]
    num = "NOT FOUND"
    for i in FCEUseOfEnglish:
        if a in i:
            num = i[1]
    return num


@app.route("/FCEWriting")
def test11():
    a = flask.request.args.get("score")
    FCEWriting = [['40', '190'], ['39', '189'], ['38', '187'],
                  ['37', '185'], ['36', '183'], ['35', '181'], ['34', '180'], ['33', '178'], ['32', '176'],
                  ['31', '174'],
                  ['30', '172'], ['29', '170'], ['28', '168'], ['27', '166'], ['26', '164'], ['25', '162'],
                  ['24', '160'],
                  ['23', '158'], ['22', '156'], ['21', '153'], ['20', '150'], ['19', '146'], ['18', '144'],
                  ['17', '142'],
                  ['16', '140'], ['15', '137'], ['14', '133'], ['13', '130'], ['12', '127'], ['11', '124'],
                  ['10', '122']]
    num = "NOT FOUND"
    for i in FCEWriting:
        if a in i:
            num = i[1]
    return num


@app.route("/FCESpeaking")
def test12():
    a = flask.request.args.get("score")
    FCESpeaking = [['60', '190'],
                   ['59', '189'],
                   ['58', '187'], ['57', '185'], ['56', '183'], ['55', '181'], ['54', '180'], ['53', '179'],
                   ['52', '178'],
                   ['51', '177'], ['50', '176'], ['49', '175'], ['48', '173'], ['47', '172'], ['46', '171'],
                   ['45', '170'],
                   ['44', '169'], ['43', '168'], ['42', '167'], ['41', '166'], ['40', '165'], ['39', '163'],
                   ['38', '162'],
                   ['37', '161'], ['36', '160'], ['35', '159'], ['34', '158'], ['33', '157'], ['32', '155'],
                   ['31', '152'],
                   ['30', '151'], ['29', '149'], ['28', '147'], ['27', '146'], ['26', '144'], ['25', '142'],
                   ['24', '140'],
                   ['23', '139'], ['22', '137'], ['21', '135'], ['20', '133'], ['19', '131'], ['18', '130'],
                   ['17', '128'],
                   ['16', '126'], ['15', '124'], ['14', '122']]
    num = "NOT FOUND"
    for i in FCESpeaking:
        if a in i:
            num = i[1]
    return num


@app.route("/CAEListening")
def test13():
    a = flask.request.args.get("score")
    CAEListening = [['30', '210'], ['29', '208'],
                    ['28', '205'], ['27', '203'], ['26', '200'], ['25', '198'], ['24', '196'], ['23', '194'],
                    ['22', '191'],
                    ['21', '188'], ['20', '185'], ['19', '183'], ['18', '180'], ['17', '176'], ['16', '173'],
                    ['15', '170'],
                    ['14', '165'], ['13', '160'], ['12', '150'], ['11', '142']]
    num = "NOT FOUND"
    for i in CAEListening:
        if a in i:
            num = i[1]
    return num


@app.route("/CAEReading")
def test14():
    a = flask.request.args.get("score")
    CAEReading = [['50', '210'],
                  ['49', '209'], ['48', '208'], ['47', '207'], ['46', '205'], ['45', '203'], ['44', '202'],
                  ['43', '200'],
                  ['42', '198'], ['41', '196'], ['40', '194'], ['39', '192'], ['38', '189'], ['37', '187'],
                  ['36', '185'],
                  ['35', '183'], ['34', '182'], ['33', '181'], ['32', '180'], ['31', '178'], ['30', '177'],
                  ['29', '175'],
                  ['28', '173'], ['27', '170'], ['26', '167'], ['25', '165'], ['24', '163'], ['23', '160'],
                  ['22', '158'],
                  ['21', '155'], ['20', '153'], ['19', '149'], ['18', '145'], ['17', '142']]
    num = "NOT FOUND"
    for i in CAEReading:
        if a in i:
            num = i[1]
    return num


@app.route("/CAEUseOfEnglish")
def test15():
    a = flask.request.args.get("score")
    CAEUseOfEnglish = [['28', '210'], ['27', '208'], ['26', '206'], ['25', '204'], ['24', '202'], ['23', '200'],
                       ['22', '198'],
                       ['21', '195'], ['20', '193'], ['19', '190'], ['18', '187'], ['17', '184'], ['16', '180'],
                       ['15', '178'],
                       ['14', '172'], ['13', '168'], ['12', '164'], ['11', '160'], ['10', '152'], ['9', '148'],
                       ['8', '142']]
    num = "NOT FOUND"
    for i in CAEUseOfEnglish:
        if a in i:
            num = i[1]
    return num


@app.route("/CAEWriting")
def test16():
    a = flask.request.args.get("score")
    CAEWriting = [['40', '210'], ['39', '208'], ['38', '206'], ['37', '205'], ['36', '204'], ['35', '202'],
                  ['34', '200'], ['33', '197'], ['32', '195'], ['31', '193'], ['30', '191'], ['29', '189'],
                  ['28', '187'],
                  ['27', '185'], ['26', '183'], ['25', '181'], ['24', '180'], ['23', '178'], ['22', '175'],
                  ['21', '173'],
                  ['20', '170'], ['19', '168'], ['18', '165'], ['17', '163'], ['16', '160'], ['15', '157'],
                  ['14', '154'],
                  ['13', '151'], ['12', '148'], ['11', '145'], ['10', '142']]
    num = "NOT FOUND"
    for i in CAEWriting:
        if a in i:
            num = i[1]
    return num


@app.route("/CAESpeaking")
def test17():
    a = flask.request.args.get("score")
    CAESpeaking = [['75', '210'],
                   ['74', '209'], ['73', '208'], ['72', '207'], ['71', '206'], ['70', '205'], ['69', '204'],
                   ['68', '203'],
                   ['67', '202'], ['66', '201'], ['65', '200'], ['64', '199'], ['63', '198'], ['62', '197'],
                   ['61', '196'],
                   ['60', '195'], ['59', '194'], ['58', '193'], ['57', '192'], ['56', '191'], ['55', '190'],
                   ['54', '189'],
                   ['53', '188'], ['52', '187'], ['51', '186'], ['50', '185'], ['49', '184'], ['48', '183'],
                   ['47', '182'],
                   ['46', '181'], ['45', '180'], ['44', '178'], ['43', '175'], ['42', '173'], ['41', '172'],
                   ['40', '171'],
                   ['39', '170'], ['38', '169'], ['37', '168'], ['36', '167'], ['35', '166'], ['34', '165'],
                   ['33', '163'],
                   ['32', '162'], ['31', '161'], ['30', '160'], ['29', '159'], ['28', '158'], ['27', '157'],
                   ['26', '156'],
                   ['25', '155'], ['24', '154'], ['23', '152'], ['22', '150'], ['21', '149'], ['20', '147'],
                   ['19', '146'],
                   ['18', '144'], ['17', '142']]
    num = "NOT FOUND"
    for i in CAESpeaking:
        if a in i:
            num = i[1]
    return num


if __name__ == '__main__':
    app.run(debug=True)
