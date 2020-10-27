'''
    unmocked_unit_tests.py
    
    This file tests all methods in message_type.py
'''
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import unittest
from message_type import get_message_type
from bot import command

KEY_INPUT = "input"
KEY_EXPECTED = "expected"
KEY_MESSAGE_TYPE = "message_type"
KEY_BOT_ANSWER = "bot_answer"

class MessageTypeTestCase(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: "Hey Hasan whats'up",
                KEY_EXPECTED: {
                    KEY_MESSAGE_TYPE : "text"
                }
            },
            {
                KEY_INPUT: "https://console.aws.amazon.com/cloud9/ide/55d7f555b49e4aaf8e2cafacdb2e11df",
                KEY_EXPECTED: {
                    KEY_MESSAGE_TYPE : "url"
                }
            },
            {
                KEY_INPUT: "https://i.pinimg.com/originals/ab/a8/9e/aba89e26e7fb5a827b9456f1f017a8e2.jpg",
                KEY_EXPECTED: {
                    KEY_MESSAGE_TYPE : "image"
                }
            },
        ]
        self.failure_test_params = [
            {
                KEY_INPUT: "hello my name is https://console.aws.amazon.com/cloud9/ide/55d7f555b49e4aaf8e2cafacdb2e11df",
                KEY_EXPECTED: {
                    KEY_MESSAGE_TYPE : "url"
                }
            },
            {
                KEY_INPUT: "hey this is not by itself https://i.pinimg.com/originals/ab/a8/9e/aba89e26e7fb5a827b9456f1f017a8e2.jpg",
                KEY_EXPECTED: {
                    KEY_MESSAGE_TYPE : "image"
                }
            },
        ]
    def test_get_message_type_success(self):
        for test in self.success_test_params:
            response = get_message_type(test[KEY_INPUT])
            expected = test[KEY_EXPECTED]
            self.assertEqual(response, expected[KEY_MESSAGE_TYPE])
            
            
    def test_get_message_type_failure(self):
        for test in self.failure_test_params:
            response = get_message_type(test[KEY_INPUT])
            expected = test[KEY_EXPECTED]
            self.assertNotEqual(response, expected[KEY_MESSAGE_TYPE])
            
            # TODO add assertNotEqual cases here instead


if __name__ == '__main__':
    unittest.main()