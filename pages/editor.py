import streamlit as st
import json
import time
from bson import ObjectId
from datetime import datetime
from utils.mongo_handler import sanitize_uri
from pymongo import MongoClient

from utils.ui import add_footer

class MongoEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime): return obj.isoformat()
        if isinstance(obj, ObjectId): return str(obj)
        return super().default(obj)

def show(uri):
    add_footer("Indranil Chatterjee")
    st.header("📝 Universal Document Editor")
    
    if "search_version" not in st.session_state:
        st.session_state.search_version = 0
    if "confirm_delete" not in st.session_state:
        st.session_state.confirm_delete = None
    if "page_number" not in st.session_state:
        st.session_state.page_number = 0

    LIMIT = 25
    
    default_db = st.session_state.get("selected_db", "")
    default_coll = st.session_state.get("selected_coll", "")

    col1, col2 = st.columns(2)
    db_name = col1.text_input("Database Name", value=default_db)
    coll_name = col2.text_input("Collection Name", value=default_coll)

    if not db_name or not coll_name:
        st.info("💡 Select a Database and Collection in the Dashboard to begin.")
        return

    search_col, refresh_col = st.columns([4, 1])
    with search_col:
        search_key = f"editor_search_{st.session_state.search_version}"
        search_term = st.text_input("🔍 Search documents", placeholder="Type to filter...", label_visibility="collapsed", key=search_key)
    with refresh_col:
        if st.button("🔄 Refresh", use_container_width=True):
            st.session_state.search_version += 1
            st.session_state.page_number = 0
            st.rerun()

    try:
        clean_uri = sanitize_uri(uri)
        with MongoClient(clean_uri, serverSelectionTimeoutMS=5000) as client:
            db = client[db_name]
            coll = db[coll_name]
            total_docs = coll.estimated_document_count()
            
            sample_doc = coll.find_one()
            query = {}
            if search_term and sample_doc:
                query = {"$or": [{f: {"$regex": search_term, "$options": "i"}} for f in sample_doc.keys() if isinstance(sample_doc[f], str)]}

            skip = st.session_state.page_number * LIMIT
            data = list(coll.find(query).skip(skip).limit(LIMIT))

            if not data:
                st.warning("No documents found.")
                st.info(f"📊 **Stats:** {db_name}.{coll_name} | 📑 **Total Docs:** {total_docs:,} | 🔍 **Results:** 0")
            else:
                # Instruction moved to the top of the results section
                st.info("💡 Select a row in the table below to view or edit the full document.")
                
                display_data = [{k: v for k, v in d.items() if k != "_id"} for d in data]
                event = st.dataframe(display_data, use_container_width=True, selection_mode="single-row", on_select="rerun", hide_index=True)

                # --- PAGINATION CONTROLS ---
                p_col1, p_col2, p_col3, p_col4, p_col5 = st.columns([2, 0.5, 1, 0.5, 2])
                with p_col2:
                    # Using double arrow icon for clarity
                    if st.button("«", use_container_width=True, key="prev_btn", disabled=st.session_state.page_number == 0):
                        st.session_state.page_number -= 1
                        st.rerun()
                with p_col3:
                    st.markdown(f"<p style='text-align:center; padding-top:5px; font-weight:bold;'>Page {st.session_state.page_number + 1}</p>", unsafe_allow_html=True)
                with p_col4:
                    # Using double arrow icon for clarity
                    if st.button("»", use_container_width=True, key="next_btn", disabled=len(data) < LIMIT):
                        st.session_state.page_number += 1
                        st.rerun()

                st.info(f"📊 **Stats:** {db_name}.{coll_name} | 📑 **Total Docs:** {total_docs:,} | 🔍 **Viewing:** {skip+1} to {skip+len(data)}")

                # --- EDITING SECTION ---
                selected_rows = event.get("selection", {}).get("rows", [])
                if selected_rows:
                    index = selected_rows[0]
                    original_doc = data[index]
                    doc_id = original_doc["_id"]

                    st.divider()
                    st.subheader(f"🛠️ Managing Record: {doc_id}")
                    with st.container(border=True):
                        editable_content = {k: v for k, v in original_doc.items() if k != "_id"}
                        edited_text = st.text_area("JSON Content", value=json.dumps(editable_content, indent=4, cls=MongoEncoder), height=350, key=f"editor_{doc_id}")
                        
                        btn_col1, btn_col2 = st.columns(2)
                        if btn_col1.button("💾 Save Changes", type="secondary", use_container_width=True):
                            try:
                                updated_json = json.loads(edited_text)
                                coll.update_one({"_id": doc_id}, {"$set": updated_json})
                                st.success("✅ Changes saved!")
                                time.sleep(1)
                                st.rerun()
                            except Exception as e:
                                st.error(f"Invalid JSON: {e}")

                        if btn_col2.button("🗑️ Delete Record", type="secondary", use_container_width=True):
                            st.session_state.confirm_delete = doc_id

                    if st.session_state.confirm_delete == doc_id:
                        st.warning(f"⚠️ Are you sure you want to delete `{doc_id}`?")
                        c1, c2 = st.columns(2)
                        if c1.button("🔥 Yes, Delete", type="primary", use_container_width=True):
                            coll.delete_one({"_id": doc_id})
                            st.session_state.confirm_delete = None
                            st.success("Deleted!")
                            time.sleep(1)
                            st.rerun()
                        if c2.button("Cancel", use_container_width=True):
                            st.session_state.confirm_delete = None
                            st.rerun()

    except Exception as e:
        st.error(f"Connection Error: {e}")    
