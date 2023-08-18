
class Route():

    def add_route(self, app, type: str, route: str, action, name: str, **kwargs):

        def function(**kwargs):
            return action(**kwargs)

        function.__name__ = name

        app.route(route,  methods = [type])(function)


    def add_error_route(self, app, error_code:int, action, name:str, **kwargs):
    
        def function(error, **kwargs):
            return action(error, **kwargs)

        function.__name__ = name

        app.errorhandler(error_code)(function)
   


