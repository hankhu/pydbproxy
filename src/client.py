#!/usr/bin/python

from dbproxy import *

def test():
    url = "http://127.0.0.1:8000/"
    conn = Connection(url, "sqlite3", ":memory:")
    cur = conn.cursor()
    print cur
    cur.execute("create table a(abc, def)")
    cur.execute("insert into a values(1, 2)")
    for i in range(100):
            cur.execute("select * from a")
            print cur.fetchall()
    print cur.close()
    print conn.close()
    
if __name__ == '__main__':

    test()
