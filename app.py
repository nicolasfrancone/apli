from flask import Flask
from flask_cors import CORS

from src.routes.calendar_event_routes import event_bp
from src.routes.sheet_routes import sheet_bp
from src.routes.webhook_routes import webhook_bp
from src.routes.slots_routes import slots_bp

app = Flask(__name__)
CORS(app)

# Registrar Blueprints
app.register_blueprint(sheet_bp)
app.register_blueprint(webhook_bp)
app.register_blueprint(slots_bp)

app.register_blueprint(event_bp)

if __name__ == '__main__':
    app.run(debug=True)
