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
- / (GET): Renders the '3-index.html' template.

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
    Determines the best matching locale for the current request.

    The locale is selected based on the client's "Accept-Language"
    header and the supported languages defined in the app's configuration.

    Returns:
        str: The best matching language from the supported languages.
    """
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route('/')
def get_index() -> str:
    """
    Renders the home/index page.

    Returns:
        str: Rendered HTML content of '3-index.html'.
    """
    return render_template('3-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
