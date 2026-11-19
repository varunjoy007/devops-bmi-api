import os
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

HTML_UI = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>BMI Calculator — DevOps Microservice</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; }
    body {
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f766e 100%);
      color: #f8fafc;
      padding: 24px;
    }
    .card {
      background: rgba(30, 41, 59, 0.88);
      backdrop-filter: blur(14px);
      border: 1px solid rgba(255, 255, 255, 0.14);
      border-radius: 24px;
      padding: 44px 40px;
      width: 100%;
      max-width: 540px;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.55);
    }
    .badge-top {
      display: inline-block;
      background: rgba(20, 184, 166, 0.2);
      color: #5eead4;
      font-size: 14px;
      font-weight: 700;
      padding: 6px 14px;
      border-radius: 999px;
      margin-bottom: 14px;
      letter-spacing: 0.6px;
    }
    h1 { font-size: 34px; font-weight: 800; margin-bottom: 8px; }
    p.subtitle { color: #cbd5e1; font-size: 17px; line-height: 1.45; margin-bottom: 28px; }
    .form-group { margin-bottom: 20px; }
    label { display: block; font-size: 16px; font-weight: 600; color: #e2e8f0; margin-bottom: 8px; }
    input {
      width: 100%;
      padding: 15px 16px;
      border-radius: 12px;
      border: 1px solid #475569;
      background: #0f172a;
      color: #f8fafc;
      font-size: 18px;
      outline: none;
      transition: border-color 0.2s, box-shadow 0.2s;
    }
    input:focus {
      border-color: #14b8a6;
      box-shadow: 0 0 0 3px rgba(20, 184, 166, 0.28);
    }
    .row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
    button {
      width: 100%;
      margin-top: 10px;
      padding: 17px;
      border: none;
      border-radius: 14px;
      background: linear-gradient(135deg, #14b8a6, #0d9488);
      color: #fff;
      font-size: 19px;
      font-weight: 700;
      cursor: pointer;
      transition: transform 0.15s, box-shadow 0.15s;
    }
    button:hover { transform: translateY(-1px); box-shadow: 0 10px 20px -5px rgba(20, 184, 166, 0.45); }
    button:active { transform: translateY(0); }
    .result-box {
      margin-top: 28px;
      padding: 24px;
      border-radius: 16px;
      background: #0f172a;
      border: 1px solid #334155;
      text-align: center;
      display: none;
      animation: fadeIn 0.3s ease;
    }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: translateY(0); } }
    .result-label { font-size: 15px; font-weight: 600; color: #94a3b8; text-transform: uppercase; letter-spacing: 1.2px; }
    .bmi-score { font-size: 54px; font-weight: 800; line-height: 1.1; margin: 8px 0; }
    .category-pill {
      display: inline-block;
      padding: 7px 18px;
      border-radius: 999px;
      font-size: 16px;
      font-weight: 700;
      margin-top: 6px;
    }
    .meta-info { font-size: 15px; color: #cbd5e1; margin-top: 14px; }
    .error-msg { color: #f87171; font-size: 15px; font-weight: 600; margin-top: 14px; text-align: center; display: none; }
  </style>
</head>
<body>
  <div class="card">
    <span class="badge-top">KUBERNETES DEPLOYED • v2.0</span>
    <h1>BMI Health Calculator</h1>
    <p class="subtitle">Enter your age, height, and weight to compute your Body Mass Index instantly.</p>

    <form id="bmiForm">
      <div class="row">
        <div class="form-group">
          <label for="age">Age (years)</label>
          <input type="number" id="age" min="2" max="120" value="20" required />
        </div>
        <div class="form-group">
          <label for="weight">Weight (kg)</label>
          <input type="number" id="weight" step="0.1" min="1" placeholder="e.g. 70" required />
        </div>
      </div>

      <div class="form-group">
        <label for="height">Height (cm)</label>
        <input type="number" id="height" step="0.1" min="50" max="260" placeholder="e.g. 175" required />
      </div>

      <button type="submit">Calculate BMI</button>
    </form>

    <div id="errorMsg" class="error-msg"></div>

    <div id="resultBox" class="result-box">
      <div class="result-label">Your BMI Score</div>
      <div id="bmiScore" class="bmi-score">22.86</div>
      <div id="categoryPill" class="category-pill">Normal weight</div>
      <div id="metaInfo" class="meta-info"></div>
    </div>
  </div>

  <script>
    document.getElementById('bmiForm').addEventListener('submit', async (e) => {
      e.preventDefault();
      const age = parseInt(document.getElementById('age').value, 10);
      const weight = parseFloat(document.getElementById('weight').value);
      const heightCm = parseFloat(document.getElementById('height').value);
      const heightM = (heightCm / 100).toFixed(4);

      const errorBox = document.getElementById('errorMsg');
      const resultBox = document.getElementById('resultBox');
      errorBox.style.display = 'none';

      try {
        const res = await fetch(`/bmi?weight=${weight}&height=${heightM}`);
        const data = await res.json();

        if (!res.ok) {
          errorBox.textContent = data.error || 'Invalid input values.';
          errorBox.style.display = 'block';
          resultBox.style.display = 'none';
          return;
        }

        const pill = document.getElementById('categoryPill');
        const score = document.getElementById('bmiScore');
        score.textContent = data.bmi;
        pill.textContent = data.category;

        let color = '#22c55e', bg = 'rgba(34, 197, 94, 0.18)';
        if (data.category === 'Underweight') { color = '#38bdf8'; bg = 'rgba(56, 189, 248, 0.18)'; }
        else if (data.category === 'Overweight') { color = '#f59e0b'; bg = 'rgba(245, 158, 11, 0.18)'; }
        else if (data.category === 'Obese') { color = '#ef4444'; bg = 'rgba(239, 68, 68, 0.18)'; }

        score.style.color = color;
        pill.style.color = color;
        pill.style.background = bg;

        const groupNote = age < 18
          ? `Age ${age} (Youth/Teen percentile context)`
          : `Age ${age} (Adult WHO standard classification)`;
        document.getElementById('metaInfo').textContent = `${groupNote} • ${weight} kg / ${heightCm} cm`;

        resultBox.style.display = 'block';
      } catch (err) {
        errorBox.textContent = 'Unable to reach backend API.';
        errorBox.style.display = 'block';
      }
    });
  </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_UI)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route("/bmi", methods=["GET"])
def calculate_bmi():
    try:
        weight = float(request.args.get("weight", 0))
        height = float(request.args.get("height", 0))
    except ValueError:
        return jsonify({"error": "Weight and height must be valid numbers"}), 400

    if weight <= 0 or height <= 0:
        return jsonify({"error": "Weight and height must be positive values"}), 400

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

if __name__ == "__main__":
    port = int(os.environ.get("APP_PORT", 5000))
    app.run(host="0.0.0.0", port=port)
