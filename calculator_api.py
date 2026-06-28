from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

VALID_OPERATIONS = {"add", "subtract", "multiply", "divide", "percent", "toggle-sign"}


def calculate(left=None, right=None, action=None, value=None):
    try:
        if action in {"add", "subtract", "multiply", "divide"}:
            left = float(left)
            right = float(right)
        else:
            value = float(value)
    except (TypeError, ValueError):
        return None, "Invalid numeric value"

    if action == "add":
        return left + right, None
    if action == "subtract":
        return left - right, None
    if action == "multiply":
        return left * right, None
    if action == "divide":
        if right == 0:
            return None, "Division by zero"
        return left / right, None
    if action == "percent":
        return value / 100, None
    if action == "toggle-sign":
        return -value, None

    return None, "Unsupported action"


@app.route("/api/calc", methods=["POST"])
def api_calc():
    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"error": "JSON body required"}), 400

    action = payload.get("action")
    if not action or action not in VALID_OPERATIONS:
        return jsonify({"error": "Invalid or missing action"}), 400

    result, error = calculate(
        left=payload.get("left"),
        right=payload.get("right"),
        action=action,
        value=payload.get("value"),
    )

    if error:
        return jsonify({"error": error}), 400

    return jsonify({"result": result})


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
