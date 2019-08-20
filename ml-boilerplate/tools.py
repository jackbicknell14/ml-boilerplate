from scipy.stats import randint, uniform

from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline, FeatureUnion, Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics import confusion_matrix, roc_curve, roc_auc_score, accuracy_score, cohen_kappa_score, f1_score, log_loss, precision_score, recall_score
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV, cross_val_predict, cross_val_score, train_test_split
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression
from transformers import ColumnSelector, TypeSelector
from xgboost import XGBClassifier

import numpy as np
import pandas as pd
import pmlb
import random

import matplotlib.pyplot as plt
import seaborn as sns
import re


def set_x_random_missing_vals(X):
    # Randomly set 500 items as missing values
    random.seed(42)
    num_missing = 500
    indices = [(row, col) for row in range(X.shape[0]) for col in range(X.shape[1])]
    for row, col in random.sample(indices, num_missing):
        X.iat[row, col] = np.nan
    return X

def get_preprocess_pipeline(x_cols):
    return Pipeline([
        ('select_columns', ColumnSelector(columns=x_cols)),
        ('features_union', FeatureUnion(transformer_list=[
            ("numeric_features", Pipeline([
                ('selector', TypeSelector(np.number)),
                ('imputer', SimpleImputer(strategy="median")),
                ('scaler', StandardScaler()),
            ])),
            # If there are not text columns this should be hashed out
            #("text_features", Pipeline([
                #    ('selector', ColumnSelector(columns=text_columns)),
                #    ('vectoriser', TfidfVectorizer(stop_words='english')),
                #    ('select_features', SelectKBest()),
            #])),
            ("categorical_features", Pipeline([
                ('selector', TypeSelector("category")),
                ('one_hot', OneHotEncoder(categories="auto")),
                ('imputer', SimpleImputer(strategy="most_frequent")),
                ('select_features', SelectKBest()),
            ])),
            ("boolean_features", Pipeline([
                ('selector', TypeSelector("bool"))
            ]))
        ]))
    ])

def get_X_and_y(df, target_column, cols_to_drop, binary_features,
                categorical_features, text_features):
    # Remove the target column and the phone number
    cols_to_drop.append(target_column)
    x_cols = [c for c in df if c not in cols_to_drop]

    # Column types are defaulted to floats
    X = df.drop([target_column], axis=1).astype(float)

    X[binary_features] = X[binary_features].astype("bool")

    # Categorical features can't be set all at once
    for f in categorical_features:
        X[f] = X[f].astype("category")

    y = df[target_column]
    return X, y, x_cols

def get_results(y_test, y_pred):
    print(f'f1 score of {np.round(f1_score(y_test, y_pred),3)}')
    print(f'recall score of {np.round(recall_score(y_test, y_pred),3)}')
    print(f'kappa score of {np.round(cohen_kappa_score(y_test, y_pred),3)}')
    print(f'precision score of {np.round(precision_score(y_test, y_pred),3)}')
    print(f'accuracy score of {np.round(accuracy_score(y_test, y_pred),3)}')
    print(f'roc_auc score of {np.round(roc_auc_score(y_test, y_pred),3)}')
    print(f'logloss score of {np.round(log_loss(y_test, y_pred),3)}')
    confus_mat = confusion_matrix(y_test, y_pred)
    print(confus_mat)

###########################
# Dummy Run 
###########################

sns.set(rc={"figure.figsize": (12, 8)})
df = pmlb.fetch_data('churn', return_X_y=False)
binary_features = ["international plan", "voice mail plan"]
categorical_features = ["state", "area code"]
text_features = []
target_column = 'target'
cols_to_drop = ['phone_number']

# Partition data set into training/test split (2 to 1 ratio)
X, y, x_cols = get_X_and_y(df, target_column, cols_to_drop, binary_features, categorical_features, text_features)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1/3., random_state=42)

classifier_pipeline = Pipeline([
    ('preprocess_pipeline', get_preprocess_pipeline(x_cols)),
    ('classifier', XGBClassifier(max_delta_step=1,
                                objective='binary:logistic',
                                booster='gbtree',
                                njobs=1))
])

param_grid = {
    "classifier__gamma": [0.1 * x for x in range(1, 6)]
    }

param_grid = {
    "classifier__max_depth": [i for i in range(1, 15)],
    "classifier__gamma": [0.1 * x for x in range(1, 6)],
    "classifier__n_estimators": randint(1, 1000),
    "classifier__learning_rate": uniform(),
    "classifier__subsample": uniform(),
    "classifier__colsample_bytree": uniform(),
    "preprocess_pipeline__features_union__categorical_features__select_features__k":
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 25, 50, 'all'],
    }


classifier_model = RandomizedSearchCV(classifier_pipeline, param_grid, cv=5)
classifier_model.fit(X_train, y_train)

params = classifier_model.best_params_

y_pred = cross_val_predict(classifier_pipeline.set_params(**params).fit(X_train, y_train),
                            X_test, y_test, cv=5)

get_results(y_test, y_pred)
scores = cross_val_score(classifier_pipeline.set_params(**params), X_test, y_test, cv=3, scoring='f1')
print(scores)
print(scores.mean())