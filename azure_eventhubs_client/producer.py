from azure.eventhub import EventHubClient, EventData


class Producer:
    client = None
    sender = None

    def __init__(self, address, user, key):
        self.client = EventHubClient(address,
                                     debug=False,
                                     username=user,
                                     password=key)
        self.sender = self.client.add_sender(partition="0")
        self.client.run()

    def send(self, msg):
        self.sender.send(EventData(str(msg)))

    def stop(self):
        self.client.stop()
