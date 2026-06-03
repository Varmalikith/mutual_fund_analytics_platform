SELECT 
    amfi_code, 
    scheme_name, 
    fund_house, 
    category, 
    aum_crore
FROM fact_scheme_performance
ORDER BY aum_crore DESC
LIMIT 5;


SELECT 
    amfi_code,
    STRFTIME('%Y-%m', date) AS nav_month,
    ROUND(AVG(nav), 4) AS avg_nav
FROM fact_nav
GROUP BY amfi_code, nav_month
ORDER BY amfi_code, nav_month;

SELECT 
    month, 
    sip_inflow_crore, 
    yoy_growth_pct
FROM fact_monthly_sip_inflows
WHERE yoy_growth_pct IS NOT NULL
ORDER BY month;

SELECT 
    state,
    COUNT(*) AS total_transactions,
    SUM(amount_inr) AS total_invested_inr
FROM fact_transactions
GROUP BY state
ORDER BY total_invested_inr DESC;


SELECT 
    amfi_code, 
    scheme_name, 
    fund_house, 
    expense_ratio_pct
FROM dim_fund
WHERE expense_ratio_pct < 1.0
ORDER BY expense_ratio_pct ASC;


SELECT 
    stock_symbol, 
    stock_name, 
    sector, 
    ROUND(AVG(weight_pct), 2) AS avg_portfolio_weight_pct
FROM fact_portfolio_holdings
GROUP BY stock_symbol, stock_name, sector
ORDER BY avg_portfolio_weight_pct DESC
LIMIT 5;


SELECT 
    amfi_code, 
    scheme_name, 
    alpha, 
    sharpe_ratio, 
    risk_grade
FROM fact_scheme_performance
WHERE alpha > 0.0
ORDER BY alpha DESC;


SELECT 
    city_tier,
    COUNT(*) AS total_tx_count,
    SUM(amount_inr) AS total_volume_inr,
    ROUND(AVG(amount_inr), 2) AS avg_ticket_size_inr
FROM fact_transactions
GROUP BY city_tier;

SELECT 
    category,
    ROUND(SUM(net_inflow_crore), 2) AS total_net_inflow_crore
FROM fact_category_inflows
GROUP BY category
ORDER BY total_net_inflow_crore DESC;

SELECT 
    amfi_code, 
    scheme_name, 
    sharpe_ratio, 
    risk_grade
FROM fact_scheme_performance
WHERE is_negative_sharpe = 1
ORDER BY sharpe_ratio ASC;