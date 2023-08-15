from typing import Final


class UrlRef:
    AWS: Final[str] = "https://958e36p8n5.execute-api.ap-northeast-1.amazonaws.com/prod/"
    LocalNodeJs: Final[str] = "http://localhost:33000/"


class Url:
    Root = UrlRef.AWS
