import time
from datetime import datetime
from rapid_ct_app import app
from rapid_ct_app.models import User


@app.template_filter('convertdatetime')
def datetime_from_utc_to_local(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset


@app.template_filter('formatdatetime')
def format_datetime(value, format="%d/%m/%Y %H:%M"):
    """Format a date time to (Default): d Mon YYYY HH:MM P"""
    if value is None:
        return ""
    return value.strftime(format)

@app.template_filter('getuserwithid')
def get_user(id):
    try:
        user = User.query.get(int(id))
        return user.username
    except:
        return Exception
