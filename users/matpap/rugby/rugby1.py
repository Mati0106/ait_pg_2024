import os

import kagglehub
import matplotlib.pyplot as plt
import optuna
import pandas as pd
import shap
import xgboost as xgb
from optuna.visualization import plot_optimization_history
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from ydata_profiling import ProfileReport

import users.matpap.rugby.utils.form as form
import users.matpap.rugby.utils.ranking as rank

### Data pre-processing ###
# Download and read the latest version of dataset
df = pd.read_csv(kagglehub.dataset_download("lylebegbie/international-rugby-union-results-from-18712022") + '/results.csv')

# Display the shape and first few rows of the dataset
print(df.shape)
print(df.head())

# Create report to view basic data statistics and save to html
report = ProfileReport(df, title='Rugby')
report.to_file(os.getcwd() + "\\users\\matpap\\rugby\\Rugby.html")

# Add a column representing the margin in favour of the 'home' team
df['margin'] = df['home_score'] - df['away_score']

# Add team ranking based on Rugby World Union schema
rank.add_team_rankings(df)
print(df)

# Add team form for n number of games back
form.add_teams_form(df, 5)
print(df)

# Init LabelEncoder
label_encoder = LabelEncoder()

# Encode teams as unique numbers
df['team1_encoded'] = label_encoder.fit_transform(df['home_team'])
df['team2_encoded'] = label_encoder.transform(df['away_team'])
print(df)
print(label_encoder.classes_)

# Encode the neutral and world cup columns as binary indicator variables
df['neutral'] = df['neutral'].astype(int)
df['world_cup'] = df['world_cup'].astype(int)

# Encode date as number
df['date_numeric'] = pd.to_datetime(df['date']).map(lambda x: x.toordinal())
df = df.drop("date", axis=1)


# Split the dataset into features and target variable
X = df.drop(["margin", "home_team", "away_team", "competition", "stadium", "city", "country", "home_score", "away_score"], axis=1)
y = df["margin"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=None, random_state=2024)

# Initialize the StandardScaler
scaler = StandardScaler()

# Fit the scaler on the training data and transform both training and test data
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(X_train.head())


### Models training ###
# Test models for comparison
models = {
    'Linear Regression': LinearRegression(),
    'Random Forest Regressor': RandomForestRegressor(),
    'Support Vector Regressor': SVR()
}

for model_name, t_model in models.items():
    # Fit the model to the training data
    t_model.fit(X_train_scaled, y_train)

    # Predict on the test data
    y_pr = t_model.predict(X_test_scaled)

    # Calculate mean squared error (MSE) and R-squared (R2) for evaluation
    mse = mean_squared_error(y_test, y_pr)
    r2 = r2_score(y_test, y_pr)

    # Print results
    print(f"Model: {model_name}")
    print(f"Mean Squared Error (MSE): {mse:.2f}")
    print(f"R-squared (R2): {r2:.2f}")
    print("=" * 50)


# Main model -> xgboost optimised
def objective(trial):
    # Init hyperparams
    param = {
        'objective': 'reg:squarederror',
        'n_estimators': trial.suggest_int('n_estimators', 50, 300),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
        'max_depth': trial.suggest_int('max_depth', 2, 10),
        'min_child_weight': trial.suggest_int('min_child_weight', 1, 10),
        'subsample': trial.suggest_float('subsample', 0.5, 1.0),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.5, 1.0),
        'gamma': trial.suggest_float('gamma', 0, 5),
        'lambda': trial.suggest_float('lambda', 0.1, 10.0),
        'alpha': trial.suggest_float('alpha', 0.1, 10.0)
    }

    # Fit the model to the training data
    model = xgb.XGBRegressor(**param, random_state=42)
    model.fit(X_train, y_train)

    # Predict on the test data
    y_pred = model.predict(X_test)

    # Minimse MSE
    f_mse = mean_squared_error(y_test, y_pred)
    return f_mse


# Optimise
study = optuna.create_study(direction='minimize')
study.optimize(objective, n_trials=150)

# Visualise study (not working in my PyCharm)
# plt.rcParams['backend'] = "Qt5Agg"
# print(plt.get_backend())
# plt.interactive(False)

fig = plot_optimization_history(study)
# fig.show(block=True)
fig.write_image(os.getcwd() + "\\users\\matpap\\rugby\\optimization_history.png")

# Best hyperparams
best_params = study.best_params
print("Best hyperparams:", best_params)

# Fit the model with best params
final_model = xgb.XGBRegressor(**best_params, random_state=42)
final_model.fit(X_train, y_train)

### Evaluation ###
# Evaluate and print results
y_pr = final_model.predict(X_test)
final_mse = mean_squared_error(y_test, y_pr)
r2 = r2_score(y_test, y_pr)
print(f"Final Mean Squared Error (MSE): {final_mse:.2f}")
print(f"R-squared (R2): {r2:.2f}")
print("=" * 50)

# Show results plot
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pr, color='blue', alpha=0.5, label='Predicted vs Actual')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color='red', linestyle='--', label='Ideal Fit')
plt.title('Comparison of Actual and Predicted Margins')
plt.xlabel('Actual Margins')
plt.ylabel('Predicted Margins')
plt.legend()
plt.grid(True)
plt.savefig(os.getcwd() + "\\users\\matpap\\rugby\\predicted_vs_actual.png")

# Function to check accuracy
def sign(num: float,) -> int:
    if num > 0:
        return 1
    elif num < 0:
        return -1
    else:
        return 0


# Counting the number of sign differences
false_count = sum(sign(y_t) != sign(y_p) for y_t, y_p in zip(y_test, y_pr))

# Calculating the percentage of cases with different signs
total_count = len(y_test)
percent_false = (false_count / total_count) * 100
percent_correct = 100 - percent_false

# Displaying the count of discrepancies and the percentage
print(f"Number of cases where signs differ: {false_count}")
print(f"Accuracy: {percent_correct:.2f}%")

# Explain the model's predictions using SHAP
feature_names = X_test.columns
explainer = shap.Explainer(final_model, X_train)
shap_values = explainer(X_test)

# SHAP Summary Plot (global feature importance)
plt.figure()  # Create a new figure
shap.summary_plot(shap_values, X_test, feature_names=feature_names)
plt.savefig(os.getcwd() + "\\users\\matpap\\rugby\\shap_summary.png")

# SHAP Dependence Plot (feature vs. SHAP value)
shap.dependence_plot('away_form', shap_values.values, X_test, feature_names=feature_names)
plt.savefig(os.getcwd() + "\\users\\matpap\\rugby\\away_form.png")

# SHAP Waterfall Plot (breakdown of individual prediction)
plt.figure()  # Create a new figure
shap.plots.waterfall(shap_values[0])
plt.savefig(os.getcwd() + "\\users\\matpap\\rugby\\shap_water.png")





