"""
This script runs the Slack_TrashTalk application using a development server.
"""

from os import environ
from Slack_TrashTalk import app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', '192.168.1.10')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
