import time

from azure_eventhubs_client.consumer import Consumer

if __name__ == "__main__":
    # name of the eventhub/topic
    EVENTHUB = "myeventhub"
    # Address can be in either of these formats:
    # "amqps://<URL-encoded-SAS-policy>:<URL-encoded-SAS-key>@<mynamespace>.servicebus.windows.net/myeventhub"
    # "amqps://<mynamespace>.servicebus.windows.net/myeventhub"
    # For example:
    ADDRESS = f"amqps://namespace.servicebus.windows.net/{EVENTHUB}"
    # SAS policy and key are not required if they are encoded in the URL
    SharedAccessKeyName = "RootManageSharedAccessKey"
    KEY = "Primary key | Secondary key"

    # These details can be found in "Access Keys" section
    REDIS_HOSTNAME = "namespace.redis.cache.windows.net"
    REDIS_KEY = "Primary key"

    consumer = Consumer(EVENTHUB,
                        ADDRESS,
                        SharedAccessKeyName,
                        KEY,
                        "$Default",
                        REDIS_HOSTNAME, REDIS_KEY)

    for message in consumer.recieve():
        print(message.body_as_str())
        consumer.commit(message)
        time.sleep(1)
