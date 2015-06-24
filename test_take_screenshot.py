__author__ = 'amir'

from flask import request
import ddt
import unittest
from take_screenshot import(
    app,
    TIME_OUT,
    get_time_out
)
from mock import patch


@ddt.ddt
class TestTakeScreenShot(unittest.TestCase):

    def setUp(self):
        """
        Setting up app config.
        """
        self.app = app.test_client()

    def shutdown_server(self):
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

    @ddt.data(
        (None, None, None, "400", 30),
        ("", "", "", "404", 30),
        ("https://courses.edx.org/courses/course-v1:HarvardX+SPU27x+2015_Q2/courseware/af896b2371b94d409a5d2b6a3ddfb958/b2659040fa0743bba6ae16ba6832d18f/", None, None, "400", 30),
        ("https://courses.edx.org/courses/course-v1:HarvardX+SPU27x+2015_Q2/courseware/af896b2371b94d409a5d2b6a3ddfb958/b2659040fa0743bba6ae16ba6832d18f/", "", "", "404", 30),
        ("https://courses.edx.org/courses/course-v1:HarvardX+SPU27x+2015_Q2/courseware/af896b2371b94d409a5d2b6a3ddfb958/b2659040fa0743bba6ae16ba6832d18f/", "amir.qayyum@arbisoft.com", None, "400", 30),
        ("https://courses.edx.org/courses/course-v1:HarvardX+SPU27x+2015_Q2/courseware/af896b2371b94d409a5d2b6a3ddfb958/b2659040fa0743bba6ae16ba6832d18f/", "amir.qayyum@arbisoft.com", "", "404", 30),
        ("https://courses.edx.org/courses/course-v1:HarvardX+SPU27x+2015_Q2/courseware/af896b2371b94d409a5d2b6a3ddfb958/b2659040fa0743bba6ae16ba6832d18f/", "amir.qayyum@arbisoft.com", "Test1234", "success", 30),
        ("https://courses.edx.org/courses/course-v1:HarvardX+SPU27x+2015_Q2/courseware/af896b2371b94d409a5d2b6a3ddfb958/b2659040fa0743bba6ae16ba6832d18f/", "amir.qayyum@arbisoft.com", "Test1234", "success", 1)
    )
    @ddt.unpack
    def test_take_screen_shot(self, url, user_name, password, expected, timeout):
        with patch("take_screenshot.get_time_out", return_value=timeout):
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
            elif expected == "404":
                self.assertTrue(response.status_code == 404)
            elif timeout == 1:
                self.assertTrue(response.status_code == 404)
            else:
                assert "<img src=" in response.data

    def test_take_screen_shot_form_rendering(self):
        response = self.app.get('/')
        assert "Enter information of xblock you want to get screenshot" in response.data

    def test_get_time_out(self):
        self.assertEqual(get_time_out(), TIME_OUT)


if __name__ == '__main__':
    unittest.main()