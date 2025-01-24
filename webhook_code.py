from flask import Flask, request, abort, jsonify
import json

app = Flask(__name__)

# Specify the path for the log file
LOG_FILE_PATH = 'data_store.json'

def save_data_to_file(data):
    """Overwrite the JSON file with new data."""
    with open(LOG_FILE_PATH, 'w') as f:
        json.dump(data, f)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        json_data = request.json
        # Save the received JSON data to a file (overriding old data)
        save_data_to_file(json_data)
        print(f"Received data: {json_data}")  # Log the received data
        return 'success', 200
    else:
        abort(400)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify(status='healthy'), 200

@app.route('/data', methods=['GET'])
def get_data():
    """Endpoint to retrieve stored JSON data."""
    try:
        with open(LOG_FILE_PATH, 'r') as f:
            data = json.load(f)
            return jsonify(data), 200
    except FileNotFoundError:
        return jsonify(error='No data found'), 404
    except json.JSONDecodeError:
        return jsonify(error='Data file is empty or corrupted'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)