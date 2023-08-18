"""
SCRIPT     : route_config.py
OBJECTIVE  : Contain all the access routes related to the web application.
"""

from resources.vars.vars import app


"""
SECTION   : Route Declaration
OBJECTIVE : Contain all the access routes related to the web application.
FUNCTIONS : add_route(METHOD, PATH, CONTROLLER_ACTION, FLASK_NAME)
            add_error_route(ERROR_CODE, CONTROLLER_ACTION, FLASK_NAME)
"""

from app.controllers.home_controller  import HomeController
from app.controllers.error_controller import ErrorController

app.add_route('GET', '/', HomeController().index, 'home_index')
app.add_error_route(404, ErrorController().error_404, '404_error')
