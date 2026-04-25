
import streamlit as st
import pandas as pd

# Continent mapping
CONTINENT_MAP = {
    # Europe
    "GBR": "Europe", "FRA": "Europe", "GER": "Europe", "ITA": "Europe", "ESP": "Europe",
    "NED": "Europe", "POL": "Europe", "UKR": "Europe", "BEL": "Europe", "SWE": "Europe",
    "NOR": "Europe", "DEN": "Europe", "FIN": "Europe", "SUI": "Europe", "AUT": "Europe",
    "POR": "Europe", "GRE": "Europe", "CZE": "Europe", "ROU": "Europe", "HUN": "Europe",
    "IRL": "Europe", "SRB": "Europe", "CRO": "Europe", "SVK": "Europe", "SLO": "Europe",
    "BUL": "Europe", "LTU": "Europe", "LAT": "Europe", "EST": "Europe", "BLR": "Europe",
    "MDA": "Europe", "GEO": "Europe", "ARM": "Europe", "AZE": "Europe", "KOS": "Europe",
    "MKD": "Europe", "ALB": "Europe", "BIH": "Europe", "MNE": "Europe", "CYP": "Europe",
    "MLT": "Europe", "LUX": "Europe", "ISL": "Europe", "AND": "Europe", "SMR": "Europe",
    "MON": "Europe", "LIE": "Europe",
    # Asia
    "CHN": "Asia", "JPN": "Asia", "KOR": "Asia", "IND": "Asia", "THA": "Asia",
    "VIE": "Asia", "MAS": "Asia", "SGP": "Asia", "INA": "Asia", "PHI": "Asia",
    "TPE": "Asia", "HKG": "Asia", "KAZ": "Asia", "UZB": "Asia", "IRN": "Asia",
    "IRQ": "Asia", "KSA": "Asia", "UAE": "Asia", "QAT": "Asia", "KUW": "Asia",
    "BRN": "Asia", "OMA": "Asia", "JOR": "Asia", "LBN": "Asia", "SYR": "Asia",
    "PAK": "Asia", "BAN": "Asia", "SRI": "Asia", "NEP": "Asia", "MYA": "Asia",
    "CAM": "Asia", "LAO": "Asia", "MGL": "Asia", "PRK": "Asia", "TJK": "Asia",
    "TKM": "Asia", "KGZ": "Asia", "AFG": "Asia", "MDV": "Asia", "BHU": "Asia",
    "BRU": "Asia", "TLS": "Asia", "ISR": "Asia", "PLE": "Asia", "YEM": "Asia",
    # Africa
    "RSA": "Africa", "EGY": "Africa", "NGR": "Africa", "KEN": "Africa", "ETH": "Africa",
    "MAR": "Africa", "ALG": "Africa", "TUN": "Africa", "GHA": "Africa", "CIV": "Africa",
    "CMR": "Africa", "SEN": "Africa", "UGA": "Africa", "ZIM": "Africa", "TAN": "Africa",
    "NAM": "Africa", "BOT": "Africa", "ZAM": "Africa", "MOZ": "Africa", "ANG": "Africa",
    "RWA": "Africa", "BUR": "Africa", "MLI": "Africa", "NIG": "Africa", "BEN": "Africa",
    "TOG": "Africa", "GAB": "Africa", "CGO": "Africa", "COD": "Africa", "MAD": "Africa",
    "MRI": "Africa", "SEY": "Africa", "CPV": "Africa", "GAM": "Africa", "GBS": "Africa",
    "GUI": "Africa", "LBR": "Africa", "SLE": "Africa", "SOM": "Africa", "SSD": "Africa",
    "SUD": "Africa", "ERI": "Africa", "DJI": "Africa", "COM": "Africa", "LBA": "Africa",
    "MWI": "Africa", "LES": "Africa", "SWZ": "Africa", "CAF": "Africa", "CHA": "Africa",
    "EQG": "Africa", "STP": "Africa",
    # North America
    "USA": "North America", "CAN": "North America", "MEX": "North America",
    "CUB": "North America", "JAM": "North America", "PUR": "North America",
    "DOM": "North America", "HAI": "North America", "TTO": "North America",
    "BAH": "North America", "BAR": "North America", "GRN": "North America",
    "SKN": "North America", "LCA": "North America", "VIN": "North America",
    "ANT": "North America", "DMA": "North America", "BIZ": "North America",
    "GUA": "North America", "HON": "North America", "ESA": "North America",
    "NCA": "North America", "CRC": "North America", "PAN": "North America",
    "BER": "North America", "CAY": "North America", "IVB": "North America",
    "ISV": "North America", "AHO": "North America", "ARU": "North America",
    # South America
    "BRA": "South America", "ARG": "South America", "COL": "South America",
    "CHI": "South America", "PER": "South America", "VEN": "South America",
    "ECU": "South America", "URU": "South America", "PAR": "South America",
    "BOL": "South America", "GUY": "South America", "SUR": "South America",
    # Oceania
    "AUS": "Oceania", "NZL": "Oceania", "FIJ": "Oceania", "PNG": "Oceania",
    "SAM": "Oceania", "TGA": "Oceania", "VAN": "Oceania", "SOL": "Oceania",
    "FSM": "Oceania", "PLW": "Oceania", "MHL": "Oceania", "KIR": "Oceania",
    "NRU": "Oceania", "TUV": "Oceania", "COK": "Oceania", "ASA": "Oceania",
    "GUM": "Oceania",
}

# Map NOC to emoji flags
NOC_FLAGS = {
    # Europe
    "GBR": "🇬🇧", "FRA": "🇫🇷", "GER": "🇩🇪", "ITA": "🇮🇹", "ESP": "🇪🇸",
    "RUS": "🇷🇺", "NED": "🇳🇱", "SWE": "🇸🇪", "NOR": "🇳🇴", "DEN": "🇩🇰",
    "FIN": "🇫🇮", "BEL": "🇧🇪", "SUI": "🇨🇭", "AUT": "🇦🇹", "POL": "🇵🇱",
    "HUN": "🇭🇺", "CZE": "🇨🇿", "SVK": "🇸🇰", "ROU": "🇷🇴", "BUL": "🇧🇬",
    "GRE": "🇬🇷", "POR": "🇵🇹", "IRL": "🇮🇪", "CRO": "🇭🇷", "SRB": "🇷🇸",
    "SLO": "🇸🇮", "BIH": "🇧🇦", "MKD": "🇲🇰", "ALB": "🇦🇱", "MNE": "🇲🇪",
    "CYP": "🇨🇾", "MLT": "🇲🇹", "LUX": "🇱🇺", "MON": "🇲🇨", "AND": "🇦🇩",
    "LIE": "🇱🇮", "SMR": "🇸🇲", "VAT": "🇻🇦", "ISL": "🇮🇸", "LTU": "🇱🇹",
    "LAT": "🇱🇻", "EST": "🇪🇪", "BLR": "🇧🇾", "UKR": "🇺🇦", "MDA": "🇲🇩",
    "KOS": "🇽🇰",
    # Asia
    "CHN": "🇨🇳", "JPN": "🇯🇵", "KOR": "🇰🇷", "IND": "🇮🇳", "IRI": "🇮🇷",
    "THA": "🇹🇭", "KAZ": "🇰🇿", "UZB": "🇺🇿", "TPE": "🇹🇼", "PHI": "🇵🇭",
    "MAS": "🇲🇾", "SGP": "🇸🇬", "VIE": "🇻🇳", "INA": "🇮🇩", "PAK": "🇵🇰",
    "BAN": "🇧🇩", "SRI": "🇱🇰", "NEP": "🇳🇵", "MGL": "🇲🇳", "PRK": "🇰🇵",
    "HKG": "🇭🇰", "BRN": "🇧🇭", "QAT": "🇶🇦", "KSA": "🇸🇦", "UAE": "🇦🇪",
    "KUW": "🇰🇼", "OMA": "🇴🇲", "JOR": "🇯🇴", "SYR": "🇸🇾", "LIB": "🇱🇧",
    "ISR": "🇮", "AFG": "🇦🇫", "KGZ": "🇰🇬", "TJK": "🇹🇯", "TKM": "🇹🇲",
    "YEM": "🇾🇪", "LAO": "🇱🇦", "CAM": "🇰🇭", "MYA": "🇲🇲", "BHU": "🇧🇹",
    "MDV": "🇲🇻", "BRU": "🇧🇳", "TLS": "🇹🇱",
    # Africa
    "RSA": "🇿🇦", "EGY": "🇪🇬", "NGR": "🇳🇬", "KEN": "🇰🇪", "ETH": "🇪🇹",
    "MAR": "🇲🇦", "ALG": "🇩🇿", "TUN": "🇹🇳", "GHA": "🇬🇭", "CIV": "🇨🇮",
    "SEN": "🇸🇳", "CMR": "🇨🇲", "UGA": "🇺🇬", "ZIM": "🇿🇼", "ZAM": "🇿🇲",
    "ANG": "🇦🇴", "MOZ": "🇲🇿", "TAN": "🇹🇿", "RWA": "🇷🇼", "BDI": "🇧🇮",
    "BEN": "🇧🇯", "BFA": "🇧🇫", "BOT": "🇧🇼", "CAF": "🇨🇫", "CHA": "🇹🇩",
    "COM": "🇰🇲", "CGO": "🇨🇬", "COD": "🇨🇩", "DJI": "🇩🇯", "ERI": "🇪🇷",
    "SWZ": "🇸🇿", "GAB": "🇬🇦", "GAM": "🇬🇲", "GBS": "🇬🇼", "GUI": "🇬🇳",
    "EQG": "🇬🇶", "LES": "🇱🇸", "LBR": "🇱🇷", "LBA": "🇱🇾", "MAD": "🇲🇬",
    "MAW": "🇲🇼", "MLI": "🇲🇱", "MTN": "🇲🇷", "MRI": "🇲🇺", "NAM": "🇳🇦",
    "NIG": "🇳🇪", "STP": "🇸🇹", "SEY": "🇸🇨", "SLE": "🇸🇱", "SOM": "🇸🇴",
    "SSD": "🇸🇸", "SUD": "🇸🇩", "TOG": "🇹🇬", "CPV": "🇨🇻",
    # North America
    "USA": "🇺🇸", "CAN": "🇨🇦", "MEX": "🇲🇽", "CUB": "🇨🇺", "JAM": "🇯🇲",
    "PUR": "🇵🇷", "DOM": "🇩🇴", "HAI": "🇭🇹", "TTO": "🇹🇹", "BAH": "🇧🇸",
    "BAR": "🇧🇧", "GRN": "🇬🇩", "SKN": "🇰🇳", "LCA": "🇱🇨", "VIN": "🇻🇨",
    "ANT": "🇦🇬", "DMA": "🇩🇲", "BIZ": "🇧🇿", "GUA": "🇬🇹", "HON": "🇭🇳",
    "ESA": "🇸🇻", "NCA": "🇳🇮", "CRC": "🇨🇷", "PAN": "🇵🇦", "BER": "🇧🇲",
    "CAY": "🇰🇾", "IVB": "🇻🇬", "ISV": "🇻🇮", "AHO": "🇳🇱", "ARU": "🇦🇼", # AHO was Netherlands Antilles
    # South America
    "BRA": "🇧🇷", "ARG": "🇦🇷", "COL": "🇨🇴", "CHI": "🇨🇱", "PER": "🇵🇪",
    "VEN": "🇻🇪", "ECU": "🇪🇨", "URU": "🇺🇾", "PAR": "🇵🇾", "BOL": "🇧🇴",
    "GUY": "🇬🇾", "SUR": "🇸🇷",
    # Oceania
    "AUS": "🇦🇺", "NZL": "🇳🇿", "FIJ": "🇫🇯", "PNG": "🇵🇬", "SAM": "🇼🇸",
    "TGA": "🇹🇴", "VAN": "🇻🇺", "SOL": "🇸🇧", "FSM": "🇫🇲", "PLW": "🇵🇼",
    "MHL": "🇲🇭", "KIR": "🇰🇮", "NRU": "🇳🇷", "TUV": "🇹🇻", "COK": "🇨🇰",
    "ASA": "🇦🇸", "GUM": "🇬🇺",
}

def get_continent(noc: str) -> str:
    """Get continent for a country code."""
    return CONTINENT_MAP.get(noc, "Other")

def noc_with_flag(noc: str) -> str:
    """Return country code with emoji flag."""
    flag = NOC_FLAGS.get(noc, "")
    return f"{flag} {noc}" if flag else noc

def render_global_filters(
    countries: list,
    sports: list,
    disciplines: list = None,
) -> dict:
    """
    Render global filters in the sidebar.
    
    Returns dict with filter selections:
    - countries: list of selected countries
    - sports: list of selected sports
    - medal_types: list of selected medal types
    - continents: list of selected continents
    """
    st.sidebar.header("🎛️ Filters")
    
    # Continent filter
    all_continents = ["Europe", "Asia", "Africa", "North America", "South America", "Oceania"]
    selected_continents = st.sidebar.multiselect(
        "🌍 Continent",
        options=all_continents,
        default=[],
        help="Filter by continent"
    )
    
    # Filter countries by selected continents
    if selected_continents:
        filtered_countries = [c for c in countries if get_continent(c) in selected_continents]
    else:
        filtered_countries = countries
    
    # Country filter with flags
    selected_countries = st.sidebar.multiselect(
        "🏳️ Country (NOC)",
        options=[noc_with_flag(c) for c in filtered_countries],
        default=[],
        help="Filter by country"
    )
    # Convert back to NOC codes for filtering
    selected_countries = [c.split()[-1] for c in selected_countries]
    
    # Sport filter
    selected_sports = st.sidebar.multiselect(
        "🏃 Sport",
        options=sports,
        default=[],
        help="Filter by sport"
    )
    
    # Medal type checkboxes
    st.sidebar.markdown("**🏅 Medal Type**")
    col1, col2, col3 = st.sidebar.columns(3)
    gold = col1.checkbox("🥇Gold", value=True, help="Gold")
    silver = col2.checkbox("🥈Silver", value=True, help="Silver")
    bronze = col3.checkbox("🥉Bronze", value=True, help="Bronze")
    
    medal_types = []
    if gold:
        medal_types.append("Gold")
    if silver:
        medal_types.append("Silver")
    if bronze:
        medal_types.append("Bronze")
    
    return {
        "countries": selected_countries,
        "sports": selected_sports,
        "medal_types": medal_types,
        "continents": selected_continents,
    }

def apply_filters(df: pd.DataFrame, filters: dict, noc_col: str = "noc") -> pd.DataFrame:
    """Apply global filters to a DataFrame."""
    if df.empty:
        return df
    
    result = df.copy()
    
    # Apply country filter
    if filters["countries"] and noc_col in result.columns:
        result = result[result[noc_col].isin(filters["countries"])]
    
    # Apply continent filter
    if filters["continents"] and noc_col in result.columns:
        result = result[result[noc_col].apply(get_continent).isin(filters["continents"])]
    
    # Apply sport filter
    if filters["sports"]:
        if "discipline" in result.columns:
            result = result[result["discipline"].isin(filters["sports"])]
        elif "sport" in result.columns:
            result = result[result["sport"].isin(filters["sports"])]
    
    # Apply medal type filter
    if filters["medal_types"] and "medal" in result.columns:
        result = result[result["medal"].isin(filters["medal_types"])]
    
    return result
