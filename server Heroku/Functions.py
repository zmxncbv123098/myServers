from UsersDB import UsersDB
import time

a = UsersDB()


def createLinksTable():
    a.query(
        'CREATE TABLE links(id INTEGER NOT NULL PRIMARY KEY autoincrement UNIQUE, destination TEXT, isDeleted INTEGER);'
    )
    return


def createVisitsTable():
    a.query(
        'CREATE TABLE visits(id INTEGER NOT NULL PRIMARY KEY autoincrement UNIQUE, vk_id INTEGER, link_id INTEGER, fromWhere TEXT, date INTEGER);'
    )
    return


def createUsersTable():
    a.query(
        'CREATE TABLE users(uid INTEGER NOT NULL, first_name TEXT, last_name TEXT, sex INTEGER, bday INTEGER, city INTEGER, country INTEGER, home_town INTEGER, university_ids TEXT, schools_ids TEXT, followers INTEGER, relation INTEGER, groups_ids TEXT, date_creation INTEGER);'
    )

# ----------------------------------------------------------------


def IdToShortUrl(Id):

    def reverse(s):
        new_s = ''
        for i in range(1, (len(s) + 1)):
            new_s += s[len(s) - i]
        return new_s

    mapp = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    ShortUrl = ''

    while int(Id) != 0:
        ShortUrl += mapp[Id % 62]
        Id = int(Id / 62)

    return reverse(ShortUrl)


def ShortUrlToId(ShortUrl):
    Id = 0

    for i in range(0, len(ShortUrl)):
        if 'a' <= ShortUrl[i] <= 'z':
            Id = Id * 62 + ord(ShortUrl[i]) - ord('a')
        if 'A' <= ShortUrl[i] <= 'Z':
            Id = Id * 62 + ord(ShortUrl[i]) - ord('A') + 26
        if '0' <= ShortUrl[i] <= '9':
            Id = Id * 62 + ord(ShortUrl[i]) - ord('0') + 52

    return Id

# ----------------------------------------------------------------


def find_url_in_links_by_id(Id):
    result = a.fetch('Select * from links where id = \'%s\';' % Id)
    return result[0][1]


def show_all_urls_in_links():
    text = ''
    for elem in a.fetch('Select * from links;'):
        text += str(elem[0]) + ': ' + str(elem[1]) + ' Short=' + str(IdToShortUrl(elem[0])) + ' || '
    return text

# ----------------------------------------------------------------


def add_url_to_links(url):
    a.query(
        'INSERT INTO links(destination) values (\'%s\')' % url
    )


def addUser(d):
    if len(a.fetch('Select * from users where uid = %d' % d['uid'])) == 0:
        a.query('INSERT INTO users(uid) values(%d)' % d['uid'])

    uid = d['uid']
    del d['uid']
    for key in d.keys():
        a.query('UPDATE users SET \'%s\'=\'%s\' WHERE uid=\'%s\'' % (key, d[key], uid))
    a.query('UPDATE users SET date_creation=\'%s\' WHERE uid=\'%s\'' % (time.clock(), uid))
    return


def addVisit(link_id, vk_id, fromWhere):
    a.query(
        'INSERT INTO visits(vk_id, link_id, fromWhere) values (%d,%d,\'%s\')' % (vk_id, link_id, fromWhere)
    )
    return
