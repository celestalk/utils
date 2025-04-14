import urllib.parse


class Url(str):
    """ String super class for URL
    """

    def __new__(cls, value: str):
        p = urllib.parse.urlparse(value, scheme='http', allow_fragments=False)
        inst = super().__new__(cls, str(urllib.parse.urlunparse(p)))
        inst.p = p
        return inst
