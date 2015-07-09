import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from grap3 import models  # noqa
from grap3 import views  # noqa

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
