import redis
import json
import datetime
import re
import pickle

DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'

def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")


def datetime_parser(dct):
    for k, v in dct.items():
        if isinstance(v, basestring) and re.search("\d{4}-\d{1,2}-\d{1,2}T", v):
            try:
                v, _, ms = v.partition('.')
                dct[k] = datetime.datetime.strptime(v, DATE_FORMAT)
                dct[k] += datetime.timedelta(microseconds=int(ms))
            except:
                pass
    return dct


class ElastiCache(object):
    def __init__(self, host, port):

        self.redis = redis.StrictRedis(host=host,
                                       port=int(port),
                                       db=0,
                                       )

    def get(self, name, ex=None, callback=None):
        '''

        :param name:
        :param ex:
        :param callback:
        :return:
        '''
        value = self.redis.get(name)
        if value and value[0] in {'{', '['} and value[-1] in {'}', ']'}:
            try:
                value = json.loads(value, object_hook=datetime_parser)
            except:
                pass
        elif isinstance(value, object):
            try:
                value = pickle.loads(value)
            except:
                pass

        if not value and callback:
            value = callback(name)
            if value:
                self.set(name, value, ex)
        return value

    def set(self, name, value, ex=None):
        '''
        :param name:
        :param value:
        :param ex: expire in seconds
        :return:
        '''
        if isinstance(value, dict) or isinstance(value, list) or isinstance(value, tuple):
            value = json.dumps(value, default=datetime_handler)
        elif isinstance(value, object):
            value = pickle.dumps(value)
        return self.redis.set(name, value, ex=int(ex) if ex else None)

    def lpush(self, name, value):
        if isinstance(value, dict) or isinstance(value, list) or isinstance(value, tuple):
            value = json.dumps(value, default=datetime_handler)
        return self.redis.lpush(name, value)

    def lrange(self, name, start=0, end=100):
        values = self.redis.lrange(name, start, end)
        items = []
        for value in values:
            if isinstance(value, str) or isinstance(value, unicode):
                if value[0] in {'{', '['} and value[-1] in {'}', ']'}:
                    try:
                        value = json.loads(value, object_hook=datetime_parser)
                    except:
                        pass
            items.append(value)
        return items

    def mget(self, names):
        names = self.redis.keys(names)
        if not names: return None
        values = self.redis.mget(names)
        items = []
        for value in values:
            if isinstance(value, str) or isinstance(value, unicode):
                if value[0] in {'{', '['} and value[-1] in {'}', ']'}:
                    try:
                        value = json.loads(value, object_hook=datetime_parser)
                    except:
                        pass
            items.append(value)
        return items

    def delete(self, names):
        self.redis.delete(names)


if __name__ == '__main__':

    '''
    Turn on ssh for local testing
    ssh -L 6379:redis.vb7e4x.0001.use1.cache.amazonaws.com:6379 phuong@52.205.118.35
    '''

    import ConfigParser
    import os

    #
    cache = ElastiCache('127.0.0.1', 6379)
    cache.set('foo2', {
        'a': 1,
        'b': 'string',
        'c': 1.1
    })
    print(cache.get('foo2'))
    cache.delete('foo2')
    print(cache.get('foo2'))
    from pprint import pprint
    import pickle
    # pprint(cache.lrange('user:-70Xzpab1m5l', 0, 10))
    # cache.redis.rename('user:7BvGnROA1ox-', 'user:7BvGnROA1ox')
    # cache.redis.delete('user:7BvGnROA1ox')

    # pprint(cache.mget('d427a9a9a23777545cdefa22203d0af15d725475'))
    # a = cache.get('maker-audi')
    # print(a.description)







