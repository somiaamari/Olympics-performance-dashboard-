"""Model training and holdout evaluation for the Paris 2024 Glory Path Dashboard."""

import re

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from utils.data import load_required_csv

CATEGORICAL_FEATURES = ["gender", "country_code", "discipline"]
NUMERIC_FEATURES = ["age", "height", "weight"]
FEATURE_COLUMNS = CATEGORICAL_FEATURES + NUMERIC_FEATURES


def _prepare_training_data() -> tuple[pd.DataFrame, pd.Series]:
    athletes = load_required_csv("athletes.csv")
    medallists = load_required_csv("medallists.csv")

    athletes["age"] = (
        (pd.Timestamp("2024-07-26") - pd.to_datetime(athletes["birth_date"], errors="coerce"))
        .dt.days
        / 365.25
    )
    athletes["discipline"] = (
        athletes["disciplines"]
        .fillna("")
        .astype(str)
        .str.extract(r"^\s*\[\s*['\"]?([^,'\"]+)", expand=False)
        .fillna("Unknown")
        .str.strip()
    )
    for column in ("height", "weight"):
        athletes[column] = pd.to_numeric(athletes[column], errors="coerce").replace(0, np.nan)

    medalist_ids = pd.to_numeric(medallists["code_athlete"], errors="coerce").dropna().astype("int64")
    target = athletes["code"].isin(set(medalist_ids)).astype("int8")
    return athletes[FEATURE_COLUMNS], target


def _make_model():
    preprocessing = ColumnTransformer(
        [
            (
                "categorical",
                make_pipeline(
                    SimpleImputer(strategy="most_frequent"),
                    OneHotEncoder(handle_unknown="ignore"),
                ),
                CATEGORICAL_FEATURES,
            ),
            (
                "numeric",
                make_pipeline(SimpleImputer(strategy="median"), StandardScaler()),
                NUMERIC_FEATURES,
            ),
        ]
    )
    return make_pipeline(
        preprocessing,
        LogisticRegression(class_weight="balanced", max_iter=1000, random_state=42),
    )


@st.cache_resource
def load_podium_model() -> tuple[object, dict[str, float | int]]:
    """Evaluate once on a stratified holdout and return a final fitted model."""
    features, target = _prepare_training_data()
    train_indices, test_indices = train_test_split(
        np.arange(len(target)),
        test_size=0.2,
        random_state=42,
        stratify=target,
    )

    evaluation_model = _make_model()
    evaluation_model.fit(features.iloc[train_indices], target.iloc[train_indices])
    predictions = evaluation_model.predict(features.iloc[test_indices])
    probabilities = evaluation_model.predict_proba(features.iloc[test_indices])[:, 1]
    test_target = target.iloc[test_indices]

    metrics = {
        "accuracy": float(accuracy_score(test_target, predictions)),
        "balanced_accuracy": float(balanced_accuracy_score(test_target, predictions)),
        "precision": float(precision_score(test_target, predictions, zero_division=0)),
        "recall": float(recall_score(test_target, predictions, zero_division=0)),
        "f1": float(f1_score(test_target, predictions, zero_division=0)),
        "roc_auc": float(roc_auc_score(test_target, probabilities)),
        "train_rows": int(len(train_indices)),
        "test_rows": int(len(test_indices)),
        "test_medalists": int(test_target.sum()),
        "total_rows": int(len(target)),
        "total_medalists": int(target.sum()),
    }

    final_model = _make_model()
    final_model.fit(features, target)
    return final_model, metrics


def first_disciplines(values: pd.Series) -> list[str]:
    """Return displayable primary-discipline options from source list strings."""
    return sorted(
        {
            re.split(r"[,\]]", str(value).strip(" []'\""))[0].strip()
            for value in values.dropna()
            if str(value).strip(" []'\"")
        }
    )