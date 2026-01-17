import streamlit as st
from utils.mongo_handler import get_mongo_data
from utils.ui import add_footer

def show(uri):
    add_footer("Indranil Chatterjee")
    st.header("📊 Cluster Overview")
    st.caption("Connected successfully. Select your targets below.")
    try:
        # 1. Database Selection
        dbs = get_mongo_data(uri, action="list_dbs")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### 1. Select Database")
            db_default = 0
            if "selected_db" in st.session_state and st.session_state.selected_db in dbs:
                db_default = dbs.index(st.session_state.selected_db)
            
            selected_db = st.radio("Databases", dbs, index=db_default, key="db_radio")
            st.session_state["selected_db"] = selected_db

        # 2. Collection Selection
        with col2:
            st.write("### 2. Select Collection")
            colls = get_mongo_data(uri, db_name=selected_db, action="list_colls")
            
            if colls:
                coll_default = 0
                if "selected_coll" in st.session_state and st.session_state.selected_coll in colls:
                    coll_default = colls.index(st.session_state.selected_coll)
                
                selected_coll = st.radio("Collections", colls, index=coll_default, key="coll_radio")
                st.session_state["selected_coll"] = selected_coll
                
                st.success(f"Target: **{selected_db}.{selected_coll}**")
            else:
                st.warning("No collections found.")

    except Exception as e:
        st.error(f"Error: {e}")    
