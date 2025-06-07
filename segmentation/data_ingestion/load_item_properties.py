import pandas as pd
from segmentation.utils.mongo_connection import get_collection
from datetime import datetime

def convert_timestamp(ts):
    return datetime.fromtimestamp(int(ts) / 1000)

def fetch_item_properties(collection_name, limit=30000):
    print(f"Fetching {limit} docs from {collection_name}...")
    collection = get_collection(collection_name)
    data = list(collection.find({}, {"_id": 0, "timestamp": 1, "itemid": 1, "property": 1, "value": 1}).limit(limit))
    df = pd.DataFrame(data)
    df["timestamp"] = df["timestamp"].apply(lambda x: convert_timestamp(x))
    return df

if __name__ == "__main__":
    df1 = fetch_item_properties("item_properties_1")
    df2 = fetch_item_properties("item_properties_2")

    print(f"item_properties_1 shape: {df1.shape}")
    print(f"item_properties_2 shape: {df2.shape}")

    df1.to_csv("segmentation/data/cleaned_item_properties_1.csv", index=False)
    df2.to_csv("segmentation/data/cleaned_item_properties_2.csv", index=False)
