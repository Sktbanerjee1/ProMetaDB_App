import time
from datetime import datetime
from rapid_ct_app import app
from rapid_ct_app.users.models import User


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

@app.template_filter('humansize')
def human_size(bytes, units=[' bytes','KB','MB','GB','TB', 'PB', 'EB']):
    """ Returns a human readable string reprentation of bytes"""
    return str(bytes) + units[0] if bytes < 1024 else human_size(bytes>>10, units[1:])