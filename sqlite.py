import time
import sqlite3
conn = sqlite3.connect('docs/information.db', check_same_thread=False)
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users(login TEXT, time TEXT);""")
conn.commit()
def databasetrace(user_name, date):
    date = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(date))
    user = (user_name, date)
    cur.execute("INSERT INTO users(login, time) VALUES(?, ?);", user)
    conn.commit()
def getdatabase():
    logins = []
    attendance = []
    cur.execute("SELECT * FROM users;")
    all_results = cur.fetchall()
    for each in sorted(all_results):
        if len(logins) == 0:
            logins.append(each[0])
            attendance.append(1)
        elif each[0] != logins[-1]:
            logins.append(each[0])
            attendance.append(1)
        else:
            attendance[-1] += 1
    return logins, attendance