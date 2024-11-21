from config import COOKIES, CSRF_TOKEN
from mapping import OFFICE_MAPPING, QUESTION_MAPPING

class ScriptState:
    def __init__(self):
        self.static_cookies = COOKIES
        self.running = False
        self.webchsid2 = "" 
        self._csrf = ""
        self.csrf_token = CSRF_TOKEN
        self.offices_ids = []
        self.current_question_type = 'practic'
        self.url_template = self._get_url_template(self.current_question_type)

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

    def update_offices(self, office_names):
        """Update the list of office IDs based on office names."""
        self.offices_ids = [self._map_office_name_to_id(office_name) for office_name in office_names]

    def _map_office_name_to_id(self, office_name):
        """Helper method to map office name to office ID using the OFFICE_MAPPING."""
        return OFFICE_MAPPING.get(office_name)

    def update_question_type(self, question_type):
        """Update the question type and URL template based on the provided question type."""
        if question_type not in QUESTION_MAPPING:
            raise ValueError("Invalid question type. Use 'practic' or 'theory'.")

        self.current_question_type = question_type
        self.url_template = self._get_url_template(question_type)
    def _get_url_template(self, question_type):
        """Helper method to return the URL template based on the question type."""
        question_id = QUESTION_MAPPING.get(question_type)
        return f"https://eq.hsc.gov.ua/site/stepmap?chdate={{chdate}}&question_id={question_id}"

    def get_current_question_type(self):
        """Returns the current question type."""
        return self.current_question_type

script_state = ScriptState()
