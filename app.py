import streamlit as st
import pandas as pd

# Load your email output
df = pd.read_csv("mistral_100_emails.csv", dtype={"MASTER_GUEST_ID": str})

# Clean up
df.columns = df.columns.str.strip()
df["email_intent"] = df["email_intent"].astype(str).str.strip()
df["MASTER_GUEST_ID"] = df["MASTER_GUEST_ID"].astype(str).str.strip()
df = df.dropna(subset=["email_intent", "MASTER_GUEST_ID"])

# Sidebar filters
st.sidebar.title("🔍 Email Filters")
intent = st.sidebar.selectbox("Email Intent", sorted(df["email_intent"].unique()))
filtered = df[df["email_intent"] == intent]
guest_id = st.sidebar.selectbox("Guest ID", filtered["MASTER_GUEST_ID"].tolist())

# Display email
row = filtered[filtered["MASTER_GUEST_ID"] == guest_id].iloc[0]

st.title("📬 LLM-Generated Email Viewer")
st.subheader(f"Subject: {row['subject_line']}")
st.write(row["email_body"])
st.markdown("---")
st.markdown("### ✨ HTML Preview")
st.markdown(row["email_html"], unsafe_allow_html=True)
