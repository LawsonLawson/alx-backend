#!/usr/bin/env python3
"""
A Basic Flask app.

This module sets up a Flask application with Babel for handling
internationalization and localization (i18n/l10n). The app supports
multiple languages, with English and French as the default options.

Configuration:
- Default Locale: English ("en")
- Default Timezone: UTC

Routes:
- / (GET): Renders the '2-index.html' template.

Usage:
    python3 <this_script>.py
"""

from flask_babel import Babel
from flask import Flask, render_template, request


class Config:
    """
    Represents a Flask Babel configuration.

    Attributes:
        LANGUAGES (list): Supported languages for the application.
        BABEL_DEFAULT_LOCALE (str): Default locale for the application.
        BABEL_DEFAULT_TIMEZONE (str): Default timezone for the application.
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


# Initialize the Flask application
app = Flask(__name__)


app.config.from_object(Config)
app.url_map.strict_slashes = False

# Initialize Babel for internationalization and localization
babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
    """
    Retrieves the best matching locale for a web page based on the
    client's request.

    Returns:
        str: The best matching language from the supported languages.
    """
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route('/')
def get_index() -> str:
    """
    The home/index page route.

    This route renders the '2-index.html' template.

    Returns:
        str: Rendered HTML content of '2-index.html'.
    """
    return render_template('2-index.html')


if __name__ == '__main__':
    # Run the Flask application
    app.run(host='0.0.0.0', port=5000)
