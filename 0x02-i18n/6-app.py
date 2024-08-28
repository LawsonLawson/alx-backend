#!/usr/bin/env python3
"""
A simple Flask app.

This module sets up a basic Flask application with Babel for
internationalization (i18n) and localization (l10n) support. It includes user
handling and locale-based content rendering.

Configuration:
- DEBUG: Enabled
- Supported Languages: English ("en"), French ("fr")
- Default Locale: English ("en")
- Default Timezone: UTC

Routes:
- / (GET): Renders the '6-index.html' template.

Usage:
    python3 <this_script>.py
"""

from flask import Flask, g, render_template, request
from flask_babel import Babel


app = Flask(__name__)
app.url_map.strict_slashes = False

# Sample user data
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config:
    """
    Configuration class for the Flask application.

    Attributes:
        DEBUG (bool): Enables debug mode.
        LANGUAGES (list): Supported languages for the application.
        BABEL_DEFAULT_LOCALE (str): Default locale for the application.
        BABEL_DEFAULT_TIMEZONE (str): Default timezone for the application.
    """
    DEBUG = True
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)
babel = Babel(app)


def get_user() -> dict:
    """
    Retrieves a user based on the 'login_as' query parameter.

    If the 'login_as' parameter is provided and valid, returns the
    corresponding user dictionary. If the parameter is not provided or invalid,
    returns None.

    Returns:
        dict: User dictionary if found, otherwise None.
    """
    try:
        return users.get(int(request.args.get("login_as")))
    except TypeError:
        return None


@app.before_request
def before_request() -> None:
    """
    Executes before each request to set up the user context.

    Retrieves the user from the request and stores it in the global `g` object.
    """
    user = get_user()
    if user:
        g.user = user


@app.route("/", methods=["GET"])
def home() -> str:
    """
    Renders the home page.

    Returns:
        str: Rendered HTML content of '6-index.html'.
    """
    return render_template("6-index.html")


@babel.localeselector
def get_locale() -> str:
    """
    Determines the locale for the current request.

    The order of priority for locale is as follows:
    1. Locale from URL parameters
    2. Locale from user settings, if authenticated
    3. Locale from the request header
    4. Default locale

    Returns:
        str: Selected locale based on the priority order.
    """
    locale = request.args.get("locale")
    if locale in app.config["LANGUAGES"]:
        return locale

    user = getattr(g, "user", None)
    if user and user.get("locale") in app.config["LANGUAGES"]:
        return user.get("locale")

    return request.accept_languages.best_match(app.config["LANGUAGES"])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
