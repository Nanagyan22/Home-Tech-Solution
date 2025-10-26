import streamlit as st
import os
import pandas as pd
from PIL import Image
from docx import Document
from gemini import chat_with_knowledge_base, generate_comprehensive_report
from dotenv import load_dotenv


# ENVIRONMENT SETUP
load_dotenv()

st.set_page_config(
    page_title="Home Tech Solution Dashboard",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# LOAD KNOWLEDGE BASE
@st.cache_data
def load_knowledge_base():
    """Load AI knowledge base from Word document and Excel dataset"""
    try:
        doc = Document("attached_assets/Home_Tech_Solution_Knowledge_Base.docx")
        knowledge_text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        
        dataset_path = "attached_assets/HomeTECH_Appartments.xlsx"
        df = pd.read_excel(dataset_path)
        
        excel_summary = f"""
DATASET SUMMARY (HomeTECH_Appartments.xlsx):

- Total Records: {len(df):,}
- Columns Available: {', '.join(df.columns)}
- Missing Values per Column:
{df.isnull().sum().to_string()}

BASIC STATISTICS (Numeric Columns):
{df.describe().to_string()}
"""
        return knowledge_text + "\n\n" + excel_summary
    except Exception as e:
        st.error(f"Error loading knowledge base: {e}")
        return ""


# LOAD DASHBOARDS
@st.cache_data
def load_dashboards():
    """Load both dashboard images"""
    try:
        home_dashboard = Image.open("attached_assets/Tech Dashboard.png")
        maintenance_dashboard = Image.open("attached_assets/Maintenance Dashboard.png")
        return home_dashboard, maintenance_dashboard
    except Exception as e:
        st.error(f"Error loading dashboards: {e}")
        return None, None


# HEADER
def display_header():
    """App branding"""
    st.markdown("""
        <h1 style='text-align: center; color: #156082; font-size: 48px;'>🏠 HOME TECH SOLUTION</h1>
        <p style='text-align: center; font-size: 22px; color: #666;'>Smart Apartment Monitoring Dashboard & AI Assistant</p>
        <hr style='margin-bottom: 20px;'>
    """, unsafe_allow_html=True)

# MAIN APP FUNCTION
def main():
    display_header()
    knowledge_base = load_knowledge_base()
    home_dashboard, maintenance_dashboard = load_dashboards()

    # Create two main layout columns
    dashboard_col, chat_col = st.columns([2.3, 1])

   
    # LEFT SIDE: DASHBOARD AREA (WITH TWO TABS)
    
    with dashboard_col:
        tab1, tab2 = st.tabs(["📊 Home Dashboard", "🛠 Maintenance Dashboard"])

        # TAB 1: HOME DASHBOARD 
        with tab1:
            st.markdown("### 📊 Apartment Energy & System Performance")
            if home_dashboard:
                st.image(home_dashboard, use_container_width=True, caption="Home Tech Energy Dashboard")
            else:
                st.warning("⚠️ Home Dashboard image not found.")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("📄 Generate Comprehensive AI Report", type="primary", key="report_home"):
                with st.spinner("Generating Home Tech Solution Insights Report..."):
                    if not os.environ.get("GEMINI_API_KEY"):
                        st.error("⚠️ GEMINI_API_KEY not set. Please add your API key.")
                    else:
                        report = generate_comprehensive_report(knowledge_base)
                        st.markdown("### 📋 Comprehensive System Insights Report")
                        st.markdown(report)

        # TAB 2: MAINTENANCE DASHBOARD 
        with tab2:
            st.markdown("### 🧰 Maintenance Overview and Performance Trends")
            if maintenance_dashboard:
                st.image(maintenance_dashboard, use_container_width=True, caption="Maintenance Performance Dashboard")
            else:
                st.warning("⚠️ Maintenance Dashboard image not found.")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("📊 Generate Maintenance Insights Report", type="primary", key="report_maintenance"):
                with st.spinner("Analyzing Maintenance Data..."):
                    if not os.environ.get("GEMINI_API_KEY"):
                        st.error("⚠️ GEMINI_API_KEY not set. Please add your API key.")
                    else:
                        report = generate_comprehensive_report(knowledge_base)
                        st.markdown("### 🧠 Maintenance Insights Report")
                        st.markdown(report)

   
    # RIGHT SIDE: CONSTANT CHAT ASSISTANT
    
    with chat_col:
        st.markdown("### 🤖 AI Chat Assistant")
        st.markdown("*Ask questions about energy, performance, or maintenance data.*")

        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        if 'messages' not in st.session_state:
            st.session_state.messages = []

        chat_container = st.container(height=550)
        with chat_container:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        if prompt := st.chat_input("Ask about energy trends, HVAC issues, etc."):
            st.session_state.messages.append({"role": "user", "content": prompt})

            if not os.environ.get("GEMINI_API_KEY"):
                response = "⚠️ Please set your GEMINI_API_KEY to enable AI chat."
            else:
                with st.spinner("Analyzing your question..."):
                    response = chat_with_knowledge_base(prompt, knowledge_base, st.session_state.chat_history)
                    st.session_state.chat_history.append(f"User: {prompt}")
                    st.session_state.chat_history.append(f"Assistant: {response}")

            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

        if st.button("🗑️ Clear Chat", key="clear_chat"):
            st.session_state.messages = []
            st.session_state.chat_history = []
            st.rerun()

        with st.expander("💡 Sample Questions"):
            st.markdown("""
            - What’s the total energy consumption across all apartments?
            - Which apartment requires the most maintenance?
            - When do energy peaks occur most frequently?
            - How does HVAC usage affect energy efficiency?
            - What percentage of maintenance issues involve HVAC failures?
            - What’s the average indoor temperature?
            - How can maintenance scheduling be improved?
            """)


# RUN APP

if __name__ == "__main__":
    main()
