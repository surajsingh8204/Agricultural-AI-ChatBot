import pandas as pd
from pathlib import Path
import os

# Simulate what the function does
project_root = Path(__file__).resolve().parents[1]  # Should be Agricultural-AI-ChatBot
print(f"Project root from __file__: {project_root}")

# Check different paths
paths_to_try = [
    project_root / "crop-price-prediction" / "data" / "Agriculture_price_dataset.csv",
    Path(r"c:\Users\Suraj\Desktop\coding\llm-chat-bot\Agricultural-AI-ChatBot\crop-price-prediction\data\Agriculture_price_dataset.csv"),
]

for i, data_path in enumerate(paths_to_try, 1):
    print(f"\n{i}. Trying path: {data_path}")
    print(f"   Exists: {os.path.exists(data_path)}")
    
    if os.path.exists(data_path):
        print("   ✅ File found! Testing data filtering...")
        df = pd.read_csv(data_path, low_memory=False, nrows=1000)
        print(f"   Total rows loaded: {len(df)}")
        print(f"   Unique commodities: {df['Commodity'].unique().tolist()}")
        
        # Test filtering
        crop = "Potato"
        crop_data = df[df['Commodity'].str.lower() == crop.lower()].copy()
        print(f"   Rows for {crop}: {len(crop_data)}")
        
        if not crop_data.empty:
            print(f"   ✅ Found data for {crop}!")
            print(f"   Sample: {crop_data[['STATE', 'Commodity', 'Modal_Price', 'Price Date']].head(2)}")
        break
