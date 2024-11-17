from config import COOKIES, CSRF_TOKEN

class ScriptState:
    def __init__(self):
        self.static_cookies = COOKIES
        self.running = False
        self.webchsid2 = "" 
        self._csrf = ""
        self.csrf_token = CSRF_TOKEN

        self.headers = {
            "cookie": self.get_cookie_string(),
            "referer": "https://eq.hsc.gov.ua/site/step2?chdate=2024-10-11&question_id=55&id_es=",
            "x-csrf-token": self.csrf_token,
        }

    def get_cookie_string(self):
        return f"{self.static_cookies}; WEBCHSID2={self.webchsid2}; _csrf={self._csrf}"

    def update_cookies_and_header(self, new_webchsid2, new__csrf, new_csrf_token):
        """Update the dynamic values of cookies and CSRF header."""
        self.webchsid2 = new_webchsid2
        self._csrf = new__csrf
        self.csrf_token = new_csrf_token

        self.headers["cookie"] = self.get_cookie_string()
        self.headers["x-csrf-token"] = self.csrf_token

script_state = ScriptState()
