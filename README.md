# Liver Disease Prediction System

## 🩺 Overview

An advanced machine learning web application for liver disease risk assessment built with Flask and scikit-learn. The system uses clinical laboratory parameters to predict the likelihood of liver disease using a Random Forest classifier.

## ✨ Features

- **Machine Learning Prediction**: Random Forest model with 91.45% accuracy
- **Web Interface**: Responsive Bootstrap-based UI
- **Real-time Analysis**: Instant risk assessment
- **Detailed Reporting**: Comprehensive results with recommendations
- **API Support**: RESTful API for programmatic access
- **Secure Processing**: No data storage, real-time analysis only

## 🏥 Clinical Parameters

The system analyzes 10 key clinical markers:

1. **Age** - Patient age in years
2. **Gender** - Male/Female
3. **Total Bilirubin** - Total bilirubin levels (mg/dL)
4. **Direct Bilirubin** - Direct bilirubin levels (mg/dL)
5. **Alkaline Phosphatase** - Enzyme levels (U/L)
6. **SGPT/ALT** - Alanine aminotransferase (U/L)
7. **SGOT/AST** - Aspartate aminotransferase (U/L)
8. **Total Proteins** - Total protein levels (g/dL)
9. **Albumin** - Albumin levels (g/dL)
10. **A/G Ratio** - Albumin to Globulin ratio

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone/Download the project**
   ```bash
   # Extract the project files to a directory
   cd liver_disease_project
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   python app.py
   ```

4. **Access the Application**
   - Open your web browser
   - Navigate to: `http://localhost:5000`

## 🖥️ Usage

### Web Interface

1. **Home Page**: Enter clinical parameters in the prediction form
2. **Results Page**: View risk assessment and recommendations
3. **About Page**: Learn about the system and clinical parameters

### API Usage

The system provides a REST API endpoint for programmatic access:

```bash
POST /api/predict
Content-Type: application/json

{
    "age": 45,
    "gender": "Male",
    "total_bilirubin": 1.2,
    "direct_bilirubin": 0.4,
    "alkphos": 250,
    "sgpt": 45,
    "sgot": 40,
    "total_proteins": 7.0,
    "albumin": 3.8,
    "ag_ratio": 1.2
}
```

Response:
```json
{
    "prediction": 0,
    "risk_level": "Low",
    "confidence": 89.5,
    "probabilities": {
        "no_disease": 89.5,
        "liver_disease": 10.5
    }
}
```

## 📊 Model Performance

- **Algorithm**: Random Forest Classifier
- **Accuracy**: 91.45%
- **Precision**: 93%
- **Recall**: 90%
- **F1-Score**: 92%

## 📁 Project Structure

```
liver_disease_project/
├── app.py                          # Flask application
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
├── best_model_random_forest.pkl    # Trained ML model
├── scaler.pkl                      # Feature scaler
├── label_encoder.pkl               # Gender encoder
├── model_info.pkl                  # Model metadata
├── liver_disease_dataset.csv       # Training dataset
├── templates/                      # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── result.html
│   ├── about.html
│   └── error.html
└── static/
    └── css/
        └── style.css               # Custom styling
```

## 🔒 Security & Privacy

- **No Data Storage**: Patient data is not stored or logged
- **Real-time Processing**: All analysis happens in memory
- **Secure Transmission**: HTTPS recommended for production
- **Input Validation**: Comprehensive input sanitization

## ⚠️ Medical Disclaimer

**IMPORTANT**: This system is designed for educational and research purposes only.

- This tool is **NOT** a substitute for professional medical advice
- Results should **NOT** be used for clinical diagnosis
- Always consult qualified healthcare professionals
- Individual results may vary based on factors not captured in this model
- The system is intended for screening purposes only

## 🛠️ Technical Details

### Dependencies
- **Flask**: Web framework
- **scikit-learn**: Machine learning algorithms
- **pandas**: Data manipulation
- **numpy**: Numerical computations
- **pickle**: Model serialization

### Model Training
The model was trained using:
- Cross-validation with stratified sampling
- Feature scaling using StandardScaler
- Random Forest with 100 estimators
- Train/test split: 80/20

## 📈 Performance Metrics

| Metric | Score |
|--------|-------|
| Accuracy | 91.45% |
| Precision (No Disease) | 89% |
| Precision (Liver Disease) | 93% |
| Recall (No Disease) | 93% |
| Recall (Liver Disease) | 90% |
| F1-Score | 92% |

## 🤝 Contributing

This is an educational project. For improvements or bug fixes:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📜 License

This project is created for educational purposes. Please ensure compliance with relevant healthcare regulations if used in any medical context.

## 📞 Support

For questions or issues:
- Review the About page in the application
- Check the medical disclaimer
- Ensure all dependencies are properly installed

---

**Remember**: This is a demonstration project for educational purposes. Always consult healthcare professionals for medical advice.
