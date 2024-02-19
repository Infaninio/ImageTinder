"""A WebUi for ImageTinder to access a lokal nextcloud."""
import os

from flask import Flask, redirect, render_template


def create_app(test_config=None) -> Flask:
    """Create the ImageTinder Webbapp.

    Parameters
    ----------
    test_config : _type_, optional
        Configuration for testing, by default None

    Returns
    -------
    Flask
        A Flask app.
    """
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",  # pragma: allowlist secret
        DATABASE=os.path.join(app.instance_path, "ImageTinder.sqlite"),
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello

    @app.route("/")
    def root():
        return redirect("/index")

    @app.route("/index")
    def index():
        return render_template("welcome.html")

    from . import db

    db.init_app(app)

    from . import auth

    app.register_blueprint(auth.bp)

    from . import configs

    app.register_blueprint(configs.bp)

    return app
