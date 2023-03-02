import logging


class DemoQA:
    def __init__(self, session):
        self.session = session
        self._authorization_cookie = None

    def login(self, email, password):
        return self.session.post(
            url="/login",
            params={'Email': email, 'Password': password},
            headers={'content-type': "application/x-www-form-urlencoded; charset=UTF-8"},
            allow_redirects=False
        )

    @property
    def authorization_cookie(self):
        return self._authorization_cookie

    @authorization_cookie.setter
    def authorization_cookie(self, response):
        self._authorization_cookie = {"NOPCOMMERCE.AUTH": response.cookies.get("NOPCOMMERCE.AUTH")}

    def add_to_cart(self, **kwargs):
        cookie = kwargs.get("cookies", None)
        logging.info(cookie)
        count = kwargs.get("count", 1)
        response = None
        for i in range(0, count):
            response = self.session.post('/addproducttocart/catalog/31/1/1', cookies=cookie)
        return response