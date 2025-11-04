import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

VALID_USERNAME = st.secrets["credentials"]["username"]
VALID_PASSWORD = st.secrets["credentials"]["password"]

st.set_page_config(page_title="Saudi Statistics Dashboard", page_icon="📊", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
* { 
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; 
}
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
    color: #f8fafc;
}
[data-testid="stSidebar"] {
    background-color: #0f1419;
    border-right: 1px solid #1e293b;
}
h1, h2, h3, h4, h5 {
    color: #f1f5f9;
    font-weight: 600;
    letter-spacing: -0.5px;
}
hr {
    border: none;
    height: 2px;
    background: linear-gradient(90deg, rgba(59, 130, 246, 0.5), rgba(147, 51, 234, 0.5));
    margin: 2rem 0;
}
.metric-card {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.6), rgba(15, 23, 42, 0.8));
    border-radius: 20px;
    padding: 2rem 1.5rem;
    border: 1px solid rgba(148, 163, 184, 0.1);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    text-align: center;
    backdrop-filter: blur(10px);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.metric-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 48px rgba(59, 130, 246, 0.3);
}
.metric-label { 
    color: #94a3b8; 
    font-size: 0.875rem; 
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-weight: 500;
}
.metric-value { 
    color: #60a5fa; 
    font-size: 2.25rem; 
    font-weight: 700;
    margin: 0.75rem 0;
    background: linear-gradient(135deg, #60a5fa, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.metric-subtext {
    color: #64748b;
    font-size: 0.8rem;
    margin-top: 0.5rem;
    font-weight: 500;
}
div[data-testid="stButton"] > button[kind="secondary"] {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.9)) !important;
    border-radius: 24px !important;
    padding: 2rem 1.5rem !important;
    border: 2px solid rgba(59, 130, 246, 0.2) !important;
    color: #f1f5f9 !important;
    font-weight: 600 !important;
    min-height: 160px !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    position: relative !important;
    overflow: hidden !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3) !important;
    backdrop-filter: blur(10px) !important;
}
div[data-testid="stButton"] > button[kind="secondary"]::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.4), transparent);
    transition: left 0.6s ease;
}
div[data-testid="stButton"] > button[kind="secondary"]:hover {
    border-color: rgba(59, 130, 246, 0.6) !important;
    transform: translateY(-10px) scale(1.03) !important;
    box-shadow: 0 16px 48px rgba(59, 130, 246, 0.4) !important;
}
div[data-testid="stButton"] > button[kind="secondary"]:hover::before {
    left: 100%;
}
div.stButton > button {
    background: linear-gradient(135deg, #3b82f6, #8b5cf6);
    color: white;
    border-radius: 12px;
    border: none;
    padding: 0.75rem 1.5rem;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 4px 16px rgba(59, 130, 246, 0.3);
}
div.stButton > button:hover {
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(59, 130, 246, 0.5);
}
.login-card {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.95));
    padding: 3rem 2.5rem;
    border-radius: 24px;
    border: 1px solid rgba(148, 163, 184, 0.2);
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(20px);
    width: 400px;
    margin: auto;
}
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}
.bubble-container { 
    animation: fadeInUp 0.6s ease-out;
    margin-bottom: 1rem;
}
.sankey-title {
    font-size: 1.5rem;
    font-weight: 700;
    margin: 2rem 0 1rem 0;
    background: linear-gradient(135deg, #60a5fa, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
</style>
""", unsafe_allow_html=True)

def authenticate_user():
    """
    Handles user authentication with username and password validation.
    Stores authentication state in session_state.
    """
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if not st.session_state.authenticated:
        st.markdown("<h2 style='text-align:center; margin-top: 4rem;'>📊 Saudi Statistics Dashboard</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;color:#94a3b8; margin-bottom: 3rem;'>General Authority for Statistics – Kingdom of Saudi Arabia</p>", unsafe_allow_html=True)
        with st.form("login_form"):
            st.markdown("<div class='login-card'>", unsafe_allow_html=True)
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
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
    """
    Loads and caches CSV data for imports, exports, and supply-use tables.
    Returns three DataFrames.
    """
    imports = pd.read_csv("cleaned_data/cleaned_imports.csv")
    exports = pd.read_csv("cleaned_data/cleaned_exports.csv")
    sut_io = pd.read_csv("cleaned_data/sut_io_cleaned_data.csv")
    return imports, exports, sut_io

def display_header():
    """
    Displays the application header with logo and organization name.
    """
    col1, col2 = st.columns([1, 5])
    with col1:
        st.image("logo.png", width=100)
    with col2:
        st.markdown("""
            <div style='padding-top:15px;'>
                <h2 style='margin:0; background: linear-gradient(135deg, #60a5fa, #a78bfa); 
                           -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                    General Authority for Statistics
                </h2>
                <p style='margin:0; color:#94a3b8; font-size: 1.1rem;'>Kingdom of Saudi Arabia</p>
            </div>
        """, unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

def get_sector_icon(sector):
    """
    Returns appropriate emoji icon based on sector keywords.
    """
    sector_lower = sector.lower()
    if "food" in sector_lower or "agriculture" in sector_lower:
        return "🌾"
    elif "oil" in sector_lower or "petroleum" in sector_lower:
        return "🛢️"
    elif "construction" in sector_lower:
        return "🏗️"
    elif "transport" in sector_lower:
        return "🚚"
    elif "finance" in sector_lower:
        return "💰"
    elif "health" in sector_lower:
        return "🏥"
    elif "education" in sector_lower:
        return "🎓"
    elif "technology" in sector_lower or "telecom" in sector_lower:
        return "💻"
    return "🏭"

def format_value(value):
    """
    Formats numerical values into human-readable format (B/M/K).
    """
    if value >= 1_000_000_000:
        return f"{value/1_000_000_000:.1f}B SAR"
    elif value >= 1_000_000:
        return f"{value/1_000_000:.1f}M SAR"
    elif value >= 1_000:
        return f"{value/1_000:.1f}K SAR"
    return f"{value:,.0f} SAR"

def display_sector_bubbles(sectors_data):
    """
    Displays interactive sector selection grid with bubble cards.
    Sorted by total output value in descending order.
    """
    st.markdown("<h3 style='margin: 2rem 0 1rem 0;'>🎯 Select a Sector to Explore</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8; margin-bottom: 2.5rem;'>Click on any sector to view detailed economic flow analysis</p>", unsafe_allow_html=True)
    sorted_sectors = sorted(sectors_data.items(), key=lambda x: x[1]['output'], reverse=True)
    cols = st.columns(3)
    for idx, (sector, data) in enumerate(sorted_sectors):
        with cols[idx % 3]:
            output_val = data['output']
            display_val = format_value(output_val)
            icon = get_sector_icon(sector)
            display_name = sector if len(sector) <= 45 else sector[:42] + "..."
            button_label = f"{icon}\n\n**{display_name}**\n\n📊 Output: {display_val}"
            st.markdown("<div class='bubble-container'>", unsafe_allow_html=True)
            if st.button(button_label, key=f"bubble_{sector}_{idx}", use_container_width=True, type="secondary"):
                st.session_state.selected_sector = sector
                st.session_state.view = "sankey"
                st.session_state.selected_flow_type = None
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

def create_multilevel_sankey(selected_sector, exports_df, imports_df, total_output, total_intermediate, final_consumption):
    """
    Simplified multi-level Sankey:
    - Shows only total-level flows
    - Each node label includes value + percentage of Total Output
    """
    # Compute totals
    total_exports = exports_df["2023"].sum()
    total_imports = imports_df["2023"].sum()
    total_outflow = total_exports + total_intermediate + final_consumption

    # Calculate shares (% of total output)
    pct = lambda val: (val / total_output * 100) if total_output > 0 else 0

    nodes = [
        f"<b>Total Output</b><br>{total_output:,.0f} SAR<br>(100%)",
        f"<b>Exports</b><br>{total_exports:,.0f} SAR<br>({pct(total_exports):.1f}%)",
        f"<b>Final Demand</b><br>{final_consumption:,.0f} SAR<br>({pct(final_consumption):.1f}%)",
        f"<b>Intermediate</b><br>{total_intermediate:,.0f} SAR<br>({pct(total_intermediate):.1f}%)",
        f"<b>Imports</b><br>{total_imports:,.0f} SAR<br>({pct(total_imports):.1f}%)"
    ]

    links = [
        dict(source=0, target=1, value=total_exports, color="rgba(251, 146, 60, 0.6)"),
        dict(source=0, target=2, value=final_consumption, color="rgba(52, 211, 153, 0.6)"),
        dict(source=0, target=3, value=total_intermediate, color="rgba(167, 139, 250, 0.6)"),
        dict(source=4, target=0, value=total_imports, color="rgba(96, 165, 250, 0.6)")
    ]

    fig = go.Figure(data=[go.Sankey(
        arrangement="snap",
        node=dict(
            pad=30,
            thickness=30,
            line=dict(color="rgba(255,255,255,0.2)", width=1),
            label=nodes,
            color=["#3b82f6", "#fb923c", "#34d399", "#a78bfa", "#60a5fa"],
            hovertemplate='%{label}<extra></extra>'
        ),
        link=dict(
            source=[l["source"] for l in links],
            target=[l["target"] for l in links],
            value=[l["value"] for l in links],
            color=[l["color"] for l in links],
            hovertemplate='%{source.label} → %{target.label}<br>Value: %{value:,.0f} SAR<extra></extra>'
        )
    )])

    fig.update_layout(
        template="plotly_dark",
        title=dict(
            text=f"💫 Economic Flow Analysis — {selected_sector}",
            font=dict(size=20, color="#f1f5f9", family="Inter")
        ),
        font=dict(size=11, family="Inter"),
        height=700,
        margin=dict(l=20, r=20, t=80, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig



def create_expanded_flow_sankey(selected_sector, df_flow, flow_label):
    """
    Creates an expanded Sankey for Exports or Imports.
    Shows top 10 items, aggregates the rest into 'Other Exports' or 'Other Imports'.
    """
    if df_flow.empty:
        return go.Figure()

    # Ensure clean numeric data
    df_flow = df_flow.copy()
    df_flow["2023"] = pd.to_numeric(df_flow["2023"], errors="coerce").fillna(0)

    total_flow = df_flow["2023"].sum()
    if total_flow <= 0:
        return go.Figure()

    # Sort and slice
    df_flow = df_flow.sort_values("2023", ascending=False)
    top_df = df_flow.head(10)
    other_df = df_flow.iloc[10:]
    other_val = other_df["2023"].sum()

    # Prepare nodes
    main_label = f"<b>{selected_sector}</b><br><b>{flow_label}</b><br>{total_flow:,.0f} SAR"
    nodes = [main_label]
    links = []

    # Color scheme
    base_color = "rgba(251, 146, 60, 0.7)" if flow_label == "Exports" else "rgba(96, 165, 250, 0.7)"
    light_color = "rgba(251, 146, 60, 0.4)" if flow_label == "Exports" else "rgba(96, 165, 250, 0.4)"

    # Add top 10 items
    for _, row in top_df.iterrows():
        product = str(row["COMM_NAME_EN"])
        if len(product) > 40:
            product = product[:37] + "..."
        value = row["2023"]
        nodes.append(f"{product}<br>{value:,.0f} SAR")
        links.append(dict(source=0, target=len(nodes)-1, value=value, color=base_color))

    # Add aggregated 'Other' node if applicable
    if other_val >= 1:
        other_label = f"<b>Other {flow_label}</b><br>{other_val:,.0f} SAR<br>({len(other_df)} items)"
        nodes.append(other_label)
        links.append(dict(source=0, target=len(nodes)-1, value=other_val, color=light_color))

    # Sankey diagram
    fig = go.Figure(data=[go.Sankey(
        arrangement="snap",
        node=dict(
            pad=35,
            thickness=30,
            line=dict(color="rgba(255,255,255,0.3)", width=1),
            label=nodes,
            color=["#3b82f6"] + ["#60a5fa"] * (len(nodes)-1),
            hovertemplate='%{label}<extra></extra>'
        ),
        link=dict(
            source=[l["source"] for l in links],
            target=[l["target"] for l in links],
            value=[l["value"] for l in links],
            color=[l["color"] for l in links],
            hovertemplate='Value: %{value:,.0f} SAR<extra></extra>'
        )
    )])

    fig.update_layout(
        template="plotly_dark",
        title=dict(
            text=f"📦 {flow_label} Breakdown — {selected_sector}",
            font=dict(size=20, color="#f1f5f9", family="Inter")
        ),
        font=dict(size=11, family="Inter"),
        height=850,
        margin=dict(l=20, r=20, t=80, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig



def create_bar_chart(df, title, value_column="2024"):
    """
    Creates a horizontal bar chart for top commodities.
    Shows top 15 products by value with gradient color scale.
    """
    if df.empty:
        return None
    chart_df = df.nlargest(15, value_column).copy()
    chart_df = chart_df.sort_values(value_column, ascending=True)
    
    fig = px.bar(
        chart_df, 
        y="COMM_NAME_EN", 
        x=value_column, 
        color=value_column,
        title=title, 
        color_continuous_scale=["#1e293b", "#3b82f6", "#60a5fa"],
        labels={"COMM_NAME_EN": "Commodity", value_column: "Value (SAR)"},
        orientation='h'
    )
    
    fig.update_layout(
        template="plotly_dark", 
        height=600, 
        title_font=dict(size=18, color="#f1f5f9", family="Inter"),
        margin=dict(l=20, r=20, t=60, b=40), 
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(tickfont=dict(size=10)),
        xaxis=dict(gridcolor="rgba(148, 163, 184, 0.1)")
    )
    
    fig.update_traces(
        hovertemplate="<b>%{y}</b><br>Value: %{x:,.0f} SAR<extra></extra>",
        marker=dict(line=dict(width=0))
    )
    return fig

def main():
    """
    Main application entry point.
    Handles authentication, data loading, and view navigation.
    """
    authenticate_user()
    imports, exports, sut_io = load_data()
    display_header()

    if "view" not in st.session_state:
        st.session_state.view = "bubbles"
    if "selected_sector" not in st.session_state:
        st.session_state.selected_sector = None
    if "selected_flow_type" not in st.session_state:
        st.session_state.selected_flow_type = None

    sectors = sorted(set(imports["CC_DESC_EN"].dropna()) | set(exports["CC_DESC_EN"].dropna()))
    sectors_data = {}
    for sector in sectors:
        sut_df = sut_io[sut_io["Input-Output Tables (IOTs) 2018 (Thousands of Saudi riyals) - Economic Activities (ISIC Rev. 4)"]
                        .astype(str).str.contains(sector, case=False, na=False)]
        try:
            total_output = sut_df["Total Output"].astype(float).sum() * 1000
        except Exception:
            total_output = 0
        sectors_data[sector] = {"output": total_output}

    if st.session_state.view == "bubbles":
        display_sector_bubbles(sectors_data)

    elif st.session_state.view == "sankey":
        selected_sector = st.session_state.selected_sector
        if st.button("⬅️ Back to Sectors", type="primary"):
            st.session_state.view = "bubbles"
            st.session_state.selected_flow_type = None
            st.rerun()

        st.markdown(f"<h3 class='sankey-title'>📊 Sector Analysis — {selected_sector}</h3>", unsafe_allow_html=True)
        
        imp_df = imports[imports["CC_DESC_EN"] == selected_sector]
        exp_df = exports[exports["CC_DESC_EN"] == selected_sector]
        sut_df = sut_io[sut_io["Input-Output Tables (IOTs) 2018 (Thousands of Saudi riyals) - Economic Activities (ISIC Rev. 4)"]
                        .astype(str).str.contains(selected_sector, case=False, na=False)]

        try:
            if sut_df["Total Output"].isnull().all():
                st.warning("No valid data found for Total Output in the selected sector.")
                total_output = 0
            else:
                total_output = sut_df["Total Output"].astype(float).sum() * 1000
            total_intermediate = sut_df["Total Intermediate Consumption"].astype(float).sum() * 1000
            final_consumption = sut_df["Final Demand"].astype(float).sum() * 1000
        except Exception as e:
            st.error(f"Error calculating totals: {e}")
            total_intermediate = final_consumption = total_output = 0

        exports_total = exp_df['2023'].astype(float).sum()
        
        if total_output > 0:
            exports_pct = (exports_total / total_output) * 100
            final_demand_pct = (final_consumption / total_output) * 100
            intermediate_pct = (total_intermediate / total_output) * 100
            total_output_pct = 100
        else:
            exports_pct = final_demand_pct = intermediate_pct = total_output_pct = 0

        c1, c2, c3, c4 = st.columns(4)
        metrics_data = [
            ("Total Output", total_output, total_output_pct),
            ("Exports", exports_total, exports_pct),
            ("Final Demand", final_consumption, final_demand_pct),
            ("Intermediate", total_intermediate, intermediate_pct)
        ]
        
        for col, (label, val, pct) in zip([c1, c2, c3, c4], metrics_data):
            with col:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">{label}</div>
                        <div class="metric-value">{pct:.1f}%</div>
                        <div class="metric-subtext">{format_value(val)}</div>
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)

        st.markdown("<h4 style='margin: 2rem 0 1.5rem 0;'>Choose a flow to expand:</h4>", unsafe_allow_html=True)
        col_exp, col_imp = st.columns(2)
        with col_exp:
            if st.button("🔽 View Exports Flow", key="btn_exports", use_container_width=True):
                st.session_state.selected_flow_type = "Exports"
                st.session_state.view = "sankey_expanded"
                st.rerun()
        with col_imp:
            if st.button("🔽 View Imports Flow", key="btn_imports", use_container_width=True):
                st.session_state.selected_flow_type = "Imports"
                st.session_state.view = "sankey_expanded"
                st.rerun()

        sankey_fig = create_multilevel_sankey(selected_sector, exp_df, imp_df,
                                               total_output, total_intermediate, final_consumption)
        st.plotly_chart(sankey_fig, config={"displayModeBar": False}, use_container_width=True)

        st.markdown("<h4 style='margin: 3rem 0 1.5rem 0;'>📦 Detailed Product Analysis</h4>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["📤 Export Products", "📥 Import Products"])
        
        with tab1:
            if not exp_df.empty:
                exp_chart = create_bar_chart(exp_df, f"Top Exported Commodities — {selected_sector}")
                if exp_chart:
                    st.plotly_chart(exp_chart, config={"displayModeBar": False}, use_container_width=True)
                st.dataframe(exp_df, use_container_width=True, height=400)
            else:
                st.info("No export data available for this sector.")
        
        with tab2:
            if not imp_df.empty:
                imp_chart = create_bar_chart(imp_df, f"Top Imported Commodities — {selected_sector}")
                if imp_chart:
                    st.plotly_chart(imp_chart, config={"displayModeBar": False}, use_container_width=True)
                st.dataframe(imp_df, use_container_width=True, height=400)
            else:
                st.info("No import data available for this sector.")

    elif st.session_state.view == "sankey_expanded":
        selected_sector = st.session_state.selected_sector
        flow_type = st.session_state.selected_flow_type
        
        if st.button("⬅️ Back to Sector Overview", type="primary"):
            st.session_state.view = "sankey"
            st.session_state.selected_flow_type = None
            st.rerun()

        st.markdown(f"<h3 class='sankey-title'>🔍 {flow_type} Breakdown — {selected_sector}</h3>", unsafe_allow_html=True)
        
        if flow_type == "Exports":
            df_flow = exports[exports["CC_DESC_EN"] == selected_sector]
        else:
            df_flow = imports[imports["CC_DESC_EN"] == selected_sector]

        if df_flow.empty:
            st.info(f"No {flow_type.lower()} data available for this sector.")
        else:
            expanded_fig = create_expanded_flow_sankey(selected_sector, df_flow, flow_type)
            st.plotly_chart(expanded_fig, config={"displayModeBar": False}, use_container_width=True)
            st.markdown("<h4 style='margin: 2rem 0 1rem 0;'>📋 Data Table</h4>", unsafe_allow_html=True)
            st.dataframe(df_flow, use_container_width=True, height=500)

if __name__ == "__main__":
    main()