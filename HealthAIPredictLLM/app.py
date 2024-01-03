from flask import Flask, request, jsonify
from flask_cors import CORS
from os import urandom


def create_app(analyser, gpt):
    app = Flask(__name__)
    CORS(app)  # Enable CORS
    app.secret_key = urandom(32)

    @app.route("/")
    def home():
        return "Hello World"

    @app.route("/chat", methods=["POST"])
    def chat():
        input = request.json.get("input")

        return gpt.chat(input)

    @app.route("/analysis", methods=["POST"])
    def analysis():

        if not request.is_json:
            return jsonify({"error": "Invalid request format. Please send JSON data."}), 400

        feature_dict = {}
        parameter_names = {}

        data = request.get_json()

        type_analysis = data.get("type", "invalid")

        if type_analysis == "lung":
            parameter_names = {
                "AGE": int,  # The risk of getting cancer/disease increases with age
                "GENDER": int,  # Potential variations in cancer types and risks between genders
                "SMOKING": int,  # Top risk factor for lung cancer
                "CHRONIC_DISEASE": int,  # Chronic diseases can influence lung cancer risk
                "FATIGUE": int,  # Symptom that can be associated with lung conditions
                "ALLERGY": int,  # Allergies can be a contributing factor or symptom
                "WHEEZING": int,  # Symptom of lung issues
                "ALCOHOL CONSUMING": int,  # Alcohol consumption habits
                "COUGHING": int,  # Common symptom in lung diseases
                "SHORTNESS OF BREATH": int,  # Indicates potential respiratory issues
                "SWALLOWING DIFFICULTY": int,  # Can be a symptom of certain lung diseases
                "CHEST PAIN": int  # Chest pain is a critical symptom to consider
            }

        elif type_analysis == "heart":
            parameter_names = {
                "Age": int,  # Age of the patient
                "Sex": str,  # Biological gender of the patient
                "RestingBP": int,  # Resting blood pressure
                "Cholesterol": int,  # Serum cholesterol in mg/dl
                "FastingBS": int,  # Fasting blood sugar > 120 mg/dl (1 = true, 0 = false)
                "MaxHR": int,  # Maximum heart rate achieved
                "ExerciseAngina": str,  # Exercise-induced angina (1 = yes, 0 = no)
                "Oldpeak": float,  # ST depression induced by exercise relative to rest
                "ChestPainType": str,  # Type of chest pain experienced
                # TA: Typical Angina, ATA: Atypical Angina
                # NAP: Non-Anginal Pain, ASY: Asymptomatic
                "RestingECG": str,  # Resting electrocardiographic results
                "ST_Slope": str  # The slope of the peak exercise ST segment
            }

        elif type_analysis == "breast":
            parameter_names = {
                "mean_radius": float,  # Average distance from the center to the boundary of the nucleus
                "mean_texture": float,  # Standard deviation of grayscale values in the cell nuclei
                "mean_perimeter": float,  # Average perimeter of the nucleus
                "mean_area": float,  # Average area covered by the nucleus
                "mean_smoothness": float  # Measures the variation in the radius lengths
            }

        # Read the parameters and cast them to the specified data types
        for param_name, param_type in parameter_names.items():
            if param_name in data:
                try:
                    feature_dict[param_name] = param_type(data[param_name])
                except ValueError:
                    return jsonify({"error": f"Invalid type for parameter {param_name}"}), 400
            else:
                return jsonify({"error": f"Missing parameter {param_name}"}), 400

        # Check if feature list is empty
        if len(feature_dict) == 0:
            return jsonify({"error": "Invalid analysis type or parameters."}), 400

        # Perform the analysis
        result = analyser.perform_analysis(type_analysis=type_analysis, feature_list=feature_dict)

        return jsonify({"result": result})

    return app