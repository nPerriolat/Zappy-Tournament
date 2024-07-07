from ai.src.communication.latin import Latin
from ai.src.communication.cipher import Cipher
from ai.src.communication.messages import Messages


class TestReceive:

    #  returns 'ok\n' when message is 'ok\n'
    def test_returns_ok_when_message_is_ok(self, mocker):
        cipher = Cipher("testkey")
        latin = Latin()
        messages = Messages(cipher, "123", latin)
        result = messages.receive('ok\n', ["hello"])
        assert result == [('ok', "hello")]

    #  returns 'ko\n' when message is 'ko\n'
    def test_returns_ko_when_message_is_ko(self, mocker):
        cipher = Cipher("testkey")
        latin = Latin()
        messages = Messages(cipher, "123", latin)
        result = messages.receive('ko\n', ["hello"])
        assert result == [('ko', "hello")]

    #  handles messages with invalid formats gracefully
    def test_handles_invalid_formats_gracefully(self, mocker):
        cipher = Cipher("testkey")
        latin = Latin()
        messages = Messages(cipher, "123", latin)
        result = messages.receive('INVALID MESSAGE FORMAT', ["hello"])
        assert result == [('broadcast', [{'id': 0, 'msg': 'ko'}])]
