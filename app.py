import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv
import os

load_dotenv()
VALID_USERNAME = os.getenv("USERNAME")
VALID_PASSWORD = os.getenv("PASSWORD")

st.set_page_config(
    page_title="Saudi Statistics Dashboard",
    page_icon="📊",
    layout="wide",
)

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #0e1117;
    color: #fafafa;
    font-family: "Inter", sans-serif;
}

[data-testid="stSidebar"] {
    background-color: #161a23;
}

h1, h2, h3, h4, h5, h6 {
    color: #f0f2f6;
    font-weight: 600;
    letter-spacing: -0.5px;
}

[data-testid="stMetricValue"] {
    color: #66b3ff !important;
    font-weight: 700 !important;
    font-size: 1.4rem !important;
}

[data-testid="stMetricLabel"] {
    color: #cfd3da !important;
}

[data-testid="stDataFrame"] {
    border-radius: 8px;
    overflow: hidden;
}

div.stButton > button {
    background-color: #1f77b4;
    color: white;
    border-radius: 8px;
    border: none;
    padding: 0.6rem 1.2rem;
    font-weight: 600;
    transition: all 0.3s ease;
}

div.stButton > button:hover {
    background-color: #3fa0ff;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(31, 119, 180, 0.4);
}

[data-testid="stTabs"] button {
    background-color: #161a23;
    color: #cfd3da;
    border-radius: 8px;
    font-weight: 500;
    transition: all 0.2s ease;
}

[data-testid="stTabs"] button[aria-selected="true"] {
    background-color: #1f77b4;
    color: white !important;
}

hr {
    border: none;
    height: 1px;
    background-color: #2c2f38;
    margin: 1rem 0;
}

.js-plotly-plot .plotly {
    background-color: #0e1117 !important;
}

.metric-container {
    background: linear-gradient(135deg, #1a1d29 0%, #252938 100%);
    padding: 1.5rem;
    border-radius: 12px;
    border: 1px solid #2c2f38;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}
</style>
""", unsafe_allow_html=True)


def authenticate_user():
    """Handle user authentication with username and password validation."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.markdown("<h2 style='text-align:center;'>📊 Saudi Statistics Dashboard</h2>", unsafe_allow_html=True)
        st.image("logo.png", width=200)
        st.markdown("<p style='text-align:center;'>General Authority for Statistics – Saudi Arabia</p>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login", use_container_width=True)

        if submitted:
            if password == VALID_PASSWORD:
                st.session_state.authenticated = True
                st.success("✅ Login successful")
                st.rerun()
            else:
                st.error("❌ Invalid username or password")
        st.stop()


@st.cache_data(show_spinner="Loading data...")
def load_data():
    """Load and cache all CSV data files for imports, exports, and supply-use tables."""
    imports = pd.read_csv("cleaned_data/cleaned_imports.csv")
    exports = pd.read_csv("cleaned_data/cleaned_exports.csv")
    sut_io = pd.read_csv("cleaned_data/sut_io_cleaned_data.csv")
    return imports, exports, sut_io


def display_header():
    """Render the dashboard header with logo and organization details."""
    col1, col2 = st.columns([1, 5])
    with col1:
        st.image("logo.png", width=100)
    with col2:
        st.markdown(
            """
            <div style='padding-top:10px;'>
                <h2 style='margin:0; color:#66b3ff;'>General Authority for Statistics</h2>
                <p style='margin:0; color:#cfd3da;'>Kingdom of Saudi Arabia</p>
                <a href='https://www.stats.gov.sa/en/home' target='_blank' style='font-size:13px; color:#66b3ff;'>
                    🔗 Visit Official Website
                </a>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("<hr>", unsafe_allow_html=True)


def create_bar_chart(df, title, value_column="2024"):
    """Generate an interactive bar chart for top commodities by value."""
    if df.empty:
        return None

    chart_df = df.nlargest(15, value_column)
    fig = px.bar(
        chart_df,
        x="COMM_NAME_EN",
        y=value_column,
        color=value_column,
        title=title,
        color_continuous_scale="Blues",
        labels={"COMM_NAME_EN": "Commodity", value_column: "Value (SAR)"},
    )

    fig.update_layout(
        template="plotly_dark",
        height=500,
        xaxis_tickangle=-45,
        title_font=dict(size=18),
        margin=dict(l=20, r=20, t=50, b=80),
        showlegend=False,
    )
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>Value: %{y:,.0f} SAR<extra></extra>",
        marker_line_width=0,
    )
    return fig


def create_sankey_diagram(selected_sector, imports_total, exports_total, total_intermediate, final_consumption, total_output):
    """Create a Sankey flow diagram showing economic relationships for the selected sector."""
    nodes = [
        f"Imports<br>{imports_total:,.0f}",
        f"{selected_sector}",
        f"Exports<br>{exports_total:,.0f}",
        f"Intermediate<br>{total_intermediate:,.0f}",
        f"Final<br>{final_consumption:,.0f}",
        f"Output<br>{total_output:,.0f}"
    ]
    links = [
        dict(source=0, target=1, value=imports_total),
        dict(source=1, target=2, value=exports_total),
        dict(source=1, target=3, value=total_intermediate),
        dict(source=1, target=4, value=final_consumption),
        dict(source=1, target=5, value=total_output),
    ]

    fig = go.Figure(data=[go.Sankey(
        arrangement="snap",
        node=dict(
            pad=25,
            thickness=20,
            line=dict(color="rgba(255,255,255,0.1)", width=0.5),
            label=nodes,
            color=["#1f77b4", "#2ca02c", "#ff7f0e", "#9467bd", "#8c564b", "#17becf"],
        ),
        link=dict(
            source=[l["source"] for l in links],
            target=[l["target"] for l in links],
            value=[l["value"] for l in links],
            color="rgba(100,100,100,0.3)",
        ),
    )])

    fig.update_layout(
        template="plotly_dark",
        title=f"💫 Economic Flow Diagram — {selected_sector}",
        font_size=11,
        height=650,
        margin=dict(l=10, r=10, t=50, b=10),
    )
    return fig


def main():
    """Main application entry point orchestrating authentication, data loading, and dashboard rendering."""
    authenticate_user()
    imports, exports, sut_io = load_data()
    display_header()

    st.sidebar.header("📁 Dashboard Filters")
    sectors = sorted(set(imports["CC_DESC_EN"].dropna()) | set(exports["CC_DESC_EN"].dropna()))
    selected_sector = st.sidebar.selectbox("Select Sector", sectors)

    imp_df = imports[imports["CC_DESC_EN"] == selected_sector]
    exp_df = exports[exports["CC_DESC_EN"] == selected_sector]
    sut_df = sut_io[
        sut_io["Input-Output Tables (IOTs) 2018 (Thousands of Saudi riyals) - Economic Activities (ISIC Rev. 4)"]
        .astype(str)
        .str.contains(selected_sector, case=False, na=False)
    ]

    try:
        total_intermediate = sut_df["Total Intermediate Demand"].astype(float).sum()
        final_consumption = sut_df["Final consumption expenditures"].astype(float).sum()
        total_output = sut_df["Total Output"].astype(float).sum()
    except Exception:
        total_intermediate = final_consumption = total_output = 0

    imports_total = imp_df.select_dtypes(include="number").sum().sum()
    exports_total = exp_df.select_dtypes(include="number").sum().sum()

    st.subheader(f"📊 Sector Overview — {selected_sector}")
    col1, col2, col3 = st.columns(3)
    col1.metric("Intermediate Consumption", f"{total_intermediate:,.0f} SAR")
    col2.metric("Final Consumption", f"{final_consumption:,.0f} SAR")
    col3.metric("Total Output", f"{total_output:,.0f} SAR")

    st.markdown("<hr>", unsafe_allow_html=True)

    sankey_fig = create_sankey_diagram(
        selected_sector, imports_total, exports_total,
        total_intermediate, final_consumption, total_output
    )
    st.plotly_chart(
        sankey_fig,
        config={
            "displayModeBar": False,
            "responsive": True,
            "frameMargins": 0,
            "scrollZoom": True
        },
        use_container_width=True
    )

    st.markdown("### 📦 Detailed Analysis")
    tab1, tab2 = st.tabs(["Imports", "Exports"])

    with tab1:
        if not imp_df.empty:
            imp_chart = create_bar_chart(imp_df, f"Top Imported Commodities — {selected_sector}")
            if imp_chart:
                st.plotly_chart(
                    imp_chart,
                    config={
                        "displayModeBar": False,
                        "responsive": True,
                        "frameMargins": 0,
                        "scrollZoom": True
                    },
                    use_container_width=True
                )
            st.dataframe(imp_df, use_container_width=True)
        else:
            st.info("No import data available for this sector.")

    with tab2:
        if not exp_df.empty:
            exp_chart = create_bar_chart(exp_df, f"Top Exported Commodities — {selected_sector}")
            if exp_chart:
                st.plotly_chart(
                    exp_chart,
                    config={
                        "displayModeBar": False,
                        "responsive": True,
                        "frameMargins": 0,
                        "scrollZoom": True
                    },
                    use_container_width=True
                )
            st.dataframe(exp_df, use_container_width=True)
        else:
            st.info("No export data available for this sector.")


if __name__ == "__main__":
    main()