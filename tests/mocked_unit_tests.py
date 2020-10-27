import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import unittest
from bot import command
import unittest.mock as mock

KEY_INPUT = "input"
KEY_EXPECTED = "expected"
KEY_BOT_ANSWER = "bot_answer"



class BotCommandTestCase(unittest.TestCase):
    
    def setUp(self):
        
        self.success_8ball_test_params = [
            {
                KEY_INPUT: "!! 8ball test question",
                KEY_EXPECTED: {
                    KEY_BOT_ANSWER : "Don\'t count on it"
                }
            }
            ]
        self.success_funtranslate_test_params = [
            {
                KEY_INPUT: "!! funtranslate yoo what's up",
                KEY_EXPECTED: {
                    KEY_BOT_ANSWER : "yO0 WHat'5 Up"
                }
            }
        ]
        self.success_roll_test_params = [
            {
                KEY_INPUT: "!! roll",
                KEY_EXPECTED: {
                    KEY_BOT_ANSWER : "5"
                }
            },
            {
                KEY_INPUT: "!! roll 100",
                KEY_EXPECTED: {
                    KEY_BOT_ANSWER : "5"
                }
            },
        ]
        
   
    
    def test_funtranslate_success(self):
        for test in self.success_funtranslate_test_params:
            with mock.patch("requests.get", mocked_funtranslate_request_get):
                response = command(test[KEY_INPUT])
                expected = test[KEY_EXPECTED]
                self.assertEqual(response, expected[KEY_BOT_ANSWER])
            
    
    def test_roll_success(self):
        for test in self.success_roll_test_params:
            with mock.patch("random.randint", mocked_random_int):
                response = command(test[KEY_INPUT])
                expected = test[KEY_EXPECTED]
                self.assertEqual(response, expected[KEY_BOT_ANSWER])
                
    def test_8ball_success(self):
        for test in self.success_8ball_test_params:
            with mock.patch("requests.get", mocked_8ball_request_get):
                response = command(test[KEY_INPUT])
                expected = test[KEY_EXPECTED]
                self.assertEqual(response, expected[KEY_BOT_ANSWER])
                
    
class MockedResponse():
    def __init__(self, content):
        self.text = content

def mocked_random_int(arg1,arg2=5):
    return "5"

def mocked_funtranslate_request_get(arg1,params=""):
    return MockedResponse('{"contents":{"translated": "yO0 WHat\'5 Up"}}')

def mocked_8ball_request_get(arg1, params=""):
    return MockedResponse('{"magic": {"answer": "Don\'t count on it"}}')

if __name__ == '__main__':
    unittest.main()