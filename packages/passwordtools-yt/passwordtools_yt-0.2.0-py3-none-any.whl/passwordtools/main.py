import re
import secrets
import string


class PasswordTool:
    def is_strong(password):
        """
        The function checks if a given password is strong by ensuring it has at least 12 characters and
        contains at least one lowercase letter, one uppercase letter, one digit, and one special character.
        
        :param password: The password parameter is a string that represents the password that needs to be
        tested for strength
        :type password: str
        :return: The function `test_strong` returns a boolean value. It returns `True` if the password meets
        the following criteria:
        - It has a length of at least 12 characters
        - It contains at least one lowercase letter
        - It contains at least one uppercase letter
        - It contains at least one digit
        - It contains at least one special character from the set `!@#$%^&
        """
        if len(password) < 12:
            return False

        return bool(re.match(r"(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*)(}{][><?.|\",:']).+", password))

    def generate(length=12):
        """
        This function generates a strong password of a specified length.
        
        :param length: The length parameter is an integer that specifies the desired length of the generated
        password
        :return: The function `generate` returns a string that represents a randomly generated password of
        the specified length, which is at least 12 characters long and contains a combination of letters,
        digits, and punctuation marks. If the specified length is less than 12, it returns `None`. If the
        specified length is `None`, it sets the length to 12. The function ensures that the generated
        password is strong
        """
        if length < 12:
            return None
        alphabet = string.ascii_letters + string.digits + string.punctuation
        password: str = ''.join(secrets.choice(alphabet) for i in range(length))
        while PasswordTool.test_strong(password) == False:
            alphabet = string.ascii_letters + string.digits + string.punctuation
            password = ''.join(secrets.choice(alphabet) for i in range(length))
        return password
