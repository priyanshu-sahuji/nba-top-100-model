# 🏀 Top 100 NBA Players Quantification Model

A streamlined, data-driven model to rank the greatest NBA players of all time. This project blends accolades, stats, and era-based adjustments into a unified scoring system.

---

## 🔍 Overview

This model ranks the top 100 NBA players using a custom formula that weighs:

* Individual accolades (MVPs, All-NBA, All-Star)
* Team success (Championships, Finals MVPs)
* Advanced statistics (VORP, Win Shares)
* Historical context (era adjustments, ABA compensation, height factor)

It’s designed to provide objective comparisons across generations.

---

## 📊 Features

* 🧮 Weighted scoring combining performance and recognition
* 📈 Era, ABA, and height-based compensation factors
* 🏆 Retroactive accolades for early legends
* 📊 Normalization and regression-based calibration
* 🧩 Modular design for easy updates and extensions

---

## 🧮 How Scoring Works

Each player is evaluated on a weighted sum of the following metrics:

* `MVP_Share_1st` — First-place MVP vote share
* `DPOY` — Defensive Player of the Year awards
* `Titles`, `Finals_MVP` — Team championship indicators
* `AllNBA`, `AllDefense`, `AllStar` — Selection-based achievements
* `Top3_VORP_Sum`, `Top3_WS48_Sum`, `Career_WS`, `Playoff_WS` — Longevity and peak performance metrics
* `Height` — Height-based compensation for guards

---

## 📂 Project Structure

```
nba-top-100-model/
│
├── top_100_nba_model.py      # Main ranking logic
├── players_stats.csv         # Player stats and accolades
├── README.md                 # Project overview and instructions
└── requirements.txt          # Dependencies
```

---

## ⚙️ Getting Started

Run the project locally with these steps:

```bash
pip install -r requirements.txt
streamlit run top_100_nba_model.py
```

A Streamlit dashboard will launch with rankings, filters, and interactive charts.

---

## 🗃️ Dataset Schema

The dataset contains structured stats and achievements for all included players:

```
Player, Peak_Year, Height, MVP_Share_1st, DPOY, Titles, Finals_MVP,
Top3_VORP_Sum, Playoff_WS, Top3_WS48_Sum, Career_WS,
AllNBA_1st, AllNBA_2nd, AllDefense_1st, AllDefense_2nd, AllStar
```

---

## ⚠️ Limitations

* Retroactive awards are based on historical research and estimations.
* Cultural and off-court legacy factors are excluded.
* Rankings are data-driven and may differ from public consensus.

---

## 🤝 Contributing

Ideas, feature requests, or data improvements are welcome! To contribute:

* Fork the repo
* Open a pull request
* Suggest improvements or corrections

---

## 📄 License

Licensed under the MIT License — free for public and commercial use.

---

Made with ❤️ for basketball analytics by **Priyanshu Sahu**
