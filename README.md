# Xblock screenshot api for edx-platform

##### Enable standalone xblock rendering
   TO enable xblock rendering on edX platform you need to add below flag inside features list in  lms.env.json
   ````
     "ENABLE_RENDER_XBLOCK_API":true 
   ````

##### Installation

-  Create virtual environment (i.e follow steps in http://docs.python-guide.org/en/latest/dev/virtualenvs/)
- Install requirments.txt 
   ```
     pip install -r requirments.txt
   ``` 
- Install phantom js
   ```
   npm install
   ```
   
##### Running the Development Server
  ``` 
   python take_screenshot.py
  ```  
- Open url http://0.0.0.0:5000/ (In local environment)
- Add xblock url (i.e http://localhost:8000/api/xblock/v0/xblock/i4x://edX/DemoX/html/030e35c4756a4ddc8d40b95fbbfff4d4)
- Add your edX platform credentials
- Click ```Get screenshot``` and get screenshot at location output/screens/time_mili_sec.png

##### Running the Development on heroku

- Follow below 2 links
https://devcenter.heroku.com/articles/getting-started-with-python#deploy-the-app
https://devcenter.heroku.com/articles/using-multiple-buildpacks-for-an-app

*Note* you need 2 buildpacks i.e Nodejs and python
```
https://github.com/heroku/heroku-buildpack-python.git
https://github.com/heroku/heroku-buildpack-nodejs.git
```

##### Testing
You can run tests by following command
```
python -m unittest  test_take_screenshot
```