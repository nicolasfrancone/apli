from flask import Blueprint, request, jsonify

event_bp = Blueprint('event_bp', __name__)

# Dictionary to store the event_data per profile_id
event_data = {}

@event_bp.route('/api/<profile_id>/receiveEventId', methods=['POST'])
def receive_event_id(profile_id):
    if request.is_json:  # Check if the content is JSON
        data = request.get_json()  # Get the JSON content from the request

        # Ensure there's an entry for the profile_id in the event_data dictionary
        if profile_id not in event_data:
            event_data[profile_id] = {"event_id": None}

        event_data[profile_id]['event_id'] = data.get('event_id')  # Store the event_id

        # Here you can process the 'event_id' as needed
        print(f'Received event_id for profile {profile_id}: {event_data[profile_id]["event_id"]}')
        return jsonify({"message": "Event ID received successfully", "event_id": event_data[profile_id]["event_id"]}), 200
    else:
        return jsonify({"error": "Invalid JSON format"}), 400

@event_bp.route('/api/<profile_id>/getEventId', methods=['GET'])
def get_event_id(profile_id):
    if profile_id in event_data and event_data[profile_id]["event_id"] is not None:  # Check if there is a stored event_id
        return jsonify({"event_id": event_data[profile_id]["event_id"]}), 200
    else:
        return jsonify({"error": "No event ID available"}), 404
