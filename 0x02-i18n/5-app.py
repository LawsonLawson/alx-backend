#!/usr/bin/env python3
"""
A Basic Flask app with internationalization support.

This module sets up a Flask application with Babel to provide
internationalization (i18n) and localization (l10n) support. It includes
user handling and locale-based content rendering.

Configuration:
- Default Locale: English ("en")
- Default Timezone: UTC

Routes:
- / (GET): Renders the '5-index.html' template.

Usage:
    python3 <this_script>.py
"""

from flask import Flask, render_template, request, g
from flask_babel import Babel
from typing import Union, Dict


class Config:
    """
    Represents the configuration for Flask Babel.

    Attributes:
        LANGUAGES (list): Supported languages for the application.
        BABEL_DEFAULT_LOCALE (str): Default locale for the application.
        BABEL_DEFAULT_TIMEZONE (str): Default timezone for the application.
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)

# Sample user data
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user() -> Union[Dict, None]:
    """
    Retrieves a user based on a user id.

    The user id is expected to be passed as a query parameter 'login_as'.
    If the user id is valid and found in the user data, the corresponding
    user dictionary is returned. Otherwise, returns None.

    Returns:
        Union[Dict, None]: User dictionary if found, otherwise None.
    """
    login_id = request.args.get('login_as')
    if login_id:
        return users.get(int(login_id))
    return None


@app.before_request
def before_request() -> None:
    """
    Performs some routines before each request's resolution.

    This function sets the global `g.user` variable to the user returned by
    `get_user()`, based on the 'login_as' query parameter.
    """
    user = get_user()
    g.user = user


@babel.localeselector
def get_locale() -> str:
    """
    Retrieves the locale for a web page.

    This function checks for a 'locale' query parameter. If the locale is
    in the list of supported languages, it returns that locale. Otherwise,
    it defaults to the best match from the client's "Accept-Language" header.

    Returns:
        str: The selected locale.
    """
    locale = request.args.get('locale', '')
    if locale in app.config["LANGUAGES"]:
        return locale
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route('/')
def get_index() -> str:
    """
    The home/index page.

    Renders the '5-index.html' template.

    Returns:
        str: Rendered HTML content of '5-index.html'.
    """
    return render_template('5-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
