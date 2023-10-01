from flask import Blueprint, render_template

error = Blueprint('error', __name__)

@error.app_errorhandler(404)
def error_handler_404(error):
    return render_template("error/404.html")

@error.app_errorhandler(403)
def error_handler_403(error):
    return render_template("error/403.html")

@error.app_errorhandler(500)
def error_handler_500(error):
    return render_template("error/500.html")
