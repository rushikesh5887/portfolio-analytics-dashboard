> **Interactive, data-driven portfolio analytics and decision-support dashboard built with Python and Streamlit.**
>
> Built an end-to-end analytical application that transforms transaction-level investment records into portfolio valuation, allocation, profit-and-loss, dividend, mutual fund, and historical investment insights.
>
> The application demonstrates an end-to-end workflow from raw financial data processing to interactive visualization and cloud deployment.

![Domain](https://img.shields.io/badge/Domain-Financial%20Data%20Analytics-blue)
![Focus](https://img.shields.io/badge/Focus-Portfolio%20Analytics-blueviolet)
![Platform](https://img.shields.io/badge/Platform-Streamlit-success)
![Status](https://img.shields.io/badge/Status-Deployed-success)

<p align="center">
  <a href="#overview">Overview</a> •
  <a href="#tasks">Tasks</a> •
  <a href="#skills">Skills</a> •
  <a href="#architecture">Architecture</a> •
  <a href="#analytics">Analytics</a> •
  <a href="#deployment">Deployment</a>
</p>

-------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 🚀 Live Application

### [Interactive Portfolio Analytics Dashboard](https://ra-portfolio-analytics.streamlit.app)

The dashboard provides an interactive interface to explore portfolio holdings, investment history, mutual funds, dividends, valuations, and profit-and-loss metrics.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 🧠 Overview

Investment information is often distributed across transaction ledgers, brokerage statements, spreadsheets, and manually maintained records.

This project converts these heterogeneous records into a structured analytical workflow that provides a consistent view of:

- Invested capital
- Current portfolio valuation
- Unrealized profit and loss
- Portfolio allocation
- Equity holdings
- Mutual fund investments
- Dividend income
- Historical investments
- Portfolio-level performance indicators

Rather than producing a static report, the project was developed as an **interactive analytical data product** where the underlying data can be processed and explored through a single application.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 🔑 Key Contributions

- 📊 Developed an interactive portfolio analytics dashboard using Python and Streamlit
- 🔄 Transformed transaction-level records into structured portfolio-level analytics
- 💰 Calculated invested capital, current valuation, and unrealized P&L
- 📈 Built interactive equity portfolio analysis and allocation views
- 🏦 Developed dedicated mutual fund analytics
- 💵 Integrated historical dividend data and income analysis
- 📅 Converted transaction records into yearly investment analysis
- 🔍 Built reusable data-processing pipelines for financial records
- 🌐 Deployed the application as a publicly accessible web application
- 🔧 Implemented an end-to-end workflow from raw data → analytics → visualization → deployment

-------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-Data%20Analytics-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Wrangling-purple?logo=pandas)
![NumPy](https://img.shields.io/badge/NumPy-Numerical%20Computation-teal?logo=numpy)
![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Visualization-orange?logo=plotly)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?logo=streamlit)
![Git](https://img.shields.io/badge/Git-Version%20Control-black?logo=git)
![GitHub](https://img.shields.io/badge/GitHub-Repository-black?logo=github)

**Core technologies:**

- **Python:** `pandas`, `numpy`
- **Visualization:** `Plotly`
- **Dashboard:** `Streamlit`
- **Data Processing:** CSV-based analytical pipelines
- **Version Control:** Git / GitHub
- **Deployment:** Streamlit Community Cloud

-------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 🎯 Analytical Tasks

<a id="tasks"></a>

### 1️⃣ Portfolio Valuation

- Processed individual portfolio holdings
- Calculated total invested capital
- Calculated current market valuation
- Computed unrealized profit and loss
- Derived portfolio-level performance indicators

**Capability:** Portfolio valuation + financial data aggregation

---

### 2️⃣ Equity Portfolio Analysis

- Developed interactive views of individual equity holdings
- Analyzed allocation across securities
- Identified gains and losses across holdings
- Generated portfolio concentration and performance views
- Enabled interactive filtering and exploration

**Capability:** Equity analytics + portfolio allocation analysis

---

### 3️⃣ Mutual Fund Analytics

- Processed mutual fund transaction and valuation data
- Compared invested amount against current valuation
- Calculated absolute returns
- Developed visual comparisons across funds

**Capability:** Mutual fund performance analysis + comparative visualization

---

### 4️⃣ Dividend Analytics

- Processed historical dividend transactions
- Aggregated dividend income
- Created historical dividend views
- Integrated dividend information into the broader portfolio analytics workflow

**Capability:** Income analytics + transaction-level financial data processing

---

### 5️⃣ Historical Investment Analysis

- Converted transaction-level records into yearly investment summaries
- Aggregated capital deployed over time
- Analyzed historical investment patterns
- Connected transaction-level activity with portfolio-level outcomes

**Capability:** Time-based financial analytics + historical trend analysis

-------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 📊 Analytics and Visualizations

<a id="analytics"></a>

The dashboard provides interactive analytical views including:

### Portfolio Overview

- Total invested amount
- Current valuation
- Unrealized P&L
- Portfolio-level return indicators
- Asset allocation

### Equity Analytics

- Individual holding performance
- Investment versus current valuation
- Gain/loss analysis
- Portfolio concentration

### Mutual Funds

- Invested amount versus current valuation
- Fund-level returns
- Comparative visualizations

### Dividends

- Historical dividend income
- Dividend aggregation
- Income trends

### Historical Investments

- Yearly investment amounts
- Historical capital deployment
- Investment trends

-------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 🧩 Code Architecture

<a id="architecture"></a>

### System Workflow

```text
Raw Financial Records
        │
        ▼
Data Cleaning & Validation
        │
        ▼
Transaction-Level Processing
        │
        ├───────────────┐
        │               │
        ▼               ▼
Portfolio Holdings   Transaction Ledger
        │               │
        ▼               ▼
Valuation & P&L     Historical Analysis
        │               │
        ├───────┬───────┤
        │       │       │
        ▼       ▼       ▼
    Equity   Mutual   Dividends
   Analytics  Funds   Analytics
        │       │       │
        └───────┴───────┘
                │
                ▼
      Interactive Visualization
                │
                ▼
          Streamlit Dashboard
                │
                ▼
       Cloud Deployment
