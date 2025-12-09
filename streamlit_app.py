import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import altair as alt
import seaborn as sns
import base64
import os

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(page_title="Penguins", layout="wide")

# Path for logo
script_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(script_dir, "logo.jpeg")


# ---------------------------------------------------
# CUSTOM HEADER WITH LOGO + WHITE TEXT
# ---------------------------------------------------
with open(logo_path, "rb") as f:
    encoded_logo = base64.b64encode(f.read()).decode()

header_html = f"""
<style>
.custom-header {{
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #013220;
    padding: 12px 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}}

.custom-header img {{
    height: 60px;
    margin-right: 15px;
}}

.custom-header h1 {{
    color: white;
    font-size: 38px;
    margin: 0;
    font-weight: 700;
    letter-spacing: 1px;
}}
</style>

<div class="custom-header">
    <img src="data:image/jpeg;base64,{encoded_logo}">
    <h1>Penguins</h1>
</div>
"""

st.markdown(header_html, unsafe_allow_html=True)


# ---------------------------------------------------
# REMOVE STREAMLIT DEFAULT UI (toolbar, footer, etc.)
# ---------------------------------------------------
st.markdown(
    """
    <style>
        div[data-testid="stToolbar"] {visibility: hidden;}
        div[data-testid="stDecoration"] {visibility: hidden;}
        div[data-testid="stStatusWidget"] {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------
# DARK GREEN BACKGROUND + WHITE TEXT
# ---------------------------------------------------
st.markdown(
    """
    <style>
        .stApp {
            background-color: #013220 !important;
            color: white !important;
        }
        div.stMultiSelect label, div.stDateInput label {
            color: white !important;
        }
        div[data-baseweb="tag"] {
            background-color: green !important;
            color: yellow !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------
# SUBTITLE + DESCRIPTION
# ---------------------------------------------------
st.markdown(
    """
    <p style='text-align: center; color: white; font-size: 24px;'>
        by Louise Morley
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style='text-align: center; color: white; font-size: 20px;'>
        This is a dashboard about penguins!
    </p>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------
# SAMPLE DATA
# ---------------------------------------------------
np.random.seed(42)
data_db = pd.DataFrame({
    "Category": np.random.choice(["A", "B", "C", "D"], size=100),
    "Value": np.random.randint(10, 100, size=100),
    "Date": pd.date_range(start="2024-01-01", periods=100, freq="D")
})

# ---------------------------------------------------
# FILTERS
# ---------------------------------------------------
col1, col2 = st.columns([1, 1])

with col1:
    category_filter = st.multiselect(
        "Select Category",
        options=data_db["Category"].unique(),
        default=data_db["Category"].unique()
    )

with col2:
    date_range = st.date_input(
        "Select Date Range",
        [data_db["Date"].min(), data_db["Date"].max()],
        min_value=data_db["Date"].min(),
        max_value=data_db["Date"].max()
    )

filtered_data = data_db[
    (data_db["Category"].isin(category_filter)) &
    (data_db["Date"] >= pd.to_datetime(date_range[0])) &
    (data_db["Date"] <= pd.to_datetime(date_range[1]))
]


# ---------------------------------------------------
# PLOTS
# ---------------------------------------------------
fig_bar = px.bar(
    filtered_data.groupby("Category")["Value"].mean().reset_index(),
    x="Category",
    y="Value",
    title="Average Value by Category",
    text_auto=True,
    color_discrete_sequence=["#FFD700"]
)
fig_bar.update_layout(title=dict(x=0.5, xanchor="center"))

fig_line = px.line(
    filtered_data,
    x="Date",
    y="Value",
    title="Value Trend Over Time",
    markers=True,
    color_discrete_sequence=["#FFD700"]
)
fig_line.update_layout(title=dict(x=0.5, xanchor="center"))

fig_box = px.box(
    filtered_data,
    x="Category",
    y="Value",
    title="Value Distribution by Category",
    color_discrete_sequence=["#FFD700"]
)
fig_box.update_layout(title=dict(x=0.5, xanchor="center"))

color_map = {
    "A": "#FFD700",
    "B": "#FFCC00",
    "C": "#FFB800",
    "D": "#FF9900"
}

fig_scatter = px.scatter(
    filtered_data,
    x="Date",
    y="Value",
    color="Category",
    color_discrete_map=color_map,
    title="Scatter Plot of Value Over Time",
    size_max=10
)
fig_scatter.update_layout(
    title=dict(x=0.5, xanchor="center"),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=0.97,
        xanchor="center",
        x=0.45,
        title=None
    ),
    margin=dict(t=80)
)


# ---------------------------------------------------
# 2×2 GRID LAYOUT
# ---------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig_bar, use_container_width=True)
    st.write("\n".join(np.random.choice(["Example descriptive text block."], 4)))

    st.plotly_chart(fig_box, use_container_width=True)
    st.write("\n".join(np.random.choice(["Example descriptive text block."], 4)))

with col2:
    st.plotly_chart(fig_line, use_container_width=True)
    st.write("\n".join(np.random.choice(["Example descriptive text block."], 4)))

    st.plotly_chart(fig_scatter, use_container_width=True)
    st.write("\n".join(np.random.choice(["Example descriptive text block."], 4)))


# ---------------------------------------------------
# ALTair — Penguins Data
# ---------------------------------------------------
penguins = sns.load_dataset("penguins")

brush = alt.selection_interval()

points = alt.Chart(penguins, width=550).mark_point().encode(
    x=alt.X('flipper_length_mm:Q', scale=alt.Scale(domain=[170, 240])),
    y=alt.Y('bill_length_mm:Q', scale=alt.Scale(domain=[30, 65])),
    color=alt.condition(brush, "species:N", alt.value("lightgray"))
).add_params(brush)

bars = alt.Chart(penguins, width=550).mark_bar().encode(
    y='species:N',
    color=alt.Color('species:N', scale=alt.Scale(scheme='plasma')),
    x='count(species):Q'
).transform_filter(brush)

final_chart = (points & bars).configure_axis(
    grid=True,
    gridColor='lightgray',
    gridDash=[3, 3]
)

st.altair_chart(final_chart, use_container_width=True)


# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.markdown(
    """
    <style>
        .footer {
            text-align: center;
            font-size: 14px;
            color: rgba(255, 255, 255, 0.5);
            padding: 15px 0;
        }
    </style>
    <div class="footer">© 2025 My Dashboard</div>
    """,
    unsafe_allow_html=True
)
