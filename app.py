import streamlit as st
import pandas as pd

# Load CSV with personas
df = pd.read_csv("mistral_100_emails.csv", dtype={"MASTER_GUEST_ID": str})

# Clean and prep
df.columns = df.columns.str.strip()
df["email_intent"] = df["email_intent"].astype(str).str.strip()
df["MASTER_GUEST_ID"] = df["MASTER_GUEST_ID"].astype(str).str.strip()
df = df.dropna(subset=["email_intent", "MASTER_GUEST_ID"])

# Sidebar filters
st.sidebar.title("🔍 Email Filters")
intent = st.sidebar.selectbox("Email Intent", sorted(df["email_intent"].unique()))
filtered = df[df["email_intent"] == intent]
guest_id = st.sidebar.selectbox("Guest ID", filtered["MASTER_GUEST_ID"].tolist())

# Get the selected record
row = filtered[filtered["MASTER_GUEST_ID"] == guest_id].iloc[0]

# Display header
st.title("📬 LLM-Generated Email Preview")

# Show persona
st.subheader("🧠 Guest Persona")
if "persona_sentence" in row:
    st.write(row["persona_sentence"])
elif "guest_summary" in row:
    st.write(row["guest_summary"])
else:
    st.write("_No persona column found in dataset_")

# Show subject + body
st.markdown("---")
st.subheader("✉️ Email Subject")
st.write(row["subject_line"])

st.subheader("📨 Email Body (Plain Text)")
st.text(row["email_body"])

st.subheader("✨ HTML Preview")
st.markdown(row["email_html"], unsafe_allow_html=True)
