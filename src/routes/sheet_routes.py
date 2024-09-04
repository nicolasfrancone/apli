from flask import Blueprint, request, jsonify
from src.services.scheduler import get_scheduler  # Importar get_scheduler

sheet_bp = Blueprint('sheet_bp', __name__)

@sheet_bp.route('/api/<profile_id>/receiveSheetData', methods=['POST'])
def receive_sheet_data(profile_id):
    scheduler = get_scheduler(profile_id)  # Obtener la instancia específica del Scheduler para el profile_id
    if request.is_json:
        data = request.get_json()
        scheduler.update_sheet_data(data)
        print(f"Datos recibidos de Google Sheet para el usuario {profile_id}:", data)
        if scheduler.calendar_data:
            scheduler.process_availability()
        return jsonify({"message": "Datos procesados correctamente"}), 200
    else:
        return jsonify({"error": "Invalid JSON format"}), 400

@sheet_bp.route('/api/<profile_id>/getSheetData', methods=['GET'])
def get_sheet_data(profile_id):
    scheduler = get_scheduler(profile_id)  # Obtener la instancia específica del Scheduler para el profile_id
    if scheduler.sheet_data:
        return jsonify(scheduler.sheet_data), 200
    else:
        return jsonify({"error": "No profile data available"}), 404
