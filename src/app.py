from flask import Flask
from flask_migrate import Migrate

from config import config
from src.patents.application.fetch_patents_command_controller import (
    patents_command_controller,
)


def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    with app.app_context():
        from src.patents.infrastructure.models import session

        session.init_app(app)
        Migrate(app, session)

    app.register_blueprint(patents_command_controller)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
