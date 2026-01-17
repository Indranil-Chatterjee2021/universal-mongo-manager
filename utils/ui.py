import streamlit as st

def add_footer(user_name):
    """Adds a fixed, sticky footer with a larger font size."""
    st.markdown(
        f"""
        <style>
        .footer {{
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #0e1117; 
            color: #fafafa;
            text-align: center;
            padding: 15px 0; /* Slightly more padding for the larger text */
            font-size: 16px; /* Increased from 14px */
            border-top: 1px solid #31333f;
            z-index: 999;
            font-family: sans-serif;
        }}
        /* Ensure main content doesn't get cut off at the bottom */
        .main .block-container {{
            padding-bottom: 80px !important; /* Increased to account for larger footer */
        }}
        </style>
        <div class="footer">
            🚀 <b>Universal MongoDB Manager</b>: A lightweight interface for document editing, developed by <b>{user_name}</b>
        </div>
        """,
        unsafe_allow_html=True
    )
    