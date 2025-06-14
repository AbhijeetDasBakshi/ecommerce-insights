import streamlit as st
import pandas as pd
import plotly.express as px

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("segmentation/data/customer_events_clustered.csv")
    kmeans_summary = pd.read_csv("segmentation/data/kmeans_cluster_summary.csv")
    dbscan_summary = pd.read_csv("segmentation/data/dbscan_cluster_summary.csv")
    return df, kmeans_summary, dbscan_summary

df, kmeans_summary, dbscan_summary = load_data()

# --- Sidebar ---
st.sidebar.title("🧠 Cluster Segmentation Explorer")

cluster_type = st.sidebar.selectbox(
    "Select Clustering Method",
    options=["KMeans", "DBSCAN"]
)

# Set cluster selection based on method
if cluster_type == "KMeans":
    cluster_col = "kmeans_cluster"
    summary_df = kmeans_summary
else:
    cluster_col = "dbscan_cluster"
    summary_df = dbscan_summary

selected_cluster = st.sidebar.selectbox(
    f"Select {cluster_type} Cluster",
    options=sorted(summary_df[cluster_col].unique())
)

# --- Main Title ---
st.title("🛍️ E-commerce Customer Segmentation Dashboard")
st.markdown(f"""
Explore customer clusters formed using **{cluster_type} clustering** on behavioral event data like views, add-to-carts, transactions, etc.
""")

# --- Cluster Summary ---
st.subheader(f"📊 {cluster_type} Cluster Summary")
st.dataframe(summary_df.style.format("{:.2f}"), use_container_width=True)

# --- Cluster Details ---
st.subheader(f"🔍 Customers in {cluster_type} Cluster {selected_cluster}")
cluster_df = df[df[cluster_col] == selected_cluster]
st.markdown(f"**{len(cluster_df)} visitors** in this cluster.")

# --- Feature Distribution ---
st.subheader("📈 Feature Distribution")

numeric_cols = [
    "total_events", "unique_items_viewed", "total_transactions",
    "num_views", "num_addtocarts", "num_transactions",
    "active_days", "active_hours", "session_duration_minutes"
]

selected_feature = st.selectbox("Select Feature", numeric_cols)

fig = px.histogram(cluster_df, x=selected_feature, nbins=30,
                   title=f"{selected_feature} Distribution in Cluster {selected_cluster}")
st.plotly_chart(fig, use_container_width=True)

# --- Download ---
st.download_button(
    label="📥 Download Cluster Data",
    data=cluster_df.to_csv(index=False),
    file_name=f"{cluster_type.lower()}_cluster_{selected_cluster}_data.csv"
)
