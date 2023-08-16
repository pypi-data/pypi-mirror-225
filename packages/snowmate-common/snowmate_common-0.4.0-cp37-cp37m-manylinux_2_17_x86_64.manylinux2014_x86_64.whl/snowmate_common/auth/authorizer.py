from datetime import datetime

import jwt
import requests
from dateutil import parser, tz

BAD_REQUEST = "Request could not be completed"

class AuthError(Exception):
    """
    Auth Error Exception
    """


class AuthorizerKeys:
    REFRESH_TOKEN = "refreshToken"
    CLIENT_ID = "clientId"
    SECRET = "secret"
    EXPIRES = "expires"
    ACCESS_TOKEN = "accessToken"


UNAUTHORIZED_STATUS_CODE = 401
REQUEST_TIMEOUT = 60
APPLICATION_JSON_HEADER = "application/json"


BASE_HEADERS = {
    "Accept": APPLICATION_JSON_HEADER,
    "Content-Type": APPLICATION_JSON_HEADER,
}


class Authorizer:
    """
    This class implements our authorization
    """

    def __init__(self, auth_url: str, client_id: str, secret_key: str):
        self._client_id = client_id
        self._secret_key = secret_key
        self._auth_url = auth_url
        self._bearer_token = None
        self._bearer_token_expiration_date = None
        self._bearer_token_refresher = None
        self.user_details = None
        self.fetch_bearer_token_from_server()
        self.set_user_details()

    def fetch_bearer_token_from_server(self, should_refresh: bool = False):
        """
        Fetch the token from our auth service.
        @param should_refresh: Wether or not to refresh that token.
        @return:None
        """
        url = f"{self._auth_url}/identity/resources/auth/v1/api-token"

        if should_refresh:
            url += "/token/refresh"
            payload = {
                AuthorizerKeys.REFRESH_TOKEN: self._bearer_token_refresher,
            }
        else:
            payload = {
                AuthorizerKeys.CLIENT_ID: self._client_id,
                AuthorizerKeys.SECRET: self._secret_key,
            }
        try:
            response = requests.post(url, json=payload, headers=BASE_HEADERS, timeout=60)
        except Exception:
            raise AuthError(BAD_REQUEST)
        if response.status_code == UNAUTHORIZED_STATUS_CODE:
            raise AuthError("Invalid Authentication")

        response_data = response.json()
        try:
            self._bearer_token = response_data[AuthorizerKeys.ACCESS_TOKEN]
            self._bearer_token_expiration_date = response_data[AuthorizerKeys.EXPIRES]
            self._bearer_token_refresher = response_data[AuthorizerKeys.REFRESH_TOKEN]
        except KeyError as err:
            raise AuthError("Invalid Authentication") from err

    def set_user_details(self):
        self.user_details = jwt.decode(
            self.bearer_access_token, options={"verify_signature": False}
        )

    @property
    def _is_bearer_token_valid(self):
        """
        Make sure the bearer token didn't expire
        @return: True if is bearer token didn't expired, else False
        """
        expiration_datetime = parser.parse(self._bearer_token_expiration_date)
        now_datetime = datetime.now(tz=tz.tzutc())
        if expiration_datetime > now_datetime:
            return True
        return False

    @property
    def bearer_access_token(self):
        if not self._is_bearer_token_valid:
            self.fetch_bearer_token_from_server(True)
        return self._bearer_token
