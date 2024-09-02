from flask import Blueprint, jsonify
from src.services.scheduler import scheduler

slots_bp = Blueprint('slots_bp', __name__)

@slots_bp.route('/api/getAvailableSlots', methods=['GET'])
def get_available_slots():
    return jsonify({
        "available_slots": scheduler.available_slots,
        "timezone": scheduler.sheet_time_zone,
        "intervalo": scheduler.sheet_interval,
        "modalidad": scheduler.modalidad
    })
