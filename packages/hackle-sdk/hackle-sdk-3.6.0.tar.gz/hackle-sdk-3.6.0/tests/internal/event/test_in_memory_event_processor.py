class InMemoryEventProcessor(object):
    def __init__(self):
        self.__events = []

    @property
    def processed_events(self):
        return list(self.__events)

    def process(self, event):
        self.__events.append(event)
