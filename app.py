from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/bmi')
def calculate_bmi():
    try:
        weight = float(request.args.get('weight'))  # in kg
        height = float(request.args.get('height'))  # in meters
        if weight <= 0 or height <= 0:
            return jsonify({"error": "Weight and height must be positive"}), 400
        
        bmi = round(weight / (height ** 2), 2)
        if bmi < 18.5:
            category = "Underweight"
        elif bmi < 25:
            category = "Normal weight"
        elif bmi < 30:
            category = "Overweight"
        else:
            category = "Obese"
            
        return jsonify({
            "weight_kg": weight,
            "height_m": height,
            "bmi": bmi,
            "category": category
        }), 200
    except (TypeError, ValueError):
        return jsonify({"error": "Provide valid params: ?weight=70&height=1.75"}), 400

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    port = int(os.environ.get("APP_PORT", 5000))
    app.run(host='0.0.0.0', port=port)
