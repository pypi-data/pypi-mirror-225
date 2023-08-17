def main():
   import sys, os
   
   import platform

   if platform.system() == "Windows":
      os.system("cls")
   elif platform.system() == "Linux":
      os.system("clear")
   elif platform.system() == "Darwin":
      os.system("clear")
   else:
      print(platform.system())

   from cascabel.dictionaries.commands import commands
   from cascabel.classes.cascabel import Cascabel


   if len(sys.argv) == 1:
      Cascabel().show_info()

   elif len(sys.argv) == 2 and sys.argv[1] in commands["verify_libraries"]:
      Cascabel().verify_libraries()

   elif len(sys.argv) == 2 and sys.argv[1] in commands["help"]:
      Cascabel().show_help()

   elif len(sys.argv) == 3 and sys.argv[1] in commands["new_project"]:
      Cascabel().create_new_project()

   elif len(sys.argv) == 3 and sys.argv[1] in commands["make_controller"]:
      Cascabel().make_controller()

   elif len(sys.argv) == 3 and sys.argv[1] in commands["make_crud_controller"]:
      Cascabel().make_crud_controller()
   
   elif (len(sys.argv) == 3 or len(sys.argv)) == 4 and sys.argv[1] in commands["make_model"]:
      Cascabel().make_model()

   elif len(sys.argv) == 3 and sys.argv[1] in commands["make_request"]:
      Cascabel().make_request()
      
   else:
      Cascabel().catch_error()
         
   print()

if __name__ == "__main__":
   main()