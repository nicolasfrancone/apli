from flask import Blueprint, request, jsonify

event_bp = Blueprint('event_bp', __name__)

# Global variable to store the last received event_id
event_data = {
    "event_id": None
}

@event_bp.route('/api/<profile_id>/receiveEventId', methods=['POST'])
def receive_event_id(profile_id):
    if request.is_json:  # Check if the content is JSON
        data = request.get_json()  # Get the JSON content from the request
        event_data['event_id'] = data.get('event_id')  # Store the event_id

        # Here you can process the 'event_id' as needed
        print(f'Received event_id: {event_data["event_id"]}')
        return jsonify({"message": "Event ID received successfully", "event_id": event_data["event_id"]}), 200
    else:
        return jsonify({"error": "Invalid JSON format"}), 400

@event_bp.route('/api/<profile_id>/getEventId', methods=['GET'])
def get_event_id(profile_id):
    if event_data["event_id"] is not None:  # Check if there is a stored event_id
        return jsonify({"event_id": event_data["event_id"]}), 200
    else:
        return jsonify({"error": "No event ID available"}), 404
