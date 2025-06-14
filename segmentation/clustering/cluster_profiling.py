import pandas as pd

def summarize_cluster(df: pd.DataFrame, cluster_col: str) -> pd.DataFrame:
    """
    Creates a summary of the given cluster column ('kmeans_cluster' or 'dbscan_cluster').
    """
    grouped = df.groupby(cluster_col).agg({
        'visitorid': 'count',
        'total_events': 'mean',
        'unique_items_viewed': 'mean',
        'total_transactions': 'mean',
        'num_views': 'mean',
        'num_addtocarts': 'mean',
        'num_transactions': 'mean',
        'active_days': 'mean',
        'active_hours': 'mean',
        'session_duration_minutes': 'mean'
    }).rename(columns={'visitorid': 'num_visitors'}).reset_index()

    # Add conversion rate (transactions/views)
    grouped['conversion_rate'] = grouped['num_transactions'] / (grouped['num_views'] + 1e-5)  # avoid division by zero

    return grouped


if __name__ == "__main__":
    # Load clustered data
    input_file = "segmentation/data/customer_events_clustered.csv"
    df = pd.read_csv(input_file)

    # KMeans profiling
    print("Generating KMeans cluster profile...")
    kmeans_summary = summarize_cluster(df, 'kmeans_cluster')
    kmeans_summary.to_csv("segmentation/data/kmeans_cluster_summary.csv", index=False)
    print("Saved: segmentation/data/kmeans_cluster_summary.csv")

    # DBSCAN profiling (optional if DBSCAN was applied)
    if 'dbscan_cluster' in df.columns:
        print("Generating DBSCAN cluster profile...")
        dbscan_summary = summarize_cluster(df, 'dbscan_cluster')
        dbscan_summary.to_csv("segmentation/data/dbscan_cluster_summary.csv", index=False)
        print("Saved: segmentation/data/dbscan_cluster_summary.csv")

