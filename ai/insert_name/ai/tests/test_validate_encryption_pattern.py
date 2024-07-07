import pytest

from ai.src.communication.latin import Latin
from ai.src.communication.cipher import Cipher
from ai.src.communication.messages import Messages
from ai.src.utils.messages import validate_encryption_pattern


class TestValidateEncryptionPattern:

    #  returns 0 for a string of digits
    def test_returns_1_for_string_of_digits(self):
        cipher = Cipher("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum posuere leo eget iaculis bibendu")
        language = Latin()
        messages = Messages(cipher, "123", language)
        assert validate_encryption_pattern("123456") == 1

    #  returns 0 for a string of digits separated by single '#'
    def test_returns_1_for_string_of_digits_separated_by_single_hash_but_not_10_nbr(self):
        cipher = Cipher("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum posuere leo eget iaculis bibendu")
        language = Latin()
        messages = Messages(cipher, "123", language)
        assert validate_encryption_pattern("123#456") == 1

    #  returns 0 for a string of digits separated by multiple '#'
    def test_returns_1_for_string_of_digits_separated_by_multiple_hashes_but_not_10_nbr(self):
        cipher = Cipher("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum posuere leo eget iaculis bibendu")
        language = Latin()
        messages = Messages(cipher, "123", language)
        assert validate_encryption_pattern("123#456#789") == 1

    #  returns 0 for a single digit
    def test_returns_1_for_single_digit(self):
        cipher = Cipher("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum posuere leo eget iaculis bibendu")
        language = Latin()
        messages = Messages(cipher, "123", language)
        assert validate_encryption_pattern("1") == 1

    #  returns 0 for a single digit followed by '#'
    def test_returns_1_for_single_digit_followed_by_hash(self):
        cipher = Cipher("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum posuere leo eget iaculis bibendu")
        language = Latin()
        messages = Messages(cipher, "123", language)
        assert validate_encryption_pattern("1#") == 1

    #  returns 1 for a string with trailing '#'
    def test_returns_1_for_string_with_trailing_hash(self):
        cipher = Cipher("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum posuere leo eget iaculis bibendu")
        language = Latin()
        messages = Messages(cipher, "123", language)
        assert validate_encryption_pattern("123#456#") == 1

    #  returns 0 for a string of exactly 10 digits separated by 9 '#'
    def test_returns_0_for_string_of_exactly_10_digits_separated_by_9_hashes(self):
        cipher = Cipher("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum posuere leo eget iaculis bibendu")
        language = Latin()
        messages = Messages(cipher, "123", language)
        assert validate_encryption_pattern("1#2#3#4#5#6#7#8#9#0") == 0

    #  returns 1 for a string of digits separated by less than 9 '#'
    def test_returns_1_for_string_of_digits_separated_by_less_than_9_hashes(self):
        cipher = Cipher("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum posuere leo eget iaculis bibendu")
        language = Latin()
        messages = Messages(cipher, "123", language)
        assert validate_encryption_pattern("1#2#3#4#5#6#7#8#9") == 1

    #  returns 1 for a string of digits separated by more than 9 '#'
    def test_returns_1_for_string_of_digits_separated_by_more_than_9_hashes(self):
        cipher = Cipher("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum posuere leo eget iaculis bibendu")
        language = Latin()
        messages = Messages(cipher, "123", language)
        assert validate_encryption_pattern("1#2#3#4#5#6#7#8#9#0#1") == 1

    #  returns 1 for a string with trailing '#'
    def test_returns_1_for_string_with_trailing_hash(self):
        cipher = Cipher("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum posuere leo eget iaculis bibendu")
        language = Latin()
        messages = Messages(cipher, "123", language)
        assert validate_encryption_pattern("1#2#3#4#5#6#7#8#9#") == 1

    #  returns 1 for a string with leading '#'
    def test_returns_1_for_string_with_leading_hash(self):
        cipher = Cipher("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum posuere leo eget iaculis bibendu")
        language = Latin()
        messages = Messages(cipher, "123", language)
        assert validate_encryption_pattern("#1#2#3#4#5#6#7#8#9") == 1

    #  returns 1 for a string with consecutive '#'
    def test_returns_1_for_string_with_consecutive_hashes(self):
        cipher = Cipher("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum posuere leo eget iaculis bibendu")
        language = Latin()
        messages = Messages(cipher, "123", language)
        assert validate_encryption_pattern("1##2##3##4##5##6##7##8##9") == 1

    def test_returns_0_for_string_of_20_digits_separated_by_19_hashes(self):
        cipher = Cipher("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum posuere leo eget iaculis bibendu")
        language = Latin()
        messages = Messages(cipher, "123", language)
        assert validate_encryption_pattern("1#2#3#4#5#6#7#8#9#0#1#2#3#4#5#6#7#8#9#0") == 0

    def test_returns_0_for_multiple_groups_of_10_digits_separated_by_9_hashes_each(self):
        cipher = Cipher("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum posuere leo eget iaculis bibendu")
        language = Latin()
        messages = Messages(cipher, "123", language)
        assert validate_encryption_pattern("1#2#3#4#5#6#7#8#9#0#1#2#3#4#5#6#7#8#9#0") == 0