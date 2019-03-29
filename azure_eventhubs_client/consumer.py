from azure.eventhub import EventHubClient, Offset

from .redis_cache import RedisCache


class Consumer:
    consumer_group = None
    eventhubs_client = None
    offset = Offset("-1")
    redis_cache = None

    def __init__(self, eventhub, address, user, key,
                 consumer_group, redis_hostname, redis_key):
        self.consumer_group = consumer_group
        self.eventhubs_client = EventHubClient(address,
                                               debug=False,
                                               username=user,
                                               password=key)

        redis_topic = f"eventhubs-{eventhub}-{consumer_group}"
        self.redis_cache = RedisCache(redis_hostname, redis_key, redis_topic)

    def recieve(self):
        OFFSET = Offset(self.redis_cache.get_offset())
        receiver = self.eventhubs_client.add_receiver(self.consumer_group,
                                                      "0",
                                                      prefetch=5000,
                                                      offset=OFFSET)
        self.eventhubs_client.run()
        messages = receiver.receive(timeout=100)
        self.eventhubs_client.stop()
        return messages

    def commit(self, event_data):
        self.redis_cache.set_offset(event_data.sequence_number)
