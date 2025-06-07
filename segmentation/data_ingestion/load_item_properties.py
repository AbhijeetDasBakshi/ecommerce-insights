import pandas as pd
from segmentation.utils.mongo_connection import get_collection
from datetime import datetime

def convert_timestamp(ts):
    """
    Converts Unix timestamp in milliseconds to Python datetime.
    """
    return datetime.fromtimestamp(int(ts) / 1000)

def fetch_and_clean_item_properties():
    """
    Loads, merges, and cleans item_properties_1 and item_properties_2 collections.
    """
    # Load from MongoDB
    col1 = get_collection("item_properties_1")
    col2 = get_collection("item_properties_2")

    print("Fetching 30k item_properties_1...")
    data1 = list(col1.find({}, {"_id": 0, "timestamp": 1, "itemid": 1, "property": 1, "value": 1}).limit(30000))
    
    print("Fetching 30k item_properties_2...")
    data2 = list(col2.find({}, {"_id": 0, "timestamp": 1, "itemid": 1, "property": 1, "value": 1}).limit(30000))

    # Combine
    print(f"Fetched {len(data1)} from part 1, {len(data2)} from part 2.")
    df = pd.DataFrame(data1 + data2)

    # Convert timestamp
    df["timestamp"] = df["timestamp"].apply(lambda x: convert_timestamp(x))

    return df

if __name__ == "__main__":
    df_cleaned = fetch_and_clean_item_properties()
    print(f"Cleaned item properties shape: {df_cleaned.shape}")
    print(df_cleaned.head())

    # Optional: save for later
    df_cleaned.to_csv("segmentation/data/cleaned_item_properties.csv", index=False)
