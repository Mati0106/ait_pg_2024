# Rugby Match Prediction Project

## Overview
This project involves predicting the victory margins in rugby matches using historical data. The project employs various machine learning models, including an optimized XGBoost model.

## Requirements
To run this project, ensure the following packages are installed:
- pandas
- matplotlib
- optuna
- scikit-learn
- shap
- xgboost
- ydata-profiling
- kagglehub

Use the following command to install the dependencies or use 'requirements.txt':
```bash
pip install pandas matplotlib optuna scikit-learn shap xgboost ydata-profiling kagglehub
```

## Data
The dataset used in this project is sourced from Kaggle and contains historical rugby match results. It can be downloaded using the `kagglehub` package.
A report with basic data statistics is generated and saved to an HTML file.

## Data Processing
- **Feature Engineering**: Additional features such as team ranking and form were added.
- **Data Encoding**: Categorical variables like team names are encoded into numeric values.
- **Scaling**: Features are scaled to improve model performance.

## Models
Three models are compared in this project:
1. Linear Regression
2. Random Forest Regressor
3. Support Vector Regressor (SVR)

The main model, XGBoost, is optimized using Optuna for better performance.

## Evaluation
- **Final MSE**: The final model achieves a Mean Squared Error (MSE) of 111.48.
- **R-squared (R2)**: The model explains 61% of the variance in the data.
- **Accuracy**: The model correctly predicts the winning team 83.7% of the time.

## Visualization
SHAP is used to explain feature importance and impact on predictions, providing insights into model behavior.

## Conclusion
This project demonstrates an effective method of predicting rugby match victory margins using machine learning. While the model performs reasonably well, there's potential for improvement through further experimentation with feature engineering and model tuning.

## Authors
Mateusz Paprocki
