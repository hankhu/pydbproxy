#!/usr/bin/python

import xmlrpclib

class ProxyMethod(object):
    def __init__(self, owner, name):
        self.owner = owner
        self.name = name
    def __call__(self, *args, **kwargs):
        return self.owner.proxy.call_method_ret(self.owner._id, self.name, *args, **kwargs)

class ReturnOwner(ProxyMethod):
    def __init__(self, *args, **kwargs):
        ProxyMethod.__init__(self, *args, **kwargs)
    def __call__(self, *args, **kwargs):
        self.owner.proxy.call_method(self.owner._id, self.name, *args, **kwargs)
        return self.owner
    
class ProxyClass(object):
    def __getattr__(self, name):
        if name in self.__methods__:
            if name in self.__retowner_methods__:
                return ReturnOwner(self, name)
            else:
                return ProxyMethod(self, name)
        else:
            return self.proxy.get_attr(self._id, name)

class Cursor(ProxyClass):
    __methods__ = ('callproc', 'close', 'execute', 'executemany', 'fetchone', \
        'fetchmany', 'fetchall', 'nextset', 'setinputsizes', 'setoutputsize')
    __retowner_methods__ = ('execute', 'executemany')
    __attrs__ = ('description', 'rowcount', 'arraysize')
    def __init__(self, conn):
        self.proxy = conn.proxy
        self._id = self.proxy.db_cursor(conn._id)

class Connection(ProxyClass):
    __methods__ = ('close', 'commit', 'rollback', 'cursor')
    __retowner_methods__ = ()
    def __init__(self, url, drv, *args, **kwargs):
        self.url = url
        self.proxy = xmlrpclib.ServerProxy(url)
        self._id = self.proxy.db_conn(drv, *args, **kwargs)
    def cursor(self):
        return Cursor(self)

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
