from typing import Any


class WappstoError(ConnectionError):
    """
    Exception Used if Wappsto reply with an error.
    """
    def __init__(
        self,
        code: int,
        msg: str,
        url: str,
        http_code: int,
        data: Any | None = None
    ) -> None:
        """
        Initialize the WappstoError with the Error Response info.

        Args:
            code: The Wappsto Error code, within the range of -32000 to -32099
            msg: The Wappsto Error message, that shortly describe the error for given code.
            url: The URL that was used to trigger the Exception.
            data: (Optional) The data used when triggered the Exception.
        """
        super().__init__()
        self.code = code
        self.msg = msg
        self.url = url
        self.http_code = http_code
        self.data = data
