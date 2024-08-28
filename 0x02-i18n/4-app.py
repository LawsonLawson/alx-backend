#!/usr/bin/env python3
"""
A Basic Flask app with internationalization support.

This module sets up a Flask application with Babel to provide
internationalization (i18n) and localization (l10n) support. The app
supports English and French languages by default.

Configuration:
- Default Locale: English ("en")
- Default Timezone: UTC

Routes:
- / (GET): Renders the '4-index.html' template.

Usage:
    python3 <this_script>.py
"""

from flask import Flask, render_template, request
from flask_babel import Babel


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


@babel.localeselector
def get_locale() -> str:
    """
    Retrieves the locale for a web page.

    This function first checks for a 'locale' parameter in the query string.
    If the parameter is found and its value is in the list of supported
    languages, it returns that locale. If not, it defaults to the best
    match from the client's "Accept-Language" header.

    Returns:
        str: The selected locale.
    """
    queries = request.query_string.decode('utf-8').split('&')
    query_table = dict(
        map(
            lambda x: (x if '=' in x else '{}='.format(x)).split('='),
            queries
        )
    )
    if 'locale' in query_table:
        if query_table['locale'] in app.config["LANGUAGES"]:
            return query_table['locale']
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route('/')
def get_index() -> str:
    """
    The home/index page.

    Renders the '4-index.html' template.

    Returns:
        str: Rendered HTML content of '4-index.html'.
    """
    return render_template('4-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
