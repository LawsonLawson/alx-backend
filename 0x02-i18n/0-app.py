#!/usr/bin/env python3
"""
Route module for the API - Basic Flask app.

This module sets up a basic Flask application with a single route that renders
an HTML template. The application is configured to be run as a standalone
server, with the host and port defined through environment variables.

Environment Variables:
- API_HOST: The host on which the Flask app will run (default is "0.0.0.0").
- API_PORT: The port on which the Flask app will run (default is "5000").

Routes:
- / (GET): Renders the '0-index.html' template.

Usage:
    python3 <this_script>.py
"""

from flask import Flask, request, render_template
from os import getenv

# Initialize the Flask application
app = Flask(__name__, static_url_path='')


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """
    GET /

    This route renders the '0-index.html' template when accessed.

    Returns:
        str: Rendered HTML content of '0-index.html'.
    """
    return render_template('0-index.html')


if __name__ == "__main__":
    # Get host and port from environment variables or use default values
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")

    # Run the Flask application
    app.run(host=host, port=port)
