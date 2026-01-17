import streamlit as st
import time
from utils.mongo_handler import test_connection
from utils.ui import add_footer
from pages import dashboard, editor

# 1. Page Config
st.set_page_config(
    page_title="Universal Mongo Manager | Indranil",
    page_icon="🛡️", # You can change this to 📝 or any other emoji
    layout="centered",
    initial_sidebar_state="expanded"
)

# 2. Session Timeout Configuration
TIMEOUT_SECONDS = 600  
if "last_activity" not in st.session_state:
    st.session_state.last_activity = time.time()

elapsed_time = time.time() - st.session_state.last_activity
remaining_time = max(0, int(TIMEOUT_SECONDS - elapsed_time))

if remaining_time <= 0 and st.session_state.get("verified"):
    st.session_state.verified = False
    st.session_state.uri_locked = False
    for key in ["uri_field", "selected_db", "selected_coll"]:
        if key in st.session_state: del st.session_state[key]
    st.warning("Session expired due to inactivity.")
    st.rerun()

# 3. Secure & White-Label CSS
st.markdown(
    """
    <style>
    /* 1. HIDE TOP-RIGHT ACTIONS ONLY */
    /* This hides the GitHub, Fork, and Profile icons without killing the header */
    [data-testid="stToolbarActions"] { 
        display: none !important; 
    }
    
    /* Hide the 'decoration' line at the top */
    [data-testid="stDecoration"] { 
        display: none !important; 
    }

    /* 2. HIDE MAIN MENU & FOOTER & STATUS */
    #MainMenu { visibility: hidden; } 
    footer { visibility: hidden; } 
    div[data-testid="stStatusWidget"] { visibility: hidden; } 

    /* 3. FIX THE HEADER - DO NOT USE visibility: hidden */
    /* We make it transparent so the sidebar toggle (hamburger icon) stays visible and clickable */
    header {
        background-color: rgba(0,0,0,0) !important;
        color: white !important;
    }

    /* 4. SECURE PASSWORD FIELDS */
    div[data-testid="stTextInput"] button { display: none !important; }
    button[aria-label="Show password"], button[aria-label="Hide password"] { display: none !important; }
    input[type="password"] { padding-right: 1rem !important; }
    input:disabled {
        background-color: #262730 !important;
        color: #808495 !important;
        -webkit-text-security: disc !important;
        opacity: 1 !important;
        cursor: not-allowed !important;
    }

    /* 5. TIMER TEXT */
    .timer-text { font-size: 0.8rem; color: #ff4b4b; text-align: center; margin-bottom: 10px; }
    </style>
    """,
    unsafe_allow_html=True
)

def handle_uri_entry():
    if st.session_state.uri_field:
        st.session_state.uri_locked = True
        st.session_state.last_activity = time.time()

if st.session_state.pop("clear_uri", False):
    st.session_state["uri_field"] = ""

if "uri_field" not in st.session_state:
    st.session_state["uri_field"] = ""

with st.sidebar:
    st.title("🛡️ Connection")
    if st.session_state.get("verified"):
        mins, secs = divmod(remaining_time, 60)
        st.markdown(f"<p class='timer-text'>⏱️ Session expires in: {mins:02d}:{secs:02d}</p>", unsafe_allow_html=True)

    st.text_input("Enter MongoDB URI & Press Enter", type="password", 
                  disabled=st.session_state.get("uri_locked", False),
                  key="uri_field", on_change=handle_uri_entry)

    if st.session_state.get("uri_locked") and not st.session_state.get("verified"):
        if st.button("Verify Connection", type="primary", use_container_width=True):
            with st.spinner("Verifying..."):
                success, message = test_connection(st.session_state.uri_field)
                if success:
                    st.session_state.verified = True
                    st.rerun()
                else:
                    st.session_state.login_error = f"❌ {message}"
                    st.session_state.uri_locked = False
                    st.session_state["clear_uri"] = True
                    st.rerun()

    if "login_error" in st.session_state:
        st.error(st.session_state.login_error)
        del st.session_state.login_error

    st.divider()
    if st.session_state.get("verified"):
        if st.button("🔄 Switch Cluster (Log Out)", use_container_width=True):
            st.session_state.verified = False
            st.session_state.uri_locked = False
            st.rerun()
        page = st.radio("Navigation", ["Dashboard", "Data Editor"])

# 4. Routing
if st.session_state.get("verified") and "uri_field" in st.session_state:
    current_uri = st.session_state.uri_field
    if page == "Dashboard":
        dashboard.show(current_uri)
    elif page == "Data Editor":
        editor.show(current_uri)

# 5. GLOBAL STICKY FOOTER
add_footer("Indranil Chatterjee")