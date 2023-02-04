from app import logger
from helpers.logger import exception

from flask import Blueprint, render_template

errors = Blueprint("errors", __name__)

@exception(logger)
@errors.app_errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@exception(logger)
@errors.app_errorhandler(500)
def db_issue(e):
    return render_template('500.html'), 500

@exception(logger)
@errors.app_errorhandler(429)
def limiter_issue(e):
    return render_template('429.html'), 429
