import redis


class RedisCache:
    topic = None
    redis_client = None

    def __init__(self, hostname, key, topic):
        self.topic = topic
        self.redis_client = redis.StrictRedis(host=hostname,
                                              port=6380,
                                              password=key,
                                              ssl=True, ssl_cert_reqs=u'none')
        if not self.redis_client.ping():
            raise Exception("We can't connect to the redis server, please check the config")

    def get_offset(self):
        offset = self.redis_client.get(self.topic)
        if offset is None:
            return "-1"
        else:
            return int(offset)

    def set_offset(self, sequence_number):
        self.redis_client.set(self.topic, sequence_number)
