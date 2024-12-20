from flask import Flask

def create_app():
    app = Flask(__name__, static_folder='static')

    from .routes import routes
    app.register_blueprint(routes)

    return app
