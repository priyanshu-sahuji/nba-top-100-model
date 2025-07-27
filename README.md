# Top 100 NBA Players Quantification Model 🏀

A fully data-driven model that ranks the top 100 NBA players of all time based on statistical performance, accolades, and contextual adjustments since 1975.

## 📌 Overview
This project uses a weighted scoring system to evaluate and rank NBA players by combining:
- Key performance metrics (Win Shares, VORP, etc.)
- Accolades (MVPs, All-Stars, etc.)
- Normalized adjustments for era and height

## ⚙️ Features
- Clean and modular Python pipeline
- Streamlit-based web dashboard for interactive ranking and comparison
- Score computation using weighted KPIs and compensation factors
- Dynamic radar chart and bar graphs

## 📂 Project Structure
```
├── top_100_nba_model.py   # Main analysis and UI logic
├── players_stats.csv       # Input dataset with all player stats and awards
├── README.md               # Project description and usage guide
```

## 📥 Dataset Requirements
Ensure your `players_stats.csv` file includes the following columns:
- `Player`, `Peak_Year`, `Height`
- KPI columns: MVP_Share_1st, DPOY, Titles, Finals_MVP, Top3_VORP_Sum, Playoff_WS, Top3_WS48_Sum, Career_WS, AllNBA_1st, AllNBA_2nd, AllDefense_1st, AllDefense_2nd, AllStar

## 🚀 How to Run
1. Install dependencies:
```bash
pip install -r requirements.txt
```
2. Run the Streamlit app:
```bash
streamlit run top_100_nba_model.py
```
3. Use the format `sample_players_stats.csv` file.

## 📊 KPI Weightings
The score is calculated using a weighted combination of KPIs such as:
- MVP Share (2.6x)
- Career Win Shares (1.5x)
- All-NBA & All-Defense Teams
- Playoff metrics and peak-season stats

Adjustments are made only for:
- **Era (pre-1975 reduced weight)**
- **Player height (guards slightly boosted)**

## 📎 Notes
- ABA-specific adjustments have been removed.
- Data focuses strictly on NBA players post-1975.
- You can compare any two players and visualize their metrics side by side.

## 🏀 Heatmap of Top 100 NBA Players
![Top 100 Results Heatmap](https://raw.githubusercontent.com/priyanshu-sahuji/nba-top-100-model/main/Results.jpg)


---

Built with ❤️ for 🏀 by Priyanshu Sahu.

