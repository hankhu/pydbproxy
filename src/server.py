#!/usr/bin/python
#DBAPI-2.0 spec: http://www.python.org/dev/peps/pep-0249/
import sys, xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer

HOST, PORT = ("127.0.0.1", 8000)

obj_cache = {}
def db_conn(drv, *args, **kwargs):
    print "drv:", drv
    print "args:", args
    print "kwargs:", kwargs
    #exec "drv=__import__('%s')" % drv
    drv = __import__(drv)
    conn = drv.connect(*args, **kwargs)
    _id = str(id(conn))
    obj_cache[_id] = conn
    return _id

def db_cursor(conn_id):
    cur = obj_cache[conn_id].cursor()
    cur_id = str(id(cur))
    obj_cache[cur_id] = cur
    return cur_id

def get_attr(_id, name):
    print "get_attr:", _id, name
    return getattr(obj_cache[_id], name)

def call_method_ret(_id, name, *args, **kwargs):
    method = getattr(obj_cache[_id], name)
    return method(*args, **kwargs)

def call_method(_id, name, *args, **kwargs):
    method = getattr(obj_cache[_id], name)
    method(*args, **kwargs)
    return 0

def main():
    server = SimpleXMLRPCServer((HOST, PORT), allow_none=True)
    server.register_function(db_conn,"db_conn")
    server.register_function(db_cursor,"db_cursor")
    server.register_function(get_attr,"get_attr")
    server.register_function(call_method_ret,"call_method_ret")
    server.register_function(call_method,"call_method")
    server.serve_forever()

if __name__ == '__main__':
    if len(sys.argv>2):
        HOST, PORT = sys.argv[1:3]
    

    main()
