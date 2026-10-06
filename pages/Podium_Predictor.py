"""Paris 2024 Glory Path Dashboard podium predictor and model evaluation."""

import pandas as pd
import streamlit as st

from utils.data import load_required_csv
from utils.podium_model import FEATURE_COLUMNS, first_disciplines, load_podium_model
from utils.style import apply_custom_style

st.set_page_config(
    page_title="Paris 2024 Glory Path Dashboard",
    page_icon="🏅",
    layout="wide",
)
apply_custom_style()

st.title("Paris 2024 Glory Path Dashboard")
st.subheader("Podium Predictor")
st.markdown("Explore how athlete profile characteristics relate to recorded Paris 2024 medal outcomes.")

athletes = load_required_csv("athletes.csv")
model, metrics = load_podium_model()
countries = sorted(athletes["country_code"].dropna().unique().tolist())
disciplines = first_disciplines(athletes["disciplines"])

with st.sidebar:
    st.title("Paris 2024 Glory Path Dashboard")
    st.caption("Built for the LA28 Volunteer Selection Challenge")

with st.form("podium_profile"):
    col1, col2, col3 = st.columns(3)
    gender = col1.selectbox("Gender", ["Female", "Male"])
    country = col2.selectbox("National Olympic Committee", countries)
    discipline = col3.selectbox("Primary discipline", disciplines)

    col4, col5, col6 = st.columns(3)
    age = col4.slider("Age at Paris 2024", 14, 60, 25)
    height = col5.slider("Height (cm)", 120, 220, 170)
    weight = col6.slider("Weight (kg)", 35, 180, 70)
    submitted = st.form_submit_button("Estimate medal outcome")

if submitted:
    profile = pd.DataFrame(
        [{
            "gender": gender,
            "country_code": country,
            "discipline": discipline,
            "age": age,
            "height": height,
            "weight": weight,
        }],
        columns=FEATURE_COLUMNS,
    )
    medal_score = float(model.predict_proba(profile)[0, 1])
    classification = "Medalist" if medal_score >= 0.5 else "No medal"
    st.metric("Model classification at 0.50 threshold", classification)
    st.progress(medal_score, text=f"Uncalibrated medal-likelihood score: {medal_score:.1%}")

st.divider()
st.subheader("Held-out evaluation")
st.caption(
    f"Stratified 80/20 split (random_state=42); {metrics['test_rows']:,} test athletes, "
    f"including {metrics['test_medalists']:,} recorded medalists. "
    f"Training used {metrics['train_rows']:,} athletes."
)

metric_columns = st.columns(5)
metric_columns[0].metric("ROC-AUC", f"{metrics['roc_auc']:.3f}")
metric_columns[1].metric("Balanced accuracy", f"{metrics['balanced_accuracy']:.3f}")
metric_columns[2].metric("F1", f"{metrics['f1']:.3f}")
metric_columns[3].metric("Precision", f"{metrics['precision']:.3f}")
metric_columns[4].metric("Recall", f"{metrics['recall']:.3f}")

st.info(
    "Limitations: this is a retrospective Paris 2024 association model, not a forecast for LA28. "
    "The athlete roster and medal records may be incomplete, and NOC and discipline are strong "
    "contextual predictors. The class-weighted model score is not calibrated as a probability."
)