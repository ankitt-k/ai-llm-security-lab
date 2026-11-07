from flask import Flask, request, jsonify
import requests
from validate import validate_input, scan_output

app = Flask(__name__)

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form.get('prompt', '')

    valid, error_msg = validate_input(user_input)
    if not valid:
        return jsonify({"error": error_msg}), 400

    response = requests.post('http://localhost:11434/api/generate',
                              json={"model": "llama3", "prompt": user_input, "stream": False})
    model_output = response.json().get("response", "")

    safe, error_msg = scan_output(model_output)
    if not safe:
        return jsonify({"error": error_msg}), 400

    return jsonify({"response": model_output})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
