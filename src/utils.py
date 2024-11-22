from constants import OFFICE_MAPPING

def is_sunday_or_monday(date):
    return date.weekday() in [6, 0]  

def map_offices(office_id):
    return OFFICE_MAPPING.get(office_id)

def get_headers(cookie, csrt_token):
    headers = {
        "cookie": cookie,
        "x-csrf-token": csrt_token,
        "referer": "https://eq.hsc.gov.ua/site/step2?chdate=2024-10-11&question_id=55&id_es=",
        }
    return headers

def get_url_template(question_type):
    return f"https://eq.hsc.gov.ua/site/stepmap?chdate={{chdate}}&question_id={question_type}"
