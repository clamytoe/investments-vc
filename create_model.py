#!/usr/bin/env python
# coding: utf-8
# CareerERA Invenstment VC Capstone Project
# Create model script

import pickle
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.utils import resample

warnings.filterwarnings("ignore")

DATASET = Path("data", "cleaned_data.csv")
MODEL = Path("rf-up-86.pkl")


def create_and_fit_model(X_train, y_train):
    print("Creating model...")
    model = RandomForestClassifier(
        max_depth=None, min_samples_leaf=1, min_samples_split=2, n_estimators=100
    )
    print("Fitting the model...")
    model.fit(X_train, y_train)

    return model


def ds_splits(df, categorical, numeric):
    print("Splitting the data into train, validation, and test sets...")

    df_train_full, df_test = train_test_split(df, test_size=0.2, random_state=42)
    df_train, df_val = train_test_split(df_train_full, test_size=0.25, random_state=42)

    df_train = df_train.reset_index(drop=True)  # type: ignore
    df_val = df_val.reset_index(drop=True)  # type: ignore
    df_test = df_test.reset_index(drop=True)  # type: ignore

    y_train = df_train.status.values
    y_val = df_val.status.values
    y_test = df_test.status.values

    del df_train["status"]
    del df_val["status"]
    del df_test["status"]

    print("Scaling numeric features...")
    scaler = StandardScaler()

    X_train_num = df_train[numeric].values
    X_train_num = scaler.fit_transform(X_train_num)

    X_val_num = df_val[numeric].values
    X_val_num = scaler.transform(X_val_num)

    X_test_num = df_test[numeric].values
    X_test_num = scaler.transform(X_test_num)

    print("One Hot Encoding categorical features...")
    ohe = OneHotEncoder(sparse=False, handle_unknown="ignore")  # type: ignore

    X_train_cat = ohe.fit_transform(df_train[categorical].values)
    X_train = np.column_stack([X_train_num, X_train_cat])

    X_val_cat = ohe.transform(df_val[categorical].values)
    X_val = np.column_stack([X_val_num, X_val_cat])  # type: ignore

    X_test_cat = ohe.transform(df_test[categorical].values)
    X_test = np.column_stack([X_test_num, X_test_cat])  # type: ignore

    return X_train, X_val, X_test, y_train, y_val, y_test


def main():
    print(f"Importing dataset: {DATASET}")
    df = pd.read_csv(DATASET)

    print("Processing data...")
    df = df.drop(["homepage_url", "state_code"], axis=1)
    numeric = [feature for feature in df.columns if df[feature].dtype == "float"]
    categorical = [feature for feature in df.columns if df[feature].dtype != "float"]

    # Turn multi-class dataset into a binary one
    status_values = {
        "acquired": 1,
        "operating": 0,
        "pending": 0,
        "closed": 0,
    }
    df["status"] = df.status.map(status_values)

    # Remove features that we don't need
    remove_cat = [
        "permalink",
        "status",
        "founded_at",
        "first_funding_at",
        "last_funding_at",
    ]
    for feature in remove_cat:
        categorical.remove(feature)

    # Resample dataset
    ud_df = resample_df(df)

    # Train, val, test split
    X_train_u, _, X_test_u, y_train_u, _, y_test_u = ds_splits(
        ud_df, categorical, numeric
    )

    # Create model
    rfu_model = create_and_fit_model(X_train_u, y_train_u)
    test_model(rfu_model, X_test_u, y_test_u)
    save_model(rfu_model)


def resample_df(df: pd.DataFrame) -> pd.DataFrame:
    print("Resampling imbalanced classes...")

    # Upsampled aquired
    a_up = df[df.status == 1]
    na_up = df[df.status == 0]
    a_upsampled = resample(
        a_up,
        replace=True,
        n_samples=5_000,
        random_state=42,
    )
    up_df = pd.concat([na_up, a_upsampled])  # type: ignore
    up_df.status.value_counts()

    # Downsample not aquired
    na_ud = up_df[up_df.status == 0]
    a_ud = up_df[up_df.status == 1]
    na_downsampled = resample(
        na_ud,
        replace=True,
        n_samples=5_000,
        random_state=42,
    )
    ud_df = pd.concat([a_ud, na_downsampled])  # type: ignore
    ud_df.status.value_counts()

    return ud_df


def test_model(model, X_test, y_test):
    print("Testing the model...")
    test_probs = model.predict_proba(X_test)[:, 1]  # type: ignore
    y_pred_class = np.where(test_probs > 0.5, 1, 0)

    print("\nClassification Report")
    print(classification_report(y_test, y_pred_class))

    print("\nConfusion Matrix")
    print(confusion_matrix(y_test, y_pred_class))
    print()


def save_model(model):
    print("Saving the model...")
    with MODEL.open("wb") as f:
        pickle.dump(model, f)

    if MODEL.exists():
        print(f"[DONE] Model saved to {MODEL}")


if __name__ == "__main__":
    main()
