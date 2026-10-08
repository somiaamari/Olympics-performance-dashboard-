# Paris 2024 Glory Path Dashboard

An interactive Streamlit dashboard for exploring Paris 2024 athlete profiles, medal outcomes, event schedules, and a measured podium-classification model.

[Live demo](https://kcgvxepsappgquxa77memd.streamlit.app/)



## Features

- **Overview:** medal distribution, country standings, KPIs, and shared country/sport/continent filters.
- **Athlete Performance:** athlete search and profiles, demographic analysis, medalist rankings, and data export.
- **Global Analysis:** medal map, continent/country/sport hierarchy, and regional medal comparisons.
- **Sports & Events:** daily medal standings, event schedule, venue map, and sport-level medal views.
- **Podium Predictor:** interactive profile scoring with a stratified holdout evaluation and visible model limitations.

## Podium Predictor

The model labels an athlete as a medalist when their `athletes.csv` identifier (`code`) appears in `medallists.csv` (`code_athlete`). Features are gender, National Olympic Committee, primary discipline, age on the Paris 2024 opening date, height, and weight. Missing numeric values are imputed; categorical features are one-hot encoded. A class-weighted logistic regression is evaluated with a stratified 80/20 train/test split and `random_state=42`. The final interactive model is then fit on all available athlete records and cached with Streamlit's `st.cache_resource`.

Held-out results (2,223 athletes; 411 recorded medalists):

| Metric | Score |
| --- | ---: |
| ROC-AUC | 0.764 |
| Accuracy | 0.690 |
| Balanced accuracy | 0.704 |
| F1 | 0.464 |
| Precision | 0.341 |
| Recall | 0.727 |

The F1 and precision show modest positive-class performance despite reasonable ranking and recall. This is a retrospective Paris 2024 association model, not an LA28 forecast. Roster and medal records may be incomplete, NOC and discipline are strong contextual predictors, and the displayed model score is not calibrated as a probability.





## Project Structure

```text
.
|-- Overview.py
|-- pages/
|-- utils/
|-- data/
|-- assets/
|-- tests/
|-- requirements.txt
|-- requirements-dev.txt
`-- .github/workflows/ci.yml
```

## Run Locally

Clone the repository:

```bash
git clone https://github.com/somiaamari/Olympics-performance-dashboard-.git
cd Olympics-performance-dashboard-
```

Windows PowerShell:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt -r requirements-dev.txt
streamlit run Overview.py
```

macOS/Linux:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt -r requirements-dev.txt
streamlit run Overview.py
```





