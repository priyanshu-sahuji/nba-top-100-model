"""
Top 100 NBA Players Quantification Model

Ranks NBA players based on accolades, advanced statistics, and era adjustments
using a weighted scoring formula and normalization techniques.

Author: Priyanshu Sahu
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.impute import SimpleImputer
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

# -----------------------------
# KPI Configuration
# -----------------------------

KPI_COLUMNS = [
    'MVP_Share_1st', 'DPOY', 'Titles', 'Finals_MVP', 'Top3_VORP_Sum',
    'Playoff_WS', 'Top3_WS48_Sum', 'Career_WS', 'AllNBA_1st', 'AllNBA_2nd',
    'AllDefense_1st', 'AllDefense_2nd', 'AllStar', 'Height'
]

KPI_WEIGHTS = {
    'MVP_Share_1st': 2.6,
    'DPOY': 0.35,
    'Titles': 0.5,
    'Finals_MVP': 1.0,
    'AllNBA_1st': 1.5,
    'AllDefense_1st': 0.6,
    'AllStar': 1.0,
    'Top3_VORP_Sum': 1.0,
    'Top3_WS48_Sum': 1.0,
    'Career_WS': 1.5,
    'Playoff_WS': 1.0,
    'AllNBA_2nd': 0.75,
    'AllDefense_2nd': 0.3,
    'Height': 0.2
}

# -----------------------------
# Data Processing Functions
# -----------------------------

def load_player_data(filepath):
    """Loads the player data from a CSV file."""
    return pd.read_csv(filepath)

def impute_missing_values(df):
    """Fills missing values in the dataframe using mean imputation."""
    imputer = SimpleImputer(strategy='mean')
    df[df.columns] = imputer.fit_transform(df[df.columns])
    return df

def normalize_kpis(df):
    """Normalizes KPI columns using Min-Max scaling."""
    scaler = MinMaxScaler()
    df[KPI_COLUMNS] = scaler.fit_transform(df[KPI_COLUMNS])
    return df

def apply_compensation_factors(df):
    """Applies era and height compensation factors to each player. ABA adjustment removed."""
    def era_adjustment(year):
        if year >= 1982:
            return 1.00
        elif year >= 1975:
            return 0.96
        else:
            return 0.87

    def height_adjustment(height):
        if height <= 72:
            return 1.12
        elif height <= 74:
            return 1.06
        elif height <= 77:
            return 1.02
        return 1.00

    df['Era_Factor'] = df['Peak_Year'].apply(era_adjustment)
    df['Height_Factor'] = df['Height'].apply(height_adjustment)
    df['Compensation'] = df['Era_Factor'] * df['Height_Factor']
    return df

def compute_scores(df):
    """Calculates a weighted score for each player based on normalized KPIs and compensation."""
    for kpi, weight in KPI_WEIGHTS.items():
        df[f'{kpi}_Weighted'] = df[kpi] * weight

    df['Score'] = df[[f'{kpi}_Weighted' for kpi in KPI_WEIGHTS]].sum(axis=1)
    df['Score'] *= df['Compensation']
    return df

def rank_top_players(df, top_n=100):
    """Ranks players based on their score and returns the top N players."""
    df = df.sort_values(by='Score', ascending=False)
    df['Rank'] = range(1, len(df) + 1)
    return df.head(top_n)

# -----------------------------
# Visualization Functions
# -----------------------------

def plot_radar_chart(df, kpis):
    """Plots a radar chart comparing KPIs of selected players."""
    categories = kpis
    fig = go.Figure()
    for idx, row in df[kpis].iterrows():
        fig.add_trace(go.Scatterpolar(
            r=row.values,
            theta=categories,
            fill='toself',
            name=idx
        ))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Streamlit Interface
# -----------------------------

def launch_interface(df):
    """Launches the Streamlit web interface for the project."""
    st.set_page_config(page_title="Top 100 NBA Players", layout="wide")
    st.title("🏀 Top 100 NBA Players of All Time")
    st.markdown("A data-driven ranking model blending accolades, stats, and historical context.")

    st.sidebar.header("🔍 Compare Players")
    players = df['Player'].tolist()
    player1 = st.sidebar.selectbox("Select Player 1", players)
    player2 = st.sidebar.selectbox("Select Player 2", players, index=1)

    if player1 != player2:
        comparison_df = df[df['Player'].isin([player1, player2])].set_index('Player')
        st.subheader("🔄 Player Comparison")
        st.dataframe(comparison_df[['Score'] + KPI_COLUMNS])

        st.subheader("📈 KPI Radar Chart")
        plot_radar_chart(comparison_df, KPI_COLUMNS)

    st.subheader("🏆 Top 100 Player Rankings")
    st.dataframe(df[['Rank', 'Player', 'Score'] + KPI_COLUMNS])

    st.subheader("📊 Top 10 Player Scores")
    fig, ax = plt.subplots()
    top10 = df.head(10).set_index('Player')
    top10['Score'].plot(kind='bar', ax=ax)
    ax.set_ylabel("Score")
    ax.set_title("Top 10 Player Scores")
    st.pyplot(fig)

# -----------------------------
# Entry Point
# -----------------------------

def main():
    """Main function to run the full pipeline and UI."""
    df = load_player_data('players_stats.csv')
    df = impute_missing_values(df)
    df = normalize_kpis(df)
    df = apply_compensation_factors(df)
    df = compute_scores(df)
    top_players = rank_top_players(df)
    launch_interface(top_players)

if __name__ == "__main__":
    main()
