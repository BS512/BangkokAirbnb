import streamlit as st
import altair as alt
import pandas as pd

# Set page layout to wide for better visualization display
st.set_page_config(layout="wide")

st.title("Global Wealth & Health Metrics")
st.subheader("Interactive Data Exploration Framework")

# 1. Load the dataset safely
@st.cache_data
def load_data():
    # Make sure 'oecd-wealth-health-2014(1).csv' is in your working app directory
    df = pd.read_csv("oecd-wealth-health-2014(1).csv")
    return df

df = load_data()

# 2. Instantiate Interactive Selection Rules (Altair 4.2 Compatible Syntax)
# - brush: dragging an interval box on the scatter plot filters the bar chart records
# - click: clicking bars on the bar chart highlights specific groups on the scatter plot
brush = alt.selection_interval()
click = alt.selection_multi(fields=['Region'])

# 3. Build View A: Income vs Life Expectancy Scatter Plot
scatter_plot = alt.Chart(df).mark_circle().encode(
    x=alt.X('Income:Q', scale=alt.Scale(type='log'), title='Income per Capita (Log Scale)'),
    y=alt.Y('LifeExpectancy:Q', scale=alt.Scale(domain=[40, 90]), title='Life Expectancy (Years)'),
    color=alt.condition(click, 'Region:N', alt.value('#e2e8f0'), title="Region"),
    size=alt.Size('Population:Q', scale=alt.Scale(range=[20, 600]), legend=None),
    opacity=alt.condition(brush, alt.value(0.75), alt.value(0.15)),
    tooltip=['Country:N', 'Region:N', 'Income:Q', 'LifeExpectancy:Q']
).properties(
    width=550,
    height=400,
    title="Drag an interval box here to filter regional counts"
).add_selection(
    brush
)

# 4. Build View B: Regional Aggregate Counter Bar Chart
bar_chart = alt.Chart(df).mark_bar().encode(
    x=alt.X('count():Q', title='Number of Selected Countries'),
    y=alt.Y('Region:N', sort='-x', title=None),
    color=alt.condition(click, 'Region:N', alt.value('#e2e8f0'), legend=None),
    opacity=alt.condition(brush, alt.value(1.0), alt.value(0.35))
).properties(
    width=300,
    height=400,
    title="Click bars here to highlight coordinates on left"
).transform_filter(
    brush
).add_selection(
    click
)

# 5. Link the layouts together into a single unified workspace view
interactive_dashboard = alt.hconcat(
    scatter_plot,
    bar_chart
).configure_view(
    strokeWidth=0
).configure_title(streamlit run app.py
    fontSize=14,
    font='Helvetica Neue',
    anchor='start',
    color='#1e293b'
)

# 6. Render chart component in Streamlit
st.altair_chart(interactive_dashboard, use_container_width=True)streamlit run app.py