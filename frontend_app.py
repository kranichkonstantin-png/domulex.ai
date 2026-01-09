"""
DOMULEX - Deep Adaptive Interface
Multi-Role Legal Tech Platform with Role-Specific UIs

Architecture:
- TENANT: Guardian (WhatsApp-like, Simple)
- INVESTOR: Deal Room (Dashboard, Analytical)
- MANAGER: Cockpit (CRM, Forms & Tools)
- LAWYER: Workbench (IDE-like, Split-screen)
"""

import os
import time
import streamlit as st
import requests
from datetime import datetime
from typing import Dict, List, Optional

# Import both subscription systems (legacy and new paywall)
from subscription import (
    render_subscription_widget,
    render_pricing_page,
    render_checkout_page,
    check_query_quota,
    increment_query_count,
)
from paywall import (
    render_quota_counter,
    show_paywall_modal,
    check_and_enforce_quota,
    check_feature_access,
    increment_query_count as increment_paywall_query,
    init_user_state,
    render_pricing_table_inline,
)

# Import new landing page and dashboard
from landing_page import render_landing_page, render_signup_page
from user_dashboard import render_user_dashboard, render_subscription_settings
import time


# ==================== CONFIGURATION ====================

st.set_page_config(
    page_title="DOMULEX - Adaptive Legal Platform",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Constants
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
MOCK_MODE = os.getenv("MOCK_MODE", "true").lower() == "true"

# Role Mappings
ROLE_MAP = {
    "👤 Tenant (Mieter)": "TENANT",
    "💼 Investor": "INVESTOR",
    "🏠 Landlord": "LANDLORD",
    "⚙️ Property Manager": "MANAGER",
    "🔑 Property Owner": "OWNER",
    "⚖️ Lawyer (Anwalt)": "LAWYER",
}

JURISDICTION_MAP = {
    "🇩🇪 Germany": "DE",
    "🇺🇸 United States": "US",
    "🇪🇸 Spain": "ES",
}

LANGUAGE_MAP = {
    "🇬🇧 English": "en",
    "🇩🇪 Deutsch": "de",
    "🇪🇸 Español": "es",
}

SUB_JURISDICTION_MAP = {
    "DE": [
        "Baden-Württemberg",
        "Bayern",
        "Berlin",
        "Brandenburg",
        "Bremen",
        "Hamburg",
        "Hessen",
        "Mecklenburg-Vorpommern",
        "Niedersachsen",
        "Nordrhein-Westfalen",
        "Rheinland-Pfalz",
        "Saarland",
        "Sachsen",
        "Sachsen-Anhalt",
        "Schleswig-Holstein",
        "Thüringen",
    ],
    "US": [
        "Alabama", "Alaska", "Arizona", "Arkansas", "California",
        "Colorado", "Connecticut", "Delaware", "Florida", "Georgia",
        "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa",
        "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland",
        "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri",
        "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey",
        "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio",
        "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina",
        "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
        "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming",
        "District of Columbia",
    ],
    "ES": [
        "Andalucía",
        "Aragón",
        "Asturias",
        "Baleares (Illes Balears)",
        "Canarias",
        "Cantabria",
        "Castilla-La Mancha",
        "Castilla y León",
        "Cataluña (Catalunya)",
        "Ceuta",
        "Comunidad Valenciana",
        "Extremadura",
        "Galicia",
        "La Rioja",
        "Madrid",
        "Melilla",
        "Murcia",
        "Navarra",
        "País Vasco (Euskadi)",
    ],
}


# ==================== MOCK DATA ====================

MOCK_RESPONSES = {
    "tenant_mold": {
        "answer": """**Ihre Rechte bei Schimmelbefall (Deutschland):**

1. **Mietminderung:** Bei erheblichem Schimmelbefall können Sie die Miete um 20-50% mindern (je nach Schweregrad).

2. **Mängelanzeige:** Informieren Sie Ihren Vermieter sofort schriftlich über den Mangel.

3. **Fristsetzung:** Setzen Sie dem Vermieter eine angemessene Frist zur Beseitigung (meist 2-4 Wochen).

4. **Selbstbeseitigung:** Nur in Notfällen dürfen Sie selbst handeln und die Kosten zurückfordern.

**Wichtig:** Dokumentieren Sie den Schimmel mit Fotos und Datum!""",
        "sources": [
            {
                "title": "BGH VIII ZR 271/11 - Schimmelbefall und Mietminderung",
                "jurisdiction": "DE",
                "publication_date": "2013-01-09",
                "source_url": "https://example.com/bgh-schimmel",
                "document_type": "Case Law",
            }
        ],
        "warning": "Dies ist keine Rechtsberatung. Konsultieren Sie bei ernsthaften Problemen einen Anwalt.",
    },
    "investor_risk": {
        "answer": "**Risikoanalyse Ihrer Immobilie:**\n\nLegal Risk: MEDIUM\nTax Impact: HIGH\nLiquidity: GOOD",
        "sources": [],
        "metrics": {
            "legal_risk": 45,
            "tax_impact": 78,
            "liquidity": 82,
            "roi_projection": 6.2,
        },
    },
}


# ==================== SESSION STATE ====================

def init_session_state():
    """Initialize all session state variables."""
    # Paywall system
    init_user_state()
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "role" not in st.session_state:
        st.session_state.role = "TENANT"
    if "jurisdiction" not in st.session_state:
        st.session_state.jurisdiction = "DE"
    if "language" not in st.session_state:
        st.session_state.language = "de"
    if "sub_jurisdiction" not in st.session_state:
        st.session_state.sub_jurisdiction = None
    if "lawyer_draft" not in st.session_state:
        st.session_state.lawyer_draft = ""
    if "research_results" not in st.session_state:
        st.session_state.research_results = []
    if "critique_results" not in st.session_state:
        st.session_state.critique_results = {}
    if "manager_form_data" not in st.session_state:
        st.session_state.manager_form_data = {}


# ==================== API FUNCTIONS ====================

def check_api_health() -> bool:
    """Check if backend API is available."""
    if MOCK_MODE:
        return False
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False


def query_backend(
    query: str,
    role: str,
    jurisdiction: str,
    language: str,
    sub_jurisdiction: Optional[str] = None,
) -> Dict:
    """Query the backend API or return mock data."""
    # NEW: Check quota with paywall system
    if not check_and_enforce_quota():
        return {
            "error": "Quota exceeded",
            "suggestion": "Upgrade to continue asking questions.",
        }
    
    # Check international search feature gate
    if jurisdiction != "DE" and st.session_state.user_tier == "FREE":
        if not check_feature_access("INTERNATIONAL_SEARCH"):
            return {
                "error": "Feature locked",
                "suggestion": "International search requires Mieter Plus or higher.",
            }
    
    # Increment query counter
    increment_paywall_query()
    
    if MOCK_MODE:
        time.sleep(1)  # Simulate API delay
        if "schimmel" in query.lower() or "mold" in query.lower():
            return MOCK_RESPONSES["tenant_mold"]
        return {
            "answer": f"Mock response for: {query}\n\nRole: {role}, Jurisdiction: {jurisdiction}",
            "sources": [
                {
                    "title": "Mock Source Document",
                    "jurisdiction": jurisdiction,
                    "publication_date": "2024-01-01",
                    "source_url": "https://example.com/mock",
                    "document_type": "Case Law",
                }
            ],
        }
    
    try:
        payload = {
            "query": query,
            "target_jurisdiction": jurisdiction,
            "user_role": role,
            "user_language": language,
            "sub_jurisdiction": sub_jurisdiction,
        }
        response = requests.post(f"{API_BASE_URL}/query", json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {
            "error": f"API Error: {str(e)}",
            "suggestion": "Backend offline. Enable MOCK_MODE or start backend.",
        }


# ==================== SIDEBAR ====================

def setup_sidebar():
    """Configure the global sidebar with all settings."""
    st.sidebar.title("⚙️ DOMULEX Settings")
    st.sidebar.markdown("---")
    
    # Dashboard Link (if authenticated)
    if st.session_state.get("authenticated", False):
        if st.sidebar.button("🏠 Dashboard", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()
        st.sidebar.markdown("---")
    
    # API Status
    api_healthy = check_api_health()
    if MOCK_MODE:
        st.sidebar.warning("🔧 **Mock Mode** (Offline Demo)")
    else:
        status_icon = "🟢" if api_healthy else "🔴"
        status_text = "Backend Online" if api_healthy else "Backend Offline"
        st.sidebar.markdown(f"{status_icon} **{status_text}**")
    
    st.sidebar.markdown("---")
    
    # User Role Selection
    st.sidebar.subheader("👤 Your Role")
    role_display = st.sidebar.selectbox(
        "Who are you?",
        options=list(ROLE_MAP.keys()),
        index=0,
        help="Select your role to see a customized interface",
    )
    st.session_state.role = ROLE_MAP[role_display]
    
    # Jurisdiction Selection
    st.sidebar.subheader("🌍 Jurisdiction")
    jurisdiction_display = st.sidebar.selectbox(
        "Which country's law?",
        options=list(JURISDICTION_MAP.keys()),
        index=0,
    )
    st.session_state.jurisdiction = JURISDICTION_MAP[jurisdiction_display]
    
    # Sub-Jurisdiction
    sub_options = ["(Not specified)"] + SUB_JURISDICTION_MAP.get(
        st.session_state.jurisdiction, []
    )
    sub_display = st.sidebar.selectbox(
        "State/Region (Optional)",
        options=sub_options,
    )
    st.session_state.sub_jurisdiction = (
        None if sub_display == "(Not specified)" else sub_display
    )
    
    # Language Selection
    st.sidebar.subheader("🗣️ Language")
    language_display = st.sidebar.selectbox(
        "Response language",
        options=list(LANGUAGE_MAP.keys()),
        index=1 if st.session_state.jurisdiction == "DE" else 0,
    )
    st.session_state.language = LANGUAGE_MAP[language_display]
    
    st.sidebar.markdown("---")
    
    # Quota Counter (NEW PAYWALL SYSTEM)
    render_quota_counter()
    
    st.sidebar.markdown("---")
    
    # Current Setup Display
    st.sidebar.info(
        f"""
        **Current Setup:**
        - Role: {st.session_state.role}
        - Country: {st.session_state.jurisdiction}
        - Region: {st.session_state.sub_jurisdiction or 'Any'}
        - Language: {st.session_state.language}
        """
    )
    
    # Reset button
    if st.sidebar.button("🔄 Reset All Data"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
            del st.session_state[key]
        st.rerun()


# ==================== TENANT UI (The Guardian) ====================

def render_tenant_ui():
    """
    Tenant UI: WhatsApp-like, Simple, Mobile-friendly.
    
    Features:
    - SOS Quick Action Buttons
    - Large clean chat interface
    - Simplified answers with hidden details
    """
    st.title("🛡️ DOMULEX Guardian")
    st.markdown("### Your Tenant Rights Assistant")
    st.markdown("---")
    
    # SOS Quick Action Buttons
    st.subheader("⚡ Quick Help")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💧 Mold / Schimmel", use_container_width=True, type="primary"):
            sos_prompt = f"What are my tenant rights regarding mold/schimmel in {st.session_state.jurisdiction}? Give me practical steps."
            st.session_state.messages.append({"role": "user", "content": sos_prompt})
            with st.spinner("🔍 Checking your rights..."):
                response = query_backend(
                    sos_prompt,
                    st.session_state.role,
                    st.session_state.jurisdiction,
                    st.session_state.language,
                    st.session_state.sub_jurisdiction,
                )
            st.session_state.messages.append({
                "role": "assistant",
                "content": response.get("answer", "No answer"),
                "sources": response.get("sources", []),
                "warning": response.get("warning"),
            })
            st.rerun()
    
    with col2:
        if st.button("📜 Eviction / Kündigung", use_container_width=True, type="primary"):
            sos_prompt = f"I received an eviction notice in {st.session_state.jurisdiction}. What should I do?"
            st.session_state.messages.append({"role": "user", "content": sos_prompt})
            with st.spinner("🔍 Analyzing eviction laws..."):
                response = query_backend(
                    sos_prompt,
                    st.session_state.role,
                    st.session_state.jurisdiction,
                    st.session_state.language,
                    st.session_state.sub_jurisdiction,
                )
            st.session_state.messages.append({
                "role": "assistant",
                "content": response.get("answer", "No answer"),
                "sources": response.get("sources", []),
                "warning": response.get("warning"),
            })
            st.rerun()
    
    with col3:
        if st.button("💰 Rent / Miete", use_container_width=True, type="primary"):
            sos_prompt = f"My landlord raised the rent in {st.session_state.jurisdiction}. Is this legal?"
            st.session_state.messages.append({"role": "user", "content": sos_prompt})
            with st.spinner("🔍 Checking rent laws..."):
                response = query_backend(
                    sos_prompt,
                    st.session_state.role,
                    st.session_state.jurisdiction,
                    st.session_state.language,
                    st.session_state.sub_jurisdiction,
                )
            st.session_state.messages.append({
                "role": "assistant",
                "content": response.get("answer", "No answer"),
                "sources": response.get("sources", []),
                "warning": response.get("warning"),
            })
            st.rerun()
    
    st.markdown("---")
    
    # Chat Interface
    st.subheader("💬 Chat with Guardian")
    
    # Display conversation
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Simplified source display for tenants
            if message["role"] == "assistant" and "sources" in message and message["sources"]:
                with st.expander("📚 Legal Sources (Click to expand)"):
                    for i, source in enumerate(message["sources"], 1):
                        st.markdown(f"**{i}.** [{source.get('title', 'Source')}]({source.get('source_url', '#')})")
            
            # Warning display
            if message["role"] == "assistant" and message.get("warning"):
                st.warning(message["warning"])
    
    # Chat input
    if prompt := st.chat_input("Ask your question... (e.g., 'Can my landlord enter without notice?')"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("🔍 Searching legal documents..."):
                response = query_backend(
                    prompt,
                    st.session_state.role,
                    st.session_state.jurisdiction,
                    st.session_state.language,
                    st.session_state.sub_jurisdiction,
                )
            
            if "error" in response:
                st.error(f"❌ {response['error']}")
                if "suggestion" in response:
                    st.info(f"💡 {response['suggestion']}")
            else:
                st.markdown(response.get("answer", "No answer available"))
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response.get("answer", ""),
                    "sources": response.get("sources", []),
                    "warning": response.get("warning"),
                })


# ==================== INVESTOR UI (The Deal Room) ====================

def render_investor_ui():
    """
    Investor UI: Bloomberg-like, Analytical, Dashboard-heavy.
    
    Features:
    - Risk meters and metrics
    - PDF analysis with structured reports
    - Two-column layout (Input | Analysis)
    """
    st.title("💼 DOMULEX Deal Room")
    st.markdown("### Real Estate Investment Analysis")
    st.markdown("---")
    
    # Two-column layout
    col_input, col_analysis = st.columns([1, 1])
    
    with col_input:
        st.subheader("📄 Investment Documents")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Upload Exposé or Contract (PDF)",
            type=["pdf"],
            help="Upload property documents for automated legal & financial analysis",
        )
        
        if uploaded_file:
            st.success(f"✅ Uploaded: {uploaded_file.name}")
            
            if st.button("🔍 Analyze Investment", type="primary", use_container_width=True):
                with st.spinner("⚙️ Running legal & financial analysis..."):
                    time.sleep(2)  # Mock analysis time
                    
                    # Mock metrics
                    st.session_state.investor_metrics = {
                        "legal_risk": 45,
                        "tax_impact": 78,
                        "liquidity": 82,
                        "roi_projection": 6.2,
                    }
                st.rerun()
        
        st.markdown("---")
        
        # Quick Query
        st.subheader("💬 Quick Legal Query")
        investor_query = st.text_area(
            "Ask about investment risks...",
            placeholder="e.g., What are the tax implications of buying rental property in Berlin?",
            height=150,
        )
        
        if st.button("🚀 Query", use_container_width=True):
            if investor_query:
                with st.spinner("🔍 Analyzing..."):
                    response = query_backend(
                        investor_query,
                        st.session_state.role,
                        st.session_state.jurisdiction,
                        st.session_state.language,
                        st.session_state.sub_jurisdiction,
                    )
                st.session_state.investor_response = response
                st.rerun()
    
    with col_analysis:
        st.subheader("📊 Investment Analysis")
        
        # Display metrics if available
        if "investor_metrics" in st.session_state:
            metrics = st.session_state.investor_metrics
            
            # Risk Meters
            col1, col2 = st.columns(2)
            with col1:
                st.metric(
                    "⚖️ Legal Risk",
                    f"{metrics['legal_risk']}%",
                    delta="-5%" if metrics['legal_risk'] < 50 else "+5%",
                    delta_color="inverse",
                )
                st.metric(
                    "💧 Liquidity",
                    f"{metrics['liquidity']}%",
                    delta="+10%",
                )
            
            with col2:
                st.metric(
                    "💰 Tax Impact",
                    f"{metrics['tax_impact']}%",
                    delta="+12%" if metrics['tax_impact'] > 50 else "-2%",
                    delta_color="inverse",
                )
                st.metric(
                    "📈 ROI Projection",
                    f"{metrics['roi_projection']}%",
                    delta="+0.5%",
                )
            
            st.markdown("---")
            
            # Red Flag Report
            st.subheader("🚩 Red Flags Detected")
            
            with st.status("⚠️ High Tax Burden", state="complete"):
                st.markdown("""
                **Issue:** Property located in high-tax municipality.
                
                **Impact:** 78% tax impact detected (above average).
                
                **Recommendation:** Consider tax-optimization strategies or alternative locations.
                
                **Sources:** [Grundsteuergesetz §25](https://example.com)
                """)
            
            with st.status("✅ Good Liquidity Position", state="complete"):
                st.markdown("""
                **Assessment:** Property in high-demand area with strong rental market.
                
                **Impact:** 82% liquidity score (excellent).
                
                **Recommendation:** Proceed with investment.
                """)
        
        else:
            st.info("📤 Upload a document or enter a query to see analysis.")
        
        # Display query response if available
        if "investor_response" in st.session_state:
            response = st.session_state.investor_response
            st.markdown("---")
            st.subheader("🧠 AI Analysis")
            st.markdown(response.get("answer", "No answer"))
            
            if response.get("sources"):
                with st.expander("📚 Legal Sources"):
                    for i, source in enumerate(response["sources"], 1):
                        st.markdown(
                            f"**{i}.** {source.get('title', 'Untitled')}  \n"
                            f"[{source.get('source_url', 'N/A')}]({source.get('source_url', '#')})"
                        )


# ==================== MANAGER UI (The Cockpit) ====================

def render_manager_ui():
    """
    Manager UI: CRM-like, Process-oriented, Forms & Generators.
    
    Features:
    - Legally Safe Document Generator
    - Rent increase calculator
    - Notice templates
    """
    st.title("⚙️ DOMULEX Cockpit")
    st.markdown("### Property Management Tools")
    st.markdown("---")
    
    # Tab navigation
    tab1, tab2, tab3 = st.tabs([
        "📝 Document Generator",
        "💬 Legal Assistant",
        "📊 Portfolio Overview"
    ])
    
    with tab1:
        st.subheader("⚖️ Legally Safe Document Generator")
        st.markdown("Generate legally compliant documents based on local laws.")
        
        # Document type selector
        doc_type = st.selectbox(
            "Document Type",
            options=[
                "Rent Increase Notice (Mieterhöhung)",
                "Termination Notice (Kündigung)",
                "Repair Request (Mängelanzeige)",
                "Rent Reduction (Mietminderung)",
            ],
        )
        
        st.markdown("---")
        
        # Form for Rent Increase (most complex example)
        if "Rent Increase" in doc_type:
            with st.form("rent_increase_form"):
                st.markdown("#### Rent Increase Details")
                
                col1, col2 = st.columns(2)
                with col1:
                    current_rent = st.number_input(
                        "Current Rent (€/month)",
                        min_value=0.0,
                        value=1000.0,
                        step=50.0,
                    )
                    new_rent = st.number_input(
                        "Proposed New Rent (€/month)",
                        min_value=0.0,
                        value=1100.0,
                        step=50.0,
                    )
                
                with col2:
                    increase_reason = st.selectbox(
                        "Legal Basis",
                        options=[
                            "Index Adjustment (Indexmiete)",
                            "Comparison Rent (Mietspiegel)",
                            "Modernization (Modernisierung)",
                        ],
                    )
                    effective_date = st.date_input(
                        "Effective Date",
                        value=datetime.now(),
                    )
                
                tenant_name = st.text_input("Tenant Name", value="Max Mustermann")
                property_address = st.text_area(
                    "Property Address",
                    value="Musterstraße 123\n12345 Berlin",
                    height=80,
                )
                
                submitted = st.form_submit_button(
                    "🚀 Generate Document",
                    type="primary",
                    use_container_width=True,
                )
                
                if submitted:
                    with st.spinner("⚖️ Generating legally compliant document..."):
                        time.sleep(2)
                        
                        # Mock document generation
                        st.session_state.generated_document = f"""
**MIETERHÖHUNGSERKLÄRUNG**
gemäß § 558 BGB

Sehr geehrte(r) {tenant_name},

hiermit erhöhen wir die Miete für die von Ihnen bewohnte Wohnung

{property_address}

von derzeit **{current_rent:.2f} EUR** auf **{new_rent:.2f} EUR** monatlich.

**Rechtliche Grundlage:** {increase_reason}

**Begründung:**
Die Erhöhung erfolgt gemäß § 558 BGB auf Grundlage des örtlichen Mietspiegels. 
Die neue Miete liegt innerhalb der ortsüblichen Vergleichsmiete.

**Wirksamkeit:** Die Erhöhung wird zum **{effective_date}** wirksam, 
frühestens jedoch nach Ablauf von zwei Monaten nach Zugang dieses Schreibens.

**Ihre Rechte:**
- Sie können der Erhöhung widersprechen (§ 558b BGB)
- Bei Zweifeln können Sie die Begründung überprüfen lassen
- Konsultieren Sie bei Bedarf einen Mieterverein

Mit freundlichen Grüßen,
Ihre Hausverwaltung

---
*Generiert von DOMULEX am {datetime.now().strftime("%d.%m.%Y")}*
*Jurisdiction: {st.session_state.jurisdiction} | Language: {st.session_state.language}*
"""
                    st.rerun()
        
        # Display generated document
        if "generated_document" in st.session_state:
            st.markdown("---")
            st.success("✅ Document Generated Successfully!")
            
            st.text_area(
                "Generated Document (Copy & Download)",
                value=st.session_state.generated_document,
                height=400,
            )
            
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    "📥 Download as TXT",
                    data=st.session_state.generated_document,
                    file_name=f"rent_increase_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain",
                    use_container_width=True,
                )
            with col2:
                if st.button("🔄 Generate New", use_container_width=True):
                    del st.session_state.generated_document
                    st.rerun()
    
    with tab2:
        st.subheader("💬 Legal Assistant for Managers")
        st.markdown("Ask legal questions about property management.")
        
        # Simple chat interface
        manager_query = st.text_area(
            "Your Question",
            placeholder="e.g., Can I terminate a tenant for non-payment after 2 months?",
            height=150,
        )
        
        if st.button("🔍 Ask", type="primary"):
            if manager_query:
                with st.spinner("🔍 Searching legal database..."):
                    response = query_backend(
                        manager_query,
                        st.session_state.role,
                        st.session_state.jurisdiction,
                        st.session_state.language,
                        st.session_state.sub_jurisdiction,
                    )
                
                st.markdown("#### Answer:")
                st.info(response.get("answer", "No answer"))
                
                if response.get("sources"):
                    with st.expander("📚 Legal Sources"):
                        for i, source in enumerate(response["sources"], 1):
                            st.markdown(
                                f"**{i}.** {source.get('title', 'Untitled')}  \n"
                                f"[Link]({source.get('source_url', '#')})"
                            )
    
    with tab3:
        st.subheader("📊 Portfolio Overview (Coming Soon)")
        st.info("This feature will show a dashboard of all managed properties.")


# ==================== LAWYER UI (The Workbench) ====================

def render_lawyer_workbench():
    """
    Lawyer UI: IDE-like, Split-screen, Professional.
    
    Features:
    - 2-column layout (Editor | AI Counsel)
    - Devil's Advocate mode
    - Precise citations with Aktenzeichen
    
    (Adapted from existing implementation)
    """
    st.title("⚖️ DOMULEX Legal Workbench")
    st.markdown("### Professional Legal Research & Drafting")
    st.markdown("---")
    
    # 2-Column Layout (60/40 split)
    col_editor, col_counsel = st.columns([2, 1])
    
    with col_editor:
        st.subheader("📝 Document Editor")
        
        draft_text = st.text_area(
            "Draft your legal brief, motion, or document",
            value=st.session_state.lawyer_draft,
            height=600,
            placeholder=(
                "Type or paste your legal document here...\n\n"
                "Highlight sections and use the AI Counsel panel → "
                "to research precedents or test arguments with Devil's Advocate."
            ),
        )
        
        st.session_state.lawyer_draft = draft_text
        
        # Stats
        word_count = len(draft_text.split()) if draft_text else 0
        char_count = len(draft_text)
        st.caption(f"📊 {word_count:,} words · {char_count:,} characters")
    
    with col_counsel:
        st.subheader("🧠 AI Legal Counsel")
        
        # Tabs for different functions
        tab_research, tab_devil, tab_precedents = st.tabs([
            "🔍 Research",
            "⚠️ Devil's Advocate",
            "📚 Precedents"
        ])
        
        with tab_research:
            st.markdown("**Contextual Legal Research**")
            st.markdown("Find supporting AND opposing precedents.")
            
            research_text = st.text_area(
                "Text to research",
                height=120,
                placeholder="Paste argument from your draft...",
            )
            
            if st.button("🔍 Analyze", type="primary", use_container_width=True):
                if research_text and len(research_text) > 10:
                    with st.spinner("⚖️ Searching case law..."):
                        response = query_backend(
                            f"Find legal precedents both supporting AND opposing: {research_text}",
                            "LAWYER",
                            st.session_state.jurisdiction,
                            st.session_state.language,
                            st.session_state.sub_jurisdiction,
                        )
                        st.session_state.research_results = response.get("sources", [])
                    st.success(f"✅ Found {len(st.session_state.research_results)} sources")
                else:
                    st.warning("⚠️ Enter at least 10 characters")
            
            # Display citations
            if st.session_state.research_results:
                st.markdown("---")
                st.markdown("**📖 Citations:**")
                for i, source in enumerate(st.session_state.research_results, 1):
                    st.markdown(
                        f"**{i}.** [{source.get('title', 'Untitled')}]({source.get('source_url', '#')})  \n"
                        f"&nbsp;&nbsp;&nbsp;&nbsp;{source.get('jurisdiction', 'N/A')} · {source.get('publication_date', 'N/A')}"
                    )
        
        with tab_devil:
            st.markdown("**👿 Opposing Counsel Mode**")
            st.markdown("Find weaknesses before they do.")
            
            critique_text = st.text_area(
                "Argument to attack",
                height=120,
                placeholder="Paste your legal argument...",
            )
            
            if st.button("⚔️ Attack", type="secondary", use_container_width=True):
                if critique_text and len(critique_text) > 10:
                    with st.spinner("👿 Analyzing as opposing counsel..."):
                        response = query_backend(
                            f"You are opposing counsel. Find all logical gaps and counterarguments to: {critique_text}",
                            "LAWYER",
                            st.session_state.jurisdiction,
                            st.session_state.language,
                            st.session_state.sub_jurisdiction,
                        )
                        st.session_state.critique_results = {
                            "critique": response.get("answer", ""),
                            "sources": response.get("sources", []),
                        }
                    st.success("✅ Critique complete")
                else:
                    st.warning("⚠️ Enter at least 10 characters")
            
            # Display critique
            if st.session_state.critique_results:
                st.markdown("---")
                st.error("⚠️ **Potential Weaknesses:**")
                st.markdown(st.session_state.critique_results.get("critique", ""))
        
        with tab_precedents:
            st.markdown("**📚 Source Library**")
            
            # Court filter
            court_filter = st.selectbox(
                "Filter by court",
                options=[
                    "All Courts",
                    "BGH (Supreme)",
                    "BFH (Tax)",
                    "BVerfG (Constitutional)",
                    "Supreme Court (US)",
                    "Circuit Courts (US)",
                ],
            )
            
            # Combine and display all sources
            all_sources = (
                st.session_state.research_results +
                st.session_state.critique_results.get("sources", [])
            )
            
            if all_sources:
                # Deduplicate
                unique_sources = {s.get("source_url"): s for s in all_sources}.values()
                
                st.markdown(f"**{len(unique_sources)} precedent(s) loaded**")
                
                for i, source in enumerate(unique_sources, 1):
                    with st.expander(f"📄 {i}. {source.get('title', 'Untitled')}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**Court:** {source.get('jurisdiction', 'N/A')}")
                            st.markdown(f"**Date:** {source.get('publication_date', 'N/A')}")
                        with col2:
                            st.markdown(f"**Type:** {source.get('document_type', 'Case Law')}")
                        
                        st.markdown(f"**🔗 [Source]({source.get('source_url', '#')})**")
            else:
                st.info("💡 Use Research or Devil's Advocate to load precedents.")


# ==================== MAIN ROUTER ====================

def main():
    """Main application router - Landing → Signup → Dashboard → App."""
    
    # Initialize session state
    init_session_state()
    
    # Check for URL parameters (Stripe success/cancel)
    try:
        params = st.query_params
        if "upgrade_success" in params:
            tier = params.get("tier", [""])[0] if isinstance(params.get("tier"), list) else params.get("tier", "")
            st.success(f"🎉 Zahlung erfolgreich! Ihr Account wurde auf **{tier}** upgraded!")
            st.balloons()
            # Update session state (in production: fetch from database)
            if tier:
                st.session_state.user_tier = tier
                st.session_state.queries_used = 0
            # Clear URL parameters
            st.query_params.clear()
            
        elif "upgrade_cancelled" in params:
            st.warning("ℹ️ Zahlung abgebrochen. Sie können jederzeit upgraden.")
            # Clear URL parameters
            st.query_params.clear()
    except Exception:
        pass  # No query params or error parsing them
    
    # Initialize page routing
    if "page" not in st.session_state:
        # Check if user is authenticated
        if st.session_state.get("authenticated", False):
            st.session_state.page = "dashboard"  # Logged in users see dashboard
        else:
            st.session_state.page = "landing"  # New visitors see landing page
    
    # Page router
    current_page = st.session_state.page
    
    # Landing Page (Marketing)
    if current_page == "landing":
        render_landing_page()
        return
    
    # Signup/Login Page
    elif current_page == "signup":
        render_signup_page()
        return
    
    # User Dashboard (Post-Login)
    elif current_page == "dashboard":
        render_user_dashboard()
        return
    
    # Subscription Settings
    elif current_page == "subscription_settings":
        render_subscription_settings()
        return
    
    # Main App (Chat Interface) - current_page == "app"
    # Check if paywall modal should be shown (NEW)
    if st.session_state.get("show_paywall", False):
        st.title("🚀 Upgrade erforderlich")
        show_paywall_modal(reason="quota")
        return
    
    # Check if pricing/checkout pages should be shown
    if st.session_state.get("show_pricing", False):
        render_pricing_page()
        if st.button("← Zurück zur App"):
            st.session_state.show_pricing = False
            st.rerun()
        return
    
    if st.session_state.get("show_checkout", False):
        render_checkout_page()
        if st.button("← Zurück"):
            st.session_state.show_checkout = False
            st.rerun()
        return
    
    # Setup global sidebar
    setup_sidebar()
    
    # Route to appropriate UI based on role
    role = st.session_state.role
    
    if role == "TENANT":
        render_tenant_ui()
    elif role == "INVESTOR":
        render_investor_ui()
    elif role in ["MANAGER", "LANDLORD", "OWNER"]:
        render_manager_ui()
    elif role == "LAWYER":
        render_lawyer_workbench()
    else:
        # Fallback for any undefined roles
        st.error(f"❌ Unknown role: {role}")
        st.info("Please select a valid role from the sidebar.")
    
    # Global disclaimer
    st.markdown("---")
    st.caption(
        "⚠️ **Disclaimer:** DOMULEX provides legal information, not legal advice. "
        "Consult a licensed attorney for specific legal matters."
    )


if __name__ == "__main__":
    main()
