class APIError(Exception):
    """
    API error.

    Attributes:
        _code (str): The error code.
        _message (str): The error message.
    """
    code: str
    message: str

    def __init__(self, code: str, message: str) -> None:
        """
        Initializes a new instance of the AllDebridError class.

        Args:
            code (str): The error code.
            message (str): The error message.
        """
        super().__init__(f"{code} - {message}")
        self._code = code
        self._message = message

    @property
    def code(self) -> str:
        """
        The error code.

        Returns:
            str: The error code.
        """
        return self._code
    
    @property
    def message(self) -> str:
        """
        The error message.

        Returns:
            str: The error message.
        """
        return self._message
    
class EndpointNotFoundError(Exception):
    """
    Endpoint not found error.

    Attributes:
        _endpoint (str): The endpoint that was not found.
    """
    endpoint: str

    def __init__(self, endpoint: str) -> None:
        """
        Initializes a new instance of the EndpointNotFoundError class.

        Args:
            endpoint (str): The endpoint that was not found.
        """
        super().__init__(f"Endpoint not found for {endpoint}")
        self._endpoint = endpoint

    @property
    def endpoint(self) -> str:
        """
        The endpoint that was not found.

        Returns:
            str: The endpoint that was not found.
        """
        return self._endpoint
    
class UnknownAPIError(Exception):
    pass

class MaxAttemptsExceededException(Exception):
    pass
    
apiErrors = {
    'GENERIC': 'An error occurred',
    '404': "Endpoint doesn't exist",

    'AUTH_MISSING_AGENT': "You must send a meaningful agent parameter, see api docs",
    'AUTH_BAD_AGENT': "Bad agent",
    'AUTH_MISSING_APIKEY': 'The auth apikey was not sent',
    'AUTH_BAD_APIKEY': 'The auth apikey is invalid',
    'AUTH_BLOCKED': 'This apikey is geo-blocked or ip-blocked',
    'AUTH_USER_BANNED': 'This account is banned',

    'LINK_IS_MISSING': 'No link was sent',
    'LINK_HOST_NOT_SUPPORTED': 'This host or link is not supported',
    'LINK_DOWN': 'This link is not available on the file hoster website',
    'LINK_PASS_PROTECTED': 'Link is password protected',
    'LINK_HOST_UNAVAILABLE': 'Host under maintenance or not available',
    'LINK_TOO_MANY_DOWNLOADS': 'Too many concurrent downloads for this host',
    'LINK_HOST_FULL': 'All servers are full for this host, please retry later',
    'LINK_HOST_LIMIT_REACHED': "You have reached the download limit for this host",
    'LINK_ERROR': 'Could not unlock this link',

    'REDIRECTOR_NOT_SUPPORTED': 'Redirector not supported',
    'REDIRECTOR_ERROR': 'Could not extract links',

    'STREAM_INVALID_GEN_ID': 'Invalid generation ID',
    'STREAM_INVALID_STREAM_ID': 'Invalid stream ID',

    'DELAYED_INVALID_ID': "This delayed link id is invalid",

    'FREE_TRIAL_LIMIT_REACHED': 'You have reached the free trial limit (7 days // 25GB downloaded or host ineligible for free trial)', #pylint: disable=C0301
    'MUST_BE_PREMIUM': "You must be premium to process this link",

    'MAGNET_INVALID_ID': 'This magnet ID does not exists or is invalid',
    'MAGNET_INVALID_URI': "Magnet is not valid",
    'MAGNET_INVALID_FILE': "File is not a valid torrent",
    'MAGNET_FILE_UPLOAD_FAILED': "File upload failed",
    'MAGNET_NO_URI': "No magnet sent",
    'MAGNET_PROCESSING': "Magnet is processing or completed",
    'MAGNET_TOO_MANY_ACTIVE': "Already have maximum allowed active magnets (30)",
    'MAGNET_MUST_BE_PREMIUM': "You must be premium to use this feature",
    'MAGNET_NO_SERVER': "Server are not allowed to use this feature. Visit https://alldebrid.com/vpn if you're using a VPN.", #pylint: disable=C0301
    'MAGNET_TOO_LARGE': "Magnet files are too large (max 1TB)",

    'PIN_ALREADY_AUTHED': "You already have a valid auth apikey",
    'PIN_EXPIRED': "The pin is expired",
    'PIN_INVALID': "The pin is invalid",

    'USER_LINK_MISSING': "No link provided",
    'USER_LINK_INVALID': "Can't save those links",

    'NO_SERVER': "Server are not allowed to use this feature. Visit https://alldebrid.com/vpn if you're using a VPN.", #pylint: disable=C0301

    'MISSING_NOTIF_ENDPOINT': 'You must provide an endpoint to unsubscribe',

    'VOUCHER_DURATION_INVALID': 'Invalid voucher duration (must be either 15, 30, 90, 180 or 365)',
    'VOUCHER_NB_INVALID': 'Invalid voucher number, must be between 1 and 10',
    'NO_MORE_VOUCHER': 'No voucher of this type available in your account',
    'INSUFFICIENT_BALANCE': 'Your current reseller balance is not enough to generate the requested vouchers', #pylint: disable=C0301
}
