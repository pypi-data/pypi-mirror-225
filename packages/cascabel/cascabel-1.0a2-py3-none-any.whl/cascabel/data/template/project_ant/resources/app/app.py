from flask import Flask
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

#++++++++++++++++++++++++++++++++++++++++++++++++++++++
class App(Flask):
    
    SQLAlchemy_instance : SQLAlchemy
    
    
    #++++++++++++++++++++++++++++++++++++++++++++++++++
    def __init__(self, app_name : str):
        super(App, self).__init__(app_name)
        self.__config_declaration()
        
        
    #++++++++++++++++++++++++++++++++++++++++++++++++++
    def __config_declaration(self):
        import pathlib
        
        main_path = str(pathlib.Path(__file__).parent.absolute())
        main_path = main_path.split('\\')
        main_path.pop(); main_path.pop()
        main_path = '/'.join(main_path)
        
        self.config['FOLDER'] = main_path
        self.config['ENV_PATH'] = f"{self.config['FOLDER']}/.env"
        
        load_dotenv(self.config['ENV_PATH'])
        
        self.secret_key = os.getenv("SECRET_KEY")
    
    
    #++++++++++++++++++++++++++++++++++++++++++++++++++
    def add_route(self, method: str, route: str, action, flask_name: str, **kwargs):
        
        def function(**kwargs):
            return action(**kwargs)

        function.__name__ = flask_name

        self.route(route,  methods = [method])(function)
        
        
    #++++++++++++++++++++++++++++++++++++++++++++++++++
    def add_error_route(self, error_code:int, action, flask_name:str, **kwargs):
    
        def function(error, **kwargs):
            return action(error, **kwargs)

        function.__name__ = flask_name

        self.errorhandler(error_code)(function)
        
    
