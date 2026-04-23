"""
LA28 Olympics Dashboard - Page 1: Overview (Command Center)

Provides high-level summary with KPIs and key visualizations.
Per official requirements:
- Title with description
- 5 KPI Metrics (Athletes, Countries, Sports, Medals, Events)
- Global Medal Distribution (Pie/Donut)
- Top 10 Medal Standings (Horizontal Bar)
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

from utils.shared_filters import render_global_filters, apply_filters, get_continent
from utils.style import apply_custom_style

st.set_page_config(
    layout="wide",
    page_title="LA28: The Golden State Scoreboard",
    page_icon="🏅",
    initial_sidebar_state="expanded",
)
apply_custom_style()

DATA_PATH = Path(__file__).parent / "data"


@st.cache_data
def load_athletes():
    """Load athletes data."""
    try:
        df = pd.read_csv(DATA_PATH / "athletes.csv")
        df = df.rename(columns={"country_code": "noc"})
        return df
    except:
        return pd.DataFrame()


@st.cache_data
def load_medals_total():
    """Load medal totals by country."""
    try:
        df = pd.read_csv(DATA_PATH / "medals_total.csv")
        df = df.rename(columns={"country_code": "noc"})
        return df
    except:
        return pd.DataFrame()


@st.cache_data
def load_medals():
    """Load individual medals."""
    try:
        df = pd.read_csv(DATA_PATH / "medals.csv")
        df = df.rename(columns={"country_code": "noc", "medal_type": "medal"})
        df["medal"] = df["medal"].str.replace(" Medal", "", regex=False)
        return df
    except:
        return pd.DataFrame()


@st.cache_data
def load_events():
    """Load events data."""
    try:
        return pd.read_csv(DATA_PATH / "events.csv")
    except:
        return pd.DataFrame()


@st.cache_data
def load_nocs():
    """Load NOCs data."""
    try:
        return pd.read_csv(DATA_PATH / "nocs.csv")
    except:
        return pd.DataFrame()


# Load all data
athletes_df = load_athletes()
medals_total_df = load_medals_total()
medals_df = load_medals()
events_df = load_events()
nocs_df = load_nocs()

# =============================================================================
# SIDEBAR - GLOBAL FILTERS
# =============================================================================
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/5/5c/Olympic_rings_without_rims.svg", width=150)
    st.title("🥇 Paris 2024 Glory Path Dashboard!")
    st.markdown(' Paris 2024 Dashboard — track performance, medals & athletes. Use sidebar filters to explore.')

    
    # Get filter options
    all_countries = sorted(medals_total_df["noc"].dropna().unique().tolist()) if not medals_total_df.empty else []
    all_sports = sorted(medals_df["discipline"].dropna().unique().tolist()) if not medals_df.empty else []
    
    # Render global filters
    filters = render_global_filters(
        countries=all_countries,
        sports=all_sports,
    )
    st.divider()
    st.caption("Built for LA28 Volunteer Selection Challenge")

# =============================================================================
# APPLY FILTERS
# =============================================================================
filtered_medals = apply_filters(medals_df, filters)
filtered_athletes = apply_filters(athletes_df, filters)

# Recalculate totals based on filtered medals

if not filtered_medals.empty:
    filtered_totals = filtered_medals.groupby("noc").agg(
        Gold=("medal", lambda x: (x == "Gold").sum()),
        Silver=("medal", lambda x: (x == "Silver").sum()),
        Bronze=("medal", lambda x: (x == "Bronze").sum()),
    ).reset_index()
    filtered_totals["Total"] = filtered_totals["Gold"] + filtered_totals["Silver"] + filtered_totals["Bronze"]
    
    # Add country names
    if not medals_total_df.empty:
        country_map = medals_total_df.set_index("noc")["country"].to_dict()
        filtered_totals["country"] = filtered_totals["noc"].map(country_map).fillna(filtered_totals["noc"])
    else:
        filtered_totals["country"] = filtered_totals["noc"]
    
    filtered_totals = filtered_totals.sort_values(["Gold", "Silver", "Bronze"], ascending=False)
else:
    filtered_totals = pd.DataFrame()

# Filter athletes by country/continent
filtered_athletes = athletes_df.copy()
if filters["countries"]:
    filtered_athletes = filtered_athletes[filtered_athletes["noc"].isin(filters["countries"])]
if filters["continents"]:
    filtered_athletes = filtered_athletes[filtered_athletes["noc"].apply(get_continent).isin(filters["continents"])]

# =============================================================================
# HEADER
# =============================================================================

# 
# =============================================================================
# PROFESSIONAL HEADER
# =============================================================================
st.markdown(
    """
    <div style='text-align: left; padding: 2rem 0; border-bottom: 3px solid #FFD700;'>
        <h1 style='
            font-size: 3.2rem; 
            font-weight: 700; 
            color: #0033A0; 
            margin: 0;
            display: inline;
        '>
            Paris 2024 
            <span style='color: #FFD700; font-weight: 800;'>Glory Path</span> Dashboard
        </h1>
    </div>
    """, 
    unsafe_allow_html=True
)

# Optional subtitle
st.markdown(
    """
    <p style='
        font-size: 1.2rem; 
        color: #444; 
        margin-top: 1.5rem; 
        line-height: 1.6;
        max-width: 900px;
    '>
        Track Olympic performance, medal counts, and athlete insights. 
        Powered by official Paris 2024 data for your analysis.
    </p>
    <br>
    """, 
    unsafe_allow_html=True
)


# Show active filters
active_filters = []
if filters["countries"]:
    active_filters.append(f"Countries: {len(filters['countries'])}")
if filters["sports"]:
    active_filters.append(f"Sports: {len(filters['sports'])}")
if filters["continents"]:
    active_filters.append(f"Continents: {', '.join(filters['continents'])}")
if len(filters["medal_types"]) < 3:
    active_filters.append(f"Medals: {', '.join(filters['medal_types'])}")

if active_filters:
    st.info(f"📌 Active filters: {' | '.join(active_filters)}")

st.divider()

# =============================================================================
# KPI METRICS SECTION
# =============================================================================
st.subheader("📊 Key Performance Indicators")

# Calculate KPIs
total_athletes = len(filtered_athletes) if not filtered_athletes.empty else 0
total_countries = len(nocs_df) if not nocs_df.empty else 0
total_sports = events_df["sport"].nunique() if not events_df.empty else 0
total_medals = int(filtered_totals["Total"].sum()) if not filtered_totals.empty else 0
total_events = len(events_df) if not events_df.empty else 0

# Display KPIs in columns
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="🏃 Total Athletes",
        value=f"{total_athletes:,}",
        help="From athletes.csv"
    )

with col2:
    st.metric(
        label="🌍 Total Countries",
        value=total_countries,
        help="From nocs.csv"
    )

with col3:
    st.metric(
        label="🎯 Total Sports",
        value=total_sports,
        help="From events.csv"
    )

with col4:
    st.metric(
        label="🏅 Medals Awarded",
        value=f"{total_medals:,}",
        help="From medals_total.csv"
    )

with col5:
    st.metric(
        label="🏆 Number of Events",
        value=total_events,
        help="From events.csv"
    )

st.divider()

# =============================================================================
# CHARTS ROW
# =============================================================================
# Create tabs
tab1, tab2 = st.tabs(["🥇 Global Medal Distribution", "🏆 Top 10 Medal Standings"])

# -------------------------------------------------------------------------
# Tab 1: Global Medal Distribution
# -------------------------------------------------------------------------
with tab1:
    if not filtered_totals.empty:
        gold_total = int(filtered_totals["Gold"].sum())
        silver_total = int(filtered_totals["Silver"].sum())
        bronze_total = int(filtered_totals["Bronze"].sum())
        
        medal_data = pd.DataFrame({
            "Medal": ["Gold", "Silver", "Bronze"],
            "Count": [gold_total, silver_total, bronze_total]
        })
        
        fig = px.pie(
            medal_data,
            values="Count",
            names="Medal",
            hole=0.4,
            color="Medal",
            color_discrete_map={
               "Gold": "#E50914",    # Rouge intense
            "Silver": "#AFAFAF",  # Gris chic
            "Bronze": "#8B4513"   # Marron profond
            },
        )
        fig.update_traces(
            textposition="inside",
            textinfo="percent+label+value",
            hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>"
        )
        fig.update_layout(
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2),
            height=400,
            margin=dict(t=20, b=60, l=20, r=20),
        )
        st.plotly_chart(fig, use_container_width=True, key="medal_donut")
    else:
        st.warning("No medal data available for selected filters.")

# -------------------------------------------------------------------------
# Tab 2: Top 10 Medal Standings
# -------------------------------------------------------------------------
with tab2:
    if not filtered_totals.empty:
        top10 = filtered_totals.head(10).copy()
        top10 = top10.sort_values("Total", ascending=True)
        
        fig = go.Figure()
        
        # Add bars for each medal type
        fig.add_trace(go.Bar(
            y=top10["country"],
            x=top10["Bronze"],
            name="Bronze",
            orientation="h",
            marker_color="#8B4513",
            text=top10["Bronze"],
            textposition="inside",
        ))
        fig.add_trace(go.Bar(
            y=top10["country"],
            x=top10["Silver"],
            name="Silver",
            orientation="h",
            marker_color="#AFAFAF",
            text=top10["Silver"],
            textposition="inside",
        ))
        fig.add_trace(go.Bar(
            y=top10["country"],
            x=top10["Gold"],
            name="Gold",
            orientation="h",
            marker_color= "#E50914", 
            text=top10["Gold"],
            textposition="inside",
        ))
        
        fig.update_layout(
            barmode="stack",
            height=400,
            margin=dict(t=20, b=20, l=20, r=20),
            xaxis_title="Total Medals",
            yaxis_title="",
            legend=dict(orientation="h", yanchor="bottom", y=-0.2),
            hovermode="y unified",
        )
        st.plotly_chart(fig, use_container_width=True, key="top10_bar")
    else:
        st.warning("No data available for selected filters.")

st.divider()


