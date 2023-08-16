import requests
import ConfigParser

class PasswordlessClient:
    def __init__(self):
        # Read API configurations from the config file
        config = ConfigParser.ConfigParser()
        config.read('passwordlessconfig.ini')
        self.API_URL = config.get('API', 'API_URL')
        self.API_SECRET = config.get('API', 'API_SECRET')
        self.API_KEY = config.get('API', 'API_KEY')
        self.VERIFY = config.getboolean('API', 'VERIFY')
        self.headers = {"ApiSecret": self.API_SECRET, "Api-Key": self.API_KEY, "Content-Type": "application/json"}

    def register_token(self, user_id, username, displayname, authenticator_type="any", user_verification="preferred", aliases=[], alias_hashing=True):
        payload = {
            "userId": user_id,
            "username": username,
            "displayname": displayname,
            "authenticatorType": authenticator_type,
            "userVerification": user_verification,
            "aliases": aliases,
            "aliasHashing": alias_hashing
        }
        return self._make_request("register/token", payload)

    def signin_verify(self, token):
        payload = {"token": token}
        return self._make_request("signin/verify", payload)

    def alias(self, user_id, aliases, hashing=True):
        payload = {"userId": user_id, "aliases": aliases, "hashing": hashing}
        return self._make_request("alias", payload)

    def credentials_list(self, user_id):
        payload = {"userId": user_id}
        return self._make_request("credentials/list", payload)

    def credentials_delete(self, credential_id):
        payload = {"credentialId": credential_id}
        return self._make_request("credentials/delete", payload)

    def _make_request(self, endpoint, payload):
        # General method to make requests
        response = requests.post(
            "{}/{}".format(self.API_URL, endpoint),
            verify=self.VERIFY,
            json=payload,
            headers=self.headers
        )
        if response.ok:
            return response.json()
        else:
            raise Exception("Failed to fetch response successfully. Status Code: {}\n{}".format(response.status_code, response.text))
