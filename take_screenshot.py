import os
from subprocess import Popen, PIPE
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import (
    webdriver
)
from flask import (
    Flask,
    render_template,
    request
)
from flask_bootstrap import Bootstrap

abspath = lambda *p: os.path.abspath(os.path.join(*p))
ROOT = abspath(os.path.dirname(__file__))
app = Flask(__name__)
Bootstrap(app)


def execute_command(command):
    result = Popen(command, shell=True, stdout=PIPE).stdout.read()
    if len(result) > 0 and not result.isspace():
        raise Exception(result)


def do_screen_capturing(url, screen_path, width, height, username , password):
    print "Capturing screen.."
    driver = webdriver.PhantomJS()
    # it save service log file in same directory
    # if you want to have log file stored else where
    # initialize the webdriver.PhantomJS() as
    # driver = webdriver.PhantomJS(service_log_path='/var/log/phantomjs/ghostdriver.log')
    driver.set_script_timeout(30)
    if width and height:
        driver.set_window_size(width, height)
    driver.get(url)
    field_username = driver.find_element_by_css_selector("#email")
    field_password = driver.find_element_by_css_selector("#password")

    field_username.clear()
    field_username.send_keys(username)

    field_password.clear()
    field_password.send_keys(password)

    driver.find_element_by_css_selector("#submit").click()

    try:
        WebDriverWait(driver, 500).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#courseware-search-bar form div")
            )
        )
    finally:
        driver.save_screenshot(screen_path)
        driver.quit()


def get_screen_shot(**kwargs):
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


@app.route('/', methods=['GET', 'POST'])
def make_screenshot():
    if request.method == 'POST':
        url = request.form["url"]
        user_name = request.form["user_name"]
        password = request.form["pass"]

        screen_path = get_screen_shot(
            url=url, filename='output.png', user_name=user_name, password=password,
            width=1440, height=900
        )
        return render_template('screenshot_form.html', messgae=screen_path)

    return render_template('screenshot_form.html')



if __name__ == '__main__':
    app.run(debug=True, port=55551)
