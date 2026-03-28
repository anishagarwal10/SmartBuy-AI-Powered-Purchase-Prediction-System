from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

# 🔥 Load trained pipeline (VERY IMPORTANT)
model = pickle.load(open("model.pkl", "rb"))

# 🏠 Home Route
@app.route('/')
def home():
    return render_template('index.html')


# 🎯 Prediction Route (Form Submit)
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.form

        # 🔥 Create DataFrame (same columns as training)
        new_data = pd.DataFrame([{
            "Administrative": int(data['Administrative']),
            "Administrative_Duration": float(data['Administrative_Duration']),
            "Informational": 0,
            "Informational_Duration": 0.0,
            "ProductRelated": int(data['ProductRelated']),
            "ProductRelated_Duration": float(data['ProductRelated_Duration']),
            "BounceRates": float(data['BounceRates']),
            "ExitRates": float(data['ExitRates']),
            "PageValues": 0.0,
            "SpecialDay": 0.0,
            "Month": data['Month'],
            "OperatingSystems": 2,
            "Browser": 2,
            "Region": 1,
            "TrafficType": 2,
            "VisitorType": data['VisitorType'],
            "Weekend": True if data['Weekend'] == "True" else False
        }])

        # 🔥 Prediction
        prediction = model.predict(new_data)[0]

        # 🎯 Result
        result = "🛒 Customer WILL Purchase" if prediction == 1 else "❌ Customer WILL NOT Purchase"

        return render_template('index.html', prediction_text=result)

    except Exception as e:
        return render_template('index.html', prediction_text=f"Error: {str(e)}")


# 🚀 API Route (Optional - Future use)
@app.route('/api/predict', methods=['POST'])
def api_predict():
    data = request.get_json()

    new_data = pd.DataFrame([data])
    prediction = model.predict(new_data)[0]

    return jsonify({
        "prediction": int(prediction)
    })


# ▶️ Run App
if __name__ == "__main__":
    app.run(debug=True)