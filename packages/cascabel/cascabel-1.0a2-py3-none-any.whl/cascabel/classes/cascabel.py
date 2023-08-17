import os, sys, shutil, colorama
cmd_dir  = os.getcwd()
file_dir = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/").replace("/classes", "")

class Cascabel:
    
    PROJECT_DIR     = f'{cmd_dir}'.replace("\\", "/")
    CONTROLLER_DIR  = f"{PROJECT_DIR}/app/controllers"
    ROUTE_FILE      = f"{PROJECT_DIR}/route_config.py"
    CONFIG_FILE     = f"{PROJECT_DIR}/app_config.py"
    DATABASE_FILE   = f"{PROJECT_DIR}/database_config.py"
    EXCECUTION_FILE = f"{PROJECT_DIR}/execute.py"
    
    VERSION = "1.0a2"
    
    
    #================================================================================================
    def print_simplify_logo (self):

        w_c = colorama.Style.RESET_ALL
        y_c = colorama.Fore.YELLOW

        logo =   y_c + "   _______  _\n"
        logo +=  y_c + "  /  __  c\\|_|\n"
        logo +=  y_c + " |  /  \__/|__|\n"
        logo +=  y_c + " |  |      | __|\n"
        logo +=  y_c + " |  \__/\\  | |\n"
        logo +=  y_c + "  \_____/ |_/  versión " + self.VERSION + "\n" + w_c

        print(logo)
        

    #==============================================================#
    def print_logo (self):

        clear_command = 'cls' if os.name in ('nt', 'dos') else 'clear'
        os.system(clear_command)

        w_c = colorama.Style.RESET_ALL #Si la consola es oscura se muestra de color blanco y viceversa.
        y_c = colorama.Fore.YELLOW

        logo =   f"{y_c}   _______  {w_c}                       _            {y_c} _\n"
        logo +=  f"{y_c}  /  __  c\\{w_c}                       | |          {y_c} |_|\n"
        logo +=  f"{y_c} |  /  \__/{w_c}__ _  ___   ___   __ _ | |__    ___  {y_c}|__|\n"
        logo +=  f"{y_c} |  |     {w_c}/ _' |/ __| / __| / _' || '_ \  / _ \\{y_c} | __|\n"
        logo +=  f"{y_c} |  \__/\\{w_c}| (_| |\__ \| (__ | (_| || |_) ||  __/{y_c} | |\n"
        logo +=  f"{y_c}  \_____/ {w_c}\__,_||___/ \___| \__,_||_.__/  \___|{y_c}|_/  versión {self.VERSION} \n {w_c}"

        print(logo)

        """
        import platform
          
        print(' Sistema Operativo:', platform.system() )
        print(' Platafotma       :', sys.platform)
        print(' Distribucion     :', platform.platform())
        print(' Version de python:', sys.version.replace('\n',''))
        print(' Version dict     :', sys.version_info)
        print(' Ejecutable actual:', sys.executable)
        print(' Argumentos       :', sys.argv)
        print(' Ruta actual      :', os.getcwd())
        print(' Ruta de ejecución:', os.path.dirname(os.path.realpath(__file__)))
        """
        print('')

    
    #==============================================================#
    def catch_error(self):

        w_c = colorama.Fore.WHITE
        y_c = colorama.Fore.YELLOW

        Cascabel().print_logo()

        from cascabel.dictionaries.commands import commands, full_commands
        
        print(" Comando no valido")

        import difflib
        import itertools

        keys = list(commands.keys())
        values = list(itertools.chain.from_iterable(commands.values()))

        all_words = keys + values

        coincidences = difflib.get_close_matches(sys.argv[1], all_words)

        possible_command = ""
        
        if len(coincidences) != 0:
            coincidence = coincidences[0]

            if coincidence in keys:
                possible_command = full_commands[coincidence]
                print(f"\n ¿Quisiste ejecutar el siguiente comando '{y_c}{possible_command}{w_c}' ?")
                return
        
        for arg in sys.argv:
            for key, value in commands.items():
                if arg in value:
                    possible_command = full_commands[key]
                    
        if possible_command != "":
            print(f"\n ¿Quisiste ejecutar el siguiente comando '{y_c}{possible_command}{w_c}' ?")
                
            
    #==============================================================#
    def verify_libraries(self):
        self.print_logo()

        w_c = colorama.Style.RESET_ALL
        y_c = colorama.Fore.YELLOW
        r_c = colorama.Fore.RED

        print(y_c + " Librerias Necesarias" + w_c)

        try:
            import flask
            print(" |- Flask  : Instalado")
        except:
            print(" |- Flask  : " + r_c + "No instalado" + w_c)

        try:
            import dotenv 
            print(" |- Dotevn: Instalado")
        except:
            print(" |- Dotevn: " + r_c + "No instalado" + w_c)

        try:
            import flask_wtf
            print(" |- Flask-WTF: Instalado")
        except:
            print(" |- Flask-WTF: " + r_c + "No instalado" + w_c)

        try:
            import flask_sqlalchemy 
            print(" |- Flask-SqlAlchemy: Instalado")
        except:
            print(" |- Flask-SqlAlchemy: " + r_c + "No instalado" + w_c) 


    #==============================================================#
    def show_info(self):

        self.print_logo()

        print(" Versión de python : " + sys.version.split(" ")[0] + "\n")
        print(" Desarrollado por Ignacio Aguilera")

    
    #==============================================================#
    def show_help(self):
        self.print_logo()

        from cascabel.dictionaries.commands import full_commands
    
        for key, command in full_commands.items():
            print(f' {key.ljust(20)} -> {command}')

    
    #==============================================================#
    def create_new_project(self):

        project_name = sys.argv[2].lower()
        project_dir  = f'{cmd_dir}/{project_name}/'
        template_dir = f'{file_dir}/data/template/project/'

        if os.path.isdir((project_dir)):
            self.print_logo()
            print(f" Ya existe una carpeta con el nombre '{project_name}' en el directorio actual")
        else:
            self.print_logo()
            shutil.copytree(template_dir, project_dir, ignore=shutil.ignore_patterns('empty_file.txt'))
            print(" La plantilla del proyecto ha sido creada correctamente")
    
    #==============================================================#
    def make_controller(self):

        self.print_logo()
        
        controller_name = sys.argv[2].lower()
        controller_class_name = controller_name.replace("_", " ").title().replace(" ", "") + "Controller"

        controller_template_dir = f'{file_dir}/data/template/controller/simple_controller.py'
        
        content = open(controller_template_dir, "r").read().replace("NAME", controller_class_name)
        
        new_controller_path = f"{self.CONTROLLER_DIR}/{controller_name}_controller.py"
        
        if not os.path.isdir(self.CONTROLLER_DIR):
            print(f" No se detecta siguiente directorio : {self.CONTROLLER_DIR}/")
            return
        
        elif not os.path.isfile(self.ROUTE_FILE):
            print(f" No se detecta archivo : {self.CONTROLLER_DIR}")
            return
        
        if os.path.isfile(new_controller_path):
            print(f" Error ya existe {controller_name}_controller.py")
            return
        
        file = open(new_controller_path, "w")
        file.write(content)
        file.close()

        routes_content = open(self.ROUTE_FILE, "r+").read()
        
        import_stat = f"\nfrom app.controllers.{controller_name}_controller import {controller_class_name}\n"
        add_route_stat = f"app.add_route('GET', '/{controller_name}',  {controller_class_name}().index , '{controller_name}_index') \n"
        
        routes_content = routes_content +import_stat + add_route_stat
        
        file = open(self.ROUTE_FILE, "w").write(routes_content)

        print(" El controlador ha sido creada correctamente")

    #==============================================================#
    def make_request(self):
        
        self.print_logo()

        request_name = sys.argv[2].lower()
        request_class_name = request_name.replace("_", " "). title().replace(" ", "") + "Request"

        project_dir  = f'{cmd_dir}/'
        request_template_dir = f'{file_dir}/data/template/request/request.py'

        content = open(request_template_dir, "r").read().replace("NAME", request_class_name)

        if not os.path.isdir(project_dir + "app/requests/"):
            print(" Directorio invalido")
            return

        if os.path.isfile(project_dir + "app/requests/" + request_name +"_controller.py"):
            print(" Error el archivo ya existe")
            return

        file = open( f"{project_dir}app/requests/{request_name}_request.py", "w")
        
        file.write(content)
        file.close()

        print(" El request ha sido creado correctamente")

    #==============================================================#
    def make_crud_controller(self):

        self.print_logo()

        controller_name = sys.argv[2].lower()
        controller_class_name = controller_name.replace("_", " ").title().replace(" ", "") + "Controller"

        project_dir  = f'{cmd_dir}/'
        controller_template_dir = f'{file_dir}/data/template/controller/manager_controller.py'

        content = open(controller_template_dir, "r").read().replace("CLASSNAME", controller_class_name).replace("NAME", controller_name)
        
        new_controller_path = f"{self.CONTROLLER_DIR}/{controller_name}_controller.py"
        
        if not os.path.isdir(self.CONTROLLER_DIR):
            print(f" No se detecta siguiente directorio : {self.CONTROLLER_DIR}/")
            return
        
        elif not os.path.isfile(self.ROUTE_FILE):
            print(f" No se detecta archivo : {self.CONTROLLER_DIR}")
            return
        
        if os.path.isfile(new_controller_path):
            print(f" Error ya existe {controller_name}_controller.py")
            return
        
        file = open(new_controller_path, "w")
        file.write(content)
        file.close()

        routes_content = open(project_dir + "route_config.py", "r+").read()
        import_stat = f"\nfrom app.controllers.{controller_name}_controller import {controller_class_name}\n"
        add_route_stat =  f"app.add_route('GET', '/{controller_name}',  {controller_class_name}().index , '{controller_name}_index') \n"
        add_route_stat += f"app.add_route('GET', '/{controller_name}/view/<id>',  {controller_class_name}().read , '{controller_name}_view') \n"
        add_route_stat += f"app.add_route('GET', '/{controller_name}/store',  {controller_class_name}().get_store , 'get_{controller_name}_store') \n"
        add_route_stat += f"app.add_route('POST', '/{controller_name}/store',  {controller_class_name}().post_store , 'post_{controller_name}_store') \n"
        add_route_stat += f"app.add_route('GET', '/{controller_name}/update/<id>',  {controller_class_name}().get_update , 'get_{controller_name}_update') \n"
        add_route_stat += f"app.add_route('POST', '/{controller_name}/update/<id>',  {controller_class_name}().post_update , 'post_{controller_name}_update') \n"
        add_route_stat += f"app.add_route('POST', '/{controller_name}/delete/<id>',  {controller_class_name}().delete , '{controller_name}_delete') \n"

        routes_content = routes_content +import_stat + add_route_stat
        
        file = open(self.ROUTE_FILE, "w").write(routes_content)

        controller_html_path = f'templates/{controller_name}' 
        if not os.path.exists(controller_html_path):
            os.makedirs(controller_html_path)

        html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PAGE</title>
</head>
<body>
    <p>PAGE</p>
</body>
</html>
        """

        file = open(controller_html_path + "/index.html", "w").write(html_content.replace('PAGE', f'{controller_name}_index'))
        file = open(controller_html_path + "/view.html", "w").write(html_content.replace('PAGE', f'{controller_name}_view'))
        file = open(controller_html_path + "/store.html", "w").write(html_content.replace('PAGE', f'get_{controller_name}_store'))
        file = open(controller_html_path + "/update.html", "w").write(html_content.replace('PAGE', f'get_{controller_name}_update'))

        print(" El controlador sido creada correctamente")
    
    
    #==============================================================#
    def make_model(self):
        self.print_logo()

        model_name = sys.argv[2].lower()
        model_bind = sys.argv[3]
        model_class_name = model_name.replace("_", " ").title().replace(" ", "") + "Model"

        project_dir  = f'{cmd_dir}'
        
        model_path = f"{project_dir}/app/models/"
        model_file_path = f"{project_dir}/app/models/{model_bind}/{model_name}_model.py"
        
        if not os.path.isdir(model_path):
            print(" No se detecta directorio {model_path}")
            return 
        
        if not os.path.isfile(project_dir + "/database_config.py"):
            print(" No se detecta archivo database_config.py")
            return 
        
        if not os.path.isdir(project_dir + f"/app/models/{model_bind}/"):
            os.mkdir(project_dir + f"/app/models/{model_bind}/")
        
        if os.path.isfile(model_file_path):
            print(f" Error: ya existe componente {model_file_path}")
            return 
        
        with open(model_file_path, "w") as file:
            model_template_dir = f'{file_dir}/data/template/model/model.py'
            
            content = open(model_template_dir, "r").read()
            content = content.replace("TABLE_NAME", model_name)
            content = content.replace("NAME", model_class_name)
            content = content.replace("BIND", model_bind)
            
            file.write(content)

        database_content = open(project_dir + "/model_config.py", "r+").read()
        import_stat = f"from app.models.{model_bind}.{model_name}_model import {model_class_name}\n"

        database_content =  database_content + import_stat
 
        file = open(project_dir + "/model_config.py", "w").write(database_content)

        print(f" El modelo {model_class_name} sido creada correctamente")
