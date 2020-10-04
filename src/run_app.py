import os
from flask_api import app

if __name__ == '__main__':
    from werkzeug.serving import run_simple

    listening_port = int(os.getenv('PORT', 5008))
    run_simple(hostname='0.0.0.0', # keep it this way for VM development
               port=listening_port,
               application=app,
               use_debugger=False,
               use_reloader=True)
