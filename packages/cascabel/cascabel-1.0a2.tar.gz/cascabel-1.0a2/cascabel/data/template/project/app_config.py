"""
SCRIPT    : app_config.py
OBJECTIVE : Assign or modify attributes of the 'flask' object.
"""

from resources.vars.vars import app

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

