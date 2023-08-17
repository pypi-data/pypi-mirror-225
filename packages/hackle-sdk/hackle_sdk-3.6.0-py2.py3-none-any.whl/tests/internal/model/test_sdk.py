from unittest import TestCase

from hackle.internal.model.sdk import Sdk


class SdkTest(TestCase):

    def test_sdk(self):
        sdk = Sdk('key', 'name', 'version')
        self.assertEqual('key', sdk.key)
        self.assertEqual('name', sdk.name)
        self.assertEqual('version', sdk.version)
