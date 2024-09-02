from flask import Blueprint, request, jsonify
from src.services.scheduler import scheduler

webhook_bp = Blueprint('webhook_bp', __name__)

@webhook_bp.route('/api/receiveWebhookData', methods=['POST'])
def receive_webhook_data():
    if request.is_json:
        data = request.get_json()
        scheduler.update_calendar_data(data)
        print("Datos recibidos del calendario:", data)
        if scheduler.sheet_data:
            scheduler.process_availability()
        return jsonify({"message": "Datos procesados correctamente"}), 200
    else:
        return jsonify({"error": "Invalid JSON format"}), 400
