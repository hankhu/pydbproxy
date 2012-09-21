#!/usr/bin/python
#DBAPI-2.0 spec: http://www.python.org/dev/peps/pep-0249/
import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer

#new code
#import BaseHTTPServer
#def not_insane_address_string(self):
#    host, port = self.client_address[:2]
#    return '%s (no getfqdn)' % host #used to call: socket.getfqdn(host)
#BaseHTTPServer.BaseHTTPRequestHandler.address_string = \
#    not_insane_address_string
#end new code

def is_even(n):
	return n%2 == 0

conn_cache = {}
cur_cache = {}
def db_conn(drv, *args, **kwargs):
	print "drv:", drv
	print "args:", args
	print "kwargs:", kwargs
	exec "drv=__import__('%s')" % drv
	conn = drv.connect(*args, **kwargs)
	conn_id = str(id(conn))
	conn_cache[conn_id] = conn
	return conn_id

def db_commit(conn_id):
	conn_cache[conn_id].commit()
	return 1

def db_rollback(conn_id):
	conn_cache[conn_id].rollback()
	return 1

def db_close(conn_id):
	conn_cache[conn_id].close()
	del conn_cache[conn_id]
	return 1

def db_cursor(conn_id):
	cur = conn_cache[conn_id].cursor()
	cur_id = str(id(cur))
	cur_cache[cur_id] = cur
	return cur_id

def db_cur_desc(cur_id):
	return cur_cache[cur_id].description

def db_cur_rowcount(cur_id):
	return cur_cache[cur_id].rowcount

def db_callproc(cur_id, name, *args, **kwargs):
	cur_cache[cur_id].callproc(name, *args, **kwargs)
	reuturn 1

def db_execute(cur_id, *qargs):
	cur_cache[cur_id].execute(*qargs)
	return 1

def db_executemany(cur_id, *qargs):
	cur_cache[cur_id].executemany(*qargs)
	return 1

def db_fetchone(cur_id):
	return cur_cache[cur_id].fetchone()

def db_fetchall(cur_id):
	return cur_cache[cur_id].fetchall()

def db_fetchmany(cur_id, size):
	return cur_cache[cur_id].fetchmany(size)

def db_nextset(cur_id):
	return cur_cache[cur_id].nextset() or 0

def db_cur_close(cur_id):
	cur_cache[cur_id].close()
	del cur_cache[cur_id]
	return 1

server = SimpleXMLRPCServer(("127.0.0.1", 8000))
print "Listening on port 8000..."

server.register_function(is_even,"is_even")
server.register_function(db_conn,"db_conn")
server.register_function(db_cursor,"db_cursor")
server.register_function(db_execute,"db_execute")
server.register_function(db_fetchall,"db_fetchall")
server.register_function(db_cur_close,"db_cur_close")
server.register_function(db_close,"db_close")
server.serve_forever()
