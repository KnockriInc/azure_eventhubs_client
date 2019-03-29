from azure_eventhubs_client.producer import Producer

if __name__ == "__main__":
    # name of the eventhub/topic
    EVENTHUB = "myeventhub"
    # Address can be in either of these formats:
    # "amqps://<URL-encoded-SAS-policy>:<URL-encoded-SAS-key>@<mynamespace>.servicebus.windows.net/myeventhub"
    # "amqps://<mynamespace>.servicebus.windows.net/myeventhub"
    # For example:
    ADDRESS = f"amqps://namespace.servicebus.windows.net/{EVENTHUB}"
    # SAS policy and key are not required if they are encoded in the URL
    # the following is the user
    SharedAccessKeyName = "RootManageSharedAccessKey"
    KEY = "Primary key | Secondary key"

    producer = Producer(ADDRESS, SharedAccessKeyName, KEY)
    for i in range(10):
        producer.send(i)
        print(i)
    producer.stop()
