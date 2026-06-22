import streamlit as st
import pandas as pd
import io
import matplotlib.pyplot as plt
import networkx as nx

# ==========================================
# PAGE CONFIG & THEME INITIALIZATION
# ==========================================
st.set_page_config(
    page_title="Digital Government Services Analytics",
    page_icon="(●'◡'●)",
    layout="wide",
    initial_sidebar_state="collapsed" # Collapsed by default for clean top-nav layout
)

# Initialize Session State for Page Navigation if it doesn't exist
if "current_page" not in st.session_state:
    st.session_state.current_page = "Overview Dashboard"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght=300;400;500;600;700;800;900&family=Space+Grotesk:wght=400;500;600;700&display=swap');

/* ================================
    ROOT TOKENS (LIGHT THEME)
================================ */
:root {
    --bg-base:        #FFFFFF;
    --bg-surface:     #F8FAFC;
    --bg-elevated:    #F1F5F9;
    --bg-card:        #FFFFFF;
    --border-subtle:  #E2E8F0;
    --border-glow:    rgba(59, 130, 246, 0.2);
    --accent-blue:    #2563EB;
    --accent-cyan:    #0891B2;
    --accent-violet:  #7C3AED;
    --text-primary:   #0F172A;
    --text-muted:     #475569;
    --text-dim:       #64748B;
    --success:        #10B981;
    --warning:        #F59E0B;
    --danger:         #EF4444;
}

/* ================================
    GLOBAL RESET
================================ */
* { box-sizing: border-box; padding: 0; margin: 0;}

.stApp {
    background: var(--bg-base) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif;
}

/* Hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }

/* Hide default sidebar altogether to shift focus to Top-Nav */
section[data-testid="stSidebar"] {
    display: none !important;
}

/* ================================
    MODERN LIGHT TOP-BAR NAVIGATION
================================ */
.top-navbar {
    background: #FFFFFF;
    border-bottom: 1px solid var(--border-subtle);
    border-radius: 12px;
    margin:0;
    padding: 0px 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05), 0 1px 2px rgba(0, 0, 0, 0.03);
}

.nav-brand {
    display: flex;
    align-items: center;
    gap: 12px;
}

.brand-icon {
    width: 36px;
    height: 36px;
    background: linear-gradient(135deg, #2563EB, #0891B2);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    color: #FFFFFF;
}

.brand-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 18px;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: -0.01em;
}

.brand-subtitle {
    font-size: 10px;
    color: var(--text-dim);
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* Custom CSS to style ALL base navigation buttons */
div[data-testid="stHorizontalBlock"] button {
    font-size: 14px !important;
    padding: 6px 12px !important;
    transition: all 0.2s ease !important;
}

/* Inactive Nav Tabs (Secondary Buttons) */
div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] button[background-color="transparent"] ,
div[data-testid="stHorizontalBlock"] button[kind="secondary"] {
    background-color: transparent !important;
    border: none !important;
    color: var(--text-muted) !important;
    font-weight: 500 !important;
}

div[data-testid="stHorizontalBlock"] button[kind="secondary"]:hover {
    color: var(--accent-blue) !important;
    background-color: #F1F5F9 !important;
}

/* Active Highlighted Nav Tab (Primary Buttons) */
div[data-testid="stHorizontalBlock"] button[kind="primary"] {
    background-color: #2563EB !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 8px !important;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25) !important;
}

/* ================================
    METRIC CARDS — CLEAN WHITE
================================ */
.metric-card {
    background: #FFFFFF;
    border: 1px solid var(--border-subtle);
    border-radius: 16px;
    padding: 24px 20px;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}

.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.1);
    border-color: #BFDBFE;
}

.metric-title {
    font-size: 10px;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    font-weight: 700;
    color: var(--text-dim);
    margin-bottom: 8px;
}

.metric-value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 38px;
    font-weight: 800;
    background: linear-gradient(135deg, #1E40AF, #0369A1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    margin-bottom: 6px;
}

.metric-tag {
    font-size: 11px;
    color: var(--text-muted);
    font-weight: 500;
}

/* ================================
    SECTION CARDS
================================ */
.dashboard-section {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}

/* ================================
    PAGE HEADER CHIPS
================================ */
.page-eyebrow {
    display: inline-block;
    background: rgba(37, 99, 235, 0.08);
    border: 1px solid rgba(37, 99, 235, 0.15);
    border-radius: 999px;
    padding: 4px 12px;
    font-size: 11px;
    letter-spacing: 0.10em;
    text-transform: uppercase;
    color: #2563EB;
    font-weight: 700;
    margin-bottom: 8px;
}

.page-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 26px;
    font-weight: 800;
    color: var(--text-primary);
    margin: 0 0 6px 0;
    letter-spacing: -0.02em;
}

.page-subtitle {
    font-size: 14px;
    color: var(--text-muted);
    margin-bottom: 24px;
    font-weight: 400;
    max-width: 600px;
}

/* ================================
    SECTION LABELS
================================ */
.section-label {
    font-size: 11px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    font-weight: 700;
    color: var(--text-dim);
    margin-bottom: 4px;
}

.section-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 16px;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0 0 16px 0;
}

/* ================================
    DATAFRAME — LIGHT TABLE OVERRIDE
================================ */
div[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    overflow: hidden;
    border: 1px solid var(--border-subtle) !important;
}

/* ================================
    DOWNLOAD BUTTON (SPECIFICITY ENHANCED FIX)
================================ */
div[data-testid="stAppViewBlock"] .stDownloadButton > button,
div.stDownloadButton > button {
    background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    padding: 0.55rem 1.2rem !important;
    transition: all 0.2s ease !important;
    box-shadow: none !important;
}

div[data-testid="stAppViewBlock"] .stDownloadButton > button:hover,
div.stDownloadButton > button:hover {
    transform: translateY(-1px) !important;
    color: #FFFFFF !important;
    box-shadow: 0 8px 20px rgba(37, 99, 235, 0.25) !important;
}

/* ================================
    TABS
================================ */
.stTabs [data-baseweb="tab-list"] {
    background: #F1F5F9 !important;
    border-radius: 10px !important;
    padding: 4px !important;
    gap: 4px !important;
    border: 1px solid var(--border-subtle) !important;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 7px !important;
    padding: 6px 16px !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    color: var(--text-muted) !important;
    background: transparent !important;
    transition: all 0.2s ease !important;
}

.stTabs [aria-selected="true"] {
    background: #FFFFFF !important;
    color: #2563EB !important;
    box-shadow: 0 2px 6px rgba(0,0,0,0.06) !important;
}

/* ================================
    RULE CARD (green/red)
================================ */
.rule-card-green {
    background: #F0FDF4;
    border: 1px solid #BBF7D0;
    border-top: 3px solid #16A34A;
    border-radius: 14px;
    padding: 20px;
}

.rule-card-red {
    background: #FEF2F2;
    border: 1px solid #FEE2E2;
    border-top: 3px solid #DC2626;
    border-radius: 14px;
    padding: 20px;
}

.rule-card-title-green {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 15px;
    font-weight: 700;
    color: #15803D;
    margin: 0 0 10px 0;
}

.rule-card-title-red {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 15px;
    font-weight: 700;
    color: #B91C1C;
    margin: 0 0 10px 0;
}

.rule-card-body {
    font-size: 13px;
    color: var(--text-muted);
    line-height: 1.6;
    margin-bottom: 12px;
}

.rule-card-list {
    font-size: 13px;
    color: var(--text-primary);
    line-height: 1.8;
    padding-left: 18px;
}

.rule-card-footer-green {
    font-size: 11.5px;
    color: #16A34A;
    font-weight: 600;
    margin-top: 14px;
    padding-top: 10px;
    border-top: 1px solid #E2E8F0;
}

.rule-card-footer-red {
    font-size: 11.5px;
    color: #DC2626;
    font-weight: 600;
    margin-top: 14px;
    padding-top: 10px;
    border-top: 1px solid #E2E8F0;
}

/* ================================
    EXPORT CARD
================================ */
.export-card {
    background: #FFFFFF;
    border: 1px solid var(--border-subtle);
    border-radius: 14px;
    padding: 24px 20px;
    text-align: center;
    transition: border-color 0.2s ease;
  
}

.export-card:hover {
    border-color: #BFDBFE;
    
}

.export-icon {
    font-size: 28px;
    margin-bottom: 8px;
}

.export-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 15px;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 6px;
}

.export-desc {
    font-size: 12px;
    color: var(--text-dim);
    margin-bottom: 14px;
}

/* ================================
    DIVIDER
================================ */
hr {
    border: none !important;
    border-top: 1px solid var(--border-subtle) !important;
    margin: 20px 0 !important;
}

/* ================================
    SCROLL BAR
================================ */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-base); }
::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: #94A3B8; }

</style>
""", unsafe_allow_html=True)

# ==========================================
# DATA LOADING ENGINE
# ==========================================
@st.cache_data
def load_and_preprocess_data():
    total_respondents = 3502
    
    freq_data = [
        ("National ID & Civil Registration", 1949, 55.65),
        ("Digital Electricity Billing Systems", 1891, 54.00),
        ("Digital Water Monitoring Systems", 1869, 53.37),
        ("Water Monitoring Systems", 1850, 52.83),
        ("Public Transport Tracking Systems", 1822, 52.03),
        ("Online Learning Platforms", 1749, 49.94),
        ("Student Information Systems", 1727, 49.31),
        ("Mobile Money Fare Payment Systems", 1719, 49.09),
        ("Smart Electricity Billing Systems", 1708, 48.77),
        ("Digital Examination Systems", 1613, 46.06),
        ("Digital Waste Management Systems", 1574, 44.95),
        ("Passport & Immigration Services", 1558, 44.49),
        ("Tax Payment Systems", 1525, 43.55),
        ("Learning Management Systems (LMS)", 1519, 43.38),
        ("Traffic Management Systems", 1501, 42.86),
        ("Smart Waste Management Systems", 1486, 42.43),
        ("Business Registration & Licensing", 1371, 39.15),
        ("Teacher Training Platforms", 1211, 34.58),
        ("Infrastructure Fault Reporting Systems", 1187, 33.89),
        ("Public Complaints & Feedback Systems", 1171, 33.44),
        ("Social Protection Services", 1131, 32.30),
        ("Infrastructure Fault Reporting Platforms", 1117, 31.90),
        ("Land Registration & Property Records", 1093, 31.21),
        ("Road Condition Reporting Systems", 1036, 29.58),
        ("Ride-Hailing Applications", 1032, 29.47),
        ("Court & Legal Services", 716, 20.45),
        ("Municipal Services", 605, 17.30),
    ]
    
    freq_table = pd.DataFrame(freq_data, columns=["Service", "Frequency", "Percentage"])
    
    rules_data = [
        ("Digital Electricity Billing Systems", "Smart Electricity Billing Systems", 0.54, 0.49, 0.44, 0.81, 1.66),
        ("Smart Electricity Billing Systems", "Digital Electricity Billing Systems", 0.49, 0.54, 0.44, 0.90, 1.66),
        ("Digital Water Monitoring Systems", "Water Monitoring Systems", 0.53, 0.53, 0.42, 0.79, 1.49),
        ("Water Monitoring Systems", "Digital Water Monitoring Systems", 0.53, 0.53, 0.42, 0.79, 1.49),
        ("Digital Electricity Billing Systems", "Digital Water Monitoring Systems", 0.54, 0.53, 0.38, 0.70, 1.31),
        ("Digital Water Monitoring Systems", "Digital Electricity Billing Systems", 0.53, 0.54, 0.38, 0.71, 1.31),
        ("National ID & Civil Registration", "Passport & Immigration Services", 0.56, 0.44, 0.35, 0.63, 1.43),
        ("Passport & Immigration Services", "National ID & Civil Registration", 0.44, 0.56, 0.35, 0.80, 1.43),
        ("Online Learning Platforms", "Student Information Systems", 0.50, 0.49, 0.36, 0.72, 1.47),
        ("Student Information Systems", "Online Learning Platforms", 0.49, 0.50, 0.36, 0.73, 1.47)
    ]
    
    rules_df = pd.DataFrame(rules_data, columns=[
        "Antecedents", "Consequents", "Antecedent Support", "Consequent Support", "Support", "Confidence", "Lift"
    ])
    
    return total_respondents, freq_table, rules_df

total_respondents, freq_table, rules_df = load_and_preprocess_data()

# ==========================================
# WEBSITE TOP NAVIGATION HEADER BAR WITH LINKS
# ==========================================

# Create a master layout split: 35% Left side for Brand Header, 65% Right side for Navigation Items
header_left, header_right = st.columns([35, 65], vertical_alignment="center")

with header_left:
    st.markdown("""
    <div class="top-navbar" style="border-bottom: none; box-shadow: none; padding: 0;">
        <div class="nav-brand">
            <div class="brand-icon">M</div>
            <div>
                <div class="brand-title" style="white-space: nowrap;">Mining Patterns in Citizen Demand</div>
                <div class="brand-subtitle">Analytic Dashboard</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with header_right:
    # Generate horizontal sub-columns for each navigation element inside the right alignment block
    nav_items = ["Overview", "Frequency", "Association Rules", "Network", "Export"]
    nav_cols = st.columns(len(nav_items))
    
    for index, item in enumerate(nav_items):
        with nav_cols[index]:
            # Evaluates true if partial text aligns cleanly with active session state value
            is_active = item in st.session_state.current_page
            
            button_type = "primary" if is_active else "secondary"
            
            if st.button(item, key=f"nav_link_{index}", use_container_width=True, type=button_type):
                full_page_names = {
                    "Overview": "Overview Dashboard",
                    "Frequency": "Frequency Analysis",
                    "Association Rules": "Association Rules",
                    "Network": "Network Graph",
                    "Export": "Export Report"
                }
                st.session_state.current_page = full_page_names[item]
                st.rerun()

# Thin visual divider line across the web page layout
st.markdown("""<div style="height:1px; background:#E2E8F0; margin-top:12px; margin-bottom:28px;"></div>""", unsafe_allow_html=True)

# Map the active structural page selection parameter
page = st.session_state.current_page


# ==========================================
# MATPLOTLIB LIGHT THEME HELPER
# ==========================================
def apply_light_theme(fig, ax):
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#F8FAFC')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('#CBD5E1')
    ax.spines['left'].set_color('#CBD5E1')
    ax.tick_params(axis='both', colors='#475569', labelsize=10)
    ax.xaxis.label.set_color('#475569')
    ax.yaxis.label.set_color('#475569')
    ax.title.set_color('#0F172A')
    ax.grid(axis="x", linestyle="--", alpha=0.5, color='#E2E8F0')

# ==========================================
# PAGE 1: OVERVIEW DASHBOARD
# ==========================================
if page == "Overview Dashboard":
    st.markdown("""
        <div class="page-eyebrow">Overview</div>
        <h1 class="page-title">Overview Dashboard</h1>
        <p class="page-subtitle">High-level metrics and prioritization indices of citizen demand for digital government transformation.</p>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Total Respondents</div>
                <div class="metric-value">{total_respondents:,}</div>
                <div class="metric-tag">Survey participants</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Services Analyzed</div>
                <div class="metric-value">{len(freq_table)}</div>
                <div class="metric-tag">Digital service categories</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Peak Demand</div>
                <div class="metric-value">{freq_table.iloc[0]['Percentage']}%</div>
                <div class="metric-tag">{freq_table.iloc[0]['Service'][:28]}…</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
        <div class="dashboard-section">
            <div class="section-label">Prioritization Agenda</div>
            <div class="section-title">Top 5 Most Demanded Services</div>
    """, unsafe_allow_html=True)
    top_5 = freq_table.head(5).copy()
    top_5.index = range(1, 6)
    st.dataframe(top_5, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# PAGE 2: FREQUENCY ANALYSIS
# ==========================================
elif page == "Frequency Analysis":
    st.markdown("""
        <div class="page-eyebrow">Analysis</div>
        <h1 class="page-title">Frequency & Proportion Analysis</h1>
        <p class="page-subtitle">Empirical distribution metrics sorted by citizen selection parameters.</p>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Demand Visualization", "Complete Data Table"])
    
    with tab1:
        sorted_freq = freq_table.sort_values(by="Frequency", ascending=True)
        
        fig, ax = plt.subplots(figsize=(14, 10))
        apply_light_theme(fig, ax)
        
        colors = [f'#3B82F6' for _ in range(len(sorted_freq))]
        
        bars = ax.barh(sorted_freq["Service"], sorted_freq["Frequency"], 
                       color=colors, height=0.62, edgecolor='none')
        
        ax.set_xlabel("Number of Respondents (Frequency)", fontsize=12, labelpad=14, fontweight='600')
        ax.set_title("Citizen Demand for Digital Government Services", fontsize=15, pad=20, fontweight='800')
        
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 12, bar.get_y() + bar.get_height()/2, f'{int(width):,}', 
                    va='center', ha='left', fontsize=9.5, color='#475569', fontweight='600')
        
        ax.tick_params(axis='y', labelsize=9.5)
        plt.tight_layout()
        st.pyplot(fig)
        
    with tab2:
        st.dataframe(freq_table.style.format({"Percentage": "{:.2f}%"}), use_container_width=True)

# ==========================================
# PAGE 3: ASSOCIATION RULES
# ==========================================
elif page == "Association Rules":
    st.markdown("""
        <div class="page-eyebrow">Intelligence</div>
        <h1 class="page-title">Smart Service Connections & Predictions</h1>
        <p class="page-subtitle">Discovering connected citizen trends to predict strategic next steps for government platform deployment.</p>
    """, unsafe_allow_html=True)
    
    col_param1, col_param2 = st.columns(2)
    with col_param1:
        min_lift = st.slider("Connection Strength (Minimum Lift)", min_value=1.0, max_value=2.0, value=1.2, step=0.05)
    with col_param2:
        min_conf = st.slider("Certainty Level (Minimum Confidence %)", min_value=40, max_value=100, value=50, step=5)
        
    filtered_rules = rules_df[
        (rules_df["Lift"] >= min_lift) & 
        ((rules_df["Confidence"] * 100) >= min_conf)
    ].sort_values(by=["Lift", "Confidence"], ascending=False)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <div class="dashboard-section">
            <div class="section-label">Connection Map</div>
            <div class="section-title">How Services Connect</div>
            <p style="font-size:13px; color:#475569; margin-bottom:18px; margin-top:-8px;">
                When citizens select Service A, how likely are they to also want Service B?
            </p>
    """, unsafe_allow_html=True)
    
    simple_table_data = []
    for idx, row in filtered_rules.iterrows():
        simple_table_data.append({
            "If They Want This (A)": row["Antecedents"],
            "They Also Want This (B)": row["Consequents"],
            "Confidence Match": f"{row['Confidence']*100:.0f}%",
            "Connection Strength": f"{row['Lift']:.2f}×"
        })
    
    if simple_table_data:
        st.dataframe(pd.DataFrame(simple_table_data), use_container_width=True, hide_index=True)
    else:
        st.warning("No connections found matching your current filter settings. Try lowering the sliders!")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
        <div style="margin-top:32px; margin-bottom:16px;">
            <div class="section-label">Strategic Intelligence</div>
            <div class="section-title">Data-Driven Decision Predictions</div>
        </div>
    """, unsafe_allow_html=True)
    
    top_rule_1 = rules_df.iloc[1]
    top_rule_2 = rules_df.iloc[2]
    top_rule_3 = rules_df.iloc[7]
    
    col_dec1, col_dec2 = st.columns(2)
    
    with col_dec1:
        st.markdown(f"""
        <div class="rule-card-green">
            <div class="rule-card-title-green">Best Systems to Launch Next</div>
            <p class="rule-card-body">Based on the data rules, these combinations carry the strongest predictive affinity. Developing them together ensures seamless citizen experience and high adoption:</p>
            <ul class="rule-card-list">
                <li><b>{top_rule_1['Antecedents']} → {top_rule_1['Consequents']}</b><br>
                    <span style="color:#16A34A; font-size:12px; font-weight:600;">{top_rule_1['Confidence']*100:.0f}% certainty</span> — Highest connection pattern in the study.</li>
                <li><b>{top_rule_2['Antecedents']} → {top_rule_2['Consequents']}</b><br>
                    <span style="color:#16A34A; font-size:12px; font-weight:600;">{top_rule_2['Confidence']*100:.0f}% certainty</span> — Citizens want unified natural resource portals.</li>
                <li><b>{top_rule_3['Antecedents']} → {top_rule_3['Consequents']}</b><br>
                    <span style="color:#16A34A; font-size:12px; font-weight:600;">{top_rule_3['Confidence']*100:.0f}% certainty</span> — Core credential link; immigration requires base registry.</li>
            </ul>
            <div class="rule-card-footer-green">Strategy: Group these into synchronous rollout packages.</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_dec2:
        st.markdown(f"""
        <div class="rule-card-red">
            <div class="rule-card-title-red">Least Requested / Split Restrictions</div>
            <p class="rule-card-body">These configurations represent the lowest isolated priority tracks or conditional dependencies before development investment:</p>
            <ul class="rule-card-list">
                <li><b>{freq_table.iloc[-1]['Service']}</b><br>
                    <span style="color:#DC2626; font-size:12px; font-weight:600;">{freq_table.iloc[-1]['Percentage']}% demand</span> — Absolute lowest frequency. Avoid starting here.</li>
                <li><b>{freq_table.iloc[-2]['Service']}</b><br>
                    <span style="color:#DC2626; font-size:12px; font-weight:600;">{freq_table.iloc[-2]['Percentage']}% demand</span> — Second lowest standalone element.</li>
                <li><b>Isolated {top_rule_1['Antecedents']} Sprints</b><br>
                    <span style="color:#DC2626; font-size:12px; font-weight:600;">Ecosystem dependency</span> — Standalone builds drop utility without {top_rule_1['Consequents']}.</li>
            </ul>
            <div class="rule-card-footer-red">Precaution: Delay standalone investments to focus resources effectively.</div>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# PAGE 4: NETWORK GRAPH
# ==========================================
elif page == "Network Graph":
    st.markdown("""
        <div class="page-eyebrow">Graph Analysis</div>
        <h1 class="page-title">Cross-Service Dependency Network</h1>
        <p class="page-subtitle">Spatial visualization mapping lift weights between linked digital governance clusters.</p>
    """, unsafe_allow_html=True)
    
    G = nx.DiGraph()
    for _, row in rules_df.iterrows():
        G.add_edge(row["Antecedents"], row["Consequents"], weight=float(row["Lift"]))
        
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#F8FAFC')
    
    pos = nx.spring_layout(G, k=1.4, seed=42)
    
    nx.draw_networkx_nodes(G, pos, node_color="#E2E8F0", node_size=2000, 
                           edgecolors="#2563EB", linewidths=2.0, ax=ax)
    
    edges = G.edges(data=True)
    weights = [edge[2]['weight'] for edge in edges]
    max_w = max(weights) if weights else 1
    scaled_widths = [((w / max_w) * 3.5) for w in weights]
    
    nx.draw_networkx_edges(G, pos, width=scaled_widths, edge_color="#94A3B8", 
                           arrows=True, arrowsize=18, connectionstyle="arc3,rad=0.15", ax=ax)
    
    clean_labels = {}
    for node in G.nodes():
        words = node.split(" ")
        if len(words) > 2:
            clean_labels[node] = "\n".join([" ".join(words[:2]), " ".join(words[2:])])
        else:
            clean_labels[node] = node
            
    nx.draw_networkx_labels(G, pos, labels=clean_labels, font_size=8.5, 
                            font_family="sans-serif", font_color="#0F172A", 
                            font_weight='bold', ax=ax)
    
    plt.axis('off')
    plt.tight_layout()
    st.pyplot(fig)
    st.caption("💡 Edge thickness corresponds proportionally to the relationship strength (Lift metric score between service items).")

# ==========================================
# PAGE 5: EXPORT REPORT
# ==========================================
elif page == "Export Report":
    st.markdown("""
        <div class="page-eyebrow">Export</div>
        <h1 class="page-title">Export Report Interface</h1>
        <p class="page-subtitle">Download thesis-grade data assets formatted to academic defense distribution specifications.</p>
    """, unsafe_allow_html=True)
    
    def create_excel_download(dataframe, sheet_name):
        output = io.BytesIO()
        with pd.ExcelWriter(output) as writer:
            dataframe.to_excel(writer, index=False, sheet_name=sheet_name)
        return output.getvalue()

    st.markdown("""
        <div class="dashboard-section">
            <div class="section-label">Asset Packages</div>
            <div class="section-title">Select Download Package</div>
    """, unsafe_allow_html=True)
    
    c_exp1, c_exp2 = st.columns(2)
    
    with c_exp1:
        st.markdown("""
            <div class="export-card">
                <div class="export-title">Frequency Table</div>
                <div class="export-desc">Service demand frequencies and percentage distributions across all categories.</div>
            </div>
        """, unsafe_allow_html=True)
        freq_excel = create_excel_download(freq_table, "Frequency_Metrics")
        st.download_button(
            label="Download Frequency Excel",
            data=freq_excel,
            file_name="Frequency_Analysis_Report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
        
    with c_exp2:
        st.markdown("""
            <div class="export-card">
                <div class="export-title">Association Rules</div>
                <div class="export-desc">Full rule set with support, confidence and lift metrics for each service pair.</div>
            </div>
        """, unsafe_allow_html=True)
        rules_excel = create_excel_download(rules_df, "Association_Rules")
        st.download_button(
            label="Download Rules Excel",
            data=rules_excel,
            file_name="Association_Rules_Report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    st.markdown("</div>", unsafe_allow_html=True)