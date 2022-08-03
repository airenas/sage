from sage.api.data import Sender


def test_sender_to_str():
    assert Sender.BOT.to_str() == "BOT"
    assert Sender.USER.to_str() == "USER"
