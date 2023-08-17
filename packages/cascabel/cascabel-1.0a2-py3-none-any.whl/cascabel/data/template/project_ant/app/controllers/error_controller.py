from flask import render_template

class ErrorController:

    def error_404(self, error = ""):
        return render_template("error/index.html", error = error)
