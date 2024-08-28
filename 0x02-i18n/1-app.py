#!/usr/bin/env python3
"""
Route module for the API - Basic Babel setup.

This module sets up a Flask application with Babel for internationalization
and localization (i18n/l10n). The application supports English and French
languages by default. The host and port for the application are configurable
through environment variables.

Environment Variables:
- API_HOST: The host on which the Flask app will run (default is "0.0.0.0").
- API_PORT: The port on which the Flask app will run (default is "5000").

Routes:
- / (GET): Renders the '1-index.html' template.

Usage:
    python3 <this_script>.py
"""

from flask import Flask, request, render_template
from flask_babel import Babel
from os import getenv

# Initialize the Flask application
app = Flask(__name__)

# Initialize Babel for internationalization and localization
babel = Babel(app)


class Config(object):
    """
    Config class for setting up Babel configuration.

    Attributes:
        LANGUAGES (list): Supported languages for the application.
        BABEL_DEFAULT_LOCALE (str): Default locale for the application.
        BABEL_DEFAULT_TIMEZONE (str): Default timezone for the application.
    """
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


# Set the above Config class as the configuration for the Flask app
app.config.from_object('1-app.Config')


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """
    GET /

    This route renders the '1-index.html' template when accessed.

    Returns:
        str: Rendered HTML content of '1-index.html'.
    """
    return render_template('1-index.html')


if __name__ == "__main__":
    # Get host and port from environment variables or use default values
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")

    # Run the Flask application
    app.run(host=host, port=port)
