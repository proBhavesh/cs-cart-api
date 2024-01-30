class SessionStore:
    """
    This class provides a mechanism to store the session keys for multiple users.
    This allows the session keys to be accessed throughout the application.
    """

    def __init__(self):
        """
        Initialize an empty dictionary to store the session keys.
        """
        self.session_keys = {}

    def store_session_key(self, user_email, key):
        """
        This function stores the session key for a specific user.
        """
        self.session_keys[user_email] = key

    def get_session_key(self, user_email):
        """
        This function retrieves the session key for a specific user.
        """
        return self.session_keys.get(user_email)


# TODO: What is this?