from mapping import OFFICE_MAPPING

def is_sunday_or_monday(date):
    return date.weekday() in [6, 0]  

def map_offices(office_id):
    return OFFICE_MAPPING.get(office_id)