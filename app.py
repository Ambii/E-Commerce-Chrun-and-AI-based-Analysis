import streamlit as st
import pandas as pd
import google.generativeai as genai
import os


st.set_page_config(page_title="E-Commerce Chrun and AI based Analysis")
csv_FILENAME = "ecommerce_churn_data.csv"

if os.path.exists(csv_FILENAME):
    df = pd.read_csv(csv_FILENAME)
else:
    print("Dataset not found")

st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Gemini API Key", type="password")
uploaded_file = st.sidebar.file_uploader("Upload custom CSV Dataset", type = ["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("Custom CSV Loaded Successfully!")
    st.sidebar.divider()
    st.sidebar.caption("10Pearls WTQ 2026 | Churn & Sentiment Track")
    
    st.title("E-Commerce Churn Risk & Sentiment Intelligence")
    st.markdown("Identify high-churn customers from buried support reviews and automate targeted recovery offers.")
    high_risk_df = df[(df["Days_Since_Last_Order"] > 60) | (df["Support_Tickets_Logged"] >= 3)]
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total columns evaluated", len(df))
    col2.metric("High churn risk customers", len(high_risk_df), delta_color= "inverse")
    col3.metric("Avg days since last order", f"{int(df['Days_Since_Last_Order'].mean())} days")
    col4.metric("Total open support tickets", int(df["Support_Tickets_Logged"].sum()))
    
    st.divider()
    
    st.subheader("Customer Risk Explorer")
    risk_filter = st.radio("Filter Dataset:", ["All Customers", "High Risk Only (Churn Warning)"], horizontal=True)
    display_df = high_risk_df if risk_filter == "High Risk Only (Churn Warning)" else df
    st.dataframe(display_df, use_container_width=True)
    
    st.divider()
    
    st.subheader("🤖 AI Customer Triage & Recovery Engine")

# Dropdown to select specific customer for drilldown
selected_id = st.selectbox("Select Customer ID for Deep AI Analysis:", df["Customer_ID"].tolist())
customer_row = df[df["Customer_ID"] == selected_id].iloc[0]

c_col1, c_col2 = st.columns([1, 1])

with c_col1:
    st.markdown(f"**Customer Profile: ID #{customer_row['Customer_ID']}**")
    st.write(f"- **Purchase History:** `{customer_row['Purchase_Count']} orders`")
    st.write(f"- **Days Since Last Order:** `{customer_row['Days_Since_Last_Order']} days`")
    st.write(f"- **Support Tickets Logged:** `{customer_row['Support_Tickets_Logged']} tickets`")
    st.info(f"**Last Review/Feedback:**\n\n\"{customer_row['Last_Review_Text']}\"")

with c_col2:
    st.markdown("**AI Intelligence Actions**")
    
    # Action 1: Categorize Feedback with Gemini
    if st.button("🔍 Categorize Complaint Bucket", type="secondary", use_container_width=True):
        if not api_key:
            st.error("Please enter your Gemini API key in the sidebar.")
        else:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-3.5-flash-lite")
                
                prompt = f"""
                Analyze the following e-commerce customer feedback:
                "{customer_row['Last_Review_Text']}"
                
                Provide a structured summary containing:
                1. Primary Complaint Category (e.g., Shipping Delay, Product Defect, Customer Service, Returns/Refunds)
                2. Sentiment Score (Positive, Neutral, Negative, Severe Frustration)
                3. Root Cause Analysis (1 sentence)
                """
                
                with st.spinner("Analyzing review sentiment with Gemini..."):
                    response = model.generate_content(prompt)
                    st.success("Analysis Complete!")
                    st.markdown(response.text)
            except Exception as e:
                st.error(f"Gemini API Error: {str(e)}")

    # Action 2: Generate Personalized Retention Offer
    if st.button("🎁 Generate Retention Offer Email", type="primary", use_container_width=True):
        if not api_key:
            st.error("Please enter your Gemini API key in the sidebar.")
        else:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-3.5-flash-lite")
                
                prompt = f"""
                You are a Customer Retention Specialist for an e-commerce platform.
                
                Customer Details:
                - ID: {customer_row['Customer_ID']}
                - Days Inactive: {customer_row['Days_Since_Last_Order']} days
                - Complaints Logged: {customer_row['Support_Tickets_Logged']}
                - Review Text: "{customer_row['Last_Review_Text']}"
                
                Task:
                Draft a highly empathetic, professional apology email addressing their exact complaint.
                Include a custom promotional discount code (e.g., RECOVER20 or VIPGIFT) and offer direct assistance to resolve their issue. Keep it under 150 words.
                """
                
                with st.spinner("Drafting personalized retention offer..."):
                    response = model.generate_content(prompt)
                    st.success("Retention Email Generated!")
                    st.text_area("Generated Outreach Email", value=response.text, height=220)
            except Exception as e:
                st.error(f"Gemini API Error: {str(e)}")