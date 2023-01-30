#!/usr/bin/env python
# coding: utf-8
# CareerERA Invenstment VC Capstone Project
# Data clean up script

import calendar
from pathlib import Path
from typing import Optional

import pandas as pd

DATA_DIR = Path("data")
INPUT_FILENAME = DATA_DIR / "investments_VC.csv"
OUTPUT_FILENAME = "cleaned_data.csv"
CLEANED_FILE = DATA_DIR / OUTPUT_FILENAME


def main():
    """Cleans up dataset

    It imports a dataset, processes it, and exports it to a
    new file.
    """
    # Import data file
    df = pd.read_csv(INPUT_FILENAME, engine="python", encoding="unicode_escape")

    # Data Cleanup
    df.drop_duplicates(inplace=True)
    df.dropna(axis=0, how="all", inplace=True)

    # Remove extra spaces around column names
    df.columns = [column.strip() for column in df.columns]  # type: ignore

    # Fill in missing name
    df["name"].fillna(
        df.iloc[28221].homepage_url.split(".")[0].replace("http://", "").title(),
        inplace=True,
    )
    df.dropna(subset=["permalink"], inplace=True)

    # Remove commas in funding_total_usd
    df["funding_total_usd"] = df["funding_total_usd"].apply(
        lambda x: x.strip().replace(",", "") if isinstance(x, str) else x
    )
    df["funding_total_usd"] = df["funding_total_usd"].apply(
        lambda x: 0.0 if x == "-" else float(x)
    )

    # Cleaned up date fields
    df["founded_month"] = pd.to_datetime(df.founded_month, format="%Y-%m").dt.to_period(
        "M"
    )
    df["founded_quarter"] = df.founded_quarter.apply(
        lambda x: str(x.split("-")[1]) if isinstance(x, str) else x
    )
    df["founded_at"] = pd.DatetimeIndex(df["founded_year"]).year
    df = df[df.founded_year.notna()]
    df["founded_year"] = df.founded_year.astype(int)

    # Feature Engineering

    # Turn category_list into features
    df["category_list"] = df.category_list.apply(
        lambda x: str(x).lstrip("|").rstrip("|").split("|")
    )
    df["category_list"] = df.category_list.apply(
        lambda x: [c.replace(" ", "_").lower() for c in x]
    )
    df["category_list"] = df.category_list.apply(lambda x: [c.strip() for c in x])

    cat_dummies = pd.get_dummies(df.category_list.apply(pd.Series).stack(),).sum(
        level=0  # type: ignore
    )
    df = pd.concat([df, cat_dummies], axis=1)
    df.drop(["category_list"], axis=1, inplace=True)

    # Add a feature to see how many days it took a company to get funding
    dt_objects = ["founded_at", "first_funding_at", "last_funding_at"]
    for d in dt_objects:
        df[d] = pd.to_datetime(df[d], errors="coerce")
    df["days_to_funding"] = (df.first_funding_at - df.founded_at).dt.days

    # Change `status` null values into pending
    df["status"].fillna("pending", inplace=True)

    # Turn categorical features into categories.
    categorical = [
        "market",
        "status",
        "country_code",
        "state_code",
        "founded_month",
        "founded_quarter",
        "founded_year",
    ]
    df[categorical] = df[categorical].astype("category")

    # Turn column values into features
    df["month_founded"] = df.founded_month.apply(lambda x: str(x).rsplit("-")[1])
    df["month_founded"].fillna(0, inplace=True)
    df["month_founded"] = df.month_founded.astype(int)
    df["month_founded"] = df.month_founded.apply(lambda x: calendar.month_abbr[x])
    df = df.drop(["founded_month"], axis=1)

    df = ohe(df, "month_founded", "month")
    df = ohe(df, "founded_quarter", "quarter", False)
    df = ohe(df, "state_code", "state", False)
    df = ohe(df, "founded_year", "year", False)

    # Add time between the first and last funding rounds
    df["funding_days"] = df.last_funding_at - df.first_funding_at
    df["funding_days"] = df.funding_days.apply(lambda x: x.days)

    # Get rid of null values
    nulls = [
        "market",
        "city",
        "days_to_funding",
        "funding_days",
    ]
    df.dropna(subset=nulls, inplace=True)

    # Cleanup market names
    df["market"] = df.market.apply(lambda x: x.strip().lower())

    # Save the processed data
    save_dataset(df)


def save_dataset(df: pd.DataFrame):
    """Save DataFrame to CSV

    Args:
        df (pd.DataFrame): The DataFrame to save to file.
    """
    df.to_csv(CLEANED_FILE, index=False)

    if CLEANED_FILE.exists():
        print(f"Created {CLEANED_FILE}")


def ohe(
    df: pd.DataFrame, feature: str, prefix: Optional[str] = None, drop: bool = True
) -> pd.DataFrame:
    """One Hot Encode features

    Args:
        df (DataFrame): DataFrame to modify
        feature (str): Column name to turn into a feature
        prefix (str, optional): Prefix to add to the front of the
            new feature name. Defaults to None.
        drop (bool, optional): Whether or not to drop the original
            feature. Defaults to True.

    Returns:
        DataFrame: The modified dataframe
    """
    if prefix is None:
        dummies = pd.get_dummies(df[feature], drop_first=True)
    else:
        dummies = pd.get_dummies(df[feature], drop_first=True, prefix=prefix)

    df = pd.concat([df, dummies], axis=1)

    if drop:
        df = df.drop([feature], axis=1)

    return df


if __name__ == "__main__":
    main()
