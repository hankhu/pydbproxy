#!/usr/bin/python

import xmlrpclib

proxy = xmlrpclib.ServerProxy("http://127.0.0.1:8000/")
print "3 is even: %s" % str(proxy.is_even(3))
print "100 is even: %s" % str(proxy.is_even(100))

cid = proxy.db_conn("sqlite3", ":memory:")
cur_id = proxy.db_cursor(cid)
proxy.db_execute(cur_id, "create table a(abc, def)")
proxy.db_execute(cur_id, "insert into a values(1, 2)")
for i in range(100):
	proxy.db_execute(cur_id, "select * from a")
	print proxy.db_fetchall(cur_id)
print proxy.db_cur_close(cur_id)
print proxy.db_close(cid)
