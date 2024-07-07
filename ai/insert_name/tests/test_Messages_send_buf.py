from ai.src.communication.cipher import Cipher
from ai.src.communication.latin import Latin
from ai.src.communication.messages import Messages


class TestSendBuf:

    #  returns the correctly formatted broadcast message when msg is initialized
    def test_returns_correctly_formatted_message_when_msg_initialized(self):
        cipher = Cipher("testkey")
        language = Latin()
        messages = Messages(cipher, "123", language)
        messages.msg = 'Broadcast "ACCMST 1 12345 encrypted_message'
        result = messages.send_buf()
        assert result == 'Broadcast "ACCMST 1 12345 encrypted_message"'

    #  appends a closing quote to the msg attribute
    def test_appends_closing_quote_to_msg(self):
        cipher = Cipher("testkey")
        language = Latin()
        messages = Messages(cipher, "123", language)
        messages.msg = 'Broadcast "ACCMST 1 12345 encrypted_message'
        messages.send_buf()
        assert messages.msg.endswith('"')

    #  returns the msg attribute with the appended closing quote
    def test_returns_msg_with_appended_closing_quote(self):
        cipher = Cipher("testkey")
        language = Latin()
        messages = Messages(cipher, "123", language)
        messages.msg = 'Broadcast "ACCMST 1 12345 encrypted_message'
        result = messages.send_buf()
        assert result == 'Broadcast "ACCMST 1 12345 encrypted_message"'

    #  msg attribute is empty before calling send_buf
    def test_msg_empty_before_calling_send_buf(self):
        cipher = Cipher("testkey")
        language = Latin()
        messages = Messages(cipher, "123", language)
        messages.msg = ''
        result = messages.send_buf()
        assert result == '"'

    #  msg attribute already contains a closing quote before calling send_buf
    def test_msg_contains_closing_quote_before_calling_send_buf(self):
        cipher = Cipher("testkey")
        language = Latin()
        messages = Messages(cipher, "123", language)
        messages.msg = 'Broadcast "ACCMST 1 12345 encrypted_message"'
        result = messages.send_buf()
        assert result == 'Broadcast "ACCMST 1 12345 encrypted_message""'

    #  msg attribute contains special characters or escape sequences
    def test_msg_contains_special_characters_or_escape_sequences(self):
        cipher = Cipher("testkey")
        language = Latin()
        messages = Messages(cipher, "123", language)
        messages.msg = 'Broadcast "ACCMST 1 12345 encrypted_message\n\t"'
        result = messages.send_buf()
        assert result == 'Broadcast "ACCMST 1 12345 encrypted_message\n\t""'
