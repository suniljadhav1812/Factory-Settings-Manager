import streamlit as st
import pandas as pd
import sqlite3

DB_FILE = "parameters.db"
PASSWORD = "apple"  # You can set this to a secure value or use secrets
# Page configuration
st.set_page_config(page_title="Factory Settings Manager", layout="wide")

# --- CSS Styling ---
st.markdown("""
    <style>
        .header-container {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 20px;
        }
        .title {
            font-size: 32px !important;   /* consistent size */
            font-weight: 700 !important;
            color: #333 !important;
        }
        .search-input input {
            font-size: 18px !important;
            padding: 8px;
            width: 300px;
        }
    </style>
""", unsafe_allow_html=True)


def load_data():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM parameters", conn)
    conn.close()
    return df

def save_data(df):
    conn = sqlite3.connect(DB_FILE)
    df.to_sql("parameters", conn, if_exists="replace", index=False)
    conn.close()

# --- Authentication ---
#st.set_page_config(page_title="Edit Parameters", layout="wide")
#st.markdown('<div class="title">🔐 Edit Parameters (Admin Only)</div>', unsafe_allow_html=True)
st.markdown('<div class="title">🔐 Edit Parameters (Admin Only)</div>', unsafe_allow_html=True)
#st.title("🔐 Edit Parameters (Admin Only)")

password_input = st.text_input("Enter Password", type="password")

if password_input == PASSWORD:
    df = load_data()
    st.subheader("Edit Parameters")
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
    
    if st.button("💾 Save Changes"):
        save_data(edited_df)
        st.success("✅ Changes saved!")
else:
    st.warning("Enter the correct password to access editing.")

