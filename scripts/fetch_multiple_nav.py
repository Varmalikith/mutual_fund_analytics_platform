import requests
import pandas as pd
import os
print("started")
# Create raw folder if it doesn't exist
os.makedirs("data/raw", exist_ok=True)

schemes = {
    "SBI_Bluechip": 119551,
    "ICICI_Bluechip": 120503,
    "Nippon_LargeCap": 118632,
    "Axis_Bluechip": 119092,
    "Kotak_Bluechip": 120841
}

for fund_name, scheme_code in schemes.items():

    try:
        print(f"\nFetching {fund_name}...")

        url = f"https://api.mfapi.in/mf/{scheme_code}"

        response = requests.get(url)

        if response.status_code == 200:

            data = response.json()

            nav_df = pd.DataFrame(data["data"])

            file_path = f"data/raw/{fund_name}.csv"

            nav_df.to_csv(file_path, index=False)

            print(f"Saved: {file_path}")

        else:
            print(f"Failed for {fund_name}")

    except Exception as e:
        print(f"Error for {fund_name}: {e}")

print("\nAll downloads completed!")