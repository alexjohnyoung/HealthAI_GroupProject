import numpy as np
import pandas as pd
import tensorflow as tf
from joblib import dump, load
from os.path import isfile

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

class MLAnalyser:
    _instance = None

    def _init(self):

        # Load our saved training models
        self.heart_model = None
        self.heart_scaler = None
        self.lung_model = None
        self.breast_model = None
        self.breast_scaler = None

        if isfile("heart_model.pkl"):
            self.heart_model = load("heart_model.pkl")
        else:
            print("[MLAnalyser]: No heart model dataset loaded; model not present")

        if isfile("heart_scaler.pkl"):
            self.heart_scaler = load("heart_scaler.pkl")
        else:
            print("[MLAnalyser]: No heart scaler loaded; scaler not present")

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
    def custom_one_hot_encoder(df):

        # Perform necessary transformations like mapping, one-hot encoding
        df['Sex'] = df['Sex'].map({'M': 1, 'F': 0})
        df["ExerciseAngina"] = df["ExerciseAngina"].map({"N": 0, "Y": 1})

        # One-hot encode categorical variables
        categorical_cols = ["ChestPainType", "RestingECG", "ST_Slope"]
        df = pd.get_dummies(df, columns=categorical_cols, drop_first=False)

        # Make sure we don't have any boolean values
        for column in df.columns:
            if df[column].dtype == "bool":
                df[column] = df[column].astype(int)

        # Original dataset: Age,Sex,ChestPainType,RestingBP,Cholesterol,FastingBS,RestingECG,MaxHR,
        # ExerciseAngina,Oldpeak,ST_Slope,HeartDisease

        model_columns = [
            "Age", "Sex", "RestingBP", "Cholesterol", "FastingBS", "MaxHR",
            "ExerciseAngina", "Oldpeak",
            "ChestPainType_ASY", "ChestPainType_ATA", "ChestPainType_NAP", "ChestPainType_TA",
            "RestingECG_LVH", "RestingECG_Normal", "RestingECG_ST",
            "ST_Slope_Down", "ST_Slope_Flat", "ST_Slope_Up"
        ]

        # Add missing columns for one-hot encoded features
        for col in model_columns:
            if col not in df.columns:
                df[col] = 0

        # Reorder columns to match the training data
        df = df[model_columns]

        return df

    def perform_analysis(self, type_analysis, feature_list):

        prediction = []
        threshold = 0.4
        y_prob = None

        if type_analysis == "heart":

            # age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal,target

            data = pd.DataFrame([feature_list], columns=["Age", "Sex", "ChestPainType", "RestingBP",
                                                         "Cholesterol", "FastingBS", "RestingECG",
                                                         "MaxHR", "ExerciseAngina", "Oldpeak", "ST_Slope"])

            # Transform to one-hot encoded format
            encoded_data = self.custom_one_hot_encoder(data)

            features_to_scale = ["Age", "RestingBP", "Cholesterol", "MaxHR", "Oldpeak"]
            scaled_features = self.heart_scaler.transform(encoded_data[features_to_scale])

            encoded_data[features_to_scale] = scaled_features

            y_prob = self.heart_model.predict_proba(encoded_data)[:, 1]
            prediction = (y_prob > threshold).astype(int)

        elif type_analysis == "lung":
            data = pd.DataFrame([feature_list],
                                columns=["GENDER", "AGE", "SMOKING", "CHRONIC_DISEASE", "FATIGUE",
                                         "ALLERGY", "WHEEZING", "ALCOHOL CONSUMING", "COUGHING", "SHORTNESS OF BREATH",
                                         "SWALLOWING DIFFICULTY", "CHEST PAIN"])

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
    def tune_svm(filename, target):
        data = pd.read_csv(filename)
        data = data.drop_duplicates()

        if "heart" in filename:
            data = pd.get_dummies(data, columns=['cp', 'slope', 'ca'], drop_first=False)

        # Split data into features and target
        x = data.drop(target, axis=1)
        y = data[target]

        # Splitting the data into training and testing sets
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

        scaler = StandardScaler()
        if "breast" in filename:
            # Standardize features for breast dataset
            fields_to_standardize = ['mean_radius', 'mean_texture', 'mean_perimeter', 'mean_area', 'mean_smoothness']
            x_train[fields_to_standardize] = scaler.fit_transform(x_train[fields_to_standardize])
            x_test[fields_to_standardize] = scaler.transform(x_test[fields_to_standardize])

        model = SVC()

        # Parameters for hyperparameter tuning
        param_grid = {
            'C': [0.1, 1, 10, 100],
            'gamma': [1, 0.1, 0.01, 0.001],
            'kernel': ['rbf', 'linear']
        }

        # Using GridSearchCV for hyperparameter tuning and cross-validation
        grid_search = GridSearchCV(model, param_grid, cv=5, scoring='accuracy')
        grid_search.fit(x_train, y_train)

        # Get the best parameters and best model
        best_params = grid_search.best_params_
        best_model = grid_search.best_estimator_

        print(f"After analysing {filename}: ")
        print(f"Best Parameters: {best_params}")

        y_pred = best_model.predict(x_test)
        accuracy = accuracy_score(y_test, y_pred)

        print(f"Test Accuracy: {accuracy}")
        print(classification_report(y_test, y_pred))

    @staticmethod
    def get_feature_importance(filename, target):
        data = pd.read_csv(filename)

        # Logistic Regression
        x = data.drop(target, axis=1)
        y = data[target]

        model = LogisticRegression()
        model.fit(x, y)

        feature_names = x.columns

        # Get the coefficients as log odds
        coefficients = model.coef_[0]

        # As these are in log odds, they are much harder to interpret than percentages
        # We can convert these into odds ratios
        # Odds Ratios:
        # Above 1: as the feature value increases, the odds of the outcome are multiplied by the odds ratio
        # Below 1: as the feature value increases, the odds of the outcome decrease and are multiplied by the odds ratio
        # Exactly 1: changes in the feature do not affect the odds of the outcome

        odds_ratios = np.exp(coefficients)

        print(f"Feature importance for {filename}")

        importance_str = ""
        for key, item in enumerate(feature_names):
            current_feature = feature_names[key]
            current_importance = odds_ratios[key]

            importance_str += f"Feature {current_feature} -> {current_importance:.2f}\n"

        print(importance_str)


    @staticmethod
    def train_logistic_regression(filename, target):
        data = pd.read_csv(filename)

        # Remove duplicates
        data = data.drop_duplicates()

        # Logistic Regression
        x = data.drop(target, axis=1)
        y = data[target]

        # Split our data into two sets: training and testing set
        # We will use 20% of the data for testing, and 80% of the data for training
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

        scaler = StandardScaler()

        if "breast" in filename:
            # Perform Standardization Feature Scaling
            # This ensures that all features have a similar scale,
            # meaning they all fall within a similar range of values.
            # This is important for many machine learning algorithms (such as our Logistic Regression)
            # that are sensitive to the scales of their input features.
            fields_to_standardize = ['mean_radius', 'mean_texture', 'mean_perimeter', 'mean_area', 'mean_smoothness']
            x_train[fields_to_standardize] = scaler.fit_transform(x_train[fields_to_standardize])
            x_test[fields_to_standardize] = scaler.transform(x_test[fields_to_standardize])

        elif "heart" in filename:
            fields_to_standardize = ["Age", "RestingBP", "Cholesterol", "MaxHR", "Oldpeak"]
            # Transform x_train and x_test using the same scaler
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
            dump(scaler, "heart_scaler.pkl")
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


