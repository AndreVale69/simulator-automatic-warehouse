import os

DOCUMENTATION = """
The configuration file contains all the variables required to run the webpage.
The following variables are required or optional:
- HOST: Host IP used to serve the application.
- PORT: Port used to serve the application.
- (optional) PROXY: If this application will be served to a different URL
                    via a proxy configured outside of Python, you can list it here
                    as a string of the form {input}::{output}, for example:
                    http://0.0.0.0:8050::https://my.domain.com
                    so that the startup message will display an accurate URL.
"""

HOST = os.environ['HOST']
PORT = int(os.environ['PORT'])
PROXY = os.environ.get('PROXY', None)