from flask import Flask

app = Flask(__name__)

app.config.from_object('rdany.config.Config')

from rdany.modules.main import main
app.register_blueprint(main)
