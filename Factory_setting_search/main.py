import streamlit as st
import pandas as pd
import sqlite3

DB_FILE = "parameters.db"

def load_data():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM parameters", conn)
    conn.close()
    return df

def search_data(query):
    conn = sqlite3.connect(DB_FILE)
    if query:
        query_like = f"%{query}%"
        df = pd.read_sql_query("""
            SELECT * FROM parameters
            WHERE parameter LIKE ?
            OR description LIKE ?
        """, conn, params=(query_like,)*2)
    else:
        df = pd.read_sql_query("SELECT * FROM parameters", conn)
    conn.close()
    return df

st.set_page_config(page_title="Factory Settings Manager", layout="wide")
st.title("📊 Factory Settings Manager")

search_query = st.text_input("🔍 Search", "")
df = search_data(search_query)

st.subheader("Data Table")
st.dataframe(df, use_container_width=True)

# Add New Entry
st.subheader("➕ Add New Entry")
with st.form("add_form"):
    col1, col2, col3, col4 = st.columns(4)
    parameter = col1.text_input("Parameter")
    param_value = col2.text_input("Parameter Value")
    description = col3.text_input("Description")
    status = col4.selectbox("Status", ["In Use", "Not in Use"])
    submitted = st.form_submit_button("Add Entry")

    if submitted:
        if parameter:
            new_entry = pd.DataFrame([[parameter, param_value, description, status]],
                                     columns=["parameter", "parameter_value", "description", "status"])
            full_df = pd.concat([load_data(), new_entry], ignore_index=True)
            conn = sqlite3.connect(DB_FILE)
            full_df.to_sql("parameters", conn, if_exists="replace", index=False)
            conn.close()
            st.success("✅ Entry added successfully!")
        else:
            st.error("❌ Parameter is required.")

# 🔗 Link to edit page
st.markdown("[✏️ Go to Edit Page](http://localhost:8501/edit)", unsafe_allow_html=True)
