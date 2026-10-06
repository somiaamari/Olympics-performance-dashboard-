from pathlib import Path

import pandas as pd
import streamlit as st

DATA_DIRECTORY = Path(__file__).resolve().parent.parent / "data"


@st.cache_data
def load_required_csv(filename: str) -> pd.DataFrame:
    """Load a required project CSV or stop with a user-visible error."""
    file_path = DATA_DIRECTORY / filename
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        st.error(f"Could not load {filename}: {e}")
        st.stop()
