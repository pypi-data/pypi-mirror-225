__token__ = None

class Token():
    def __init__(self) -> None:
        global __token__
        __token__ = None
    
    def set_token(self, token):
        global __token__
        __token__ = token


def get_token():
    return __token__