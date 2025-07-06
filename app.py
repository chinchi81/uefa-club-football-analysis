# ┌────────────────────────────────────────────────────────────┐
# │ Streamlit Dashboard: Two-Leg Qualification Insights        │
# └────────────────────────────────────────────────────────────┘

import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df_stats = pd.read_csv("qualification_stats.csv")          # Leg-level and Elo stats
qual_by_gd = pd.read_csv("qualification_by_gd.csv")        # GD-dependent qualification

st.set_page_config(page_title="UEFA Qualification Dashboard", layout="wide")

st.title("🏆 Two-Leg Qualification Simulation Dashboard")
st.markdown("Analyze win probabilities, Elo profiles, and leg-wise performance")

# Sidebar filters
teams = sorted(set(df_stats["Team 1"]).union(df_stats["Team 2"]))
team_filter = st.sidebar.selectbox("🔍 Filter by team", ["All"] + teams)

filtered_df = df_stats.copy()
if team_filter != "All":
    filtered_df = filtered_df[(filtered_df["Team 1"] == team_filter) | (filtered_df["Team 2"] == team_filter)]

# Section 1: Table summary
st.subheader("📋 Qualification Summary")
st.dataframe(filtered_df.style.format({
    "Team 1 Win %": "{:.1f}%", "Team 2 Win %": "{:.1f}%",
    "1st Leg Win % T1": "{:.1f}%", "1st Leg Win % T2": "{:.1f}%", "1st Leg Draw %": "{:.1f}%",
    "2nd Leg Win % T1": "{:.1f}%", "2nd Leg Win % T2": "{:.1f}%", "2nd Leg Draw %": "{:.1f}%"
}))

# Section 2: Elo plot
st.subheader("📈 Elo Ratings (1st Leg)")
elo_plot = px.scatter(
    filtered_df,
    x="Team 1 Elo",
    y="Team 2 Elo",
    color="Team 1 Win %",
    hover_data=["Team 1", "Team 2"],
    labels={"Team 1 Elo": "Team 1 Elo", "Team 2 Elo": "Team 2 Elo"},
    title="Elo Comparison (Team 1 vs Team 2)"
)
st.plotly_chart(elo_plot, use_container_width=True)

# Section 3: Qualification by GD
st.subheader("🎯 Qualification Odds by 1st Leg Goal Difference")
gd_plot = px.bar(
    qual_by_gd,
    x="1st Leg GD",
    y=["Team 1 Qualification %", "Team 2 Qualification %"],
    barmode="group",
    labels={"value": "Qualification %"},
    title="How 1st Leg Scorelines Shape Qualification Odds"
)
st.plotly_chart(gd_plot, use_container_width=True)