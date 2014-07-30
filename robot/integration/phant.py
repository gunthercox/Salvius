import sys
import datetime
import requests as rq


if sys.version_info[0] < 3:
    def only_strings_in(iterable):
        return all((isinstance(x, (str, unicode)) for x in iterable))
else:
    def only_strings_in(iterable):
        return all((isinstance(x, str) for x in iterable))


def check_json_response(response):
    if isinstance(response, dict) and not response['success']:
        raise ValueError(response['message'])


class Phant(object):

    def __init__(self, public_key, *fields, **kwargs):
        """
        *fields is a tuple containg the field names of the stream identified by
        *public_key*. **kwargs can additionally contain the *private_key*, the
        *delete_key* and an alternative *base_url*.
        """
        if not only_strings_in(fields):
            raise ValueError("String type expected for *fields")

        self.public_key = public_key
        self.private_key = kwargs.pop('private_key', None)
        self.delete_key = kwargs.pop('delete_key', None)
        self.base_url = kwargs.pop('base_url', None) or 'http://data.sparkfun.com'
        self._fields = fields
        self._stats = None
        self._last_headers = None

    def log(self, *args):
        """
        Log arguments. args must match the fields and the object must be
        created with a *private_key*.
        """
        self._check_private_key("log data")
        params = {'private_key': self.private_key}
        params.update(dict((k, v) for k, v in zip(self._fields, args)))
        response = rq.post(self._get_url('input'), params=params)
        check_json_response(response.json())

        self._last_headers = response.headers
        self._stats = None

    def clear(self):
        """
        Clear data from stream. Object must be created with a *private_key*.
        """
        self._check_private_key("clear data")
        headers = {'Phant-Private-Key': self.private_key}
        rq.delete(self._get_url('input', ext=''), headers=headers)

    def get(self, convert_timestamp=True):
        """
        Return the data as a list of dictionaries.

        If *convert_timestamp* is False, the timestamps will not be converted to
        datetime.datetime objects.
        """
        response = rq.get(self._get_url('output')).json()
        check_json_response(response)

        if convert_timestamp:
            pattern = '%Y-%m-%dT%H:%M:%S.%fZ'
            for entry in response:
                timestamp = entry['timestamp']
                entry['timestamp'] = datetime.datetime.strptime(timestamp, pattern)

        return response

    @property
    def remaining_requests(self):
        """Number of remaining requests."""
        return self._get_limit('Remaining')

    @property
    def request_limit(self):
        """Request limit."""
        return self._get_limit('Limit')

    @property
    def reset_time(self):
        """Request reset time."""
        return self._get_limit('Reset')

    @property
    def remaining_bytes(self):
        """Number of remaining stream bytes."""
        return self._get_stat('remaining')

    @property
    def used_bytes(self):
        """Used stream bytes."""
        return self._get_stat('used')

    @property
    def cap(self):
        """Stream limit."""
        return self._get_stat('cap')

    def _check_private_key(self, message):
        if not self.private_key:
            raise ValueError("Must create Phant object with private_key to {}".format(message))

    def _get_url(self, command, ext='.json'):
        return '{}/{}/{}{}'.format(self.base_url, command, self.public_key, ext)

    def _get_stat(self, name):
        if not self._stats:
            response = rq.get(self._get_url('output', '/stats.json'))
            self._stats = response.json()

        return self._stats[name]

    def _get_limit(self, name):
        if not self._last_headers:
            raise ValueError("No request made yet")

        return self._last_headers['X-Rate-Limit-{}'.format(name)]
