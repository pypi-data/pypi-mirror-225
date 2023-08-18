"""
SCRIPT    : execute.py
OBJECTIVE : Initialize the app.
"""

import app_config
import route_config
import database_config

from resources.vars.vars import app
from resources.vars.vars import db

app.run(debug=True)
