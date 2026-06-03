# 📘 Bluestock Mutual Fund Analytics Platform - Data Dictionary

This document provides a comprehensive schema reference for the relational SQLite database (`bluestock_mf.db`). The database is structured as a normalized Star Schema designed to facilitate fast mutual fund engineering, performance tracking, and interactive dashboard analytics.

---

## 🗺️ Schema Relationship Map

* **dim_fund** (Master Dimension) acts as the primary lookup hub.
* **fact_nav**, **fact_transactions**, **fact_portfolio_holdings**, and **fact_scheme_performance** link to `dim_fund` via the common key `amfi_code`.
* Macro industry trend tables link together logically across the timeline via the `month` or `date` attributes.

---

## 🗄️ Table Specifications

### 1. dim_fund (Dimension Table)
* **Description:** Contains the master descriptive registry for all 40 unique mutual fund schemes.
* **Source:** `01_fund_master.csv`

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `amfi_code` | INTEGER | PRIMARY KEY | Unique 6-digit identifier for the mutual fund scheme. |
| `fund_house` | TEXT | NOT NULL | Name of the Asset Management Company (e.g., SBI Mutual Fund). |
| `scheme_name` | TEXT | NOT NULL | Full official name of the mutual fund scheme. |
| `category` | TEXT | - | Asset class category (Equity / Debt). |
| `sub_category` | TEXT | - | Specific fund category (Large Cap, Small Cap, Gilt, etc.). |
| `plan` | TEXT | - | Distribution type (Regular / Direct). |
| `launch_date` | TEXT | - | The official launch date of the scheme (YYYY-MM-DD). |
| `benchmark` | TEXT | - | The official market index used for fund benchmarking. |
| `expense_ratio_pct`| REAL | - | Annual management fee charged by the fund in %. |
| `exit_load_pct` | REAL | - | Percentage penalty charged if units are redeemed early. |
| `min_sip_amount` | INTEGER | - | Minimum allowable Systematic Investment Plan amount (INR). |
| `min_lumpsum_amount`| INTEGER| - | Minimum allowable one-time investment amount (INR). |
| `fund_manager` | TEXT | - | Name of the primary portfolio fund manager. |
| `risk_category` | TEXT | - | SEBI-defined risk tier (Low, Moderate, High, Very High). |
| `sebi_category_code`| TEXT | - | Internal regulatory category code (e.g., EC01, EC03). |

---

### 2. fact_nav (Fact Table)
* **Description:** Tracks the daily continuous pricing timeline (Net Asset Value) for all mutual fund schemes. Expanded to full calendar days via forward-fill handling.
* **Source:** `02_nav_history.csv` (Processed via Task 1)

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `amfi_code` | INTEGER | FOREIGN KEY | References `dim_fund(amfi_code)`. |
| `date` | TEXT | NOT NULL | The date of the NAV entry (YYYY-MM-DD). |
| `nav` | REAL | NOT NULL | The price value per unit of the scheme on that day. |
| **Composite PK** | `(amfi_code, date)` | PRIMARY KEY | Guarantees exactly one unique price entry per fund per day. |

---

### 3. fact_transactions (Fact Table)
* **Description:** Captures individual investor deposit, withdrawal, and purchasing activity across states and demographic cohorts.
* **Source:** `08_investor_transactions.csv` (Processed via Task 2)

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `tx_id` | INTEGER | PRIMARY KEY AUTOINCREMENT | System-generated unique transaction tracking number. |
| `investor_id` | TEXT | NOT NULL | Unique lookup code for individual retail investors. |
| `transaction_date` | TEXT | NOT NULL | The execution date of the transaction (YYYY-MM-DD). |
| `amfi_code` | INTEGER | FOREIGN KEY | References `dim_fund(amfi_code)`. |
| `transaction_type` | TEXT | NOT NULL | Category of movement: `SIP`, `Lumpsum`, or `Redemption`. |
| `amount_inr` | INTEGER | NOT NULL | Total financial volume of the transaction in Indian Rupees. |
| `state` | TEXT | - | Indian state location of the retail investor. |
| `city` | TEXT | - | City location of the retail investor. |
| `city_tier` | TEXT | - | Geographic sorting: `T30` (Top 30) or `B30` (Beyond Top 30). |
| `age_group` | TEXT | - | Demographic bracket of the investor (e.g., 18-25, 26-35). |
| `gender` | TEXT | - | Gender classification of the investor. |
| `annual_income_lakh`| REAL | - | Self-reported annual income of the investor in Lakhs INR. |
| `payment_mode` | TEXT | - | Method used for payment execution (UPI, Net Banking, etc.). |
| `kyc_status` | TEXT | - | Standardized industry verification state (`Verified` / `Pending`). |

---

### 4. fact_scheme_performance (Fact Table)
* **Description:** Holds core trailing returns alongside historical volatility and risk-adjusted return ratios for every fund.
* **Source:** `07_scheme_performance.csv` (Processed via Task 3)

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `amfi_code` | INTEGER | PRIMARY KEY, FOREIGN KEY | Maps directly back to `dim_fund(amfi_code)`. |
| `scheme_name` | TEXT | - | Duplicate string copy of scheme name for clean joins. |
| `fund_house` | TEXT | - | Name of the managing Asset Management Company. |
| `category` | TEXT | - | Asset sorting type. |
| `plan` | TEXT | - | Plan tier distribution format. |
| `return_1yr_pct` | REAL | - | 1-Year absolute calculated return percentage. |
| `return_3yr_pct` | REAL | - | 3-Year compounded annual growth rate (CAGR %). |
| `return_5yr_pct` | REAL | - | 5-Year compounded annual growth rate (CAGR %). |
| `benchmark_3yr_pct` | REAL | - | 3-Year performance CAGR percentage of the official benchmark index. |
| `alpha` | REAL | - | Outperformance metric relative to the benchmark index. |
| `beta` | REAL | - | Volatility sensitivity scale relative to the benchmark market. |
| `sharpe_ratio` | REAL | - | Risk-adjusted returns factor relative to volatility. |
| `sortino_ratio` | REAL | - | Risk-adjusted returns factor penalizing only downside volatility. |
| `std_dev_ann_pct` | REAL | - | Annualized standard deviation of historical daily returns. |
| `max_drawdown_pct` | REAL | - | Maximum historical peak-to-trough decline percentage. |
| `aum_crore` | INTEGER | - | Total scheme-level Assets Under Management in Crores INR. |
| `expense_ratio_pct`| REAL | - | Cleaned operational expense ratio percentage. |
| `morningstar_rating`| INTEGER | - | Categorical quality score scale from 1 to 5 stars. |
| `risk_grade` | TEXT | - | Plain-text evaluation of fund risk behavior profiles. |
| `is_negative_sharpe`| INTEGER | - | Boolean audit indicator (1 = True, 0 = False). |

---

### 5. fact_portfolio_holdings (Fact Table)
* **Description:** Breaks down the underlying stock company asset compositions and sector weights for each fund.
* **Source:** `09_portfolio_holdings.csv`

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `amfi_code` | INTEGER | FOREIGN KEY | References `dim_fund(amfi_code)`. |
| `stock_symbol` | TEXT | NOT NULL | NSE/BSE public equity ticker symbol (e.g., HDFCBANK). |
| `stock_name` | TEXT | - | Corporate name of the holding company asset. |
| `sector` | TEXT | - | Macro business industry sector classification (e.g., Banking). |
| `weight_pct` | REAL | - | Allocation weight percentage of the asset inside the fund. |
| `market_value_cr` | REAL | - | Capital valuation size of holding in Crores INR. |
| `current_price_inr` | REAL | - | Trading price of the underlying equity stock in INR. |
| `portfolio_date` | TEXT | - | Snapshot timestamp of the portfolio registry data. |
| **Composite PK** | `(amfi_code, stock_symbol)` | PRIMARY KEY | Maps stock distribution metrics directly back to each mutual fund scheme. |

---

### 6. fact_benchmark_indices (Fact Table)
* **Description:** Stores historical closing values for benchmark market indices like NIFTY50 and BSE SmallCap.
* **Source:** `10_benchmark_indices.csv`

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `date` | TEXT | NOT NULL | The market trading day date (YYYY-MM-DD). |
| `index_name` | TEXT | NOT NULL | Name of the benchmark index tracker (e.g., NIFTY50). |
| `close_value` | REAL | NOT NULL | Real daily price valuation metric of the index. |
| **Composite PK** | `(date, index_name)`| PRIMARY KEY | Records exactly one historical market closing marker per index per day. |

---

### 7. fact_aum_fund_house (Fact Table)
* **Description:** Monitors broad asset growth trends across the 10 major asset management organizations over time.
* **Source:** `03_aum_by_fund_house.csv`

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `date` | TEXT | NOT NULL | Reporting date of the asset balance (YYYY-MM-DD). |
| `fund_house` | TEXT | NOT NULL | Name of the primary corporate Asset Management Company. |
| `aum_lakh_crore` | REAL | - | Industry valuation sizing mapped in Lakh Crores INR. |
| `aum_crore` | INTEGER | - | Valuation sizing mapped in Crores INR. |
| `num_schemes` | INTEGER | - | Total active fund scheme options managed by that fund house. |
| **Composite PK** | `(date, fund_house)`| PRIMARY KEY | Tracks periodic asset size shifts per AMC. |

---

### 8. fact_monthly_sip_inflows (Fact Table)
* **Description:** Measures systematic investment framework growth parameters for the Indian industry.
* **Source:** `04_monthly_sip_inflows.csv`

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `month` | TEXT | PRIMARY KEY | Timestamp reference index mapped in YYYY-MM structure. |
| `sip_inflow_crore` | INTEGER | - | Aggregated systematic monthly inflow value in Crores INR. |
| `active_sip_accounts_crore`| REAL | - | Aggregated active retail investor plan registries in Crores. |
| `new_sip_accounts_lakh`| REAL | - | Brand new systematic contract accounts created during the month (Lakhs). |
| `sip_aum_lakh_crore` | REAL | - | Total overall industry capital value backed by systematic flows. |
| `yoy_growth_pct` | REAL | - | Year-over-year percentage expansion metric. |

---

### 9. fact_category_inflows (Fact Table)
* **Description:** Breaks down monthly net inflows across specific market sectors (Large Cap, Mid Cap, Small Cap, etc.).
* **Source:** `05_category_inflows.csv`

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `month` | TEXT | NOT NULL | Reporting date period mapped in YYYY-MM format. |
| `category` | TEXT | NOT NULL | Specific fund capitalization or structure style. |
| `net_inflow_crore` | REAL | - | Net monthly investment capital entering the asset sub-class. |
| **Composite PK** | `(month, category)` | PRIMARY KEY | Maps cash flow choices to market sub-classes. |

---

### 10. fact_industry_folio_count (Fact Table)
* **Description:** Measures total account creation metrics across major investment classes (Equity, Debt, Hybrid).
* **Source:** `06_industry_folio_count.csv`

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `month` | TEXT | PRIMARY KEY | Reporting time checkpoint index mapped in YYYY-MM structure. |
| `total_folios_crore` | REAL | - | Aggregated total industry investor account accounts in Crores. |
| `equity_folios_crore`| REAL | - | Total equity strategy investor accounts in Crores. |
| `debt_folios_crore` | REAL | - | Total debt strategy investor accounts in Crores. |
| `hybrid_folios_crore`| REAL | - | Total asset-blended strategy accounts in Crores. |
| `others_folios_crore`| REAL | - | Other strategy asset classification profiles in Crores. | 