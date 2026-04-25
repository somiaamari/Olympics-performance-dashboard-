# ===================================================================
# 2_Globe_Global_Analysis.py → Modern Tabs Version
# ===================================================================
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ------------------- CONFIG -------------------
st.set_page_config(page_title="Global Analysis", page_icon="Globe", layout="wide")

# ------------------- DATA -------------------
DATA_PATH = Path(__file__).parent.parent / "data"

@st.cache_data
def load_data():
    medals = pd.read_csv(DATA_PATH / "medals.csv")
    medals_total = pd.read_csv(DATA_PATH / "medals_total.csv")
    medals = medals.rename(columns={"country_code": "noc", "medal_type": "medal"})
    medals["medal"] = medals["medal"].str.replace(" Medal", "", regex=False)
    medals_total = medals_total.rename(columns={"country_code": "noc"})
    return medals, medals_total

medals_df, medals_total_df = load_data()

# Mappings
country_name = dict(zip(medals_total_df["noc"], medals_total_df["country"]))
continent_map = {
    "USA":"North America","CAN":"North America","BRA":"South America","ARG":"South America",
    "FRA":"Europe","GBR":"Europe","GER":"Europe","ITA":"Europe","ESP":"Europe","NED":"Europe",
    "SWE":"Europe","NOR":"Europe","CHN":"Asia","JPN":"Asia","KOR":"Asia","IND":"Asia",
    "AUS":"Oceania","NZL":"Oceania","EGY":"Africa","MAR":"Africa","ALG":"Africa","NGR":"Africa",
}
def get_continent(c): return continent_map.get(c, "Other")

iso3_map = {"USA":"USA","CHN":"CHN","JPN":"JPN","GBR":"GBR","FRA":"FRA","GER":"DEU","ITA":"ITA","NED":"NLD","AUS":"AUS","KOR":"KOR"}
def get_iso3(c): return iso3_map.get(c, "")

# ------------------- SIDEBAR -------------------
# Sidebar style override
st.markdown("""
    <style>
        /* Sidebar background */
        [data-testid="stSidebar"] {
            background-color: #1e293b
        }

        /* Sidebar text color */
        [data-testid="stSidebar"] * {
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)



with st.sidebar:
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/5/5c/Olympic_rings_without_rims.svg",
        width=130
    )
    st.markdown("## Globe Global Analysis")
    countries = st.multiselect("Country (NOC)", sorted(medals_total_df["noc"].unique()))
    sports = st.multiselect("Sport", sorted(medals_df["discipline"].unique()))
    medal_sel = st.multiselect("Medal Type",
                               ["Gold", "Silver", "Bronze"],
                               default=["Gold", "Silver", "Bronze"])


# ------------------- FILTER -------------------
df = medals_df.copy()
if countries: df = df[df["noc"].isin(countries)]
if sports: df = df[df["discipline"].isin(sports)]
if medal_sel: df = df[df["medal"].isin(medal_sel)]

# ------------------- TOTALS -------------------
if not df.empty:
    totals = df.groupby("noc")["medal"].value_counts().unstack(fill_value=0)
    for m in ["Gold","Silver","Bronze"]:
        if m not in totals.columns:
            totals[m] = 0
    totals["Total"] = totals.sum(axis=1)
    totals = totals.reset_index()
    totals["Country"] = totals["noc"].map(country_name)
    totals["Continent"] = totals["noc"].apply(get_continent)
    totals["iso_alpha"] = totals["noc"].apply(get_iso3)
else:
    totals = pd.DataFrame(columns=["noc", "Gold", "Silver", "Bronze", "Total", "Country", "Continent", "iso_alpha"])

# ===================================================================
# MAIN PAGE – TABS (super clean & modern)
# ===================================================================
st.markdown("# Globe Global Medal Analysis")
st.markdown("### Paris 2024 Olympics")
st.markdown("---")

# Create 4 beautiful tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "World Medal Map",
    "Continent → Country → Sport",
    "Medals by Continent",
    "Top 20 Countries"
])

# ==================== TAB 1: World Map ====================
with tab1:
    st.subheader("World Medal Map")
    if not totals.empty and totals["iso_alpha"].any():
        fig = px.choropleth(
            totals,
            locations="iso_alpha",
            color="Total",
            hover_name="Country",
            hover_data=["Gold","Silver","Bronze","Total"],
            color_continuous_scale="Plasma",
            projection="natural earth",
            title=None
        )
        fig.update_layout(height=600, margin=dict(t=20, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No country with ISO code for the selected filters.")

# ==================== TAB 2: Hierarchy ====================
with tab2:
    st.subheader("Continent → Country → Discipline")
    if not df.empty:
        hier = df.copy()
        hier["Continent"] = hier["noc"].apply(get_continent)
        hier["Country"] = hier["noc"].map(country_name)
        agg = hier.groupby(["Continent","Country","discipline"]).size().reset_index(name="Medals")

        col1, col2 = st.columns(2)
        with col1:
            fig_sun = px.sunburst(
                agg, path=["Continent","Country","discipline"], values="Medals",
                color="Continent", color_discrete_sequence=px.colors.qualitative.Vivid
            )
            fig_sun.update_layout(height=550, margin=dict(t=30))
            st.plotly_chart(fig_sun, use_container_width=True)

        with col2:
            fig_tree = px.treemap(
                agg, path=["Continent","Country","discipline"], values="Medals",
                color="Medals", color_continuous_scale="Turbo"
            )
            fig_tree.update_layout(height=550, margin=dict(t=30))
            st.plotly_chart(fig_tree, use_container_width=True)
    else:
        st.info("No data for selected filters.")

# ==================== TAB 3: Medals by Continent ====================
with tab3:
    st.subheader("Medals by Continent")
    if not totals.empty:
        cont = totals.groupby("Continent")[["Gold","Silver","Bronze"]].sum().reset_index()
        cont_melt = cont.melt("Continent", var_name="Medal", value_name="Count")
        fig = px.bar(
            cont_melt, x="Continent", y="Count", color="Medal", barmode="group",
            text="Count",
            color_discrete_map={"Gold":"#E50914", "Silver":"#AFAFAF", "Bronze":"#8B4513"}
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data")

# ==================== TAB 4: Top 20 ====================
with tab4:
    st.subheader("Top 20 Countries")
    if not totals.empty:
        top20 = totals.sort_values("Total", ascending=False).head(20)
        top_melt = top20.melt(id_vars="Country", value_vars=["Gold","Silver","Bronze"],
                              var_name="Medal", value_name="Count")
        fig = px.bar(
            top_melt, x="Country", y="Count", color="Medal", barmode="group",
            text="Count",
            color_discrete_map={"Gold":"#E50914", "Silver":"#AFAFAF", "Bronze":"#8B4513"}
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(xaxis_tickangle=-45, height=550)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data")

# Footer
st.markdown("---")
st.caption("Paris 2024 – Global Analysis | Design by You")
