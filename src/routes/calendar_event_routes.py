from flask import Blueprint, request, jsonify

event_bp = Blueprint('event_bp', __name__)

# Variable global para almacenar el último event_id recibido
event_data = {
    "event_id": None
}

@event_bp.route('/api/receiveEventId', methods=['POST'])
def receive_event_id():
    if request.is_json:  # Verifica si el contenido es JSON
        data = request.get_json()  # Obtén el contenido JSON del request
        event_data['event_id'] = data.get('event_id')  # Guarda el event_id

        # Aquí puedes procesar el 'event_id' como lo necesites
        print(f'Recibido event_id: {event_data["event_id"]}')
        return jsonify({"message": "Event ID recibido correctamente", "event_id": event_data["event_id"]}), 200
    else:
        return jsonify({"error": "Invalid JSON format"}), 400

@event_bp.route('/api/getEventId', methods=['GET'])
def get_event_id():
    if event_data["event_id"] is not None:  # Verifica si hay un event_id almacenado
        return jsonify({"event_id": event_data["event_id"]}), 200
    else:
        return jsonify({"error": "No event ID available"}), 404
