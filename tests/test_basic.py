# imports the unittest module - used for writing and running unit tests in python
# sys- module uses for manipulating the system path
import unittest, sys

# append the repo to the system path
# allows importing python files from parent directory
sys.path.append('../instance') # imports python file from parent directory

# imports the app object from the app.py
from app import app, db #imports flask app object

class BasicTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        self.app = app.test_client()

    ###############
    #### tests ####
    ###############

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
# ^^This is a test case that checks if the main page exists
# A GETRequest is made to the root URLfollow_redirects 
# tells the client to follwo any redirects -- all stored in variable response
#self.assertEqual tests if response.status_code is 200, which means it was successful

if __name__ == "__main__":
    unittest.main()