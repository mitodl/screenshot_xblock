__author__ = 'amir'

import ddt
from flask import (
    Flask
)
from flask.ext.testing import TestCase

app = Flask(
    __name__,
    static_url_path="",
    static_folder="output"
)  # pylint: disable=invalid-name


@ddt.ddt
class TestTakeScreenShot(TestCase):

    def setUp(self):
        """
        Setting up app config.
        """
        app.config['TESTING'] = True
        app.config['SERVER_NAME'] = 'localhost'
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SECRET_KEY'] = 'you-will-never-guess'

        self.app = app.test_client()

    def assert404(self, response):
        """
        Checks if a HTTP 404 returned
        """
        self.assertTrue(response.status_code == 404)

    @ddt.data(
        (None, None, None, "404"),
        ("https://www.edx.org/course/science-cooking-haute-cuisine-soft-harvardx-spu27x-0", None, None, "404"),
        ("https://www.edx.org/course/science-cooking-haute-cuisine-soft-harvardx-spu27x-0", "amir.qayyum@arbisoft.com", None, "404"),
        ("https://www.edx.org/course/science-cooking-haute-cuisine-soft-harvardx-spu27x-0", "amir.qayyum@arbisoft.com", "Test1234", "success"),
        ("http://muzaffar-ora1-msg.m.sandbox.edx.org/courses/course-v1:Test+cx101+2015_T/courseware/df44b2d5cd794b1cb91ce1c5e3af470b/1748193e1936460483fa0c3db33e9f24/", "staff@example.com", "edx", "success")
    )
    @ddt.unpack
    def test_take_screen_shot(self, url, user_name, password, expected):
        response = self.client.post(
            '/',
            data=dict(
                url=url,
                user_name=user_name,
                password=password
            ),
            follow_redirects=True
        )
        if expected == "404":
            self.assert404(response)
        else:
            self.assertFalse(response.data)
            assert ".png" in response.data


if __name__ == '__main__':
    unittest.main()