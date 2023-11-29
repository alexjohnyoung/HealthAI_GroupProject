from flask import request, jsonify, session
from re import sub
import openai

openai.api_key = "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"


class GPT:
    _instance = None

    def _init(self, analyser):
        self.analyser = analyser
        print("Created LLM Object")

    @staticmethod
    def get_feature_list(type_feature):
        features = []

        if type_feature == "heart":
            features = ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg",
                       "thalach", "exang", "oldpeak", "slope", "ca", "thal"]

        elif type_feature == "lung":
            features = ["GENDER", "AGE", "SMOKING", "CHRONIC_DISEASE", "FATIGUE",
                                         "ALLERGY", "WHEEZING", "ALCOHOL CONSUMING", "COUGHING", "SHORTNESS OF BREATH",
                                         "SWALLOWING DIFFICULTY", "CHEST PAIN"]
        elif type_feature == "breast":
            features = ["mean_radius", "mean_texture", "mean_perimeter", "mean_area", 'mean_smoothness']

        return features

    def has_all_features(self, type_feature, user_features):
        required_features = set(self.get_feature_list(type_feature))
        provided_features = []

        for feature in user_features:
            feature_name = feature[0]
            provided_features.append(feature_name)

        provided_features = set(provided_features)

        return required_features == provided_features

    @staticmethod
    def get_missing_features(feature_list, user_features):
        missing_features = []

        for feature in feature_list:
            if feature not in user_features:
                missing_features.append(feature)

        return missing_features

    @staticmethod
    def translate_feature_name(risk_type, given_feature):
        feature_translation = []

        if risk_type == "lung":
            feature_translation = [
                ["gender", "GENDER"],
                ["age", "AGE"],
                ["smoking", "SMOKING"],
                ["chronic", "CHRONIC_DISEASE"],
                ["fatigue", "FATIGUE"],
                ["allerg", "ALLERGY"],
                ["wheez", "WHEEZING"],
                ["alcohol", "ALCOHOL CONSUMING"],
                ["cough", "COUGHING"],
                ["shortness", "SHORTNESS OF BREATH"],
                ["swallow", "SWALLOWING DIFFICULTY"],
                ["chestpain", "CHEST PAIN"]
            ]

        elif risk_type == "heart":
            feature_translation = [
                ["age", "age"],
                ["sex", "sex"],
                ["chestpaintype", "cp"],
                ["restingblood", "trestbps"],
                ["cholesterol", "chol"],
                ["fastingblood", "fbs"],
                ["restingelectro", "restecg"],
                ["maximumheart", "thalach"],
                ["exerciseinduced", "exang"],
                ["stdepression", "oldpeak"],
                ["slopeof", "slope"],
                ["numberofmajor", "ca"],
                ["thalassemia", "thal"]

            ]

        for key, feature in enumerate(feature_translation):
            if given_feature.find(feature[0]) != -1:
                given_feature = feature[1]
                break

        return given_feature

    @staticmethod
    def translate_feature_value(feature):
        feature = feature.lower()
        feature = feature.replace("(yes/no)", "")
        feature = feature.replace("(male/female)", "")
        feature = feature.replace(",", "")
        feature = feature.replace("male", "1")
        feature = feature.replace("female", "0")
        feature = feature.replace("yes", "1")
        feature = feature.replace("none", "0")
        feature = feature.replace("no", "0")

        return feature

    @staticmethod
    def has_extra_colons(feature):
        num_colons = 0

        for i, char in enumerate(feature):
            if char == ":":
                num_colons += 1

        return num_colons > 1

    @staticmethod
    def remove_extra_colons(feature):
        colon = feature.rfind(":")

        if colon == -1:
            return False, "incorrect format for response!"

        new_feature = ""

        for i, char in enumerate(feature):
            if char != ":" or i == colon:
                new_feature += char

        feature = new_feature

        return feature, "success"

    def parse_feature_val(self, risk_type, feature):
        feat = feature[0].replace(" ", "")
        feat = feat.replace(".", "")
        feat = sub(r'[0-9]', '', feat)
        val = feature[1].replace(" ", "")

        if val == "":
            val = "0"
        else:
            if risk_type == "lung":
                val = "1"

        feat = self.translate_feature_name(risk_type, feat)

        return feat, val

    def chat(self, user_input):

        # Check that we got input
        if not user_input:
            return jsonify({"error": "No input "})

        # If we do not have a 'context' cookie in the session
        if "context" not in session:
            # Set up a new 'context' cookie in the session
            session["context"] = []

            print("[LLM]: Setting up a new context")

        # If we do not have a 'state' cookie in the session
        if "state" not in session:
            # Set up a new 'state' cookie in the session
            session["state"] = "gathering"
            print("[LLM]: Setting up a new state")

        # If we do not have a 'risk_type' cookie in the session
        if "risk_type" not in session:
            # Set up a new 'risk_type' cookie in the session
            session["risk_type"] = "heart"

        # The context session cookie created to keep track of the conversation
        context = session["context"]

        # The state of the current conversation
        # initial: asking questions, anything before risk assessment
        # gathering: gathering information for the risk assessment
        state = session["state"]

        # The current risk type, used when gathering information for the risk assessment
        risk_type = session["risk_type"]

        # If we are gathering information currently, just move into this statement instead of the main logic
        if session["state"] == "gathering":
            # Split the users input with newline (as this is how they are entering the risk information)
            user_input = user_input.split("\n")

            # Enumerate through the now list, filtered with newline
            for key, feature in enumerate(user_input):
                # Translate the value inputted by the user for the current feature into a more machine-readable format
                # This will perform some string replacements (i.e 'male' to 1, 'yes' to 1, 'no' to 0, etc)
                feature = self.translate_feature_value(feature)

                # Redefine the now changed feature in our user_input list
                user_input[key] = feature

            # Create a list to hold our edited feature & value
            parsed_features = []

            # Iterate through our features
            for feature in user_input:
                # Check if we have extra colons
                if self.has_extra_colons(feature):
                    # Remove any extra colons as it interferes with our split operation
                    feature, reason = self.remove_extra_colons(feature)

                    # If we got a negative response for any reason:
                    if not feature:
                        # Return this error to the user
                        return jsonify({"error": reason})

                # Split our feature as [feature, value] to make it into a more operational format
                feature = feature.split(":")

                # Call our parse_feature_val function, passing in our risk type and current feature
                # This will perform some string corrections (removing numbers, extra spaces, etc)
                feature, val = self.parse_feature_val(risk_type, feature)

                # Add our parsed feature into our parsed_features list as [feature, value]
                parsed_features.append([feature, val])

            # Check if we have all features provided for use with our machine learning prediction
            if not self.has_all_features(risk_type, parsed_features):
                # If not return an error to the user
                return jsonify({"error": "Please enter all fields!"})

            # We now need to make it a dictionary as that's what the MLAnalyser accepts
            feature_dict = {}

            # Iterate through our parsed_features
            for feature_list in parsed_features:
                # The feature name is our first index
                feature = feature_list[0]

                # The value is our second index
                val = feature_list[1]

                # Create the key with the feature name and assign it to the value from our second index in our dict
                feature_dict[feature] = val

            print(feature_dict)

            # And finally get our result and the probability
            result, probability = self.analyser.perform_analysis(risk_type, feature_dict)

            # Put both the result and the probability into one string
            result = result + " - " + probability

            # Return the result to the user
            return jsonify({"msg": result})

        # If we are here, it means that we are still in the 'initial' stage, where the user asks questions etc before
        # making a risk assessment
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are Doc-bot, a virtual assistant designed to help users understand their "
                               "risk factors for heart disease, lung cancer, and breast cancer based on their symptoms "
                               "and lifestyle factors. "
                               "You are not a substitute for professional medical advice, diagnosis, or treatment."
                },
                {
                    "role": "system",
                    "content": "For breast cancer risk assessment, discuss factors like mean radius, "
                               "mean texture, mean perimeter, mean area, and mean smoothness."
                },
                {
                    "role": "system",
                    "content": "For lung cancer risk assessment, factors would be gender, age, smoking history, "
                               "chronic diseases, fatigue, allergies, wheezing, alcohol consumption, coughing, "
                               "shortness of breath, difficulty swallowing, and chest pain."
                },
                {
                    "role": "system",
                    "content": "For heart disease risk assessment, consider the following parameters: "
                               "Age (age of the patient), Sex (biological gender of the patient), "
                               "RestingBP (resting blood pressure), Cholesterol (serum cholesterol in mg/dl), "
                               "FastingBS (fasting blood sugar > 120 mg/dl, 1 = true; 0 = false), "
                               "MaxHR (maximum heart rate achieved), "
                               "ExerciseAngina (exercise-induced angina, 1 = yes; 0 = no), "
                               "Oldpeak (ST depression induced by exercise relative to rest), "
                               "ChestPainType (type of chest pain experienced with categories TA: Typical Angina "
                               "ATA: Atypical Angina, NAP: Non-Anginal Pain, ASY: Asymptomatic)"
                               "RestingECG (resting electrocardiographic results with categories like Normal, LVH, ST),"
                               " and ST_Slope (the slope of the peak exercise ST segment with categories like Up, Flat, Down)."
                },
                {
                    "role": "system",
                    "content": "If the user wishes to enter details for a risk assessment, make sure to include in "
                               "your reply the text 'to assess your risk for [chosen risk assessment]' and put each "
                               "feature question in just one line so that the users entered details can be easily "
                               "split using a newline and do not order them alphabetically."
                },
               # *context,
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        )

        # Get the reply from the AI
        reply = response.choices[0].message.content

        print(reply)

        # Convert the reply into all lowercase and store in reply_lower
        reply_lower = reply.lower()

        # Filter if the user wishes to make a risk assessment
        if "to assess your risk for" or "help you assess" in reply_lower:
            # Enter into the 'gathering' state, as we now are inputting feature information
            session["state"] = "gathering"

            # If there was a mention of 'heart' in the reply
            if "heart" in reply_lower:
                # Set the risk type to 'heart'
                session["risk_type"] = "heart"

            # If there was a mention of 'lung' in the reply
            elif "lung" in reply_lower:
                # Set the risk type to 'lung'
                session["risk_type"] = "lung"

            # If there was a mention of 'breast' in the reply
            elif "breast" in reply_lower:
                # Set the risk type to 'breast'
                session["risk_type"] = "breast"

            # Redefine our risk_type variable to our now changed risk type
            risk_type = session["risk_type"]

            print(f"Now gathering risk details for {risk_type}!")

        # Append the new conversation to our context, in order to keep track
        context.append({"role": "user", "content": user_input})
        context.append({"role": "assistant", "content": reply})

        # Return the reply to the user
        return jsonify({"test": reply})

    @classmethod
    def get_instance(cls, analyser):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._instance._init(analyser)

        return cls._instance

