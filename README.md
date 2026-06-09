# mutual_fund_analytics_platform
# 📈 Mutual Fund Analytics Platform

A powerful, data-driven web platform designed to analyze, visualize, and track mutual fund performance. This platform helps investors and analysts evaluate risk, compare historical returns, and make informed portfolio allocation decisions.

---

## ✨ Features

* **Fund Performance Tracking:** Visualize historical Net Asset Value (NAV) data with interactive charts.
* **Risk Metrics Calculator:** Compute essential financial indicators including Sharpe Ratio, Alpha, Beta, and Standard Deviation to assess risk-adjusted returns.
* **Peer Comparison:** Compare multiple mutual funds side-by-side across various time horizons (1Y, 3Y, 5Y, CAGR).
* **Portfolio Simulation:** Model a hypothetical investment portfolio and track its consolidated growth and asset allocation.
* **Data Export:** Download analysis reports and historical data tables in CSV or PDF formats.

---


# ⚙️ Core System Architecture

The Mutual Fund Analytics Platform follows a structured end-to-end data pipeline that transforms raw mutual fund data into actionable investment insights.

## Architecture Flow

```text
📥 INGESTION TIER
│
├── AMFI CSV Datasets
└── MFAPI REST API Endpoints
        │
        ▼
🔧 TRANSFORMATION TIER
│
├── Data Cleaning
├── Type Validation
├── Missing Value Imputation
├── Duplicate Removal
└── Feature Engineering
        │
        ▼
🗄️ STORAGE TIER
│
└── SQLite Relational Database
        │
        ▼
🧮 ANALYTICS TIER
│
├── Return Analysis
├── Risk Analytics
├── Benchmark Comparison
├── Investor Analytics
└── Portfolio Analytics
        │
        ▼
📊 VISUALIZATION TIER
│
└── Power BI Interactive Dashboard
```

---

# 🛠️ Local Environment Setup

## Prerequisites

* Python 3.9+
* Git
* Jupyter Notebook
* Power BI Desktop

---

## 1️⃣ Clone Repository

```bash
git clone https://github.com/Varmalikith/mutual_fund_analytics_platform.git

cd mutual_fund_analytics_platform
```

---

## 2️⃣ Install Required Packages

```bash
pip install pandas numpy matplotlib seaborn plotly sqlalchemy requests scipy python-docx reportlab python-pptx jupyter
```

---

## 3️⃣ Execute Pipeline

```bash
python scripts/run_pipeline.py
```

### Pipeline Operations

The pipeline automatically:

* Loads raw datasets
* Cleans and validates records
* Creates SQLite tables
* Calculates performance metrics
* Generates analytics outputs
* Prepares dashboard-ready datasets

---

# 🧮 Advanced Analytics Engine

The platform includes multiple analytical modules for risk assessment, investor behavior analysis, and portfolio evaluation.

---

## 🎯 Fund Recommendation Engine

### Purpose

Provides fund recommendations based on investor risk appetite.

### Execution

```bash
python recommender.py "High"
```

### Supported Profiles

```text
Low
Moderate
High
```

### Sample Output

```text
🚀 BLUESTOCK AUTOMATED ADVISORY ENGINE

Risk Profile: HIGH

Top Recommended Funds

1. Quant Small Cap Fund
2. Nippon India Growth Fund
3. SBI Contra Fund

Recommendation completed successfully.
```

---

## 📉 Value at Risk (VaR) & Conditional VaR (CVaR)

### Output File

```text
outputs/var_cvar_report.csv
```

### Metrics Calculated

* Historical VaR (95%)
* Conditional VaR (Expected Shortfall)

### Business Value

* Measures downside risk
* Estimates potential losses during market stress
* Enables risk comparison across mutual funds

---

## 👥 Investor Cohort Analysis

### Output File

```text
outputs/cohort_analysis.csv
```

### Analysis Performed

* Investor acquisition year
* Average SIP contribution
* Total invested amount
* Fund category preference

### Business Value

* Understand investor lifecycle
* Identify valuable customer segments
* Support retention strategies

---

## 🚨 SIP Continuity Analysis

### Output File

```text
outputs/sip_continuity.csv
```

### Methodology

* Calculates average gap between SIP transactions
* Flags investors with gaps greater than 35 days

### Business Value

* Detects potential churn
* Helps improve investor retention
* Identifies inactive accounts

---

## 🏗️ Sector Concentration Risk Analysis

### Output File

```text
outputs/sector_hhi.csv
```

### Metric Used

Herfindahl-Hirschman Index (HHI)

```text
HHI = Σ (Sector Weight²)
```

### Interpretation

| HHI Range   | Concentration Level    |
| ----------- | ---------------------- |
| < 1500      | Low Concentration      |
| 1500 – 2500 | Moderate Concentration |
| > 2500      | High Concentration     |

### Business Value

* Measures portfolio diversification
* Identifies concentration risk
* Supports portfolio optimization

---

# 📊 Power BI Dashboard

The project includes a four-page interactive Power BI dashboard.

---

## Page 1: Market Overview

### Key Visuals

* Industry AUM
* SIP Inflow Trends
* Folio Growth
* Category-wise Inflows

### Key KPIs

* Total AUM
* Active SIP Accounts
* Monthly Inflows
* Folio Growth Rate

---

## Page 2: Fund Performance & Risk

### Key Visuals

* CAGR Comparison
* Sharpe Ratio Ranking
* Sortino Ratio Ranking
* Alpha & Beta Analysis
* Maximum Drawdown Comparison

### Key KPIs

* Best Performing Fund
* Highest Sharpe Ratio
* Lowest Drawdown
* Top Alpha Generator

---

## Page 3: Investor Demographics

### Key Visuals

* Age Distribution
* Income Distribution
* State-wise Transactions
* City Tier Analysis

### Key Insights

* Investor Age Patterns
* Geographic Penetration
* Transaction Behavior
* SIP Adoption Trends

---

## Page 4: Portfolio Holdings & Sector Exposure

### Key Visuals

* Sector Allocation
* Top Holdings
* Portfolio Concentration
* Fund Diversification

### Key Insights

* Sector Dominance
* Stock Exposure
* Diversification Score
* Concentration Risk

---

# 💼 Core Deliverables

## Reports

```text
reports/Final_Report.pdf
```

Comprehensive project report containing:

* Project Overview
* ETL Architecture
* EDA Findings
* Risk Analytics
* Dashboard Analysis
* Recommendations

---

## Presentation Deck

```text
reports/Bluestock_MF_Presentation.pptx
```

Executive presentation covering:

* Project Objectives
* Data Sources
* Architecture
* Analytics
* Dashboard Insights
* Business Recommendations

---

## Dashboard

```text
dashboard/Mutual_Fund_Dashboard.pbix
```

Interactive Power BI dashboard containing all visual analytics pages.

---

## Analytics Outputs

```text
outputs/fund_scorecard.csv
outputs/alpha_beta.csv
outputs/var_cvar_report.csv
outputs/cohort_analysis.csv
outputs/sector_hhi.csv
outputs/sip_continuity.csv
```

---

# ⚖️ Disclaimer

This project is developed strictly for educational and analytical purposes.

All financial metrics including:

* CAGR
* Sharpe Ratio
* Sortino Ratio
* Alpha
* Beta
* Value at Risk (VaR)
* Conditional Value at Risk (CVaR)

are computed using historical market data.

Past performance does not guarantee future returns.

The platform relies on publicly available datasets and APIs. Changes to source structures or API responses may require modifications to the ETL pipeline and database schema.
