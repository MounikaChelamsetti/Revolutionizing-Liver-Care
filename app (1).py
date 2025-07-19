
from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)

# Load model components
def load_model_components():
    try:
        with open('model_info.pkl', 'rb') as f:
            model_info = pickle.load(f)

        with open(model_info['model_filename'], 'rb') as f:
            model = pickle.load(f)

        with open(model_info['scaler_filename'], 'rb') as f:
            scaler = pickle.load(f)

        with open(model_info['encoder_filename'], 'rb') as f:
            label_encoder = pickle.load(f)

        return model, scaler, label_encoder, model_info
    except Exception as e:
        print(f"Error loading model: {e}")
        return None, None, None, None

# Load components at startup
model, scaler, label_encoder, model_info = load_model_components()

@app.route('/')
def home():
    return render_template('index.html', 
                         model_name=model_info['model_name'] if model_info else 'N/A',
                         accuracy=f"{model_info['accuracy']*100:.2f}" if model_info else 'N/A')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form data
        features = []
        feature_names = ['Age', 'Gender', 'Total_Bilirubin', 'Direct_Bilirubin', 
                        'Alkphos', 'Sgpt', 'Sgot', 'Total_Protiens', 'Albumin', 'A_G_Ratio']

        # Parse input values
        age = float(request.form['age'])
        gender = request.form['gender']
        total_bilirubin = float(request.form['total_bilirubin'])
        direct_bilirubin = float(request.form['direct_bilirubin'])
        alkphos = float(request.form['alkphos'])
        sgpt = float(request.form['sgpt'])
        sgot = float(request.form['sgot'])
        total_proteins = float(request.form['total_proteins'])
        albumin = float(request.form['albumin'])
        ag_ratio = float(request.form['ag_ratio'])

        # Encode gender
        gender_encoded = label_encoder.transform([gender])[0]

        # Create feature array
        features = np.array([[age, gender_encoded, total_bilirubin, direct_bilirubin,
                            alkphos, sgpt, sgot, total_proteins, albumin, ag_ratio]])

        # Make prediction
        if model_info['uses_scaling']:
            features_scaled = scaler.transform(features)
            prediction = model.predict(features_scaled)[0]
            probability = model.predict_proba(features_scaled)[0]
        else:
            prediction = model.predict(features)[0]
            probability = model.predict_proba(features)[0]

        # Interpret results
        if prediction == 1:
            result = "High Risk of Liver Disease"
            risk_level = "High"
            confidence = probability[1] * 100
            color_class = "danger"
        else:
            result = "Low Risk of Liver Disease"
            risk_level = "Low"
            confidence = probability[0] * 100
            color_class = "success"

        # Generate recommendations
        recommendations = generate_recommendations(prediction, {
            'age': age, 'total_bilirubin': total_bilirubin, 'direct_bilirubin': direct_bilirubin,
            'alkphos': alkphos, 'sgpt': sgpt, 'sgot': sgot, 'total_proteins': total_proteins,
            'albumin': albumin, 'ag_ratio': ag_ratio
        })

        return render_template('result.html',
                             result=result,
                             risk_level=risk_level,
                             confidence=f"{confidence:.1f}",
                             color_class=color_class,
                             recommendations=recommendations,
                             input_data={
                                 'Age': age, 'Gender': gender, 'Total Bilirubin': total_bilirubin,
                                 'Direct Bilirubin': direct_bilirubin, 'Alkaline Phosphatase': alkphos,
                                 'SGPT': sgpt, 'SGOT': sgot, 'Total Proteins': total_proteins,
                                 'Albumin': albumin, 'A/G Ratio': ag_ratio
                             })

    except Exception as e:
        return render_template('error.html', error=str(e))

def generate_recommendations(prediction, values):
    recommendations = []

    if prediction == 1:  # High risk
        recommendations.append("⚠️ Consult a healthcare professional immediately for proper evaluation")
        recommendations.append("🩺 Schedule comprehensive liver function tests")
        recommendations.append("🚫 Avoid alcohol consumption completely")
        recommendations.append("🍃 Follow a liver-friendly diet (low fat, high fiber)")

        # Specific recommendations based on values
        if values['total_bilirubin'] > 2.0:
            recommendations.append("⚡ Elevated bilirubin levels detected - may indicate liver dysfunction")
        if values['sgpt'] > 80 or values['sgot'] > 80:
            recommendations.append("📈 Elevated liver enzymes - avoid medications that can damage the liver")
        if values['alkphos'] > 300:
            recommendations.append("🔬 High alkaline phosphatase - may indicate bile duct problems")
    else:  # Low risk
        recommendations.append("✅ Results suggest low liver disease risk")
        recommendations.append("🎉 Continue maintaining a healthy lifestyle")
        recommendations.append("🥗 Maintain a balanced diet with plenty of fruits and vegetables")
        recommendations.append("💧 Stay well hydrated (8+ glasses of water daily)")
        recommendations.append("🏃‍♀️ Regular exercise helps maintain liver health")
        recommendations.append("📅 Regular health checkups are still recommended")

    return recommendations

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint for programmatic access"""
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['age', 'gender', 'total_bilirubin', 'direct_bilirubin', 
                          'alkphos', 'sgpt', 'sgot', 'total_proteins', 'albumin', 'ag_ratio']

        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Create feature array
        gender_encoded = label_encoder.transform([data['gender']])[0]
        features = np.array([[
            data['age'], gender_encoded, data['total_bilirubin'], data['direct_bilirubin'],
            data['alkphos'], data['sgpt'], data['sgot'], data['total_proteins'], 
            data['albumin'], data['ag_ratio']
        ]])

        # Make prediction
        if model_info['uses_scaling']:
            features_scaled = scaler.transform(features)
            prediction = model.predict(features_scaled)[0]
            probability = model.predict_proba(features_scaled)[0]
        else:
            prediction = model.predict(features)[0]
            probability = model.predict_proba(features)[0]

        return jsonify({
            'prediction': int(prediction),
            'risk_level': 'High' if prediction == 1 else 'Low',
            'confidence': float(probability[prediction]) * 100,
            'probabilities': {
                'no_disease': float(probability[0]) * 100,
                'liver_disease': float(probability[1]) * 100
            }
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
