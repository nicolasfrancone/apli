from flask import Blueprint, jsonify
from src.services.scheduler import get_scheduler  # Importar la función get_scheduler

slots_bp = Blueprint('slots_bp', __name__)

@slots_bp.route('/api/<profile_id>/getAvailableSlots', methods=['GET'])
def get_available_slots(profile_id):
    scheduler = get_scheduler(profile_id)  # Obtener la instancia específica del Scheduler para el profile_id
    return jsonify({
        "available_slots": scheduler.available_slots,
        "timezone": scheduler.sheet_time_zone,
        "intervalo": scheduler.sheet_interval,
        "modalidad": scheduler.modalidad
    })
