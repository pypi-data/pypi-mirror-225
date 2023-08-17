from flask_sqlalchemy import SQLAlchemy
from resources.app.app import App

class Database(SQLAlchemy):
    app = App
    
    def __init__(self, app):
        self.app = app

    def add_database(self, bind:str, url:str):

        #Si no se ha asignado una base de datos se le asigna la primera bd como principal
        if self.app.config.get("SQLALCHEMY_DATABASE_URI") == None:
            self.app.config["SQLALCHEMY_DATABASE_URI"] = url

        #Se agrega la base de datos como un bind
        if self.app.config.get("SQLALCHEMY_BINDS") == None:
            self.app.config["SQLALCHEMY_BINDS"] = {}

        self.app.config["SQLALCHEMY_BINDS"][bind] = url
    
    def initialize_db_binds(self):
        super(Database, self).__init__(app = self.app)
        
    def initialize_models(self):
        with self.app.app_context():
            super(Database, self).create_all()

            