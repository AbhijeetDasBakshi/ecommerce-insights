import pandas as pd
from datetime import datetime

DATA_PATH = "segmentation/data/cleaned_customer_events.csv"
OUTPUT_PATH = "segmentation/data/customer_events_features.csv"

def main():
    print(" Loading first 30,000 rows from cleaned customer event data...")
    df = pd.read_csv(DATA_PATH, parse_dates=["timestamp"], nrows=30000)

    # Extract hour and day of week
    print(" Extracting time features...")
    df["hour"] = df["timestamp"].dt.hour
    df["day_of_week"] = df["timestamp"].dt.dayofweek  # Monday=0

    # Aggregate per visitor
    print(" Aggregating per visitor...")
    agg_df = df.groupby("visitorid").agg(
        total_events=("event", "count"),
        unique_items_viewed=("itemid", pd.Series.nunique),
        total_transactions=("transactionid", lambda x: (x != 0).sum()),
        num_views=("event", lambda x: (x == "view").sum()),
        num_addtocarts=("event", lambda x: (x == "addtocart").sum()),
        num_transactions=("event", lambda x: (x == "transaction").sum()),
        first_visit=("timestamp", "min"),
        last_visit=("timestamp", "max"),
        active_days=("day_of_week", pd.Series.nunique),
        active_hours=("hour", pd.Series.nunique)
    ).reset_index()

    # Calculate session duration
    print(" Calculating session durations...")
    agg_df["session_duration_minutes"] = (
        (agg_df["last_visit"] - agg_df["first_visit"]).dt.total_seconds() / 60
    )

    # Fill missing values
    print(" Filling missing values...")
    agg_df = agg_df.fillna({
        "session_duration_minutes": 0,
        "unique_items_viewed": 0,
        "num_views": 0,
        "num_addtocarts": 0,
        "num_transactions": 0
    })

    # Drop datetime columns if not needed
    agg_df.drop(columns=["first_visit", "last_visit"], inplace=True)

    # Save to CSV
    print(f" Saving visitor-level features to {OUTPUT_PATH}...")
    agg_df.to_csv(OUTPUT_PATH, index=False)
    print(f" Done! Processed shape: {agg_df.shape}")

if __name__ == "__main__":
    main()
