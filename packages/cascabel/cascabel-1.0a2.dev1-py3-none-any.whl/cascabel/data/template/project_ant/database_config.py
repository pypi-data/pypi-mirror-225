"""
SCRIPT    : database_config.py
OBJECTIVE : Declare databases and related models
"""

from resources.vars.vars import db
from resources.vars.vars import app

"""
SECTION   : Database Declaration
OBJECTIVE : Declare the database to be used
FUNCTIONS : add_database("BIND_KEY", "CONNECTION STRING [SQLALCHEMY FORMAT]")
"""

db.add_database('main', f"sqlite:///{app.config['FOLDER']}/databases/main.db")


"""
SECTION   : Binds and Models Initialization
OBJECTIVE : Initialize all the declared databases from the previous section and models in model_config.py.
"""

db.initialize_db_binds()
import model_config
db.initialize_models()

