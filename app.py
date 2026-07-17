import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIG & STYLING ---
st.set_page_config(
    page_title="Minimalist Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Minimalist CSS
st.markdown("""
    <style>
    .reportview-container { background: #fdfdfd; }
    h1, h2, h3 { font-weight: 400; color: #111111; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    div[data-testid="stMetricValue"] { font-size: 2rem; font-weight: 300; color: #222222; }
    div[data-testid="stMetricLabel"] { font-size: 0.85rem; color: #666666; text-transform: uppercase; letter-spacing: 0.5px; }
    hr { margin-top: 1rem; margin-bottom: 1rem; border-color: #eeeeee; }
    </style>
""", unsafe_allow_html=True)

# --- MOCK DATA CREATION ---
# Replace this chunk with reading your actual file: pd.read_csv('your_file.csv')
@st.cache_data
def load_data():
    data = {
        'Category': ['Electronics', 'Electronics', 'Apparel', 'Apparel', 'Home', 'Home', 'Office', 'Office'] * 25,
        'Subcategory': ['Phones', 'Laptops', 'Shirts', 'Shoes', 'Furniture', 'Decor', 'Paper', 'Pens'] * 25,
        'Region': ['North', 'East', 'South', 'West', 'North', 'East', 'South', 'West'] * 25,
        'Sales': [1200, 2400, 450, 800, 1500, 300, 150, 80] * 25,
        'Profit': [150, 400, 90, 120, -50, 45, 30, 15] * 25,
        'Rating': [4.2, 4.6, 4.0, 4.3, 3.8, 4.1, 4.5, 4.2] * 25
    }
    return pd.DataFrame(data)

df = load_data()

# --- SIDEBAR INTERACTIVE FILTERS ---
st.sidebar.markdown("### Filters")
st.sidebar.markdown("---")

# Filter 1: Dropdown (Multi-select)
selected_regions = st.sidebar.multiselect(
    "Select Region(s)",
    options=df['Region'].unique(),
    default=df['Region'].unique()
)

# Filter 2: Slider (Continuous variable coordination)
min_profit, max_profit = float(df['Profit'].min()), float(df['Profit'].max())
profit_range = st.sidebar.slider(
    "Profit Range Threshold",
    min_value=min_profit,
    max_value=max_profit,
    value=(min_profit, max_profit)
)

# --- DATA COORDINATION LOGIC ---
# Dynamically filtering dataframe based on UI states
filtered_df = df[
    (df['Region'].isin(selected_regions)) & 
    (df['Profit'] >= profit_range[0]) & 
    (df['Profit'] <= profit_range[1])
]

# --- MAIN DASHBOARD LAYOUT ---
st.title("Performance Summary")
st.markdown("A coordinated multi-chart exploration interface.")
st.markdown("---")

# Top Level Metrics (KPIs)
kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    st.metric("Total Filtered Sales", f"${filtered_df['Sales'].sum():,}")
with kpi2:
    st.metric("Net Profit Margin", f"{(filtered_df['Profit'].sum() / filtered_df['Sales'].sum() * 100):.1f}%" if filtered_df['Sales'].sum() > 0 else "0%")
with kpi3:
    st.metric("Average Item Rating", f"{filtered_df['Rating'].mean():.2f} ★")

st.markdown("---")

# Visualization Grid
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 1. Sales Distribution by Category")
    # Visualization 1: Minimal Bar Chart
    fig_bar = px.bar(
        filtered_df.groupby('Category', as_index=False)[['Sales', 'Profit']].sum(),
        x='Category',
        y='Sales',
        color_discrete_sequence=['#4A5568'],
        text_auto='.2s'
    )
    fig_bar.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, title=""),
        yaxis=dict(showgrid=True, gridcolor='#f0f0f0', title="Sales ($)"),
        margin=dict(l=20, r=20, t=10, b=20)
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    st.markdown("### 2. Profitability vs. Rating Scatter Matrix")
    # Visualization 2: Coordinated Scatter Plot
    fig_scatter = px.scatter(
        filtered_df,
        x='Rating',
        y='Profit',
        color='Category',
        color_discrete_sequence=['#3182CE', '#E53E3E', '#319795', '#D69E2E'],
        hover_data=['Subcategory']
    )
    fig_scatter.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor='#f0f0f0', title="Customer Rating"),
        yaxis=dict(showgrid=True, gridcolor='#f0f0f0', title="Profit ($)"),
        margin=dict(l=20, r=20, t=10, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("---")

# Full-width Breakdown Chart
st.markdown("### 3. Regional Segment Contribution Comparison")
# Visualization 3: Stacked Horizontal Breakdown
fig_breakdown = px.bar(
    filtered_df.groupby(['Region', 'Subcategory'], as_index=False)['Sales'].sum(),
    y='Region',
    x='Sales',
    color='Subcategory',
    orientation='h',
    color_discrete_sequence=px.colors.qualitative.Muted
)
fig_breakdown.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(showgrid=True, gridcolor='#f0f0f0', title="Aggregated Sales volume"),
    yaxis=dict(showgrid=False, title=""),
    margin=dict(l=20, r=20, t=10, b=20)
)
st.plotly_chart(fig_breakdown, use_container_width=True)
