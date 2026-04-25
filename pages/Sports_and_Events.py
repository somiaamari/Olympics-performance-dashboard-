"""
LA28 Olympics Dashboard - Page 4: Sports and Events (Competition Arena)

Analysis from sports and events perspective.
Per official requirements:
- Event Schedule (Gantt/Timeline Chart)
- Medal Count by Sport (Treemap)
- Venue Map (Scatter Mapbox)
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.shared_filters import render_global_filters, apply_filters, get_continent
from utils.style import apply_custom_style

# =============================================================================
# PAGE CONFIG
# =============================================================================
st.set_page_config(
    layout="wide",
    page_title="Sports & Events | LA28 Dashboard",
    page_icon="🏟️",
    initial_sidebar_state="expanded",
)
apply_custom_style()

# =============================================================================
# DATA LOADING
# =============================================================================
DATA_PATH = Path(__file__).parent.parent / "data"


@st.cache_data
def load_schedules():
    """Load schedules data."""
    try:
        df = pd.read_csv(DATA_PATH / "schedules.csv")
        df["start_date"] = pd.to_datetime(df["start_date"], errors="coerce")
        df["end_date"] = pd.to_datetime(df["end_date"], errors="coerce")
        return df
    except Exception as e:
        return pd.DataFrame()


@st.cache_data
def load_medals():
    """Load medals data."""
    try:
        df = pd.read_csv(DATA_PATH / "medals.csv")
        df = df.rename(columns={"country_code": "noc", "medal_type": "medal"})
        df["medal"] = df["medal"].str.replace(" Medal", "", regex=False)
        return df
    except:
        return pd.DataFrame()


@st.cache_data
def load_venues():
    """Load venues data."""
    try:
        return pd.read_csv(DATA_PATH / "venues.csv")
    except:
        return pd.DataFrame()


@st.cache_data
def load_events():
    """Load events data."""
    try:
        return pd.read_csv(DATA_PATH / "events.csv")
    except:
        return pd.DataFrame()


# Load data
schedules_df = load_schedules()
medals_df = load_medals()
venues_df = load_venues()
events_df = load_events()

# =============================================================================
# SIDEBAR - GLOBAL FILTERS
# =============================================================================
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/5/5c/Olympic_rings_without_rims.svg", width=150)
    st.title("🏟️ Sports & Events")
    st.divider()
    
    all_sports = sorted(medals_df["discipline"].dropna().unique().tolist()) if not medals_df.empty else []
    
    filters = render_global_filters(countries=[], sports=all_sports)
    
    st.divider()
    st.caption("LA28 Volunteer Selection Challenge")

# =============================================================================
# APPLY FILTERS
# =============================================================================
filtered_medals = medals_df.copy()
if filters["sports"]:
    filtered_medals = filtered_medals[filtered_medals["discipline"].isin(filters["sports"])]
if filters["medal_types"]:
    filtered_medals = filtered_medals[filtered_medals["medal"].isin(filters["medal_types"])]

# =============================================================================
# HEADER
# =============================================================================
st.title("🏟️ Sports & Events Analysis")
st.markdown("Explore Olympic sports, event schedules, and competition venues.")
st.divider()

# =============================================================================
# KPIs
# =============================================================================
col1, col2, col3, col4 = st.columns(4)
col1.metric("🎯 Sports", medals_df["discipline"].nunique() if not medals_df.empty else 0)
col2.metric("🏆 Events", len(events_df) if not events_df.empty else 0)
col3.metric("🏟️ Venues", len(venues_df) if not venues_df.empty else 0)
col4.metric("📅 Competition Days", 17)

st.divider()

# =============================================================================
# 0. WHO WON THE DAY? (Timeline Feature)
# =============================================================================
st.subheader("📅 Who Won the Day?")
st.markdown("Select a date to see the daily medal tally and key events.")

if not medals_df.empty and "medal_date" in medals_df.columns:
    # Convert dates
    medals_df["medal_date"] = pd.to_datetime(medals_df["medal_date"], errors="coerce")
    valid_dates = sorted(medals_df["medal_date"].dropna().unique())
    
    if valid_dates:
        # Date Slider
        min_date = valid_dates[0].date()
        max_date = valid_dates[-1].date()
        
        selected_date = st.slider(
            "Select Date",
            min_value=min_date,
            max_value=max_date,
            value=min_date,
            format="MMM DD"
        )
        
        # Filter data for selected date
        day_medals = medals_df[medals_df["medal_date"].dt.date == selected_date]
        
        if not day_medals.empty:
            # Daily Stats
            daily_total = len(day_medals)
            daily_gold = len(day_medals[day_medals["medal"] == "Gold"])
            
            col_d1, col_d2, col_d3 = st.columns(3)
            col_d1.metric("Medals Awarded Today", daily_total)
            col_d2.metric("🥇 Gold Medals", daily_gold)
            col_d3.metric("Countries on Podium", day_medals["noc"].nunique())
            
            # Daily Medal Table
            st.markdown(f"**Medal Standings for {selected_date.strftime('%B %d')}**")
            daily_standings = day_medals.groupby("noc").agg(
                Gold=("medal", lambda x: (x == "Gold").sum()),
                Silver=("medal", lambda x: (x == "Silver").sum()),
                Bronze=("medal", lambda x: (x == "Bronze").sum()),
                Total=("medal", "count")
            ).sort_values(["Gold", "Total"], ascending=False).head(10)
            
            st.dataframe(daily_standings, use_container_width=True)
            
            # Events on this day
            if not schedules_df.empty:
                day_events = schedules_df[pd.to_datetime(schedules_df["start_date"]).dt.date == selected_date]
                if not day_events.empty:
                    st.markdown(f"**Key Events on {selected_date.strftime('%B %d')}**")
                    st.dataframe(
                        day_events[["start_date", "discipline", "event", "venue", "status"]].sort_values("start_date").head(10),
                        use_container_width=True,
                        hide_index=True
                    )
        else:
            st.info(f"No medals awarded on {selected_date.strftime('%B %d')}.")
    else:
        st.warning("No valid dates found in medal data.")
else:
    st.warning("Date information not available.")

st.divider()

# =============================================================================
# 1. EVENT SCHEDULE (Gantt/Timeline Chart)
# =============================================================================
st.subheader("📅 Event Schedule")

if not schedules_df.empty:
    # Filter for valid dates
    schedule_valid = schedules_df.dropna(subset=["start_date", "end_date"]).copy()
    
    if not schedule_valid.empty:
        # Sport selector for schedule
        schedule_sports = sorted(schedule_valid["discipline"].dropna().unique().tolist())
        selected_schedule_sport = st.selectbox(
            "Select Sport:",
            options=["All Sports"] + schedule_sports,
            key="schedule_sport"
        )
        
        if selected_schedule_sport != "All Sports":
            schedule_filtered = schedule_valid[schedule_valid["discipline"] == selected_schedule_sport]
        else:
            # Show top events by discipline
            schedule_filtered = schedule_valid.head(50)
        
        if not schedule_filtered.empty:
            # Create Gantt chart
            fig = px.timeline(
                schedule_filtered,
                x_start="start_date",
                x_end="end_date",
                y="event" if "event" in schedule_filtered.columns else "discipline",
                color="discipline",
                hover_data=["venue"] if "venue" in schedule_filtered.columns else None,
            )
            fig.update_layout(
                height=450,
                xaxis_title="Date",
                yaxis_title="",
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.3),
            )
            fig.update_yaxes(categoryorder="category ascending")
            st.plotly_chart(fig, use_container_width=True, key="schedule_gantt")
        else:
            st.info("No schedule data available for the selected sport.")
    else:
        st.warning("Schedule data has missing dates.")
else:
    st.warning("Schedule data not available.")

st.divider()

# =============================================================================
# 2. MEDAL COUNT BY SPORT (Treemap)
# =============================================================================
st.subheader("🏅 Medal Count by Sport")

if not filtered_medals.empty:
    # Aggregate medals by sport and medal type
    sport_medals = filtered_medals.groupby(["discipline", "medal"]).size().reset_index(name="Count")
    
    fig = px.treemap(
        sport_medals,
        path=["discipline", "medal"],
        values="Count",
        color="medal",
        color_discrete_map={
            "Gold": "#FFD700",
            "Silver": "#C0C0C0",
            "Bronze": "#CD7F32"
        },
    )
    fig.update_layout(
        height=500,
        margin=dict(t=20, b=20, l=20, r=20),
    )
    fig.update_traces(
        textinfo="label+value",
        hovertemplate="<b>%{label}</b><br>Count: %{value}<extra></extra>"
    )
    st.plotly_chart(fig, use_container_width=True, key="sport_treemap")
    
    # Also show as table
    sport_summary = filtered_medals.groupby("discipline").agg(
        Total=("medal", "count"),
        Gold=("medal", lambda x: (x == "Gold").sum()),
        Silver=("medal", lambda x: (x == "Silver").sum()),
        Bronze=("medal", lambda x: (x == "Bronze").sum()),
    ).reset_index().sort_values("Total", ascending=False)
    
    sport_summary.columns = ["Sport", "Total", "🥇", "🥈", "🥉"]
    st.dataframe(sport_summary, use_container_width=True, hide_index=True)
else:
    st.warning("No medal data available.")

st.divider()

# =============================================================================
# 3. VENUE MAP (Scatter Mapbox)
# =============================================================================
st.subheader("🗺️ Olympic Venues Map")

if not venues_df.empty:
    # Check for lat/long columns
    lat_col = None
    lon_col = None
    
    for col in venues_df.columns:
        if "lat" in col.lower():
            lat_col = col
        if "lon" in col.lower() or "lng" in col.lower():
            lon_col = col
    
    if lat_col and lon_col:
        venues_map = venues_df.dropna(subset=[lat_col, lon_col])
        
        if not venues_map.empty:
            fig = px.scatter_mapbox(
                venues_map,
                lat=lat_col,
                lon=lon_col,
                hover_name="venue" if "venue" in venues_map.columns else venues_map.columns[0],
                zoom=10,
                height=500,
            )
            fig.update_layout(
                mapbox_style="open-street-map",
                margin=dict(t=0, b=0, l=0, r=0),
            )
            st.plotly_chart(fig, use_container_width=True, key="venue_map")
        else:
            st.info("No venues with valid coordinates.")
    else:
        # Show Paris area with placeholder markers
        st.markdown("**Paris Olympic Area**")
        
        # Create Paris area map with known venues
        paris_venues = pd.DataFrame({
            "venue": [
                "Stade de France", "Champs de Mars Arena", "Grand Palais",
                "Roland-Garros", "Parc des Princes", "Arena Bercy",
                "Stade Pierre-Mauroy", "Vélodrome de Saint-Quentin"
            ],
            "lat": [48.9244, 48.8584, 48.8660, 48.8469, 48.8414, 48.8386, 50.6127, 48.7866],
            "lon": [2.3601, 2.2945, 2.3125, 2.2472, 2.2530, 2.3786, 3.0299, 2.0448],
            "sports": [
                "Athletics, Rugby", "Judo, Wrestling", "Fencing, Taekwondo",
                "Tennis", "Football", "Basketball, Gymnastics",
                "Handball", "Cycling"
            ]
        })
        
        fig = px.scatter_mapbox(
            paris_venues,
            lat="lat",
            lon="lon",
            hover_name="venue",
            hover_data={"sports": True, "lat": False, "lon": False},
            zoom=10,
            height=500,
            size_max=15,
        )
        fig.update_traces(marker=dict(size=15, color="#0033A0"))
        fig.update_layout(
            mapbox_style="open-street-map",
            margin=dict(t=0, b=0, l=0, r=0),
        )
        st.plotly_chart(fig, use_container_width=True, key="venue_map_paris")
        
        # Also show venues as table
        st.markdown("**Venue List**")
        st.dataframe(venues_df, use_container_width=True, hide_index=True)
else:
    # Show Paris area with known Olympic venues
    st.markdown("Showing major Paris 2024 Olympic venues:")
    
    paris_venues = pd.DataFrame({
        "venue": [
            "Stade de France", "Champs de Mars Arena", "Grand Palais",
            "Roland-Garros", "Parc des Princes", "Arena Bercy"
        ],
        "lat": [48.9244, 48.8584, 48.8660, 48.8469, 48.8414, 48.8386],
        "lon": [2.3601, 2.2945, 2.3125, 2.2472, 2.2530, 2.3786],
    })
    
    fig = px.scatter_mapbox(
        paris_venues,
        lat="lat",
        lon="lon",
        hover_name="venue",
        zoom=11,
        height=450,
    )
    fig.update_traces(marker=dict(size=15, color="#0033A0"))
    fig.update_layout(mapbox_style="open-street-map", margin=dict(t=0, b=0, l=0, r=0))
    st.plotly_chart(fig, use_container_width=True, key="venue_map_default")

st.divider()

# =============================================================================
# 4. EVENTS BY SPORT
# =============================================================================
st.subheader("📋 Events by Sport")

if not events_df.empty:
    sport_select = st.selectbox(
        "Select Sport:",
        options=["All"] + sorted(events_df["sport"].dropna().unique().tolist()),
        key="events_sport"
    )
    
    if sport_select != "All":
        display_events = events_df[events_df["sport"] == sport_select]
    else:
        display_events = events_df
    
    st.dataframe(display_events, use_container_width=True, hide_index=True)
else:
    st.warning("Events data not available.")

st.divider()

# =============================================================================
# EXPORT
# =============================================================================
col1, col2 = st.columns(2)

with col1:
    if not filtered_medals.empty:
        csv_data = filtered_medals.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Download Medals by Sport",
            data=csv_data,
            file_name="sports_medals.csv",
            mime="text/csv",
            use_container_width=True,
        )

with col2:
    if not venues_df.empty:
        csv_venues = venues_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Download Venues",
            data=csv_venues,
            file_name="venues.csv",
            mime="text/csv",
            use_container_width=True,
        )

st.divider()
st.caption("🏅 LA28 Olympics Glory Dashboard | Sports & Events")
