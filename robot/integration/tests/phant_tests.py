from httmock import urlmatch, HTTMock, all_requests, response
import json
import phant
import unittest


BASE_URL = r'data.sparkfun.com'
PUBLIC = 'foo'
PRIVATE = 'bar'


def json_response(data):
    return response(200, data, {'Content-Type': 'application/json'})


class Server(object):

    def __init__(self):
        self.remaining_requests = 100
        self.remaining_bytes = 50 * 1024 * 1024
        self.used_bytes = 0

    @urlmatch(scheme=r'http', netloc=BASE_URL, path=r'/input/foo.json')
    def mock_input(self, url, request):
        self.remaining_requests -= 1
        self.remaining_bytes -= 1
        self.used_bytes += 1
        return json_response(json.dumps({'success': True}))

    @urlmatch(scheme='http', netloc=BASE_URL, path='/output/' + PUBLIC + '/stats.json')
    def mock_stats(self, url, request):
        stats = dict(remaining=self.remaining_bytes,
                     used=self.used_bytes)
        return json_response(json.dumps(stats))


class RequestTests(unittest.TestCase):

    def setUp(self):
        self.server = Server()

    def test_stats(self):
        with HTTMock(self.server.mock_input, self.server.mock_stats):
            p = phant.Phant(PUBLIC, 'field', private_key=PRIVATE)
            remaining, used = p.remaining_bytes, p.used_bytes
            p.log(123)
            self.assertLess(p.remaining_bytes, remaining)
            self.assertGreater(p.used_bytes, used)
