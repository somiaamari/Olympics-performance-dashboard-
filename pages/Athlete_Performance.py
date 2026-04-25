import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.shared_filters import render_global_filters, apply_filters, get_continent
from utils.style import apply_custom_style

# PAGE CONFIG
st.set_page_config(
    layout="wide",
    page_title="Athlete Performance | LA28 Dashboard",
    page_icon="👤",
    initial_sidebar_state="expanded",
)
apply_custom_style()

# DATA LOADING
DATA_PATH = Path(__file__).parent.parent / "data"


@st.cache_data
def load_athletes():
    """Load athletes data."""
    try:
        df = pd.read_csv(DATA_PATH / "athletes.csv")
        df = df.rename(columns={"country_code": "noc"})
        # Calculate age from birth_date
        df["birth_date"] = pd.to_datetime(df["birth_date"], errors="coerce")
        df["age"] = ((pd.Timestamp("2024-07-26") - df["birth_date"]).dt.days / 365.25).astype(float)
        return df
    except Exception as e:
        st.error(f"Error loading athletes: {e}")
        return pd.DataFrame()


@st.cache_data
def load_medallists():
    """Load medallists data."""
    try:
        df = pd.read_csv(DATA_PATH / "medallists.csv")
        df = df.rename(columns={"country_code": "noc", "medal_type": "medal"})
        df["medal"] = df["medal"].str.replace(" Medal", "", regex=False)
        return df
    except:
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
def load_coaches():
    """Load coaches data."""
    try:
        return pd.read_csv(DATA_PATH / "coaches.csv")
    except:
        return pd.DataFrame()


@st.cache_data
def load_teams():
    """Load teams data."""
    try:
        return pd.read_csv(DATA_PATH / "teams.csv")
    except:
        return pd.DataFrame()


@st.cache_data
def get_coaches_for_athlete(athlete_row, teams_df):
    """Get coaches for an athlete based on their discipline."""
    coaches_list = []
    athlete_disciplines = athlete_row.get("disciplines", "")
    
    if pd.notna(athlete_disciplines) and athlete_disciplines and not teams_df.empty:
        # Parse disciplines
        disciplines = str(athlete_disciplines).replace("[", "").replace("]", "").replace("'", "").split(",")
        disciplines = [d.strip() for d in disciplines if d.strip()]
        
        # Look for teams with matching discipline
        for discipline in disciplines[:2]:  # Check first 2 disciplines
            matching_teams = teams_df[teams_df["discipline"] == discipline]
            
            for _, team in matching_teams.iterrows():
                team_coaches = team.get("coaches", "")
                if pd.notna(team_coaches) and team_coaches:
                    # Parse coaches
                    coaches_str = str(team_coaches).replace("[", "").replace("]", "").replace("'", "")
                    team_coaches_list = [c.strip() for c in coaches_str.split(",") if c.strip()]
                    
                    for coach_name in team_coaches_list[:3]:  # Get first 3 coaches
                        if coach_name:
                            coaches_list.append({
                                "name": coach_name,
                                "team": team.get("team", "N/A"),
                                "country": team.get("country", "N/A"),
                                "discipline": team.get("discipline", "N/A"),
                                "team_gender": team.get("team_gender", "N/A")
                            })
    
    # Remove duplicates
    unique_coaches = []
    seen_names = set()
    for coach in coaches_list:
        if coach["name"] not in seen_names:
            seen_names.add(coach["name"])
            unique_coaches.append(coach)
    
    return unique_coaches[:3]  # Keep only 3 coaches


# Load all data
athletes_df = load_athletes()
medallists_df = load_medallists()
medals_df = load_medals()
coaches_df = load_coaches()
teams_df = load_teams()

# SIDEBAR - GLOBAL FILTERS
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/5/5c/Olympic_rings_without_rims.svg", width=150)
    st.title("👤 Athletes")
    st.divider()
    
    all_countries = sorted(athletes_df["noc"].dropna().unique().tolist()) if not athletes_df.empty else []
    all_sports = sorted(athletes_df["disciplines"].dropna().astype(str).str.replace(r"[\[\]']", "", regex=True).unique().tolist()) if not athletes_df.empty else []
    
    filters = render_global_filters(countries=all_countries, sports=[])
    
    st.divider()
    st.caption("LA28 Volunteer Selection Challenge")

# APPLY FILTERS
filtered_athletes = athletes_df.copy()
if filters["countries"]:
    filtered_athletes = filtered_athletes[filtered_athletes["noc"].isin(filters["countries"])]
if filters["continents"]:
    filtered_athletes = filtered_athletes[filtered_athletes["noc"].apply(get_continent).isin(filters["continents"])]

filtered_medallists = apply_filters(medallists_df, filters)

# HEADER
st.title("👤 Athlete Performance Analysis")
st.markdown("Explore individual athlete statistics, demographics, and achievements.")
st.divider()

# 1. ATHLETE PROFILE CARD
st.subheader("🔍 Athlete Profile Card")

if not filtered_athletes.empty:
    # Search box
    athlete_names = sorted(filtered_athletes["name"].dropna().unique().tolist())
    
    selected_athlete = st.selectbox(
        "Search for an athlete by name:",
        options=[""] + athlete_names,
        format_func=lambda x: "Type to search..." if x == "" else x,
        key="athlete_search"
    )
    
    if selected_athlete:
        athlete_row = filtered_athletes[filtered_athletes["name"] == selected_athlete].iloc[0]
        
        # Get coaches for this athlete
        coaches_list = get_coaches_for_athlete(athlete_row, teams_df)
        
        # Get athlete's medals
        athlete_medals = filtered_medallists[filtered_medallists["name"] == selected_athlete] if not filtered_medallists.empty else pd.DataFrame()
        
        # Create profile card
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            # Profile info without blue background
            st.markdown("### 👤 Athlete Profile")
            
            # Get gender for appropriate icon
            gender = athlete_row.get("gender", "").lower()
            athlete_icon = "🏃‍♀️" if "female" in gender else "🏃‍♂️"
            
            # Display in a clean container
            with st.container():
                st.markdown(f"<div style='text-align: center; font-size: 3rem; margin: 1rem 0;'>{athlete_icon}</div>", unsafe_allow_html=True)
                
                st.markdown(f"**Function:** {athlete_row.get('function', 'Athlete')}")
                st.markdown(f"**Category:** {athlete_row.get('category', 'N/A')}")
                st.markdown(f"**Status:** 🟢 Active")

        with col2:
            # Athlete name and info - NOT as a table
            st.markdown(f"# {selected_athlete}")
            
            # Create a clean grid layout
            info_col1, info_col2 = st.columns(2)
            
            with info_col1:
                st.markdown("##### 🏳️ Country")
                country = athlete_row.get("country", athlete_row.get("noc", "N/A"))
                noc = athlete_row.get("noc", "")
                st.markdown(f"**{country}** ({noc})")
                
                st.markdown("##### 👤 Gender")
                gender = athlete_row.get("gender", "N/A")
                st.markdown(f"**{gender}**")
            
            with info_col2:
                st.markdown("##### 🎯 Function")
                function = athlete_row.get("function", "Athlete")
                st.markdown(f"**{function}**")
                
                st.markdown("##### 🏷️ Category")
                category = athlete_row.get("category", "N/A")
                st.markdown(f"**{category}**")
            
            # Clean and display disciplines
            disciplines = str(athlete_row.get("disciplines", "N/A"))
            if "[" in disciplines:
                disciplines = disciplines.replace("[", "").replace("]", "").replace("'", "")
            st.markdown("##### 🏆 Disciplines")
            st.markdown(f"**{disciplines}**")
            
            # Clean and display events
            events = str(athlete_row.get("events", "N/A"))
            if "[" in events:
                events = events.replace("[", "").replace("]", "").replace("'", "")
            st.markdown("##### 📅 Events")
            st.markdown(f"**{events}**")

        with col3:
            # Physical Stats
            st.markdown("### 📊 Physical Stats")
            
            # Display stats in a clean layout
            height = athlete_row.get("height", 0)
            weight = athlete_row.get("weight", 0)
            
            # Height
            if height and height > 0:
                st.metric("📏 Height", f"{height:.0f} cm")
            else:
                st.markdown("**📏 Height:** N/A")
            
            # Weight
            if weight and weight > 0:
                st.metric("⚖️ Weight", f"{weight:.0f} kg")
            else:
                st.markdown("**⚖️ Weight:** N/A")
            
            # Age
            if "age" in athlete_row and athlete_row["age"] > 0:
                st.metric("🎂 Age", f"{athlete_row['age']:.0f} years")
            
            st.divider()
            
            # Coaches Section
            st.markdown("### 🧑‍🏫 Coaches")
            
            if coaches_list:
                for i, coach_info in enumerate(coaches_list):
                    with st.expander(f"👤 {coach_info.get('name', 'Coach')}", expanded=(i == 0)):
                        # Display team information
                        if coach_info.get("team") and coach_info["team"] != "N/A":
                            st.markdown(f"**Team:** {coach_info['team']}")
                        
                        if coach_info.get("country") and coach_info["country"] != "N/A":
                            st.markdown(f"**Country:** {coach_info['country']}")
                        
                        if coach_info.get("discipline") and coach_info["discipline"] != "N/A":
                            st.markdown(f"**Discipline:** {coach_info['discipline']}")
                        
                        if coach_info.get("team_gender") and coach_info["team_gender"] != "N/A":
                            st.markdown(f"**Team Gender:** {coach_info['team_gender']}")
            else:
                # Show raw coach data if available
                coach_data = athlete_row.get("coach", "")
                if pd.notna(coach_data) and coach_data:
                    coach_display = str(coach_data).replace("[", "").replace("]", "").replace("'", "")
                    st.markdown(f"**Coach(s):** {coach_display}")
                else:
                    st.info("No coach information available")

        # MEDALS SECTION - Below the profile card
        st.markdown("---")
        
        if not athlete_medals.empty:
            gold = len(athlete_medals[athlete_medals["medal"] == "Gold"])
            silver = len(athlete_medals[athlete_medals["medal"] == "Silver"])
            bronze = len(athlete_medals[athlete_medals["medal"] == "Bronze"])
            total = gold + silver + bronze
            
            medal_col1, medal_col2, medal_col3, medal_col4 = st.columns(4)
            
            with medal_col1:
                st.metric("🥇 Gold Medals", gold)
            with medal_col2:
                st.metric("🥈 Silver Medals", silver)
            with medal_col3:
                st.metric("🥉 Bronze Medals", bronze)
            with medal_col4:
                st.metric("🏅 Total Medals", total)
            
            # Show medal details in an expander
            with st.expander("📋 View Medal Details"):
                # Select available columns from your medallists data
                available_columns = []
                if "medal_date" in athlete_medals.columns:
                    available_columns.append("medal_date")
                if "discipline" in athlete_medals.columns:
                    available_columns.append("discipline")
                if "event" in athlete_medals.columns:
                    available_columns.append("event")
                if "event_type" in athlete_medals.columns:
                    available_columns.append("event_type")
                if "team" in athlete_medals.columns:
                    available_columns.append("team")
                available_columns.append("medal")  # Always include medal column
                
                medal_details = athlete_medals[available_columns]
                
                # Rename columns for better display
                column_renames = {
                    "medal_date": "Date",
                    "discipline": "Discipline",
                    "event": "Event",
                    "event_type": "Event Type",
                    "team": "Team",
                    "medal": "Medal"
                }
                medal_details = medal_details.rename(columns=column_renames)
                
                st.dataframe(medal_details, width='stretch', hide_index=True)
        else:
            st.info("This athlete has no recorded medals.")
        
        st.markdown("---")
    else:
        st.info("👆 Select an athlete from the dropdown above to view their profile.")
else:
    st.warning("No athletes data available.")

st.divider()

# 2. AGE DISTRIBUTION (Box/Violin Plot)
st.subheader("📊 Athlete Age Distribution")

if not filtered_athletes.empty and "age" in filtered_athletes.columns:
    # Add continent for grouping
    plot_athletes = filtered_athletes.copy()
    plot_athletes["Continent"] = plot_athletes["noc"].apply(get_continent)
    plot_athletes = plot_athletes.dropna(subset=["age"])
    plot_athletes = plot_athletes[plot_athletes["age"] > 0]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**By Gender**")
        if "gender" in plot_athletes.columns:
            fig = px.box(
                plot_athletes,
                x="gender",
                y="age",
                color="gender",
                color_discrete_map={"Male": "#3498db", "Female": "#e74c3c"},
                title="Age Distribution by Gender"
            )
            fig.update_layout(height=400, showlegend=False, xaxis_title="", yaxis_title="Age")
            st.plotly_chart(fig, width='stretch', key="age_gender_box")
    
    with col2:
        st.markdown("**By Continent**")
        fig = px.violin(
            plot_athletes,
            x="Continent",
            y="age",
            color="Continent",
            box=True,
            title="Age Distribution by Continent"
        )
        fig.update_layout(height=400, showlegend=False, xaxis_title="", yaxis_title="Age")
        st.plotly_chart(fig, width='stretch', key="age_continent_violin")
else:
    st.warning("Age data not available.")

st.divider()

# 3. GENDER DISTRIBUTION BY CONTINENT/COUNTRY
st.subheader("👫 Gender Distribution")

if not filtered_athletes.empty and "gender" in filtered_athletes.columns:
    # Add continent
    gender_df = filtered_athletes.copy()
    gender_df["Continent"] = gender_df["noc"].apply(get_continent)
    
    # View selector
    view_option = st.radio(
        "View by:",
        options=["World", "Continent", "Country"],
        horizontal=True,
        key="gender_view"
    )
    
    if view_option == "World":
        gender_counts = gender_df["gender"].value_counts().reset_index()
        gender_counts.columns = ["Gender", "Count"]
        
        fig = px.pie(
            gender_counts,
            values="Count",
            names="Gender",
            color="Gender",
            color_discrete_map={"Male": "#3498db", "Female": "#e74c3c"},
            hole=0.4,
            title="Global Gender Distribution"
        )
        fig.update_traces(textposition="inside", textinfo="percent+label+value")
        fig.update_layout(height=400)
        st.plotly_chart(fig, width='stretch', key="gender_world")
    
    elif view_option == "Continent":
        continent_gender = gender_df.groupby(["Continent", "gender"]).size().reset_index(name="Count")
        
        fig = px.bar(
            continent_gender,
            x="Continent",
            y="Count",
            color="gender",
            color_discrete_map={"Male": "#3498db", "Female": "#e74c3c"},
            barmode="group",
            text="Count",
            title="Gender Distribution by Continent"
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(height=400, xaxis_title="", legend_title="Gender")
        st.plotly_chart(fig, width='stretch', key="gender_continent")
    
    else:  # Country
        # Top 20 countries
        top_countries = gender_df["noc"].value_counts().head(20).index.tolist()
        country_gender = gender_df[gender_df["noc"].isin(top_countries)].groupby(["noc", "gender"]).size().reset_index(name="Count")
        
        fig = px.bar(
            country_gender,
            x="noc",
            y="Count",
            color="gender",
            color_discrete_map={"Male": "#3498db", "Female": "#e74c3c"},
            barmode="stack",
            text="Count",
            title="Gender Distribution by Country (Top 20)"
        )
        fig.update_layout(height=400, xaxis_title="Country", xaxis_tickangle=-45, legend_title="Gender")
        st.plotly_chart(fig, width='stretch', key="gender_country")
else:
    st.warning("Gender data not available.")

st.divider()

# 4. TOP ATHLETES BY MEDALS (Bar Chart)
st.subheader("🏆 Top Athletes by Medals")

if not filtered_medallists.empty:
    # Count medals per athlete
    athlete_medals = filtered_medallists.groupby(["name", "noc"]).agg(
        Total=("medal", "count"),
        Gold=("medal", lambda x: (x == "Gold").sum()),
        Silver=("medal", lambda x: (x == "Silver").sum()),
        Bronze=("medal", lambda x: (x == "Bronze").sum()),
    ).reset_index()
    
    athlete_medals = athlete_medals.sort_values(["Gold", "Total"], ascending=False).head(10)
    
    # Create stacked bar chart
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=athlete_medals["name"],
        x=athlete_medals["Bronze"],
        name="Bronze",
        orientation="h",
        marker_color="#CD7F32",
        text=athlete_medals["Bronze"],
        textposition="inside",
    ))
    fig.add_trace(go.Bar(
        y=athlete_medals["name"],
        x=athlete_medals["Silver"],
        name="Silver",
        orientation="h",
        marker_color="#C0C0C0",
        text=athlete_medals["Silver"],
        textposition="inside",
    ))
    fig.add_trace(go.Bar(
        y=athlete_medals["name"],
        x=athlete_medals["Gold"],
        name="Gold",
        orientation="h",
        marker_color="#FFD700",
        text=athlete_medals["Gold"],
        textposition="inside",
    ))
    
    fig.update_layout(
        barmode="stack",
        height=450,
        xaxis_title="Total Medals",
        yaxis_title="",
        yaxis=dict(categoryorder="total ascending"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        title="Top 10 Athletes by Medal Count"
    )
    st.plotly_chart(fig, width='stretch', key="top_athletes_bar")
    
    # Also show as table
    st.markdown("**Medal Details**")
    display_df = athlete_medals[["name", "noc", "Gold", "Silver", "Bronze", "Total"]]
    display_df.columns = ["Athlete", "Country", "🥇", "🥈", "🥉", "Total"]
    st.dataframe(display_df, width='stretch', hide_index=True)
else:
    st.warning("No medallist data available.")

st.divider()

# EXPORT
if not filtered_athletes.empty:
    csv_data = filtered_athletes[["name", "noc", "gender", "age", "disciplines", "events"]].to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Download Athletes (CSV)",
        data=csv_data,
        file_name="athletes.csv",
        mime="text/csv",
    )

st.divider()
st.caption("🏅 LA28 Olympics Glory Dashboard | Athlete Performance")