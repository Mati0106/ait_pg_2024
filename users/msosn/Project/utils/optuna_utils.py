import pandas as pd
from sklearn.metrics import accuracy_score
from typing import Callable

from xgboost import XGBClassifier

def get_objective(X_train: pd.DataFrame, X_test: pd.DataFrame, y_train: pd.Series, y_test:pd.Series) -> Callable:
    """
    Create optuna bjective function with get data from given DataFrames
    :param X_train: train DataFrame
    :param X_test: test DataFrame
    :param y_train: target train Series
    :param y_test: target test Series
    :return:
    """
    return lambda trial : objective(trial, X_train, X_test, y_train, y_test)

def objective(trial, X_train: pd.DataFrame, X_test: pd.DataFrame, y_train: pd.Series, y_test: pd.Series) -> float:
    """
    Optuna objective function implementation
    :param trial:
    :param X_train:
    :param X_test:
    :param y_train:
    :param y_test:
    :return:
    """
    params = {
        "objective": 'binary:logistic',
        "n_estimators": trial.suggest_int("n_estimators", 100, 1000),
        "verbosity": 0,
        "learning_rate": trial.suggest_float("learning_rate", 1e-3, 0.1, log=True),
        "max_depth": trial.suggest_int("max_depth", 1, 10),
        "subsample": trial.suggest_float("subsample", 0.05, 1.0),
        "colsample_bytree": trial.suggest_float("colsample_bytree", 0.05, 1.0),
        "min_child_weight": trial.suggest_int("min_child_weight", 1, 20),
    }


    model = XGBClassifier(**params)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    accuracy = accuracy_score(y_test, preds)
    return accuracy