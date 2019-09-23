from .utils import get_url


class S3DirectFile():
    def __init__(self, key):
        self.key = key
        self.url = get_url(self.key) if key else key

    def __str__(self):
        return self.url
