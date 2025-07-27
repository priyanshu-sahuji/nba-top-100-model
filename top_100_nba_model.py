"""
Top 100 NBA Players Quantification Model

Ranks NBA players based on accolades, advanced stats, and era adjustments
using a weighted formula and normalization.

Author: Priyanshu Sahu
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.impute import SimpleImputer
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# ----------------------
# KPI Configuration
# ----------------------

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

# ----------------------
# Data Processing
# ----------------------

def load_player_data(filepath):
    return pd.read_csv(filepath)

def impute_missing_values(df):
    imputer = SimpleImputer(strategy='mean')
    df[df.columns] = imputer.fit_transform(df[df.columns])
    return df

def normalize_kpis(df):
    scaler = MinMaxScaler()
    df[KPI_COLUMNS] = scaler.fit_transform(df[KPI_COLUMNS])
    return df

def apply_compensation_factors(df):
    def era_factor(year):
        return 1.00 if year >= 1982 else 0.96 if year >= 1975 else 0.87 if year >= 1965 else 0.75 if year >= 1955 else 0.60
    def aba_factor(player):
        return 0.80 if player == 'Artis Gilmore' else 0.95 if player in ['Julius Erving', 'Rick Barry'] else 1.00
    def height_factor(height):
        return 1.12 if height <= 72 else 1.06 if height <= 74 else 1.02 if height <= 77 else 1.00

    df['Era_Factor'] = df['Peak_Year'].apply(era_factor)
    df['ABA_Factor'] = df['Player'].apply(aba_factor)
    df['Height_Factor'] = df['Height'].apply(height_factor)
    df['Compensation'] = df['Era_Factor'] * df['ABA_Factor'] * df['Height_Factor']
    return df

def compute_scores(df):
    for kpi, weight in KPI_WEIGHTS.items():
        df[f'{kpi}_Weighted'] = df[kpi] * weight
    df['Score'] = df[[f'{kpi}_Weighted' for kpi in KPI_WEIGHTS]].sum(axis=1)
    df['Score'] *= df['Compensation']
    return df

def rank_top_players(df, top_n=100):
    df = df.sort_values(by='Score', ascending=False)
    df['Rank'] = range(1, len(df) + 1)
    return df.head(top_n)

# ----------------------
# Streamlit UI
# ----------------------

def launch_interface(df):
    st.set_page_config(page_title="Top 100 NBA Players", layout="wide")
    st.title("🏀 Top 100 NBA Players of All Time")
    st.markdown("A data-driven ranking model blending accolades, stats, and historical context.")

    st.sidebar.header("🔍 Compare Players")
    players = df['Player'].tolist()
    p1 = st.sidebar.selectbox("Select Player 1", players)
    p2 = st.sidebar.selectbox("Select Player 2", players, index=1)

    if p1 != p2:
        comparison = df[df['Player'].isin([p1, p2])].set_index('Player')
        st.subheader("🔄 Player Comparison")
        st.dataframe(comparison[['Score'] + KPI_COLUMNS])

        st.subheader("📈 KPI Radar Chart")
        plot_radar_chart(comparison, KPI_COLUMNS)

    st.subheader("🏆 Top 100 Player Rankings")
    st.dataframe(df[['Rank', 'Player', 'Score'] + KPI_COLUMNS])

    st.subheader("📊 Top 10 Player Scores")
    fig, ax = plt.subplots()
    top10 = df.head(10).set_index('Player')
    top10['Score'].plot(kind='bar', ax=ax)
    ax.set_ylabel("Score")
    ax.set_title("Top 10 Player Scores")
    st.pyplot(fig)

def plot_radar_chart(df, kpis):
    import plotly.graph_objects as go
    df = df[kpis]
    categories = list(df.columns)
    fig = go.Figure()
    for idx, row in df.iterrows():
        fig.add_trace(go.Scatterpolar(r=row.values, theta=categories, fill='toself', name=idx))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

# ----------------------
# Main
# ----------------------

def main():
    df = load_player_data('players_stats.csv')
    df = impute_missing_values(df)
    df = normalize_kpis(df)
    df = apply_compensation_factors(df)
    df = compute_scores(df)
    top_players = rank_top_players(df)
    launch_interface(top_players)

if __name__ == "__main__":
    main()
