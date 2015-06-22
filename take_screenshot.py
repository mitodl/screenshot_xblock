"""
This api will take xblock url of edX platform and caputure screenshot of that url
"""
from flask import (
    Flask,
    render_template,
    request,
    abort
)
from flask_bootstrap import Bootstrap
import os
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import (
    webdriver
)
import time

abspath = lambda *p: os.path.abspath(os.path.join(*p))
ROOT = abspath(os.path.dirname(__file__))
app = Flask(__name__)
Bootstrap(app)


def do_screen_capturing(url, screen_path, width, height, username, password):
    """
    it save service log file in same directory
    if you want to have log file stored else where
    initialize the webdriver.PhantomJS()
    """
    driver = webdriver.PhantomJS()

    driver.set_script_timeout(30)
    if width and height:
        driver.set_window_size(width, height)

    driver.get("http://localhost:8000/dashboard")
    field_username = driver.find_element_by_css_selector("#email")
    field_password = driver.find_element_by_css_selector("#password")

    field_username.clear()
    field_username.send_keys(username)

    field_password.clear()
    field_password.send_keys(password)

    driver.find_element_by_css_selector("#submit").click()

    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#dashboard-main")
            )
        )
        driver.get(url)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#content div.container div")
            )
        )
    except TimeoutException:
        abort(404)
    finally:
        driver.save_screenshot(screen_path)
        driver.quit()


def get_screen_shot(**kwargs):
    """ Process screenshot data"""
    print "Taking screenhot!"
    url = kwargs['url']
    width = int(kwargs.get('width', 1024)) # screen width to capture
    height = int(kwargs.get('height', 768)) # screen height to capture
    filename = kwargs.get('filename', 'screen.png') # file name e.g. screen.png
    path = kwargs.get('path', ROOT) # directory path to store screen
    user_name = kwargs['user_name']
    password = kwargs['password']

    screen_path = abspath(path, filename)
    screen_path

    do_screen_capturing(url, screen_path, width, height, user_name, password)
    return screen_path


def get_output_file_name():
    """ Returns screenshot image path """
    time_ms = str(round(time.time() * 1000))
    return 'output/screens/' + time_ms + '.png'

@app.errorhandler(404)
def page_not_found(e):
    """ Handle 404 error i.e redirect to 404 error page """
    return render_template('404.html'), 404


@app.route('/', methods=['GET', 'POST'])
def take_screen_shot():
    """
    Api that returns a form or receive post call to capture screenshot of given Xblock
    """
    if request.method == 'POST':
        url = request.form["url"]
        user_name = request.form["user_name"]
        password = request.form["pass"]

        if not url or not user_name or not password:
            abort(404)

        screen_path = get_screen_shot(
            url=url, filename=get_output_file_name(), user_name=user_name, password=password,
            width=1440, height=900
        )
        return render_template('screenshot_form.html', messgae=screen_path)

    return render_template('screenshot_form.html')



if __name__ == '__main__':
    app.run(debug=True, port=55551)
