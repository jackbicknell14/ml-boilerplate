"""Docstring."""
import random

import numpy as np
# from sklearn.linear_model import LinearRegression
from transformers import ColumnSelector, TypeSelector
from scipy.stats import uniform
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest
from sklearn.impute import SimpleImputer

from sklearn.model_selection import (RandomizedSearchCV, cross_val_predict, train_test_split)
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from xgboost import XGBRegressor


class XGBLinearReg:
    """
    A short description.

    A bit longer description.

    Args:
        variable (type): description

    Returns:
        type: description

    Raises:
        Exception: description

    """

    def __init__(self, X, y, x_cols, binary_cols, text_cols, category_cols, numerical_cols):
        """docstring."""
        self.X, self.y, self.x_cols = X, y, x_cols
        self.binary_cols = binary_cols
        self.text_cols = text_cols
        self.category_cols = category_cols
        self.numerical_cols = numerical_cols

        if binary_cols:
            boolean = True
        else:
            boolean = False

        if text_cols:
            text = True
        else:
            text = False

        if category_cols:
            category = True
        else:
            category = False

        if numerical_cols:
            number = True
        else:
            number = False

        self.pipeline = Pipeline([
            ('preprocess_pipeline', self.get_preprocess_pipeline(self.x_cols,
                                                                 numeric=number,
                                                                 text=text,
                                                                 categorical=category,
                                                                 boolean=boolean)),
            ('classifier', XGBRegressor(max_delta_step=1,
                                        objective='reg:squarederror',
                                        booster='gbtree',
                                        njobs=1))
        ])

        self.linreg_param_grid = {
            "classifier__max_depth": [i for i in range(1, 15)],
            "classifier__gamma": [0.1 * x for x in range(1, 6)],
            "classifier__min_child_weight": [i for i in range(0, 5)],
            "classifier__subsample": [i/10.0 for i in range(6, 11)],
            "classifier__colsample_bytree": uniform(),
            "preprocess_pipeline__features_union__categorical_features__select_features__k":
                [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 'all'],
            }

    def get_preprocess_pipeline(self, x_cols, numeric=True, text=True, categorical=True, boolean=True):
        """Docstring."""
        transformer_list = []

        if numeric:
            numeric_features = ("numeric_features", Pipeline([
                ('selector', TypeSelector(np.number)),
                ('imputer', SimpleImputer(strategy="median")),
                ('scaler', StandardScaler())]))
            transformer_list.append(numeric_features)

        if text:
            text_features = ("text_features", Pipeline([
                ('selector', ColumnSelector(columns=self.text_cols)),
                ('vectoriser', TfidfVectorizer(stop_words='english')),
                ('select_features', SelectKBest())]))
            transformer_list.append(text_features)

        if categorical:
            categorical_features = ("categorical_features", Pipeline([
                ('selector', TypeSelector("category")),
                ('one_hot', OneHotEncoder(categories="auto", handle_unknown='ignore')),
                ('imputer', SimpleImputer(strategy="most_frequent")),
                ('select_features', SelectKBest())]))
            transformer_list.append(categorical_features)

        if boolean:
            boolean_features = ("boolean_features", Pipeline([
                ('selector', TypeSelector("bool"))]))
            transformer_list.append(boolean_features)

        return Pipeline([
            ('select_columns', ColumnSelector(columns=x_cols)),
            ('features_union', FeatureUnion(transformer_list=transformer_list))])

    def train_model(self):
        """Docstring summary."""
        # Partition data set into training/test split (2 to 1 ratio)
        X_train, X_test, y_train, y_test = train_test_split(
            self.X, self.y, test_size=1 / 3, random_state=42)
        clf = RandomizedSearchCV(
            self.pipeline, self.linreg_param_grid, cv=5)
        clf.fit(X_train, y_train)
        params = clf.best_params_
        y_pred = cross_val_predict(self.pipeline.set_params(**params).fit(X_train, y_train),
                                   X_test, y_test, cv=5)
        self.get_results(y_test, y_pred)

    def get_results(self, y_test, y_pred):
        """Docstring summary."""
        from sklearn import metrics
        print('MAE:', metrics.mean_absolute_error(y_test, y_pred))
        print('MSE:', metrics.mean_squared_error(y_test, y_pred))
        print('RMSE:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))


def set_x_random_missing_vals(X):
    """Docstring summary."""
    # Randomly set 500 items as missing values
    random.seed(42)
    num_missing = 500
    indices = [(row, col) for row in range(X.shape[0])
               for col in range(X.shape[1])]
    for row, col in random.sample(indices, num_missing):
        X.iat[row, col] = np.nan
    return X


def get_X_and_y(df, target_column, cols_to_drop, binary_cols,
                categorical_cols, text_cols, numeric_cols):
    """Remove the target column and the phone number."""
    cols_to_drop.append(target_column)
    x_cols = [c for c in df if c not in cols_to_drop]

    X = df[x_cols]

    X[binary_cols] = X[binary_cols].astype("bool")
    X[categorical_cols] = X[categorical_cols].astype("category")
    X[text_cols] = X[text_cols].astype("object")
    X[numeric_cols] = X[numeric_cols].astype("float64")

    y = df[target_column]
    return X, y, x_cols
