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

## Data

All 13 CSVs are tracked in Git and are under 100 MB each. Source information is not consistently recorded in the repository; TODO entries require source verification and attribution before publication.

| CSV | Size | Used by app | Source |
| --- | ---: | --- | --- |
| `athletes.csv` | 7,234,642 B | Yes | TODO: verify dataset source and license |
| `coaches.csv` | 94,447 B | Yes | TODO: verify dataset source and license |
| `events.csv` | 31,953 B | Yes | Olympics.com Paris 2024 sport URLs are embedded; TODO: confirm full dataset provenance |
| `medallists.csv` | 554,831 B | Yes | TODO: verify dataset source and license |
| `medals.csv` | 184,913 B | Yes | TODO: verify dataset source and license |
| `medals_total.csv` | 3,067 B | Yes | TODO: verify dataset source and license |
| `nocs.csv` | 8,421 B | Yes | TODO: verify dataset source and license |
| `schedules.csv` | 965,594 B | Yes | TODO: verify dataset source and license |
| `schedules_preliminary.csv` | 381,129 B | No | TODO: verify dataset source and license |
| `teams.csv` | 451,048 B | Yes | TODO: verify dataset source and license |
| `technical_officials.csv` | 94,923 B | No | TODO: verify dataset source and license |
| `torch_route.csv` | 12,689 B | No | TODO: verify dataset source and license |
| `venues.csv` | 6,017 B | Yes | TODO: verify dataset source and license |

## Tech Stack

Python 3.11, Streamlit, pandas, Plotly, NumPy, and scikit-learn.

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


## Tests

Install development dependencies and run the Streamlit `AppTest` smoke suite:

```bash
python -m pip install -r requirements.txt -r requirements-dev.txt
pytest
```


