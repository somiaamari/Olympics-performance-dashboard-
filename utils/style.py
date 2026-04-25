import streamlit as st

def apply_custom_style():
    """Apply clean, professional CSS with excellent readability and hover effects."""

    st.markdown("""
        <style>
    /* ============ PAGE LINK STYLING ONLY ============ */
    
    /* If pages are links/buttons in a container */
    .stButton > button,
    .stRadio > div > label,
    .stCheckbox > div > label,
    div[class*="stPageLink"],
    div[class*="page-"],
    a[class*="page-"] {
        /* Increased spacing between pages */
        margin-bottom: 1.5rem !important;
        margin-top: 0.5rem !important;
        
        /* Bigger padding */
        padding: 2rem 1.75rem !important;
        margin:  1.25rem ;
        /* Make them look like cards */
        border-radius: 10px !important;
        border: 2px solid #e2e8f0 !important;
        background-color: #ffffff !important;
        color: #334155 !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        text-align: left !important;
    }
    
    /* Hover effect - blue background */
    .stButton > button:hover,
    .stRadio > div > label:hover,
    .stCheckbox > div > label:hover,
    div[class*="stPageLink"]:hover,
    div[class*="page-"]:hover,
    a[class*="page-"]:hover {
        background-color: #3b82f6 !important;
        color: #ffffff !important;
        border-color: #3b82f6 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 15px rgba(59, 130, 246, 0.2) !important;
    }
    
    /* Current/active page - white background */
    .stButton > button[aria-pressed="true"],
    .stRadio > div > label[data-testid="stRadioSelected"],
    .stCheckbox > div > label[data-testid="stCheckboxSelected"],
    div[class*="stPageLink"].active,
    div[class*="page-"].active,
    a[class*="page-"].active,
    .active > .stButton > button,
    .active > .stRadio > div > label {
        background-color: #ffffff !important;
        color: #1e40af !important;
        border-color: #3b82f6 !important;
        border-width: 3px !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15) !important;
    }
    
    /* Active page hover */
    .stButton > button[aria-pressed="true"]:hover,
    .stRadio > div > label[data-testid="stRadioSelected"]:hover,
    .stCheckbox > div > label[data-testid="stCheckboxSelected"]:hover,
    div[class*="stPageLink"].active:hover,
    div[class*="page-"].active:hover,
    a[class*="page-"].active:hover {
        background-color: #f0f9ff !important;
        color: #1e40af !important;
        border-color: #1d4ed8 !important;
    }
    
    /* Ensure proper spacing in sidebar too */
    section[data-testid="stSidebar"] .stButton > button,
    section[data-testid="stSidebar"] .stRadio > div > label,
    section[data-testid="stSidebar"] .stCheckbox > div > label {
        margin-bottom: 1rem !important;
        margin-top: 0.5rem !important;
    }
    
    /* Sidebar hover */
    section[data-testid="stSidebar"] .stButton > button:hover,
    section[data-testid="stSidebar"] .stRadio > div > label:hover,
    section[data-testid="stSidebar"] .stCheckbox > div > label:hover {
        background-color: #3b82f6 !important;
        color: #ffffff !important;
    }
    
    /* Sidebar active page */
    section[data-testid="stSidebar"] .stButton > button[aria-pressed="true"],
    section[data-testid="stSidebar"] .stRadio > div > label[data-testid="stRadioSelected"],
    section[data-testid="stSidebar"] .stCheckbox > div > label[data-testid="stCheckboxSelected"] {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border-color: #60a5fa !important;
    }
    
    /* For any container holding multiple page links */
    div[class*="pages"],
    div[class*="navigation"],
    div[class*="menu"] {
        display: flex !important;
        flex-direction: column !important;
        gap: 1rem !important;
        padding: 1rem 0 !important;
    }
        /* ============ MAIN APP BACKGROUND ============ */
        .stApp {
            background-color: #f8fafc !important;
        }
        
        /* ============ MAIN CONTENT AREA ============ */
        .main .block-container {
            background-color: #ffffff !important;
            border-radius: 12px;
            padding: 2rem 2.5rem;
            margin-top: 1rem;
            margin-bottom: 2rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
            border: 1px solid #e2e8f0;
            transition: box-shadow 0.3s ease;
        }
        
        /* ============ MAIN CONTENT TITLES ============ */
        
        /* Main H1 titles - Clean and clear */
        h1 {
            color: #1e40af !important;  /* Professional dark blue */
            font-size: 2.5rem !important;
            font-weight: 700 !important;
            text-align: left;
            margin-bottom: 1.5rem;
            padding-bottom: 0.8rem;
            border-bottom: 2px solid #3b82f6;  /* Subtle accent line */
            background: none !important;
            -webkit-text-fill-color: #1e40af !important;
            text-shadow: none !important;
        }
        
        /* H2 sub-titles - Clear contrast */
        h2 {
            color: #2563eb !important;  /* Bright blue */
            font-size: 1.8rem !important;
            font-weight: 600 !important;
            margin-top: 2rem;
            margin-bottom: 1rem;
            padding-left: 0;
            border-left: none;
        }
        
        /* H3 section titles */
        h3 {
            color: #475569 !important;  /* Neutral gray-blue */
            font-size: 1.4rem !important;
            font-weight: 600 !important;
            margin-top: 1.5rem;
            margin-bottom: 0.8rem;
        }
        
        /* H4 small titles */
        h4 {
            color: #64748b !important;  /* Medium gray */
            font-size: 1.1rem !important;
            font-weight: 500 !important;
            margin-top: 1.2rem;
            margin-bottom: 0.5rem;
        }
        
        /* ============ PAGE SECTION HEADERS ============ */
        
        /* For your specific page titles: Overview, Athlete Performance, etc. */
        .page-title, .section-header {
            color: #1e293b !important;
            background-color: #f1f5f9 !important;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            border-left: 4px solid #3b82f6;
            font-weight: 600;
            margin-bottom: 1.5rem;
            transition: all 0.3s ease;
        }
        
        .page-title:hover, .section-header:hover {
            background-color: #e2e8f0 !important;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
        }
        
        /* ============ TEXT CONTENT ============ */
        
        /* Regular paragraph text */
        p, .stMarkdown p, .stMarkdown {
            color: #334155 !important;
            line-height: 1.6;
            font-size: 1.05rem;
        }
        
        /* Strong/bold text */
        strong, b {
            color: #1e293b !important;
            font-weight: 600;
        }
        
        /* ============ SIDEBAR - CLEAN & PROFESSIONAL ============ */
        
        /* Sidebar container */
        section[data-testid="stSidebar"] {
            background-color: #1e293b !important;
            border-right: 1px solid #334155 !important;
        }
        
        /* Sidebar text - High contrast white */
        section[data-testid="stSidebar"] .stMarkdown,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] div,
        section[data-testid="stSidebar"] span {
            color: #f8fafc !important;
        }
        
        /* Sidebar headers */
        section[data-testid="stSidebar"] h1 {
            color: #ffffff !important;
            font-size: 1.6rem !important;
            border-bottom: 2px solid #60a5fa;
            text-align: center;
            background: none !important;
            -webkit-text-fill-color: #ffffff !important;
            transition: border-color 0.3s ease;
        }
        
        section[data-testid="stSidebar"] h1:hover {
            border-color: #93c5fd;
        }
        
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {
            color: #e2e8f0 !important;
            font-size: 1.2rem !important;
        }
        
        /* Sidebar widget labels */
        section[data-testid="stSidebar"] .stSelectbox label,
        section[data-testid="stSidebar"] .stMultiselect label,
        section[data-testid="stSidebar"] .stSlider label,
        section[data-testid="stSidebar"] .stCheckbox label,
        section[data-testid="stSidebar"] .stRadio label {
            color: #cbd5e1 !important;
            font-weight: 500;
        }
        
        /* Sidebar input fields */
        section[data-testid="stSidebar"] .stSelectbox > div > div,
        section[data-testid="stSidebar"] .stMultiselect > div > div,
        section[data-testid="stSidebar"] .stTextInput > div > div > input,
        section[data-testid="stSidebar"] .stNumberInput > div > div > input {
            background-color: #334155 !important;
            color: #f8fafc !important;
            border: 1px solid #475569 !important;
            border-radius: 6px;
            transition: all 0.2s ease;
        }
        
        section[data-testid="stSidebar"] .stSelectbox > div > div:hover,
        section[data-testid="stSidebar"] .stMultiselect > div > div:hover,
        section[data-testid="stSidebar"] .stTextInput > div > div > input:hover {
            border-color: #60a5fa !important;
            box-shadow: 0 0 0 1px rgba(96, 165, 250, 0.3);
        }
        
        /* ============ WIDGETS IN MAIN CONTENT ============ */
        
        /* Main content widgets - clean and subtle */
        .stSelectbox > div > div,
        .stMultiselect > div > div,
        .stTextInput > div > div > input {
            background-color: #ffffff !important;
            color: #1e293b !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 6px;
            transition: all 0.2s ease;
        }
        
        .stSelectbox > div > div:hover,
        .stMultiselect > div > div:hover,
        .stTextInput > div > div > input:hover {
            border-color: #3b82f6 !important;
            box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
        }
        
        .stSelectbox > div > div:focus,
        .stMultiselect > div > div:focus,
        .stTextInput > div > div > input:focus {
            border-color: #3b82f6 !important;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
        }
        
        /* Main content labels */
        .stSelectbox label,
        .stMultiselect label,
        .stCheckbox label,
        .stRadio label {
            color: #475569 !important;
            font-weight: 500;
            font-size: 0.95rem;
        }
        
        /* ============ BUTTONS ============ */
        
        /* Main content buttons */
        .stButton > button {
            background-color: #3b82f6 !important;
            color: white !important;
            border: none !important;
            border-radius: 6px;
            padding: 0.5rem 1.5rem;
            font-weight: 500;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .stButton > button:hover {
            background-color: #2563eb !important;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        }
        
        .stButton > button:active {
            transform: translateY(0);
        }
        
        /* Sidebar buttons */
        section[data-testid="stSidebar"] .stButton > button {
            background-color: #475569 !important;
            color: white !important;
            transition: all 0.3s ease;
        }
        
        section[data-testid="stSidebar"] .stButton > button:hover {
            background-color: #64748b !important;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(100, 116, 139, 0.3);
        }
        
        /* ============ METRIC CARDS WITH HOVER EFFECTS ============ */
        
        div[data-testid="stMetric"] {
            background: #d6d6d6;
            border-radius: 10px;
            padding: 1.5rem;
            border: 1px solid #e2e8f0;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: default;
            position: relative;
            overflow: hidden;
        }
        
        div[data-testid="stMetric"]:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
            border-color: #3b82f6;
        }
        
        div[data-testid="stMetric"]::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #3b82f6, #60a5fa);
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        
        div[data-testid="stMetric"]:hover::before {
            opacity: 1;
        }
        
        div[data-testid="stMetricLabel"] {
            color: #64748b;
            font-size: 0.85rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.3px;
            transition: color 0.3s ease;
        }
        
        div[data-testid="stMetric"]:hover div[data-testid="stMetricLabel"] {
            color: #475569;
        }
        
        div[data-testid="stMetricValue"] {
            color: #1e40af;
            font-size: 2rem;
            font-weight: 700;
            margin-top: 0.5rem;
            transition: color 0.3s ease;
        }
        
        div[data-testid="stMetric"]:hover div[data-testid="stMetricValue"] {
            color: #1d4ed8;
        }
        
        div[data-testid="stMetricDelta"] {
            font-weight: 600;
            transition: transform 0.3s ease;
        }
        
        div[data-testid="stMetric"]:hover div[data-testid="stMetricDelta"] {
            transform: scale(1.05);
        }
        
        /* ============ CHARTS & TABLES ============ */
        
        .stPlotlyChart {
            background-color: white;
            border-radius: 10px;
            padding: 1rem;
            border: 1px solid #e2e8f0;
            transition: all 0.3s ease;
        }
        
        .stPlotlyChart:hover {
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
            border-color: #cbd5e1;
        }
        
        .stDataFrame {
            border-radius: 8px;
            border: 1px solid #e2e8f0;
            overflow: hidden;
            transition: all 0.3s ease;
        }
        
        .stDataFrame:hover {
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        }
        
        /* ============ ALERTS ============ */
        
        .stAlert, 
        div[data-testid="stSuccess"],
        div[data-testid="stWarning"],
        div[data-testid="stError"],
        div[data-testid="stInfo"] {
            border-radius: 8px;
            border-left: 4px solid;
            transition: all 0.3s ease;
        }
        
        .stAlert:hover,
        div[data-testid="stSuccess"]:hover,
        div[data-testid="stWarning"]:hover,
        div[data-testid="stError"]:hover,
        div[data-testid="stInfo"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        }
        
        /* ============ EXPANDERS ============ */
        
        .streamlit-expanderHeader {
            background-color: #f8fafc;
            border-radius: 6px;
            border: 1px solid #e2e8f0;
            font-weight: 500;
            color: #475569;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .streamlit-expanderHeader:hover {
            background-color: #f1f5f9;
            border-color: #3b82f6;
            color: #1e40af;
        }
        
        .streamlit-expanderContent {
            background-color: #ffffff;
            border-radius: 0 0 6px 6px;
            border: 1px solid #e2e8f0;
            border-top: none;
        }
        
        /* ============ DIVIDERS ============ */
        
        hr {
            border: none;
            height: 1px;
            background-color: #e2e8f0;
            margin: 1.5rem 0;
            transition: all 0.3s ease;
        }
        
        hr:hover {
            background-color: #cbd5e1;
            height: 2px;
        }
        
        /* ============ LINKS ============ */
        
        a {
            color: #2563eb !important;
            text-decoration: none;
            font-weight: 500;
            transition: all 0.2s ease;
            position: relative;
            padding-bottom: 2px;
        }
        
        a:hover {
            color: #1d4ed8 !important;
        }
        
        a::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 0;
            height: 2px;
            background-color: #3b82f6;
            transition: width 0.3s ease;
        }
        
        a:hover::after {
            width: 100%;
        }
        
        /* Sidebar links */
        section[data-testid="stSidebar"] a {
            color: #60a5fa !important;
        }
        
        section[data-testid="stSidebar"] a:hover {
            color: #93c5fd !important;
        }
        
        /* ============ FOCUS STATES ============ */
        
        *:focus {
            outline: 2px solid #3b82f6;
            outline-offset: 2px;
            border-radius: 4px;
        }
        
        /* ============ CODE & PRE ============ */
        
        code {
            background-color: #f1f5f9;
            color: #1e293b;
            padding: 0.2rem 0.4rem;
            border-radius: 4px;
            font-family: 'SF Mono', Monaco, 'Cascadia Code', monospace;
            font-size: 0.9em;
            border: 1px solid #e2e8f0;
            transition: all 0.3s ease;
        }
        
        code:hover {
            background-color: #e2e8f0;
            border-color: #cbd5e1;
        }
        
        pre {
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 1rem;
            transition: all 0.3s ease;
        }
        
        pre:hover {
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        }
        
        /* ============ SPECIFIC FOR YOUR PAGE TITLES ============ */
        
        /* If you have specific containers for your section titles */
        div[class*="overview"],
        div[class*="performance"],
        div[class*="analysis"],
        div[class*="sports"] {
            background-color: transparent !important;
        }
        
        /* Make sure any colored backgrounds on text are removed */
        * {
            background-image: none !important;
        }
        
        /* Remove any text gradients that might be causing brightness issues */
        h1, h2, h3, h4, h5, h6 {
            background: none !important;
            -webkit-background-clip: unset !important;
            -webkit-text-fill-color: unset !important;
            text-shadow: none !important;
        }
        
        /* Force clean colors for your specific titles */
        .stTitle h1,
        .stTitle h2,
        .stTitle h3 {
            color: #1e40af !important;
            background: none !important;
        }
        
        /* ============ CUSTOM CARD HOVER ANIMATIONS ============ */
        
        @keyframes cardHover {
            0% { transform: translateY(0); }
            50% { transform: translateY(-3px); }
            100% { transform: translateY(-5px); }
        }
        
        div[data-testid="stMetric"]:hover {
            animation: cardHover 0.3s ease-out;
        }
        
        </style>
    """, unsafe_allow_html=True)

