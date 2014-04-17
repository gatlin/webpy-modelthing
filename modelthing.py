import web
import settings
import copy
import json

db = web.database(dbn=settings.DBN,
                   db=settings.DATABASE)

def make_obj(cls,params):
    return cls(**params)

class ModelThing(object):
    '''
    A base class for dabatase models.
    '''

    _table  = None
    _fields = {}
    _exists = False
    _dirty  = True

    def __init__(self, **kwargs):
        '''
        If we are given attributes, store them.
        The presence of an `id` property means this object
        already exists.
        '''
        self._fields = copy.copy(kwargs)

    @classmethod
    def retrieve(cls, **kwargs):
        '''
        Get one specific object from the database matching the key/value pairs
        in kwargs.
        '''
        try:
            if len(kwargs.keys()) == 0:
                clause = {"1":1}
            else:
                clause = kwargs
            # We get back a dictionary of fields
            _data =  db.select(cls._table,
                               where=web.db.sqlwhere(clause),
                               limit=1)
            _d = _data.list()[0]
            c = cls(**_d)
            c._exists = True
            c._dirty  = False
            return c

        except IndexError:
            return None

    @classmethod
    def list(cls, **kwargs):
        if len(kwargs.keys()) == 0:
            __data =  db.select(cls._table)
        else:
            __data =  db.select(cls._table,
                                where = web.db.sqlwhere(kwargs))

        cs = map(lambda x: dict(x), __data.list())
        xs = []
        for c in cs:
            i = cls(**c)
            i._exists = True
            i._dirty  = False
            xs.append(i)
        return xs

    def save(self):
        '''
        Either insert or delete this entry, depending on context.
        '''
        success = False
        if self._exists:   # update
            try:
                _id = self._fields["id"]
                db.update(self._table,
                          where="id=$id",
                          vars = dict(id=_id),
                          **self._fields)
                success = True
                self._dirty = False
            except IndexError:
                success = False

        else:               # insert
            newId = db.insert(self._table,
                             **self._fields)
            self._exists = True
            self._dirty  = False
            self._fields["id"] = newId
            success = True

        return success

    def delete(self):
        '''
        Delete this object from the database.
        '''
        try:
            _id = self._fields["id"]
            db.delete(self._table,
                      where="id=$id",
                      vars=dict(id=_id))
            return True
        except IndexError:
            return False

    def isdirty(self):
        return self._dirty

    def __str__(self):
        return unicode(self)

    def __getattr__(self,name):
        if name in self._fields:
            return self._fields[name]
        else:
            return self.__dict__[name]

    def __setattr__(self,name,value):
        if name in self._fields:
            self._fields[name] = value
            self._dirty = True
        else:
            self.__dict__[name] = value

    def tojson(self):
        return json.dumps(self._fields)

    @classmethod
    def multitojson(cls,xs):
        lst = []
        for x in xs:
            lst.append(x._fields)
        return json.dumps(lst)

    @classmethod
    def fromjson(cls, js):
        decoded = json.loads(js)
        if isinstance(decoded, list):
            ''' Multiple objects '''
            objs = []
            for o in decoded:
                c = cls(**o)
                if "id" in c._fields:
                    c._exists = True
                else:
                    c._dirty  = False
                objs.append(c)
            return objs
        else:
            ''' Just the one '''
            obj = cls(**decoded)
            if "id" in obj._fields:
                obj._exists = True
            else:
                obj._dirty = False
            return obj
