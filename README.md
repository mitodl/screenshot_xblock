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

##### Running the Development Server
  ``` 
   python take_screenshot.py
  ```  
- Open url http://127.0.0.1:55551/ (In local environment)
- Add xblock url (i.e http://localhost:8000/api/xblock/v0/xblock/i4x://edX/DemoX/html/030e35c4756a4ddc8d40b95fbbfff4d4)
- Add your edX platform credentials
- Click ```Get screenshot``` and get screenshot at location output/screens/time_mili_sec.png
