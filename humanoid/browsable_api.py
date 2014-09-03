class BrowsableApi(object):

    def __init__(self, endpoint, url):
        self.title = endpoint.replace("_", " ").title()

        self.endpoint = endpoint
        self.url = url
