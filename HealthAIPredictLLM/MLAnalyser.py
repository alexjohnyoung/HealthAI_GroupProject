import numpy as np
import pandas as pd
import tensorflow as tf
from joblib import dump, load
from os.path import isfile

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler


class MLAnalyser:
    _instance = None

    def _init(self):

        # Load our saved training models
        self.heart_model = None
        self.lung_model = None
        self.breast_model = None
        self.breast_scaler = None

        if isfile("heart_model.pkl"):
            self.heart_model = load("heart_model.pkl")
        else:
            print("[MLAnalyser]: No heart model dataset loaded; model not present")

        if isfile("lung_model.pkl"):
            self.lung_model = load("lung_model.pkl")
        else:
            print("[MLAnalyser]: No lung model dataset loaded; model not present")

        if isfile("breast_model.pkl"):
            self.breast_model = load("breast_model.pkl")
        else:
            print("[MLAnalyser]: No breast model dataset loaded; model not present")

        if isfile("breast_scaler.pkl"):
            self.breast_scaler = load("breast_scaler.pkl")

        print(f"Created MLAnalyser Object")

    @staticmethod
    def custom_one_hot_encoder(data, columns_to_encode):
        # Perform one-hot encoding
        data_encoded = pd.get_dummies(data, columns=columns_to_encode, drop_first=False)

        # Expected columns after one-hot encoding based on the original training data
        expected_columns = [
            "age", "sex", "trestbps", "chol", "fbs", "restecg", "thalach",
            "exang", "oldpeak", "thal", "cp_0", "cp_1", "cp_2", "cp_3",
            "slope_0", "slope_1", "slope_2", "ca_0", "ca_1", "ca_2", "ca_3", "ca_4"
        ]

        # Add missing columns with value 0
        for column in expected_columns:
            if column not in data_encoded.columns:
                data_encoded[column] = 0

        # Reorder columns to the expected order
        data_encoded = data_encoded[expected_columns]

        return data_encoded

    def perform_analysis(self, type_analysis, feature_list):

        prediction = []
        threshold = 0.4
        y_prob = None

        if type_analysis == "heart":

            # age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal,target

            data = pd.DataFrame([feature_list], columns=["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg",
                                                         "thalach", "exang", "oldpeak", "slope", "ca", "thal"])

            encoded_data = self.custom_one_hot_encoder(data, ["cp", "slope", "ca"])

            y_prob = self.heart_model.predict_proba(encoded_data)[:, 1]
            prediction = (y_prob > threshold).astype(int)

        elif type_analysis == "lung":
            data = pd.DataFrame([feature_list],
                                columns=["GENDER", "AGE", "SMOKING", "CHRONIC_DISEASE", "FATIGUE",
                                         "ALLERGY", "WHEEZING", "ALCOHOL CONSUMING", "COUGHING", "SHORTNESS OF BREATH",
                                         "SWALLOWING DIFFICULTY", "CHEST PAIN"])

            print(feature_list)

            y_prob = self.lung_model.predict_proba(data)[:, 1]
            prediction = (y_prob > threshold).astype(int)

        elif type_analysis == "breast":
            data = pd.DataFrame([feature_list], columns=["mean_radius", "mean_texture", "mean_perimeter", "mean_area", 'mean_smoothness'])
            data = self.breast_scaler.transform(data)

            y_prob = self.breast_model.predict_proba(data)[:, 1]
            prediction = (y_prob > threshold).astype(int)

        if prediction[0] == 1:
            result = "Positive for disease"
        else:
            result = "Negative for disease"

        prob_score = int(y_prob[0] * 100)
        prob_score = f"{str(prob_score)}% probability"

        return result, prob_score

    @staticmethod
    def train_logistic_regression(filename, target):
        data = pd.read_csv(filename)

        # Remove duplicates
        data = data.drop_duplicates()

        if "heart" in filename:
            # Perform One-hot encoding
            # This encoding is used to transform categorical data into a format that can be provided to
            # machine learning algorithms to do a better job with prediction.
            # Without one-hot encoding or some other form of representation,
            # machine learning algorithms may think categorical data as having an ordinal relationship

            # Let's say there are four types represented as 0, 1, 2, and 3. If you treat these as
            # continuous numerical values, the algorithm might understand it as type 3 being "three times" the type 1
            # which doesn't make sense
            data = pd.get_dummies(data, columns=['cp', 'slope', 'ca'], drop_first=False)

        # Logistic Regression
        x = data.drop(target, axis=1)
        y = data[target]

        scaler = StandardScaler()

        # Split our data into two sets: training and testing set
        # We will use 20% of the data for testing, and 80% of the data for training
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

        if "breast" in filename:
            # Perform Standardization Feature Scaling
            # This ensures that all features have a similar scale,
            # meaning they all fall within a similar range of values.
            # This is important for many machine learning algorithms (such as our Logistic Regression)
            # that are sensitive to the scales of their input features.
            fields_to_standardize = ['mean_radius', 'mean_texture', 'mean_perimeter', 'mean_area', 'mean_smoothness']
            x_train[fields_to_standardize] = scaler.fit_transform(x_train[fields_to_standardize])
            x_test[fields_to_standardize] = scaler.transform(x_test[fields_to_standardize])

        elif "lung" in filename:
            # Standardizing Lung Cancer fields yielded the same results
            pass

        # Standardizing was performed on the Heart Disease features too, but yields same result

        # We are using the LogisticRegression machine learning model for our classification issue
        model = LogisticRegression(max_iter=2000)

        # Fit the model with our training data
        model.fit(x_train, y_train)

        # We lower the threshold so that we can accept lower values as positive cases (it is usually 0.5)
        # In a healthcare setting it is better to accept more false positives rather than risk mistaking a prediction
        threshold = 0.4

        # Get the predicted probabilities for the positive class
        y_prob = model.predict_proba(x_test)[:, 1]

        # Apply the threshold and convert to binary prediction
        y_pred = (y_prob > threshold).astype(int)

        # Obtain the accuracy score from our test
        accuracy = accuracy_score(y_test, y_pred)

        # Save our trained models
        if "heart" in filename:
            dump(model, "heart_model.pkl")
        elif "lung" in filename:
            dump(model, "lung_model.pkl")
        elif "breast" in filename:
            dump(model, "breast_model.pkl")
            dump(scaler, "breast_scaler.pkl")

        # Get our Logistic Regression analysis for chosen file
        print(f"Logistic Regression Analysis for {filename}")
        print(f"Accuracy: {accuracy * 100:.2f}%")
        print(classification_report(y_test, y_pred))
        print()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._instance._init()
        return cls._instance


