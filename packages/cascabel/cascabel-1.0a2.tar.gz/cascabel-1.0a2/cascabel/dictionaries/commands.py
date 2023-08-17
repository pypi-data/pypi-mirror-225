commands = {
    "verify_libraries"        : ["--verify_libraries"       , "-vl"],
    "new_project"             : ["--new_project"            , "-new", "-n"],
    "make_controller"         : ["--make_controller"        , "-mc"],
    "make_crud_controller"    : ["--make_crud_controller", "-mcc"],
    "make_model"              : ["--make_model"             , "-mm"],
    "make_request"            : ["--make_request"           , "-re"],
    "help"                    : ["--help"                   , "-h" ],
    
}

full_commands = {
    "verify_libraries"        : "--verify_libraries",
    "new_project"             : "--new_project {project name}",
    "make_controller"         : "--make_controller {controller_name}",
    "make_crud_controller"    : "--make_crud_controller {controller_name}",
    "make_model"              : "--make_model {model_name} {bind}",
    "make_request"            : "--make_request {request_name}",
    "help"                    : "--help",
}