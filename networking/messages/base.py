from socket import gethostname


class BaseMessage(object):
    def __init__(self):
        self.sender = gethostname()
