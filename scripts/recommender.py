
import pandas as pd
from pathlib import Path
import sys

def get_fund_recommendations(risk_appetite, dataset_path):
    """
    Filters and returns the top 3 mutual funds matching an investor's risk tier 
    sorted by their risk-adjusted Sharpe Ratio performance efficiency.
    """
    # 1. Gracefully read the generated scorecard tracking tier
    if not Path(dataset_path).exists():
        print(f" Error: Database asset scorecard not found at {dataset_path}")
        return None
        
    df_scorecard = pd.read_csv(dataset_path)
    
    # 2. Normalize input casing strings to avoid matching mismatch errors
    user_risk = str(risk_appetite).strip().capitalize()
    
    if user_risk not in ['Low', 'Moderate', 'High']:
        print(" Error: Invalid risk profile input. Please choose 'Low', 'Moderate', or 'High'.")
        return None

    # 3. Handle data mapping filters safely depending on the asset risk columns present
    # Map the user risk profile directly to fund classifications (e.g., Equity=High, Debt=Low, Hybrid/Other=Moderate)
    category_mapping = {
        'Low': ['Debt', 'Liquid', 'Money Market'],
        'High': ['Equity', 'Sectoral', 'Small Cap', 'Mid Cap'],
        'Moderate': ['Hybrid', 'Balanced', 'Large Cap']
    }
    
    # Determine fallback strategy if an explicit 'risk_grade' column isn't found in the file
    if 'risk_grade' in df_scorecard.columns:
        df_filtered = df_scorecard[df_scorecard['risk_grade'].str.capitalize() == user_risk]
    elif 'category' in df_scorecard.columns:
        target_categories = category_mapping[user_risk]
        df_filtered = df_scorecard[df_scorecard['category'].str.contains('|'.join(target_categories), case=False, na=False)]
    else:
        # Fallback to general segmentation using the absolute Sharpe ratio limits
        if user_risk == 'Low':
            df_filtered = df_scorecard[df_scorecard['sharpe_ratio'] < 0.8]
        elif user_risk == 'Moderate':
            df_filtered = df_scorecard[(df_scorecard['sharpe_ratio'] >= 0.8) & (df_scorecard['sharpe_ratio'] <= 1.5)]
        else:
            df_filtered = df_scorecard[df_scorecard['sharpe_ratio'] > 1.5]

    # 4. Extract target data points and sort by risk-adjusted efficiency descending
    sort_column = 'sharpe_ratio' if 'sharpe_ratio' in df_scorecard.columns else 'composite_score'
    
    if df_filtered.empty:
        print(f" Warning: No specific funds matching the exact rules for '{user_risk}' risk profile.")
        # Return top generic performers as emergency fallback
        df_recommendations = df_scorecard.sort_values(by=sort_column, ascending=False).head(3)
    else:
        df_recommendations = df_filtered.sort_values(by=sort_column, ascending=False).head(3)
        
    return df_recommendations

if __name__ == "__main__":
    # Define production file paths
    WORKSPACE = Path(r"C:\Users\P LIKITH VARMA\OneDrive\Desktop\mutual_fund_analtics\mutual_fund_analytics_platform")
    SCORECARD_FILE = WORKSPACE / "outputs" / "fund_scorecard.csv"
    
    # Check if a custom parameter was sent through terminal arguments
    profile_input = sys.argv[1] if len(sys.argv) > 1 else "Moderate"
    
    print(f"\n --- BLUESTOCK AUTOMATED ADVISORY ENGINE ---")
    print(f"Evaluating optimal asset configurations for Risk Appetite: [{profile_input.upper()}]")
    
    # Run recommendation logic pipeline
    recommendations = get_fund_recommendations(profile_input, SCORECARD_FILE)
    
    if recommendations is not None and not recommendations.empty:
        print("\n TOP 3 RECOMMENDED ASSETS GENERATED:")
        cols_to_print = [c for c in ['amfi_code', 'scheme_name', 'category', 'sharpe_ratio', 'cagr_3yr'] if c in recommendations.columns]
        
        # Format printing structure dynamically
        formatter_dict = {}
        if 'sharpe_ratio' in cols_to_print: formatter_dict['sharpe_ratio'] = '{:,.2f}'.format
        if 'cagr_3yr' in cols_to_print: formatter_dict['cagr_3yr'] = '{:,.2%}'.format
            
        print(recommendations[cols_to_print].to_string(index=False, formatters=formatter_dict))
        print(f"\n Asset advisory routing matrix completed cleanly.")
    else:
        print(" Could not generate recommendations. Check input variables or source files.")