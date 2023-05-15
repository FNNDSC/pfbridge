import httpx

class PflinkClient(object):
    """
    A `pflink` client
    """
    def __init__(self, url, auth_token):
        self.auth_token = None
        self.url = url
        self.set_auth_token(auth_token)

    def set_auth_token(self, auth_token):
        if not auth_token:
            raise PflinkRequestInvalidTokenException(f'Invalid auth token: {auth_token}')
        self.auth_token = str(auth_token)

    async def post(self, data: dict):
        """

        Args:
            data:

        Returns:

        """
        headers = {'Authorization': 'Bearer ' + self.auth_token}
        async with httpx.AsyncClient() as client:
            try:
                response: httpx.Response = await client.post(
                    self.url,
                    data = data,
                    headers = headers
                )
            except Exception as e:
                raise Exception(str(e))
            return response

    @staticmethod
    async def get_auth_token(pflink_auth_url: str, pflink_user: str, pflink_password: str):
        """
        Make a POST request to obtain an auth token.
        Args:
            pflink_auth_url:
            pflink_user:
            pflink_password:

        Returns:

        """
        async with httpx.AsyncClient() as client:
            try:
                response: httpx.Response = await client.post(
                    pflink_auth_url,
                    data={'username': pflink_user, 'password': pflink_password}
                )
            except Exception as e:
                raise PflinkRequestException(str(e))
            return response.json().get('access_token')

class PflinkRequestException(Exception):
    pass

class PflinkRequestInvalidTokenException(PflinkRequestException):
    pass


