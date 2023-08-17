import requests

from hackle.internal.model.sdk import Sdk
from hackle.internal.time.clock import SYSTEM_CLOCK, Clock


class HttpClient(object):
    __SDK_KEY_HEADER_NAME = 'X-HACKLE-SDK-KEY'
    __SDK_NAME_HEADER_NAME = 'X-HACKLE-SDK-NAME'
    __SDK_VERSION_HEADER_NAME = 'X-HACKLE-SDK-VERSION'
    __SDK_TIME_HEADER_NAME = 'X-HACKLE-SDK-TIME'
    __CONTENT_TYPE_HEADER_NAME = 'Content-Type'
    __CONTENT_TYPE_VALUE = 'application/json'
    __TIMEOUT_SECONDS = 10

    def __init__(self, sdk, clock=SYSTEM_CLOCK):
        """
        :param Sdk sdk:
        :param Clock clock:
        """
        self.__sdk = sdk
        self.__clock = clock

    def get(self, url):
        response = requests.get(url, headers=self.__headers(), timeout=self.__TIMEOUT_SECONDS)
        response.raise_for_status()
        return response.content.decode('utf-8')

    def post(self, url, data):
        headers = self.__headers()
        headers[self.__CONTENT_TYPE_HEADER_NAME] = self.__CONTENT_TYPE_VALUE
        requests.post(url, data=data, headers=headers, timeout=self.__TIMEOUT_SECONDS).raise_for_status()

    def __headers(self):
        return {
            self.__SDK_KEY_HEADER_NAME: self.__sdk.key,
            self.__SDK_NAME_HEADER_NAME: self.__sdk.name,
            self.__SDK_VERSION_HEADER_NAME: self.__sdk.version,
            self.__SDK_TIME_HEADER_NAME: str(self.__clock.current_millis())
        }
