"""
This api will take xblock url of edX platform
and capture screenshot of that url
"""
from flask import (
    Flask,
    render_template,
    request,
    abort
)
from flask_bootstrap import Bootstrap  # pylint: disable=import-error
import os
from selenium.webdriver.common.by import By  # pylint: disable=import-error
from selenium.common.exceptions import(
    TimeoutException
)  # pylint: disable=import-error
from selenium.webdriver.support.ui import (
    WebDriverWait
)  # pylint: disable=import-error
from selenium.webdriver.support import (
    expected_conditions as EC
)  # pylint: disable=import-error
from selenium import webdriver  # pylint: disable=import-error
import time
from urlparse import urlparse

ABS_PATH = (
    lambda *p: os.path.abspath(os.path.join(*p))
)
ROOT = ABS_PATH(os.path.dirname(__file__))
app = Flask(
    __name__,
    static_url_path="",
    static_folder="output"
)  # pylint: disable=invalid-name
Bootstrap(app)
TIME_OUT = 30


def get_time_out():
    """
    :return: max time out for WebDriverWait
    """
    return TIME_OUT


def get_screen_shot(**kwargs):
    """ Process screenshot data"""
    def do_screen_capturing():
        """
        It save service log file in same directory and save
        screenshot after loging and navigation to xblock.
        """
        driver = webdriver.PhantomJS()

        driver.set_script_timeout(30)
        if width and height:
            driver.set_window_size(width, height)

        url_parse = urlparse(url)
        dashboard_url = "{}://{}/dashboard".format(
            url_parse.scheme, url_parse.netloc
        )
        driver.get(dashboard_url)
        field_username = driver.find_element_by_css_selector("#login-email")
        field_password = driver.find_element_by_css_selector("#login-password")

        field_username.clear()
        field_username.send_keys(user_name)

        field_password.clear()
        field_password.send_keys(password)

        driver.find_element_by_css_selector("#login button").click()

        try:
            WebDriverWait(driver, get_time_out()).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#dashboard-main")
                )
            )
            driver.get(url)
            WebDriverWait(driver, get_time_out()).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "body")
                )
            )
        except TimeoutException:
            abort(404)
        finally:
            driver.save_screenshot(screen_path)
            driver.quit()

    url = kwargs['url']
    width = int(
        kwargs.get('width', 1024)
    )  # screen width to capture
    height = int(
        kwargs.get('height', 768)
    )  # screen height to capture
    filename = kwargs.get(
        'filename', 'screen.png'
    )  # file name e.g. screen.png
    path = kwargs.get(
        'path', ROOT
    )  # directory path to store screen
    user_name = kwargs['user_name']
    password = kwargs['password']

    screen_path = ABS_PATH(path, filename)
    do_screen_capturing()
    return screen_path


def get_output_file_name():
    """ Returns screenshot image path. """
    time_ms = str(round(time.time() * 1000))
    output_file = 'screens/' + time_ms + '.png'
    return ('output/' + output_file), output_file


@app.errorhandler(404)
def page_not_found(error):  # pylint: disable=unused-argument
    """ Handle 404 error i.e redirect to 404 error page """
    return render_template('404.html'), 404


@app.route('/', methods=['GET', 'POST'])
def take_screen_shot():
    """
    Api that returns a form or receive post call
    to capture screenshot of given Xblock.
    """
    if request.method == 'POST':
        url = request.form["url"]
        user_name = request.form["user_name"]
        password = request.form["password"]

        if not url or not user_name or not password:
            abort(404)

        output_path, output_file = get_output_file_name()
        get_screen_shot(
            url=url,
            filename=output_path,
            user_name=user_name,
            password=password,
            width=1440, height=900
        )
        return render_template('screenshot_form.html', output_file=output_file)

    return render_template('screenshot_form.html')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
