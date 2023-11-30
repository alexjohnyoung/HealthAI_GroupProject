from MLAnalyser import MLAnalyser
from LLM import GPT
from app import create_app


def main():

    # Create our Singleton MLAnalyser Object
    analyser = MLAnalyser().get_instance()

    #analyser.train_logistic_regression("breast.csv", "diagnosis")
    # Create our Singleton LLM Object
    gpt = GPT.get_instance(analyser)

    # Start our Flask application, passing in our Singleton objects
    app = create_app(analyser, gpt)
    app.run(debug=False)


if __name__ == "__main__":
    main()
