import os
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import unittest  # noqa: E0401, C0413
import unittest.mock as mock  # noqa: E0401, C0413
from app import socketio, app, emit_all_messages  # noqa: E0401, C0413
from app import BOT_NAME, BOT_PICTURE, MESSAGES_RECEIVED_CHANNEL  # noqa: E0401, C0413
from bot import command  # noqa: E0401, C0413

KEY_INPUT = "input"
KEY_EXPECTED = "expected"
KEY_BOT_ANSWER = "bot_answer"


class BotCommandTestCase(unittest.TestCase):
    def setUp(self):

        self.success_8ball_test_params = [
            {
                KEY_INPUT: "!! 8ball test question",
                KEY_EXPECTED: {KEY_BOT_ANSWER: "Don't count on it"},
            }
        ]
        self.success_funtranslate_test_params = [
            {
                KEY_INPUT: "!! funtranslate yoo what's up",
                KEY_EXPECTED: {KEY_BOT_ANSWER: "yO0 WHat'5 Up"},
            },
        ]
        self.failure_funtranslate_test_params = [
            {
                KEY_INPUT: "!! funtranslate yoo what's up",
                KEY_EXPECTED: {KEY_BOT_ANSWER: "yO0 WHat'5 Up"},
            },
        ]
        self.keyerror_8ball_test_params = [
            {
                KEY_INPUT: "!! 8ball lallo",
                KEY_EXPECTED: {KEY_BOT_ANSWER: "I'm over my limit for this API call"},
            }
        ]

        self.keyerror_funtranslate_test_params = [
            {
                KEY_INPUT: "!! funtranslate lallo",
                KEY_EXPECTED: {KEY_BOT_ANSWER: "I'm over my limit for this API call"},
            }
        ]
        self.success_roll_test_params = [
            {KEY_INPUT: "!! roll", KEY_EXPECTED: {KEY_BOT_ANSWER: "5"}},
            {KEY_INPUT: "!! roll 100", KEY_EXPECTED: {KEY_BOT_ANSWER: "5"}},
            {
                KEY_INPUT: "!! roll asdfasdf",
                KEY_EXPECTED: {
                    KEY_BOT_ANSWER: "Please enter a valid number. !! help to learn how to use this command"
                },
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

    def test_8ball_key_error(self):
        for test in self.keyerror_8ball_test_params:
            with mock.patch("requests.get", mocked_request_get_keyerror):
                response = command(test[KEY_INPUT])
                expected = test[KEY_EXPECTED]
                self.assertEqual(response, expected[KEY_BOT_ANSWER])

    def test_funtranslate_key_error(self):
        for test in self.keyerror_funtranslate_test_params:
            with mock.patch("requests.get", mocked_request_get_keyerror):
                response = command(test[KEY_INPUT])
                expected = test[KEY_EXPECTED]
                self.assertEqual(response, expected[KEY_BOT_ANSWER])


class MockedResponse:
    def __init__(self, content):
        self.text = content


def mocked_random_int(arg1, arg2=5):
    return "5"


def mocked_request_get_keyerror(args1, params=""):
    return MockedResponse('{"error":"key"}')


def mocked_funtranslate_request_get(args1, params=""):
    return MockedResponse('{"contents":{"translated": "yO0 WHat\'5 Up"}}')


def mocked_8ball_request_get(args1, params=""):
    return MockedResponse('{"magic": {"answer": "Don\'t count on it"}}')


class AppTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_connection(self):
        with mock.patch("app.emit_all_messages"):
            socketio_test_client = socketio.test_client(app)
            assert socketio_test_client.is_connected()
            received = socketio_test_client.get_received()
            self.assertEqual("user count changed", received[0]["name"])
            self.assertEqual(0, received[0]["args"][0]["users"])
            socketio_test_client.disconnect()

    def test_disconnect(self):
        with mock.patch("app.emit_all_messages"):
            client1 = socketio.test_client(app)
            client2 = socketio.test_client(app)
            client1.disconnect()
            received = client2.get_received()
            self.assertEqual("user count changed", received[0]["name"])
            self.assertEqual(0, received[0]["args"][0]["users"])
            client2.disconnect()

    def test_authorize(self):
        with mock.patch("app.emit_all_messages"):
            with mock.patch("app.update_user"):
                client1 = socketio.test_client(app)
                client1.emit("new google user", {"email": "test"})
                received = client1.get_received()
                self.assertEqual("user count changed", received[-1]["name"])
                self.assertEqual(1, received[-1]["args"][0]["users"])
                client1.disconnect()

    def test_emit_all_messages(self):
        with mock.patch("app.get_messages", mocked_get_messages):
            with mock.patch("app.get_user", mocked_get_user):
                client = socketio.test_client(app)
                emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
                received = client.get_received()
                self.assertEqual(MESSAGES_RECEIVED_CHANNEL, received[-1]["name"])
                allMessages = received[-1]["args"][0]["allMessages"]
                self.assertEqual("test-message", allMessages[0][3])
                self.assertEqual("bot-test-message", allMessages[1][3])
                client.disconnect()

    def test_on_new_message(self):
        with mock.patch("app.emit_all_messages", mocked_emit_all_messages):
            with mock.patch("app.add_message_to_db"):
                client = socketio.test_client(app)
                client.emit("new message input", {})
                received = client.get_received()
                self.assertEqual(MESSAGES_RECEIVED_CHANNEL, received[-1]["name"])
                allMessages = received[-1]["args"][0]["allMessages"]
                self.assertEqual("test-message", allMessages[0].message)
                client.disconnect()


class MockedMessage:
    def __init__(self, msg_type, picture, sender, message):
        self.msg_type = msg_type
        self.profile_pic = picture
        self.sender = sender
        self.message = message


class MockedUser:
    def __init__(self, email, name, picture):
        self.email = email
        self.name = name
        self.profile_pic = picture


def mocked_get_messages():
    return [
        MockedMessage("text", "test.png", "test@test.com", "test-message"),
        MockedMessage("text", BOT_PICTURE, BOT_NAME, "bot-test-message"),
    ]


def mocked_get_user(email):
    return MockedUser(email, "test", "pic.png")


def mocked_emit_all_messages(channel):
    socketio.emit(
        MESSAGES_RECEIVED_CHANNEL,
        {
            "allMessages": [
                MockedMessage("text", "test.png", "test@test.com", "test-message")
            ]
        },
    )


if __name__ == "__main__":
    unittest.main()
