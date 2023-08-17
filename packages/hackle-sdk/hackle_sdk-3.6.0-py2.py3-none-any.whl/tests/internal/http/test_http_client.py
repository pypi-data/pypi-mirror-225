from unittest import TestCase, mock
from unittest.mock import Mock

from hackle.internal.http.http_client import HttpClient
from hackle.internal.model.sdk import Sdk
from tests.internal.time.test_clock import FixedClock


class HttpClientTest(TestCase):

    @mock.patch('requests.get')
    def test_get(self, mock_get):
        sdk = Sdk('test_key', 'test_name', 'test_version')
        clock = FixedClock(42, 43)
        sut = HttpClient(sdk, clock)

        response = Mock()
        response.status_code = 200
        response.content = bytes("{'a': 'b'}", 'utf-8')

        mock_get.return_value = response

        actual = sut.get('localhost')

        args = mock_get.call_args
        self.assertEqual('localhost', args[0][0])
        self.assertEqual(
            {
                'X-HACKLE-SDK-KEY': 'test_key',
                'X-HACKLE-SDK-NAME': 'test_name',
                'X-HACKLE-SDK-VERSION': 'test_version',
                'X-HACKLE-SDK-TIME': '42'
            },
            args[1]['headers']
        )
        self.assertEqual("{'a': 'b'}", actual)

    @mock.patch('requests.post')
    def test_post(self, mock_post):
        sdk = Sdk('test_key', 'test_name', 'test_version')
        clock = FixedClock(42, 43)
        sut = HttpClient(sdk, clock)

        response = Mock()
        response.status_code = 200

        sut.post('localhost', "{'a': 'b'}")

        args = mock_post.call_args
        self.assertEqual('localhost', args[0][0])

        self.assertEqual("{'a': 'b'}", args[1]['data'])
        self.assertEqual(
            {
                'X-HACKLE-SDK-KEY': 'test_key',
                'X-HACKLE-SDK-NAME': 'test_name',
                'X-HACKLE-SDK-VERSION': 'test_version',
                'X-HACKLE-SDK-TIME': '42',
                'Content-Type': 'application/json'
            },
            args[1]['headers']
        )
