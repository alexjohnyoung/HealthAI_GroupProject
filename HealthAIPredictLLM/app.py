from flask import Flask, request, jsonify
from os import urandom


def create_app(analyser, gpt):
    app = Flask(__name__)
    app.secret_key = urandom(32)

    @app.route("/")
    def home():
        return "Hello World"

    @app.route("/chat", methods=["POST"])
    def chat():
        input = request.json.get("input")

        return gpt.chat(input)

    @app.route("/analysis")
    def analysis():

        feature_list = []

        type_analysis = request.args.get("type", "invalid")

        if type_analysis == "lung":

            # The risk of getting cancer / disease increases with age
            age = int(request.args.get("AGE", "invalid"))

            # Some studies suggest slight variations in cancer and disease types and risks between genders,
            # potentially due to both biological and behavioral differences
            gender = int(request.args.get("GENDER", 1))

            # Smoking tobacco is the top risk factor for lung cancer and is responsible for the vast majority of lung cancer
            smoking = int(request.args.get("SMOKING", ""))

            chronic_disease = int(request.args.get("CHRONIC_DISEASE", 0))

            fatigue = int(request.args.get("FATIGUE", 0))

            allergy = int(request.args.get("ALLERGY", 0))

            wheezing = int(request.args.get("WHEEZING", 0))

            alcohol = int(request.args.get("ALCOHOL CONSUMING", 0))

            coughing = int(request.args.get("COUGHING", 0))

            shortness_of_breath = int(request.args.get("SHORTNESS OF BREATH", 0))

            swallowing_difficulty = int(request.args.get("SWALLOWING DIFFICULTY", 0))

            chest_pain = int(request.args.get("CHEST PAIN", 0))

            feature_list = [gender, age, smoking, chronic_disease, fatigue, allergy, wheezing,
                            alcohol, coughing, shortness_of_breath, swallowing_difficulty, chest_pain]

            print(feature_list)

        elif type_analysis == "heart":

            # The risk of getting cancer / disease increases with age
            age = int(request.args.get("age", "invalid"))

            # age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal,target

            # Some studies suggest slight variations in cancer and disease types and risks between genders,
            # potentially due to both biological and behavioral differences
            sex = int(request.args.get("sex", 1))

            # This field describes the type of chest pain the patient is experiencing.
            # 0: Typical angina (a type of chest pain related to the heart)
            # 1: Atypical angina
            # 2: Non-anginal pain
            # 3: Asymptomatic (no chest pain)
            cp = int(request.args.get("cp", 0))

            # This is the patient's resting blood pressure measured in millimeters of mercury (mm Hg).
            trestbps = int(request.args.get("trestbps", 0))

            # This represents the patient's serum cholesterol level in mg/dL (milligrams per deciliter).
            chol = int(request.args.get("chol", 0))

            # This field indicates whether the patient's fasting blood sugar level is higher than 120 mg/dL or not.
            # 0: Fasting blood sugar is not higher than 120 mg/dL
            # 1: Fasting blood sugar is higher than 120 mg/dL
            fbs = int(request.args.get("fbs", 0))

            # This field describes the results of the patient's resting electrocardiogram (ECG or EKG) test
            # 0: Normal
            # 1: Abnormality in the ST-T wave
            # 2: Showing probable or definite left ventricular hypertrophy by Estes' criteria
            restecg = int(request.args.get("restecg", 0))

            # This represents the patient's maximum heart rate achieved during exercise.
            thalach = int(request.args.get("thalach", 0))

            # It indicates whether the patient experiences exercise-induced angina (chest pain) during physical activity.
            exang = int(request.args.get("exang", 0))

            # This field quantifies the degree of ST segment depression induced by exercise relative to rest on the ECG.
            # Used as a measure of how much the heart's electrical activity changes during exercise.
            oldpeak = float(request.args.get("oldpeak", 0))

            # This field describes the slope of the peak exercise ST segment.
            # 0: Upsloping
            # 1: Flat
            # 2: Downsloping
            slope = int(request.args.get("slope", 0))

            # This represents amount of major blood vessels (coronary arteries) that are colored or stained by fluoroscopy.
            ca = int(request.args.get("ca", 0))

            # This field describes the results of a thallium stress test, which measures blood flow to the heart.
            # 0: Normal
            # 1: Fixed defect (indicative of a past heart attack)
            # 2: Reversible defect (may indicate a current blockage)
            thal = int(request.args.get("thal", 0))

            feature_list = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca,
                            thal]

        elif type_analysis == "breast":
            # mean_radius,mean_texture,mean_perimeter,mean_area,mean_smoothness,diagnosis

            # The average distance from the center of the nucleus to its boundary
            mean_radius = float(request.args.get("mean_radius", 0))

            # The standard deviation of grayscale values in the cell nuclei
            mean_texture = float(request.args.get("mean_texture", 0))

            # The average perimeter of the nucleus in the image
            mean_perimeter = float(request.args.get("mean_perimeter", 0))

            # The average area covered by the nucleus in the image
            mean_area = float(request.args.get("mean_area", 0))

            # Measures the local variation in the radius lengths
            # Measure of how smooth or irregular the edges of the cell nucleus appear
            mean_smoothness = float(request.args.get("mean_smoothness", 0))

            feature_list = [mean_radius, mean_texture, mean_perimeter, mean_area, mean_smoothness]

        # Check if feature list is empty
        if len(feature_list) == 0:
            return jsonify({"error": "Invalid analysis type or parameters."}), 400

        # Perform the analysis
        result = analyser.perform_analysis(type_analysis=type_analysis, feature_list=feature_list)

        return jsonify({"result": result})

    return app