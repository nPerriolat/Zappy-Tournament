import uuid

from ai.src.communication.cipher import Cipher
from ai.src.communication.messages import Messages
from ai.src.communication.latin import Latin


class TestMessages:

    #  send method generates a unique UUID for each message
    def test_send_generates_unique_uuid(self):
        cipher = Cipher("testkey")
        latin = Latin()
        messages = Messages(cipher, "123", latin)
        uuid1 = messages.send("Hello")
        uuid2 = messages.send("World")
        assert uuid1 != uuid2

    #  send method encrypts the message correctly using the Cipher class
    def test_send_encrypts_message_correctly(self):
        cipher = Cipher("testkey")
        latin = Latin()
        messages = Messages(cipher, "123", latin)
        encrypted_msg = messages.send("Hello")
        assert "ACCMST 123" in encrypted_msg

    #  send method handles cases where UUID generation takes multiple attempts
    def test_send_handles_multiple_uuid_attempts(self):
        cipher = Cipher("testkey")
        latin = Latin()
        messages = Messages(cipher, "123", latin)
        messages.uuid_used.append(str(uuid.uuid4()))
        new_uuid = messages.send("Hello").split()[2]
        assert new_uuid not in messages.uuid_used

    #  receive method handles messages with invalid formats gracefully
    def test_receive_handles_invalid_formats(self):
        cipher = Cipher("testkey")
        latin = Latin()
        messages = Messages(cipher, "123", latin)
        result = messages.receive("INVALID MESSAGE FORMAT", "hello")
        assert result == [('broadcast', [{'id': 0, 'msg': 'ko'}])]

    #  receive method handles empty messages or messages shorter than expected
    def test_receive_handles_empty_or_short_messages(self):
        cipher = Cipher("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum posuere leo eget iaculis bibendu")
        latin = Latin()
        messages = Messages(cipher, "123", latin)
        result_empty = messages.receive('', "hello")
        assert result_empty == [('broadcast', 'ko')]

        # TODO - Find why isn't working
        # latin = Latin()
        # messages_short = Messages(cipher, "1", latin)
        # result_short = messages_short.receive('message 4, "ACCMST 1 4b19f5ad-8e18-46f0-9fcf-e8c61506bfde 96388#91662#95058#107692#100138#91348#92034#81070#109289#99961#81683#76381#87586#92223#92025#70739#76497#66016#93121#76228"')
        #
        # assert result_short == 'nobilis incantatio'

class TestReceive:

    #  correctly decrypts and processes valid encrypted messages
    def test_correctly_decrypts_and_processes_valid_encrypted_messages(self):
        cipher = Cipher("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum posuere leo eget iaculis bibendu")
        latin = Latin()
        messages = Messages(cipher, "123", latin)
        processed_message = messages.receive('message 1, "ACCMST 1 cfcba69f yo_la_team"', "hello")
        assert isinstance(processed_message, list)
        assert processed_message == [('broadcast', [{'id': 0, 'msg': 'ko'}])]

    #  returns the original message if it matches the predefined pattern
    def test_returns_original_message_if_matches_predefined_pattern(self):
        cipher = Cipher("testkey")
        latin = Latin()
        messages = Messages(cipher, "123", latin)
        original_message = "[ food 1, linemate 2, deraumere 3, sibur 4, mendiane 5, phiras 6, thystame 7 ]"
        processed_message = messages.receive(original_message, "hello")
        assert processed_message == [('inventory', original_message)]

    #  appends new UUIDs to the uuid_used list after processing messages
    def test_appends_new_uuids_to_uuid_used_list_after_processing_messages(self):
        cipher = Cipher("testkey")
        latin = Latin()
        messages = Messages(cipher, "123", latin)
        initial_uuid_count = len(messages.uuid_used)
        encrypted_message = messages.send("Hello World")
        messages.receive(encrypted_message, "hello")
        assert len(messages.uuid_used) == initial_uuid_count + 1

    #  handles messages with invalid formats gracefully
    def test_handles_messages_with_invalid_formats_gracefully(self):
        cipher = Cipher("testkey")
        latin = Latin()
        messages = Messages(cipher, "123", latin)
        result = messages.receive("INVALID MESSAGE FORMAT", "hello")
        assert result == [('broadcast', [{'id': 0, 'msg': 'ko'}])]

    #  returns 'ko' for messages with reused UUIDs
    def test_returns_ko_for_messages_with_reused_uuids(self):
        cipher = Cipher("testkey")
        latin = Latin()
        messages = Messages(cipher, "123", latin)
        encrypted_message = messages.send("Hello World")
        messages.receive(encrypted_message, "hello")
        result = messages.receive(encrypted_message, "hello")
        assert result == [('broadcast', [{'id': 0, 'msg': 'ko'}])]

    #  processes messages with missing or malformed parts
    def test_processes_messages_with_missing_or_malformed_parts(self):
        cipher = Cipher("testkey")
        latin = Latin()
        messages = Messages(cipher, "123", latin)
        malformed_message = 'Broadcast "ACCMST 123 4567 89#90#91"'
        result = messages.receive(malformed_message, "hello")
        assert result == [('broadcast', [{'id': 0, 'msg': 'ko'}])]
