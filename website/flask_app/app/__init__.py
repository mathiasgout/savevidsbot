from helpers.logger import get_logger

from flask import Flask, abort
from flask_login import LoginManager


logger = get_logger(logger_name=__name__)

def create_app(config="DevConfig"):
    """
    Create and configure the app
    """

    app = Flask(__name__)

    # Config
    app.config.from_object(f'config.{config}')

    # Routes ans error handlers
    from .views import views
    from .errors import errors
    from .auth import auth
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(errors, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    # Login Manager
    from .models import User

    login_manager = LoginManager()
    login_manager.login_view = "views.home"
    login_manager.init_app(app)

    # Pour recharger l'instance de l'objet "User"
    @login_manager.user_loader
    def load_user(username):
        return User(id=username).get_user()
    
    # Pour retourner un 404 si l'utilisateur n'est pas log (à la place d'un 401)
    @login_manager.unauthorized_handler
    def unauthorized():
        # do stuff
        return abort(404)
        
    return app