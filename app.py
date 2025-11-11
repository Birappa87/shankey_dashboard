import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go

VALID_USERNAME = st.secrets["credentials"]["username"]
VALID_PASSWORD = st.secrets["credentials"]["password"]

st.set_page_config(page_title="Industrial economic data dashboard", page_icon="", layout="wide")

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
    padding: 1.5rem 1rem;
    border: 1px solid rgba(148, 163, 184, 0.1);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    text-align: center;
    backdrop-filter: blur(10px);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    min-height: 180px;
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
    margin-bottom: 0.75rem;
    line-height: 1.4;
}
.metric-value { 
    color: #60a5fa; 
    font-size: 2rem; 
    font-weight: 700;
    margin: 0.5rem 0;
    background: linear-gradient(135deg, #60a5fa, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.2;
}
.metric-subtext {
    color: #64748b;
    font-size: 1.1rem;
    margin-top: 0.5rem;
    font-weight: 500;
    line-height: 1.2;
}
div[data-testid="stButton"] > button[kind="secondary"] {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.9)) !important;
    border-radius: 24px !important;
    padding: 1rem 1rem !important;
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
    """Handles user authentication with username and password validation."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if not st.session_state.authenticated:
        st.markdown("<h2 style='text-align:center; margin-top: 4rem;'>Saudi Statistics Dashboard</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;color:#94a3b8; margin-bottom: 3rem;'>Industrial sector economic data</p>", unsafe_allow_html=True)
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submitted = st.form_submit_button("Login", use_container_width=True)
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
    """Loads and caches CSV data for imports, exports, and supply-use tables."""
    imports = pd.read_csv("cleaned_data/cleaned_imports.csv")
    exports = pd.read_csv("cleaned_data/cleaned_exports.csv")
    sut_io = pd.read_csv("cleaned_data/sut_io_cleaned_data.csv")
    return imports, exports, sut_io

def display_header():
    """Displays the application header with logo and organization name."""
    col1, col2 = st.columns([1, 5])
    # with col1:
    #     st.image("logo.png", width=100)
    with col2:
        st.markdown("""
            <div style='padding-top:15px;'>
                <h2 style='margin:0; background: linear-gradient(135deg, #60a5fa, #a78bfa); 
                           -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                    Industrial sector economic data
                </h2>
            </div>
        """, unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

def get_sector_icon(sector):
    """Returns appropriate emoji icon based on sector keywords."""
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
    """Formats numerical values into billions and millions for better readability."""
    if value >= 1_000_000_000:
        return f"SR {value/1_000_000_000:.2f}B"
    elif value >= 1_000_000:
        return f"SR {value/1_000_000:.2f}M"
    return f"SR {value/1_000_000:.2f}M"

def display_sector_bubbles(sectors_data):
    """Displays interactive sector selection grid with bubble cards sorted by output value."""
    st.markdown("<h3 style='margin: 2rem 0 1rem 0;'>Select a Sector to Explore</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8; margin-bottom: 2.5rem;'>Click on any sector to view detailed economic flow analysis</p>", unsafe_allow_html=True)
    
    sorted_sectors = sorted(sectors_data.items(), key=lambda x: x[1]['output'], reverse=True)
    
    sectors_to_display = [
        "Manufacture of coke and refined petroleum products",
        "Manufacture of food products",
        "Manufacture of chemicals and chemical products",
        "Manufacture of motor vehicles, trailers and semi-trailers",
        "Manufacture of machinery and equipment n.e.c.",
        "Manufacture of electrical equipment",
        "Manufacture of basic metals",
        "Manufacture of computer, electronic and optical products",
        "Manufacture of fabricated metal products, except machinery and equipment",
        "Manufacture of other transport equipment",
        "Manufacture of other non-metallic mineral products",
        "Manufacture of wearing apparel",
        "Manufacture of furniture",
        "Manufacture of rubber and plastics products",
        "Manufacture of basic pharmaceutical products and pharmaceutical preparations",
        "Other manufacturing",
        "Manufacture of beverages",
        "Manufacture of paper and paper products",
        "Manufacture of textiles",
        "Printing and reproduction of recorded media",
        "Manufacture of leather and related products",
        "Manufacture of woods, wood products and cork, except furniture"
    ]
    
    filtered_sectors = [(sector, data) for sector, data in sorted_sectors if sector in sectors_to_display]
    num_cols = 3
    
    for row_start in range(0, len(filtered_sectors), num_cols):
        cols = st.columns(num_cols)
        row_sectors = filtered_sectors[row_start:row_start + num_cols]
        
        for col_idx, (sector, data) in enumerate(row_sectors):
            with cols[col_idx]:
                output_val = data['output']
                display_val = format_value(output_val)
                icon = get_sector_icon(sector)
                button_label = f"{icon}\n\n**{sector}**\n\n Consumer Sales: {display_val}"
                
                st.markdown("<div class='bubble-container'>", unsafe_allow_html=True)
                
                if st.button(button_label, key=f"bubble_{sector}", use_container_width=True, type="secondary"):
                    st.session_state.selected_sector = sector
                    st.session_state.view = "sankey"
                    st.session_state.selected_flow_type = None
                    st.rerun()
                
                st.markdown("</div>", unsafe_allow_html=True)

def create_multilevel_sankey(selected_sector, exports_df, imports_df, total_output, total_intermediate, final_consumption):
    """Creates multi-level Sankey diagram showing total-level economic flows with dynamic node sizing."""
    total_exports = exports_df["2023"].sum()
    total_imports = imports_df["2023"].sum()

    pct = lambda val: (val / total_output * 100) if total_output > 0 else 0

    node_values = [total_output, total_exports, final_consumption, total_intermediate, total_imports]
    node_labels = [
        f"<b>Sales</b><br>{format_value(total_output)}<br>(100%)",
        f"<b>Exports</b><br>{format_value(total_exports)}<br>({pct(total_exports):.1f}%)",
        f"<b>Consumer Sales</b><br>{format_value(final_consumption)}<br>({pct(final_consumption):.1f}%)",
        f"<b>B2B Sales (Raw Material)</b><br>{format_value(total_intermediate)}<br>({pct(total_intermediate):.1f}%)",
        f"<b>Imports</b><br>{format_value(total_imports)}<br>({pct(total_imports):.1f}%)"
    ]

    min_pad, max_pad = 15, 80
    if total_output > 0:
        pad_values = np.interp(node_values, [min(node_values), max(node_values)], [max_pad, min_pad])
        avg_pad = float(np.mean(pad_values))
    else:
        avg_pad = 40

    links = [
        dict(source=0, target=1, value=total_exports, color="rgba(251, 146, 60, 0.6)"),
        dict(source=0, target=2, value=final_consumption, color="rgba(52, 211, 153, 0.6)"),
        dict(source=0, target=3, value=total_intermediate, color="rgba(167, 139, 250, 0.6)"),
        dict(source=4, target=0, value=total_imports, color="rgba(96, 165, 250, 0.6)")
    ]

    fig = go.Figure(data=[go.Sankey(
        arrangement="snap",
        node=dict(
            pad=avg_pad,
            thickness=30,
            line=dict(color="rgba(255,255,255,0.2)", width=1),
            label=node_labels,
            color=["#3b82f6", "#fb923c", "#34d399", "#a78bfa", "#60a5fa"],
            hovertemplate='%{label}<extra></extra>'
        ),
        link=dict(
            source=[l["source"] for l in links],
            target=[l["target"] for l in links],
            value=[l["value"] for l in links],
            color=[l["color"] for l in links],
            hovertemplate="Flow: %{value:,.0f} SR<extra></extra>"
        )
    )])

    fig.update_layout(
        template="plotly_dark",
        title=dict(
            text=f"Economic Flow Analysis — {selected_sector}",
            font=dict(size=20, color="#f1f5f9", family="Inter")
        ),
        font=dict(size=12, family="Inter"),
        height=700,
        margin=dict(l=20, r=20, t=80, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig

def create_expanded_flow_sankey(selected_sector, df_flow, flow_label):
    """Creates expanded Sankey showing top 10 items with aggregated 'Other' category."""
    if df_flow.empty:
        return go.Figure()

    df_flow = df_flow.copy()
    df_flow["2023"] = pd.to_numeric(df_flow["2023"], errors="coerce").fillna(0)

    total_flow = df_flow["2023"].sum()
    if total_flow <= 0:
        return go.Figure()

    df_flow = df_flow.sort_values("2023", ascending=False)
    top_df = df_flow.head(10)
    other_df = df_flow.iloc[10:]
    other_val = other_df["2023"].sum()

    main_label = f"<b>{selected_sector}</b><br><b>{flow_label}</b><br>{format_value(total_flow)}"
    nodes = [main_label]
    links = []

    base_color = "rgba(251, 146, 60, 0.7)" if flow_label == "Exports" else "rgba(96, 165, 250, 0.7)"
    light_color = "rgba(251, 146, 60, 0.4)" if flow_label == "Exports" else "rgba(96, 165, 250, 0.4)"

    for _, row in top_df.iterrows():
        product = str(row["COMM_NAME_EN"])
        if len(product) > 40:
            product = product[:37] + "..."
        value = row["2023"]
        percentage = (value / total_flow) * 100
        nodes.append(f"{product}<br>{format_value(value)}<br>({percentage:.1f}%)")
        links.append(dict(source=0, target=len(nodes)-1, value=value, color=base_color))

    if other_val >= 1:
        percentage = (other_val / total_flow) * 100
        other_label = f"<b>Other {flow_label}</b><br>{format_value(other_val)}<br>({percentage:.1f}%)<br>({len(other_df)} items)"
        nodes.append(other_label)
        links.append(dict(source=0, target=len(nodes)-1, value=other_val, color=light_color))

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
            hovertemplate="Value: SR %{value:,.2f} <br>Share: %{value:,.1%} of total<extra></extra>"
        )
    )])

    fig.update_layout(
        template="plotly_dark",
        title=dict(
            text=f"📦 {flow_label} Breakdown — {selected_sector}",
            font=dict(size=20, color="#f1f5f9", family="Inter")
        ),
        font=dict(size=11, family="Inter"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig

def create_other_items_heatmap(other_df, total_flow, flow_label, base_color):
    """Creates box heatmap visualization for remaining items sorted from largest to smallest."""
    other_df = other_df.sort_values("2023", ascending=False).reset_index(drop=True)

    n_cols = 4
    n_rows = (len(other_df) + n_cols - 1) // n_cols

    matrix = []
    labels_matrix = []

    max_value = other_df["2023"].max()

    for i in range(n_rows):
        row_values, row_labels = [], []
        for j in range(n_cols):
            idx = i * n_cols + j
            if idx < len(other_df):
                item = other_df.iloc[idx]
                value = item["2023"]
                pct = (value / total_flow) * 100
                relative_value = (value / max_value) * 100
                product_name = item["COMM_NAME_EN"]
                if len(product_name) > 30:
                    product_name = product_name[:27] + "..."
                row_values.append(relative_value)
                row_labels.append(f"{product_name}<br>{format_value(value)}<br>({pct:.1f}%)")
            else:
                row_values.append(0)
                row_labels.append("")
        matrix.append(row_values)
        labels_matrix.append(row_labels)

    matrix = matrix[::-1]
    labels_matrix = labels_matrix[::-1]

    if flow_label == "Exports":
        colorscale = [
            [0.0, "#1e293b"], [0.1, "#78350f"], [0.3, "#d97706"],
            [0.5, "#f59e0b"], [0.7, "#fbbf24"], [1.0, "#fcd34d"]
        ]
    else:
        colorscale = [
            [0.0, "#1e293b"], [0.1, "#1e3a8a"], [0.3, "#2563eb"],
            [0.5, "#3b82f6"], [0.7, "#60a5fa"], [1.0, "#93c5fd"]
        ]

    fig = go.Figure(data=go.Heatmap(
        z=matrix,
        text=labels_matrix,
        texttemplate="%{text}",
        textfont={"size": 12, "family": "Inter"},
        hoverongaps=False,
        hoverinfo="text",
        colorscale=colorscale,
        showscale=False
    ))

    other_total = other_df["2023"].sum()
    other_pct = (other_total / total_flow) * 100

    fig.update_layout(
        height=max(400, n_rows * 120),
        template="plotly_dark",
        margin=dict(l=20, r=20, t=120, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title=dict(
            text=f"📦 Remaining {len(other_df)} {flow_label} Items<br>"
                 f"<sub>Total: {format_value(other_total)} ({other_pct:.1f}% of flow)</sub>",
            font=dict(size=16, color="#f1f5f9", family="Inter"),
            x=0.5,
            xanchor='center'
        )
    )

    fig.update_xaxes(showticklabels=False, showgrid=False)
    fig.update_yaxes(showticklabels=False, showgrid=False)

    return fig

def create_bar_chart(df, title, value_column="2023"):
    """Creates horizontal bar chart for top commodities with adaptive labels and minimum visibility."""
    if df.empty:
        return None

    chart_df = df.copy()
    chart_df[value_column] = pd.to_numeric(chart_df[value_column], errors='coerce').fillna(0)
    chart_df = chart_df.nlargest(15, value_column).copy()
    chart_df = chart_df.sort_values(value_column, ascending=True)
    
    total_value = chart_df[value_column].sum()
    if total_value == 0:
        return None

    def format_value_label(x):
        if x == 0:
            return "0 (0.0%)"
        if x >= 1e9:
            val = f"{x / 1e9:.2f}B"
        elif x >= 1e6:
            val = f"{x / 1e6:.2f}M"
        else:
            val = f"{x:,.0f}"
        pct = f"{(x / total_value) * 100:.1f}%"
        return f"{val} ({pct})"

    chart_df["label_text"] = chart_df[value_column].apply(format_value_label)

    max_val = chart_df[value_column].max()
    if max_val == 0:
        return None
        
    min_visible_val = 0.02 * max_val
    chart_df["display_value"] = np.where(
        chart_df[value_column] < min_visible_val, 
        min_visible_val, 
        chart_df[value_column]
    )

    fig = px.bar(
        chart_df,
        y="COMM_NAME_EN",
        x="display_value",
        color=value_column,
        title=title,
        color_continuous_scale=["#1e293b", "#3b82f6", "#60a5fa"],
        labels={"COMM_NAME_EN": "Commodity", value_column: "Value (SR)"},
        orientation="h",
        text="label_text",
    )

    threshold = 0.15 * max_val
    textpositions = np.where(chart_df[value_column] < threshold, "outside", "inside")

    fig.update_traces(
        hovertemplate="<b>%{y}</b><br>Value: SR %{customdata[0]:,.2f}<extra></extra>",
        textposition=textpositions,
        textfont=dict(color="white", size=11),
        insidetextanchor="middle",
        cliponaxis=False,
        customdata=np.expand_dims(chart_df[value_column], axis=1),
    )

    fig.update_layout(
        template="plotly_dark",
        height=650,
        title_font=dict(size=18, color="#f1f5f9", family="Inter"),
        margin=dict(l=20, r=40, t=60, b=40),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(tickfont=dict(size=10)),
        xaxis=dict(
            gridcolor="rgba(148, 163, 184, 0.1)",
            range=[0, max_val * 1.25],
        ),
    )

    return fig

def main():
    """Main application entry point handling authentication, data loading, and view navigation."""
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
            total_output = sut_df["Final consumption expenditures"].astype(float).sum() * 1000
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

        st.markdown(f"<h3 class='sankey-title'>Sector Analysis — {selected_sector}</h3>", unsafe_allow_html=True)
        
        imp_df = imports[imports["CC_DESC_EN"] == selected_sector]
        exp_df = exports[exports["CC_DESC_EN"] == selected_sector]
        sut_df = sut_io[sut_io["Input-Output Tables (IOTs) 2018 (Thousands of Saudi riyals) - Economic Activities (ISIC Rev. 4)"]
                        .astype(str).str.contains(selected_sector, case=False, na=False)]

        try:
            total_intermediate = sut_df["Total Intermediate Consumption"].astype(float).sum() * 1000
            final_consumption = sut_df["Final consumption expenditures"].astype(float).sum() * 1000
            total_output = total_intermediate + final_consumption
        except Exception as e:
            st.error(f"Error calculating totals: {e}")
            total_intermediate = final_consumption = total_output = 0

        exports_total = exp_df['2023'].astype(float).sum()
        total_import = imp_df['2023'].astype(float).sum()

        if total_output > 0:
            exports_pct = (exports_total / total_output) * 100
            final_demand_pct = (final_consumption / total_output) * 100
            intermediate_pct = (total_intermediate / total_output) * 100
            import_pct = (total_import / total_output) * 100
            total_output_pct = 100
        else:
            exports_pct = final_demand_pct = intermediate_pct = import_pct = total_output_pct = 0

        c1, c2, c3, c4, c5 = st.columns(5)
        metrics_data = [
            ("Sales", total_output, total_output_pct),
            ("Exports", exports_total, exports_pct),
            ("Imports", total_import, import_pct),
            ("Consumer Sales", final_consumption, final_demand_pct),
            ("B2B Sales (Raw Material)", total_intermediate, intermediate_pct)
        ]

        for col, (label, val, pct) in zip([c1, c2, c3, c4, c5], metrics_data):
            with col:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">{label}</div>
                        <div class="metric-value">{format_value(val)}</div>
                        <div class="metric-subtext">{pct:.1f}%</div>
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)

        st.markdown("<h4 style='margin: 2rem 0 1.5rem 0;'>Choose a flow to expand:</h4>", unsafe_allow_html=True)
        col_exp, col_imp = st.columns(2)
        with col_exp:
            if st.button("View Exports Flow", key="btn_exports", use_container_width=True):
                st.session_state.selected_flow_type = "Exports"
                st.session_state.view = "sankey_expanded"
                st.rerun()
        with col_imp:
            if st.button("View Imports Flow", key="btn_imports", use_container_width=True):
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
        
        if flow_type == "Exports":
            df_flow = exports[exports["CC_DESC_EN"] == selected_sector]
        else:
            df_flow = imports[imports["CC_DESC_EN"] == selected_sector]

        if df_flow.empty:
            st.info(f"No {flow_type.lower()} data available for this sector.")
        else:
            expanded_fig = create_expanded_flow_sankey(selected_sector, df_flow, flow_type)
            st.plotly_chart(expanded_fig, config={"displayModeBar": False}, use_container_width=True)

            df_sorted = df_flow.sort_values("2023", ascending=False)
            other_df = df_sorted.iloc[10:]
            total_flow = df_flow["2023"].sum()

            if not other_df.empty:
                base_color = "rgba(251, 146, 60, 0.7)" if flow_type == "Exports" else "rgba(96, 165, 250, 0.7)"
                heatmap_fig = create_other_items_heatmap(other_df, total_flow, flow_type, base_color)
                st.plotly_chart(heatmap_fig, config={"displayModeBar": False}, use_container_width=True)
            
            st.markdown("<h4 style='margin: 2rem 0 1rem 0;'>📋 Data Table</h4>", unsafe_allow_html=True)
            st.dataframe(df_flow, use_container_width=True, height=500)

if __name__ == "__main__":
    main()