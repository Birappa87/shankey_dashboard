import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

VALID_USERNAME = st.secrets["credentials"]["username"]
VALID_PASSWORD = st.secrets["credentials"]["password"]

st.set_page_config(page_title="Saudi Statistics Dashboard", page_icon="📊", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
* { font-family: 'Poppins', sans-serif; }
[data-testid="stAppViewContainer"] { background: radial-gradient(circle at top left, #0e1117, #0a0c10); color: #f1f3f5; }
[data-testid="stSidebar"] { background-color: #161a23; border-right: 1px solid #20242f; }
h1, h2, h3, h4, h5 { color: #e8ecf2; font-weight: 600; letter-spacing: -0.4px; }
hr { border: none; height: 1px; background: linear-gradient(90deg, #1f77b4, #00bfff); margin: 1.5rem 0; }
.metric-card { background: linear-gradient(145deg, #1a1d29, #151823); border-radius: 16px; padding: 1.5rem; border: 1px solid #222633; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3); text-align: center; }
.metric-label { color: #a6abb5; font-size: 0.9rem; }
.metric-value { color: #66b3ff; font-size: 1.8rem; font-weight: 700; }
div.stButton > button { background: linear-gradient(90deg, #1f77b4, #3fa0ff); color: white; border-radius: 8px; border: none; padding: 0.6rem 1.2rem; font-weight: 600; transition: all 0.3s ease; }
div.stButton > button:hover { background: linear-gradient(90deg, #3fa0ff, #1f77b4); transform: translateY(-2px); box-shadow: 0 4px 12px rgba(31, 119, 180, 0.4); }
[data-testid="stTabs"] button { background-color: transparent; border-radius: 50px; border: 1px solid #2c2f38; color: #cfd3da; margin-right: 0.4rem; padding: 0.4rem 1rem; font-weight: 500; }
[data-testid="stTabs"] button[aria-selected="true"] { background: linear-gradient(90deg, #1f77b4, #00bfff); color: white !important; box-shadow: 0 0 10px rgba(31,119,180,0.6); }
.js-plotly-plot .plotly { background-color: #0e1117 !important; }
.login-card { background: rgba(22, 26, 35, 0.8); padding: 2rem; border-radius: 16px; border: 1px solid #2a2e38; box-shadow: 0 8px 24px rgba(0,0,0,0.4); backdrop-filter: blur(6px); width: 350px; margin: auto; }
</style>
""", unsafe_allow_html=True)

def authenticate_user():
    """User authentication using Streamlit secrets."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if not st.session_state.authenticated:
        st.markdown("<h2 style='text-align:center;'>📊 Saudi Statistics Dashboard</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;color:#a6abb5;'>General Authority for Statistics – Saudi Arabia</p>", unsafe_allow_html=True)
        with st.form("login_form"):
            st.markdown("<div class='login-card'>", unsafe_allow_html=True)
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        if submitted:
            if username == VALID_USERNAME and password == VALID_PASSWORD:
                st.session_state.authenticated = True
                st.success("✅ Login successful")
                st.rerun()
            else:
                st.error("❌ Invalid username or password")
        st.stop()

@st.cache_data(show_spinner="Loading data...")
def load_data():
    """Load cleaned import, export, and SUT/IO data."""
    imports = pd.read_csv("cleaned_data/cleaned_imports.csv")
    exports = pd.read_csv("cleaned_data/cleaned_exports.csv")
    sut_io = pd.read_csv("cleaned_data/sut_io_cleaned_data.csv")
    return imports, exports, sut_io

def display_header():
    """Display page header with logo and title."""
    col1, col2 = st.columns([1, 5])
    with col1:
        st.image("logo.png", width=90)
    with col2:
        st.markdown("""
            <div style='padding-top:10px;'>
                <h2 style='margin:0; color:#00bfff;'>General Authority for Statistics</h2>
                <p style='margin:0; color:#cfd3da;'>Kingdom of Saudi Arabia</p>
            </div>
        """, unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

def create_bar_chart(df, title, value_column="2024"):
    """Create Plotly bar chart for top commodities."""
    if df.empty:
        return None
    chart_df = df.nlargest(15, value_column)
    fig = px.bar(chart_df, x="COMM_NAME_EN", y=value_column, color=value_column,
                 title=title, color_continuous_scale="Blues",
                 labels={"COMM_NAME_EN": "Commodity", value_column: "Value (SAR)"})
    fig.update_layout(template="plotly_dark", height=500,
                      title_font=dict(size=18, color="#e8ecf2"),
                      margin=dict(l=20, r=20, t=50, b=80), showlegend=False)
    fig.update_traces(hovertemplate="<b>%{x}</b><br>Value: %{y:,.0f} SAR<extra></extra>")
    return fig

def create_sankey_diagram(selected_sector, imports_total, exports_total, total_intermediate, final_consumption, total_output):
    """Create Sankey diagram for economic flow visualization."""
    nodes = [
        f"Imports<br>{imports_total:,.0f}", f"{selected_sector}",
        f"Exports<br>{exports_total:,.0f}", f"Intermediate<br>{total_intermediate:,.0f}",
        f"Final<br>{final_consumption:,.0f}", f"Output<br>{total_output:,.0f}"
    ]
    links = [
        dict(source=0, target=1, value=imports_total),
        dict(source=1, target=2, value=exports_total),
        dict(source=1, target=3, value=total_intermediate),
        dict(source=1, target=4, value=final_consumption),
        dict(source=1, target=5, value=total_output)
    ]
    fig = go.Figure(data=[go.Sankey(
        arrangement="snap",
        node=dict(pad=25, thickness=20, line=dict(color="rgba(255,255,255,0.1)", width=0.5),
                  label=nodes, color=["#1f77b4", "#2ca02c", "#ff7f0e", "#9467bd", "#8c564b", "#17becf"]),
        link=dict(source=[l["source"] for l in links],
                  target=[l["target"] for l in links],
                  value=[l["value"] for l in links],
                  color="rgba(100,100,100,0.3)")
    )])
    fig.update_layout(template="plotly_dark", title=f"💫 Economic Flow — {selected_sector}",
                      font_size=11, height=650, margin=dict(l=10, r=10, t=50, b=10))
    return fig

def main():
    """Main dashboard logic and layout."""
    authenticate_user()
    imports, exports, sut_io = load_data()
    display_header()
    st.sidebar.header("📁 Dashboard Filters")
    sectors = sorted(set(imports["CC_DESC_EN"].dropna()) | set(exports["CC_DESC_EN"].dropna()))
    selected_sector = st.sidebar.selectbox("Select Sector", sectors)

    imp_df = imports[imports["CC_DESC_EN"] == selected_sector]
    exp_df = exports[exports["CC_DESC_EN"] == selected_sector]
    sut_df = sut_io[sut_io["Input-Output Tables (IOTs) 2018 (Thousands of Saudi riyals) - Economic Activities (ISIC Rev. 4)"]
                    .astype(str).str.contains(selected_sector, case=False, na=False)]
    try:
        total_intermediate = sut_df["Total Intermediate Demand"].astype(float).sum()
        final_consumption = sut_df["Final consumption expenditures"].astype(float).sum()
        total_output = sut_df["Total Output"].astype(float).sum()
    except Exception:
        total_intermediate = final_consumption = total_output = 0

    imports_total = imp_df.select_dtypes(include="number").sum().sum()
    exports_total = exp_df.select_dtypes(include="number").sum().sum()

    st.subheader(f"📊 Sector Overview — {selected_sector}")
    c1, c2, c3 = st.columns(3)
    for col, label, val in zip([c1, c2, c3],
                               ["Intermediate Consumption", "Final Consumption", "Total Output"],
                               [total_intermediate, final_consumption, total_output]):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{val:,.0f} SAR</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    sankey_fig = create_sankey_diagram(selected_sector, imports_total, exports_total,
                                       total_intermediate, final_consumption, total_output)
    st.plotly_chart(sankey_fig, config={"displayModeBar": False}, use_container_width=True)

    st.markdown("### 📦 Detailed Analysis")
    tab1, tab2 = st.tabs(["📥 Imports", "📤 Exports"])

    with tab1:
        if not imp_df.empty:
            imp_chart = create_bar_chart(imp_df, f"Top Imported Commodities — {selected_sector}")
            if imp_chart: st.plotly_chart(imp_chart, config={"displayModeBar": False}, use_container_width=True)
            st.dataframe(imp_df, use_container_width=True)
        else:
            st.info("No import data available for this sector.")

    with tab2:
        if not exp_df.empty:
            exp_chart = create_bar_chart(exp_df, f"Top Exported Commodities — {selected_sector}")
            if exp_chart: st.plotly_chart(exp_chart, config={"displayModeBar": False}, use_container_width=True)
            st.dataframe(exp_df, use_container_width=True)
        else:
            st.info("No export data available for this sector.")

if __name__ == "__main__":
    main()
