__author__ = 'amir'

import ddt
import unittest
from take_screenshot import app


@ddt.ddt
class TestTakeScreenShot(unittest.TestCase):

    def setUp(self):
        """
        Setting up app config.
        """
        self.app = app.test_client()

    @ddt.data(
        (None, None, None, "400"),
        ("https://www.edx.org/course/science-cooking-haute-cuisine-soft-harvardx-spu27x-0", None, None, "400"),
        ("https://www.edx.org/course/science-cooking-haute-cuisine-soft-harvardx-spu27x-0", "amir.qayyum@arbisoft.com", None, "400"),
        ("https://www.edx.org/course/science-cooking-haute-cuisine-soft-harvardx-spu27x-0", "amir.qayyum@arbisoft.com", "Test1234", "success"),
    )
    @ddt.unpack
    def test_take_screen_shot(self, url, user_name, password, expected):
        response = self.app.post(
            '/',
            data=dict(
                url=url,
                user_name=user_name,
                password=password
            ),
            follow_redirects=True
        )
        if expected == "400":
            self.assertTrue(response.status_code == 400)
        else:
            assert "<img src=" in response.data

if __name__ == '__main__':
    unittest.main()