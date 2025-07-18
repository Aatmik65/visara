import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Setup ---
st.set_page_config(page_title="VISARA Buyer Analytics", layout="wide")

st.markdown("<h1 style='text-align: center; color: cyan;'>🏡 VISARA Buyer Engagement Dashboard</h1>", unsafe_allow_html=True)
st.write("**Beyond Views. Into Vibes.** Real-time insights from Metaverse property tours.")

# --- Load Data ---
df = pd.read_csv("buyers.csv")

# --- Sidebar Filters ---
property_filter = st.sidebar.selectbox("🏠 Select Property", options=["All"] + sorted(df["Property_Name"].unique().tolist()))

if property_filter != "All":
    df = df[df["Property_Name"] == property_filter]

# --- Metrics Section ---
col1, col2, col3 = st.columns(3)
col1.metric("Avg Engagement Score", f"{df['Engagement_Score'].mean():.1f}%")
col2.metric("Hot Leads (>90%)", df[df["Engagement_Score'] > 90].shape[0])
col3.metric("Avg Predicted Closing", f"{df['Predicted_Close'].mean():.1f}%")

# --- Heatmap: Room Engagement ---
st.subheader("🔥 Room Engagement Heatmap")
heatmap = df.groupby(["Room_Viewed", "Property_Name"])["Time_Spent"].mean().reset_index()
fig_heatmap = px.density_heatmap(
    heatmap,
    x="Room_Viewed",
    y="Property_Name",
    z="Time_Spent",
    color_continuous_scale="Blues",
    title="Avg Time Spent in Each Room"
)
st.plotly_chart(fig_heatmap, use_container_width=True)

# --- Lead Quality Funnel ---
st.subheader("🎯 Lead Quality Funnel")
funnel_data = {
    "Stage": ["All Visitors", "Interested (>70%)", "Hot Leads (>90%)"],
    "Count": [
        df.shape[0],
        df[df["Engagement_Score"] > 70].shape[0],
        df[df["Engagement_Score"] > 90].shape[0]
    ]
}
funnel_df = pd.DataFrame(funnel_data)
fig_funnel = px.funnel(funnel_df, x="Count", y="Stage", title="Lead Conversion Funnel")
st.plotly_chart(fig_funnel, use_container_width=True)

# --- Predicted Leads Table ---
st.subheader("📋 Predicted High-Value Leads")
top_leads = df.sort_values(by="Predicted_Close", ascending=False).head(10)
st.dataframe(top_leads[["Buyer_Name", "Property_Name", "Engagement_Score", "Predicted_Close"]])

# --- AI Insight ---
st.markdown("💡 **AI Insight:** "
            f"'{df['Property_Name'].mode()[0]}' is the most engaging property. "
            f"Top hotspot room: {df['Room_Viewed'].mode()[0]} with {df['Time_Spent'].max()} seconds of interest.")

st.markdown("<br><hr><center>VISARA - Beyond Views. Into Vibes.</center>", unsafe_allow_html=True)
