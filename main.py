import requests
import sqlite3
connection=sqlite3.connect('previous')
cursor=connection.cursor()
import time
import subprocess
import os
import signal
cursor.execute('''CREATE TABLE IF NOT EXISTS news(
    name text,
    title text,
    content text,
    link varchar(255),
    picture varchar(255)
)''')
connection.commit()
while True:
    try:
        a=(requests.get('https://coinhooked.com/wp-admin/admin-ajax.php?action=fetch_posts&stream-id=1&disable-cache=',headers={'_gat':'1'}))
    except:
        time.sleep(60)
        continue
    a=(a.json())
    a=a['items'][0]

    name=a['screenname']
    if name=='Cointelegraph':
        picture='https://cointelegraph.com/assets/img/logo.png'
    else:
        picture=a['userpic'].replace('\\/','/')

    title=a['header']
    content=a['text']
    link=a['permalink']
    if 'This is a paid-for submitted press release.' not in content:
        cursor.execute('''SELECT * FROM news where link="%s"'''%(link))
        if len(cursor.fetchall())==0:
            cursor.execute('''DELETE FROM news where link=(SELECT link from news)''')
            cursor.execute('''INSERT INTO news VALUES(
            "%s",
            "%s",
            "%s",
            "%s",
            "%s")
            '''%(name,title,content,link,picture))
            connection.commit()
            pro = subprocess.Popen('python3 test123.py', stdout=subprocess.PIPE,
                                   shell=True, preexec_fn=os.setsid)

            time.sleep(10)
            os.killpg(os.getpgid(pro.pid), signal.SIGTERM)