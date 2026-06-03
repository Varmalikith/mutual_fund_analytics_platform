from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text

# 1. Setup your absolute project workspace pathways
WORKSPACE_DIR = Path(r"C:\Users\P LIKITH VARMA\OneDrive\Desktop\mutual_fund_analtics\mutual_fund_analytics_platform")
PROCESSED_DATA_DIR = WORKSPACE_DIR / "data" / "processed"
RAW_DATA_DIR = WORKSPACE_DIR / "data" 
SQL_DIR = WORKSPACE_DIR / "sql"
DB_DIR = WORKSPACE_DIR / "db"

# Safety Check: Automatically create the database storage folder if missing
DB_DIR.mkdir(parents=True, exist_ok=True)

# 2. Establish connection string to your SQLite database file
db_path = DB_DIR / "bluestock_mf.db"
engine = create_engine(f"sqlite:///{db_path}")

print("==================================================")
print("⚙️ STARTING SQL DATABASE GENERATION PIPELINE")
print("==================================================")   

# 3. Read and execute schema.sql to build the tables first
SCHEMA_FILE = SQL_DIR / "schema.sql"
if SCHEMA_FILE.exists():
    print("⏳ Executing schema.sql blueprint to build relational tables...")
    with open(SCHEMA_FILE, "r") as f:
        schema_sql = f.read()
    
    # Open a connection and execute DDL queries sequentially
    with engine.begin() as conn:
        # SQLite handles multiple statements perfectly when split by semicolons
        for statement in schema_sql.split(";"):
            clean_statement = statement.strip()
            if clean_statement:
                conn.execute(text(clean_statement))
    print("✅ Success: All tables and optimization indexes built successfully!")
else:
    print("⚠️ Warning: schema.sql file not found. Pandas will infer table layouts instead.")

print("\n==================================================")
print("⏳ LOADING CLEAN DATASETS INTO SQL TABLES")
print("==================================================")

# 4. Define dictionary mapping table names to their clean CSV files
# Note: For datasets we didn't clean in tasks 1-3, we load from raw safely.
datasets_to_load = {
    "dim_fund": RAW_DATA_DIR / "01_fund_master.csv",
    "fact_nav": PROCESSED_DATA_DIR / "clean_nav.csv",
    "fact_transactions": PROCESSED_DATA_DIR / "clean_investor_transactions.csv",
    "fact_scheme_performance": PROCESSED_DATA_DIR / "clean_scheme_performance.csv",
    "fact_aum_fund_house": RAW_DATA_DIR / "03_aum_by_fund_house.csv",
    "fact_monthly_sip_inflows": RAW_DATA_DIR / "04_monthly_sip_inflows.csv",
    "fact_category_inflows": RAW_DATA_DIR / "05_category_inflows.csv",
    "fact_industry_folio_count": RAW_DATA_DIR / "06_industry_folio_count.csv",
    "fact_portfolio_holdings": RAW_DATA_DIR / "09_portfolio_holdings.csv",
    "fact_benchmark_indices": RAW_DATA_DIR / "10_benchmark_indices.csv"
}

# 5. Loop through and systematically append records into SQLite tables
for table_name, file_path in datasets_to_load.items():
    if file_path.exists():
        print(f"⏳ Ingesting records into table '{table_name}' from {file_path.name}...")
        df = pd.read_csv(file_path)
        
        # if_exists='append' populates the pre-constructed tables built via DDL safely
        df.to_sql(table_name, engine, if_exists='append', index=False)
        print(f"   ✔ Loaded {len(df)} rows into '{table_name}'.")
    else:
        print(f"❌ Error: File missing at path: {file_path}")

print("==================================================")
print(f"🏁 PIPELINE RUN COMPLETE! Database saved at: {db_path}")
print("==================================================")