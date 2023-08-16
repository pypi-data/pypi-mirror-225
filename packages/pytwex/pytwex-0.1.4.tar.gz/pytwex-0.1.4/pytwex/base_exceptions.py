

class CookieValueError(Exception):
    def __init__(self, cookie):

        self.cookie = cookie
        self.message = f'Your cookie is invalid. Please, enter the correct form. | {cookie}'
        super().__init__(self.message)

