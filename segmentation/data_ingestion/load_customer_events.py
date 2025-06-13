import pandas as pd
from segmentation.utils.mongo_connection import get_collection
from datetime import datetime

def convert_timestamp(ts):
    """
    Converts Unix timestamp in milliseconds to Python datetime.
    """
    return datetime.fromtimestamp(int(ts) / 1000)

def fetch_and_clean_customer_events():
    collection = get_collection("customer_events")

    # Fetch relevant fields, limit to 30k docs
    cursor = collection.find({}, {
        "_id": 0,
        "timestamp": 1,
        "visitorid": 1,
        "event": 1,
        "itemid": 1,
        "transactionid": 1
    })

    # Convert to DataFrame
    df = pd.DataFrame(list(cursor))

    # Convert timestamp
    df["timestamp"] = df["timestamp"].apply(lambda x: convert_timestamp(x))

    # Print all unique event types
    print("Unique event types:", df["event"].unique())

    return df

if __name__ == "__main__":
    df_cleaned = fetch_and_clean_customer_events()
    print(f"\n Cleaned data shape: {df_cleaned.shape}")
    print(df_cleaned.head())

    # Save to CSV (optional)
    df_cleaned.to_csv("segmentation/data/cleaned_customer_events.csv", index=False)
