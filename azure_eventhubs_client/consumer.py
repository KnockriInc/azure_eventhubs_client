from azure.eventhub import EventHubClient, Offset

from .redis_cache import RedisCache


class Consumer:
    consumer_group = None
    eventhubs_client = None
    offset = Offset("-1")
    redis_cache = None  # Leaving in here for backward compatibility
    partition_ids = []
    redis_cache_partition_aware = {}

    def __init__(self, eventhub, address, user, key,
                 consumer_group, redis_hostname, redis_key):
        self.consumer_group = consumer_group
        self.eventhubs_client = EventHubClient(address,
                                               debug=False,
                                               username=user,
                                               password=key)

        # Leaving in here for backward compatibility
        redis_topic = f"eventhubs-{eventhub}-{consumer_group}"
        self.redis_cache = RedisCache(redis_hostname, redis_key, redis_topic)

        self.partition_ids = self.eventhubs_client.get_eventhub_info()[
            'partition_ids']

        for partition_id in self.partition_ids:
            redis_topic = f"eventhubs-{eventhub}-{consumer_group}-{partition_id}"
            self.redis_cache_partition_aware[partition_id] = RedisCache(
                redis_hostname, redis_key, redis_topic)

    def recieve(self):
        messages = []
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

    def receive_all_partitions(self):
        messages = []
        for partition_id in self.partition_ids:

            OFFSET = Offset(
                self.redis_cache_partition_aware[partition_id].get_offset())

            receiver = self.eventhubs_client.add_receiver(self.consumer_group,
                                                          partition_id,
                                                          prefetch=5000,
                                                          offset=OFFSET)
            self.eventhubs_client.run()
            for message in receiver.receive(timeout=100):
                messages.append(
                    {"message": message, "partition_id": partition_id})
        self.eventhubs_client.stop()
        return messages

    def commit_all_partitions(self, event_data):
        self.redis_cache_partition_aware[event_data['partition_id']].set_offset(
            event_data['message'].sequence_number)
