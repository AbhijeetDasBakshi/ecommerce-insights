import pandas as pd
from segmentation.utils.mongo_connection import get_collection


def fetch_and_clean_customer_events():
    collection = get_collection("category_tree")

    # Fetch relevant fields
    cursor = collection.find({}, {
        "_id": 0,
        "categoryid": 1,
        "parentid": 1
    })

    # Convert to DataFrame
    df = pd.DataFrame(list(cursor))

    return df

if __name__ == "__main__":
    df_cleaned = fetch_and_clean_customer_events()
    print(f"Cleaned data shape: {df_cleaned.shape}")
    print(df_cleaned.head())

    # Save to CSV (optional)
    df_cleaned.to_csv("segmentation/data/cleaned_category_tree.csv", index=False)
