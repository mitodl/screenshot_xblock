__author__ = 'amir'

import ddt
from flask import (
    Flask,
    render_template,
    request,
    abort
)
import unittest


@ddt.ddt
class TestTakeScreenShot(unittest.TestCase):

    def create_app(self):
        """
        Create your Flask app with needed
        configuration
        """
        return Flask(
            __name__,
            static_url_path="",
            static_folder="output"
        )

    def __call__(self, result=None):
        """
        Does the required setup, doing it here
        means you don't have to call super.setUp
        in subclasses.
        """
        self._pre_setup()
        super(TestTakeScreenShot, self).__call__(result)
        self._post_tearDown()

    def _pre_setup(self):
        self.app = self.create_app()
        self.client = self.app.test_client()

        # now you can use flask thread locals

        self._ctx = self.app.test_request_context()
        self._ctx.push()

    def _post_tearDown(self):
        self._ctx.pop()

    def assert404(self, response):
        """
        Checks if a HTTP 404 returned
        e.g.
        resp = self.client.get("/")
        self.assert404(resp)
        """
        self.assertTrue(response.status_code == 404)

    @ddt.data(
        (None, None, None)
        ("https://courses.edx.org/dashboard", None, None)
        ("https://courses.edx.org/dashboard", "amir.qayyum@arbisoft.com", None)
        ("https://courses.edx.org/dashboard", "amir.qayyum@arbisoft.com", "Test1234")
    )
    @ddt.unpack
    def test_take_screen_shot(self, url, user_name, passsword):
        self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()