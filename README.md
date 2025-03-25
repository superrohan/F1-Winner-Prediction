# F1-Winner-Prediction
Machine Learning model to predict the winner race lap times for the 2025 Formuala-1 Grand Prix

It utilizes FastF1 to fetch race data, Pandas for data processing, and Gradient Boosting Regression from Scikit-Learn to train a model. The model predicts lap times based on qualifying results, tire choices, and track conditions.

Features

Data Extraction: Fetches F1 race data from FastF1's API.

Preprocessing: Cleans and encodes lap times, tire life, compound type, and track conditions.

Machine Learning Model: Uses Gradient Boosting Regressor with hyperparameter tuning via GridSearchCV.

Predictions: Estimates lap times for 2025 Australian GP based on qualifying results.

Model Evaluation: Calculates mean absolute error (MAE) and visualizes prediction performance.

Installation

Ensure you have the required dependencies installed:

pip install fastf1 pandas numpy scikit-learn matplotlib seaborn

If FastF1 is missing in some environments, it will be installed automatically using micropip.

Usage

Run the script using Python:

python f1_prediction.py

The output will display the predicted winner and a ranking of drivers based on estimated race times.

Expected Output

Predicted winner of the 2025 Australian GP.

Ranked list of predicted race times.

Model performance (Mean Absolute Error).

A scatter plot showing actual vs predicted lap times.

Notes

Ensure FastF1 API access is available when running the script.

Data quality may impact prediction accuracy; missing values are handled but could affect results.

Additional feature engineering (e.g., weather conditions) can further improve predictions.

License

This project is open-source and available under the MIT License.
