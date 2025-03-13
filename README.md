# HealthAI Project

## Overview
HealthAI is a comprehensive healthcare solution that combines mobile technology, web applications, machine learning, and large language models to provide risk assessment for various medical conditions. The system includes multiple components working together to serve both patients and healthcare professionals.

## Components

### HealthAI-App
An Android mobile application that enables patients and doctors to calculate the risk of illness based on lifestyle and prior medical history. Developed with Android Studio (Java).

### HealthAI-Web
A portal website designed specifically for medical professionals to access patient data, risk assessments, and other clinical information. Built with HTML, JavaScript, and CSS.

### HealthAI-Predict
Backend machine learning models developed using internationally available medical datasets to predict various health conditions including:
- Heart Disease
- Lung Cancer 
- Breast Cancer

### HealthAI-LLM
A chatbot integration using OpenAI's Large Language Model technology to help users identify potential health conditions based on reported symptoms.

## Technologies Used
- **Android Studio (Java)** - Mobile application development
- **HTML, JavaScript, CSS** - Web development and frontend services
- **Python** - Backend services, ML model development, and API endpoints
  - **scikit-learn/numpy/tensorflow/pandas** - Data processing and machine learning models
  - **Flask** - API endpoints
- **Firebase** - Authentication and database
- **Visual Paradigm** - Modeling and design
- **Trello** - Project management
- **GitHub** - Version control and collaboration
- **OpenAI API** - LLM integration for chatbot functionality

## Team Members and Responsibilities

- **Luke Kenny (Group Leader)**
  - Project management and sprint backlog maintenance
  - Design documentation
  - Feature development process planning

- **Alex Young**
  - HealthAI-Predict development and machine learning models
  - LLM chatbot implementation using OpenAI
  - Flask API endpoints
  - ML model documentation and analysis

- **Pierce Purcell**
  - HealthAI-Web development
  - Firebase setup and integration

- **Brian Sheridan**
  - HealthAI-App development
  - Firebase setup and integration

## Project Goals and Achievements

### Goals
- Develop highly accurate predictive machine learning models
- Create a responsive, feature-complete website with Firebase integration
- Build a modern mobile application with all required features
- Integrate an LLM-powered chatbot for medical condition prediction
- Maintain strong team communication through weekly meetings
- Document the project development process
- Complete the backlog in a timely manner

### Achievements
- Successfully developed machine learning models for Heart Disease, Lung Cancer, and Breast Cancer prediction with high accuracy
- Implemented OpenAI's LLM for symptom-based chatbot interactions
- Added secure user authentication via Firebase
- Developed feature-complete web and mobile applications
- Created comprehensive design documentation
- Completed all backlog items through effective collaboration
- Demonstrated clear understanding of project goals and requirements

## Challenges Overcome
- Finding suitable datasets (substituted Breast Cancer for initially planned Colon Cancer)
- Training and optimizing machine learning models for satisfactory results
- API integration between HealthAI-App, HealthAI-Web, and HealthAI-Predict
- Firebase setup and integration as a new technology
- Adapting to Agile methodology and Sprint timelines

## Installation and Setup

### HealthAI-App
1. Clone the repository
2. Open the project in Android Studio
3. Configure Firebase credentials
4. Build and run the application

### HealthAI-Web
1. Navigate to the web directory
2. Configure Firebase settings
3. Run index.html as desired 

### HealthAI-Predict
1. Navigate to the ML directory
2. Install Python dependencies: `pip install -r requirements.txt`
3. Run the Flask server: `python app.py`

## API Documentation
The system includes API endpoints for integration between components:

- `/predict/heart` - Heart disease risk prediction
- `/predict/lung` - Lung cancer risk prediction
- `/predict/breast` - Breast cancer risk prediction
- `/chat` - LLM chatbot interaction

## Possible Future Improvements
- Expand the range of predictable medical conditions
- Enhance chatbot capabilities with more specialized medical knowledge
- Improve model accuracy through additional training data
- Develop iOS version of the mobile application
- Add more advanced visualization of prediction results
