# screenshot_xblock

To run it

##### TO enable xblock rendering on edX platform you need to add
     ````
     "ENABLE_RENDER_XBLOCK_API":true # inside features list in  lms.env.json
     ````

##### To setup project follow below:

-  Create virtual environment (http://docs.python-guide.org/en/latest/dev/virtualenvs/)
- Install requirments.txt
- **Run** python take_screenshot.py 
- Open url http://127.0.0.1:55551/
  -- Add xblock url (i.e http://localhost:8000/api/xblock/v0/xblock/i4x://edX/DemoX/html/030e35c4756a4ddc8d40b95fbbfff4d4)
  -- Add your edX credentials 
- Get screenshot at project folder
