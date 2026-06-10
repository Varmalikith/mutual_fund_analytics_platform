import requests
import pandas as pd


print("Script Started")




# HDFC Top 100 Direct Plan
scheme_code = 125497

url = f"https://api.mfapi.in/mf/{scheme_code}"

response = requests.get(url)

print("Status Code:", response.status_code)

data = response.json()

print("Fund Name:")
print(data["meta"]["scheme_name"])

# Convert NAV history to DataFrame
nav_df = pd.DataFrame(data["data"])

print(nav_df.head())

# Save CSV
nav_df.to_csv(
    "data/raw/hdfc_top100_live_nav.csv",
    index=False
)

print("CSV saved successfully!")


    
print("Script Finished")