from flask import Blueprint, request, jsonify
from src.services.scheduler import scheduler

sheet_bp = Blueprint('sheet_bp', __name__)

@sheet_bp.route('/api/receiveSheetData', methods=['POST'])
def receive_sheet_data():
    if request.is_json:
        data = request.get_json()
        scheduler.update_sheet_data(data)
        print("Datos recibidos de Google Sheet:", data)
        if scheduler.calendar_data:
            scheduler.process_availability()
        return jsonify({"message": "Datos procesados correctamente"}), 200
    else:
        return jsonify({"error": "Invalid JSON format"}), 400

@sheet_bp.route('/api/getSheetData', methods=['GET'])
def get_sheet_data():
    if scheduler.sheet_data:
        return jsonify(scheduler.sheet_data), 200
    else:
        return jsonify({"error": "No profile data available"}), 404
