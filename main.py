import streamlit as st
import pandas as pd
import sqlite3

# Constants
DB_FILE = "parameters.db"
PASSWORD = "apple"

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
            font-size: 32px;
            font-weight: 700;
            color: #333;
        }
        .search-input input {
            font-size: 18px !important;
            padding: 8px;
            width: 300px;
        }
    </style>
""", unsafe_allow_html=True)

# --- Functions ---
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
            WHERE parameter LIKE ? OR description LIKE ?
        """, conn, params=(query_like, query_like))
    else:
        df = pd.read_sql_query("SELECT * FROM parameters", conn)
    conn.close()
    return df
st.markdown('<div class="title">📊 Factory Settings Manager</div>', unsafe_allow_html=True)
# --- Password Gate ---
password_input = st.text_input("Enter Password", type="password")

if password_input == PASSWORD:
    # --- Header Layout (Title + Search) ---
    st.markdown('<div class="header-container">', unsafe_allow_html=True)
    st.markdown('<div class="title">🔍 Search</div>', unsafe_allow_html=True)
    search_query = st.text_input("🔍 Search", "", key="search", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Load and Display Data ---
    df = search_data(search_query)
    st.subheader("Data Table")
    st.dataframe(df, use_container_width=True)

    # --- Edit Page Link ---
    st.markdown("[✏️ Go to Edit Page](http://localhost:8501/edit)", unsafe_allow_html=True)
else:
    st.warning("Enter the correct password to access editing.")
