from config import app
from resources.routes.route import Route

from app.controllers.home_controller  import HomeController
from app.controllers.error_controller import ErrorController

Route().add_route(app, 'GET', '/'                                   , HomeController().index      , 'home_index')

Route().add_error_route(app, 404, ErrorController().error_404, 'error_404')
