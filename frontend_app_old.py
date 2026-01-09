"""
DOMULEX - Legal Tech Platform Frontend
Multi-Jurisdiction Real Estate Legal Assistant

Built with Streamlit for rapid MVP deployment.
"""

import streamlit as st
import requests
from datetime import datetime
from typing import Dict, List, Optional


# Page configuration
st.set_page_config(
    page_title="DOMULEX - Global Real Estate Legal Assistant",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Constants
API_BASE_URL = "http://localhost:8000"

# Mapping configurations
ROLE_MAP = {
    "🏢 Investor": "INVESTOR",
    "🏠 Landlord": "LANDLORD",
    "👤 Tenant": "TENANT",
    "🔑 Property Owner": "OWNER",
    "⚙️ Property Manager": "MANAGER",
    "⚖️ Lawyer": "LAWYER",
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
    "DE": ["Bayern", "NRW", "Berlin", "Hamburg", "Hessen"],
    "US": ["Florida", "New York", "California"],
    "ES": ["Madrid", "Catalunya", "Baleares", "Andalucía"],
}


def init_session_state():
    """Initialize session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "api_status" not in st.session_state:
        st.session_state.api_status = None


def check_api_health() -> bool:
    """Check if the backend API is accessible."""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except Exception:
        return False


def query_backend(
    query: str,
    role: str,
    jurisdiction: str,
    language: str,
    sub_jurisdiction: Optional[str] = None,
) -> Dict:
    """
    Query the DOMULEX backend API.
    
    Args:
        query: User's legal question
        role: User role (INVESTOR, LANDLORD, etc.)
        jurisdiction: Target jurisdiction (DE, ES, US)
        language: Response language (de, es, en)
        sub_jurisdiction: Optional state/region
        
    Returns:
        API response dict
    """
    payload = {
        "query": query,
        "target_jurisdiction": jurisdiction,
        "user_role": role,
        "user_language": language,
    }
    
    if sub_jurisdiction:
        payload["sub_jurisdiction"] = sub_jurisdiction
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/query",
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.ConnectionError:
        return {
            "error": "Cannot connect to backend API. Please ensure the backend is running.",
            "suggestion": "Run: cd backend && uvicorn main:app --reload"
        }
    except requests.exceptions.Timeout:
        return {
            "error": "Request timed out. The query may be too complex.",
        }
    except Exception as e:
        return {
            "error": f"API Error: {str(e)}",
        }


def analyze_contract_backend(
    pdf_file,
    jurisdiction: str,
    role: str,
) -> Dict:
    """
    Analyze a PDF contract using the backend API.
    
    Args:
        pdf_file: Uploaded PDF file from Streamlit
        jurisdiction: Target jurisdiction (DE, ES, US)
        role: User role (TENANT, LANDLORD, etc.)
        
    Returns:
        API response dict with contract analysis
    """
    try:
        files = {"file": (pdf_file.name, pdf_file, "application/pdf")}
        data = {
            "jurisdiction": jurisdiction,
            "user_role": role,
        }
        
        response = requests.post(
            f"{API_BASE_URL}/analyze_contract",
            files=files,
            data=data,
            timeout=60,  # Longer timeout for analysis
        )
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.ConnectionError:
        return {
            "error": "Cannot connect to backend API. Please ensure the backend is running.",
        }
    except requests.exceptions.Timeout:
        return {
            "error": "Analysis timed out. The PDF may be too large or complex.",
        }
    except Exception as e:
        return {
            "error": f"Analysis failed: {str(e)}",
        }


def resolve_conflict_backend(
    party_a_statement: str,
    party_b_statement: str,
    jurisdiction: str,
    party_a_label: str,
    party_b_label: str,
    language: str,
) -> Dict:
    """
    Analyze a dispute using the conflict resolution API.
    
    Args:
        party_a_statement: First party's perspective
        party_b_statement: Second party's perspective
        jurisdiction: Target jurisdiction (DE, ES, US)
        party_a_label: Label for party A (e.g., "Landlord")
        party_b_label: Label for party B (e.g., "Tenant")
        language: Response language
        
    Returns:
        API response dict with mediation analysis
    """
    try:
        payload = {
            "party_a_statement": party_a_statement,
            "party_b_statement": party_b_statement,
            "jurisdiction": jurisdiction,
            "party_a_label": party_a_label,
            "party_b_label": party_b_label,
            "user_language": language,
        }
        
        response = requests.post(
            f"{API_BASE_URL}/resolve_conflict",
            json=payload,
            timeout=60,
        )
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.ConnectionError:
        return {
            "error": "Cannot connect to backend API. Please ensure the backend is running.",
        }
    except requests.exceptions.Timeout:
        return {
            "error": "Analysis timed out. The dispute may be too complex.",
        }
    except Exception as e:
        return {
            "error": f"Conflict resolution failed: {str(e)}",
        }


def render_sidebar():
    """Render the configuration sidebar."""
    st.sidebar.title("⚙️ Configuration")
    st.sidebar.markdown("---")
    
    # API Status
    api_healthy = check_api_health()
    status_icon = "🟢" if api_healthy else "🔴"
    status_text = "Backend Online" if api_healthy else "Backend Offline"
    st.sidebar.markdown(f"{status_icon} **{status_text}**")
    
    if not api_healthy:
        st.sidebar.error("⚠️ Start backend: `uvicorn main:app --reload`")
    
    st.sidebar.markdown("---")
    
    # User Role Selection
    st.sidebar.subheader("👤 Your Role")
    role_display = st.sidebar.selectbox(
        "Select your role",
        options=list(ROLE_MAP.keys()),
        index=0,
        help="Your role determines the context and type of legal advice you receive."
    )
    role = ROLE_MAP[role_display]
    
    # Jurisdiction Selection
    st.sidebar.subheader("🌍 Target Country")
    jurisdiction_display = st.sidebar.selectbox(
        "Which country's law?",
        options=list(JURISDICTION_MAP.keys()),
        index=0,
        help="Select the jurisdiction whose legal system you want to query."
    )
    jurisdiction = JURISDICTION_MAP[jurisdiction_display]
    
    # Sub-Jurisdiction (State/Region)
    st.sidebar.subheader("📍 State/Region (Optional)")
    sub_jurisdiction_options = ["(Not specified)"] + SUB_JURISDICTION_MAP.get(jurisdiction, [])
    sub_jurisdiction_display = st.sidebar.selectbox(
        "Specific state or region",
        options=sub_jurisdiction_options,
        help="Some laws vary by state (US) or autonomous community (ES)."
    )
    sub_jurisdiction = None if sub_jurisdiction_display == "(Not specified)" else sub_jurisdiction_display
    
    # Language Selection
    st.sidebar.subheader("🗣️ Your Language")
    language_display = st.sidebar.selectbox(
        "Response language",
        options=list(LANGUAGE_MAP.keys()),
        index=0,
        help="The language in which you want the legal explanation."
    )
    language = LANGUAGE_MAP[language_display]
    
    st.sidebar.markdown("---")
    
    # Info Box
    st.sidebar.info(
        f"""
        **Current Setup:**
        - Role: {role}
        - Country: {jurisdiction}
        - Region: {sub_jurisdiction or 'Any'}
        - Language: {language}
        """
    )
    
    # Cultural Bridge Info
    if jurisdiction == "US" and language == "de":
        st.sidebar.success(
            "🌉 **Cultural Bridge Active!**\n\n"
            "You'll get US law explained in German with comparisons to German concepts "
            "(e.g., 'Security Deposit' vs. 'Kaution')."
        )
    
    st.sidebar.markdown("---")
    
    # Contract Upload & Analysis
    st.sidebar.subheader("📄 Contract Analysis")
    uploaded_file = st.sidebar.file_uploader(
        "Upload Contract (PDF)",
        type=["pdf"],
        help="Upload a lease/rental contract for automated legal analysis"
    )
    
    if uploaded_file:
        st.sidebar.info(f"📎 **{uploaded_file.name}** ({uploaded_file.size // 1024} KB)")
        
        if st.sidebar.button("🔍 Analyze Contract", type="primary"):
            with st.spinner("⚖️ Analyzing contract clauses..."):
                analysis_result = analyze_contract_backend(
                    pdf_file=uploaded_file,
                    jurisdiction=jurisdiction,
                    role=role,
                )
            
            # Store in session state for display
            st.session_state["contract_analysis"] = analysis_result
            st.rerun()
    
    return role, jurisdiction, language, sub_jurisdiction


def render_chat_interface(role: str, jurisdiction: str, language: str, sub_jurisdiction: Optional[str]):
    """Render the main chat interface."""
    
    # Header
    st.title("🏛️ DOMULEX")
    st.markdown("### Global Real Estate Legal Assistant")
    st.markdown(
        f"**Ask legal questions about {JURISDICTION_MAP_REVERSE[jurisdiction]} real estate law, "
        f"answered in {LANGUAGE_MAP_REVERSE[language]}.**"
    )
    st.markdown("---")
    
    # Display contract analysis if available
    if "contract_analysis" in st.session_state:
        display_contract_analysis(st.session_state["contract_analysis"])
        st.markdown("---")
    
    # Display conversation history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Display sources if available
            if message["role"] == "assistant" and "sources" in message:
                with st.expander("📚 Legal Sources Used"):
                    for i, source in enumerate(message["sources"], 1):
                        st.markdown(
                            f"""
                            **{i}. {source.get('title', 'Untitled')}**
                            - **Jurisdiction:** {source.get('jurisdiction', 'N/A')}
                            - **Date:** {source.get('publication_date', 'N/A')}
                            - **Source:** [{source.get('source_url', 'N/A')}]({source.get('source_url', '#')})
                            - **Type:** {source.get('document_type', 'N/A')}
                            """
                        )
            
            # Display warnings if available
            if message["role"] == "assistant" and "warning" in message and message["warning"]:
                st.warning(message["warning"])
    
    # Chat input
    if prompt := st.chat_input("Ask your legal question..."):
        # Add user message to chat
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
        })
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Query backend and display response
        with st.chat_message("assistant"):
            with st.spinner("🔍 Searching legal documents..."):
                response = query_backend(
                    query=prompt,
                    role=role,
                    jurisdiction=jurisdiction,
                    language=language,
                    sub_jurisdiction=sub_jurisdiction,
                )
            
            # Handle error responses
            if "error" in response:
                error_message = f"❌ **Error:** {response['error']}"
                if "suggestion" in response:
                    error_message += f"\n\n💡 **Suggestion:** {response['suggestion']}"
                st.error(error_message)
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_message,
                })
            else:
                # Display answer
                answer = response.get("answer", "No answer received.")
                st.markdown(answer)
                
                # Display sources
                sources = response.get("sources", [])
                if sources:
                    with st.expander("📚 Legal Sources Used"):
                        for i, source in enumerate(sources, 1):
                            st.markdown(
                                f"""
                                **{i}. {source.get('title', 'Untitled')}**
                                - **Jurisdiction:** {source.get('jurisdiction', 'N/A')}
                                - **Date:** {source.get('publication_date', 'N/A')}
                                - **Source:** [{source.get('source_url', 'N/A')}]({source.get('source_url', '#')})
                                - **Type:** {source.get('document_type', 'N/A')}
                                """
                            )
                
                # Display jurisdiction warning if present
                warning = response.get("jurisdiction_warning")
                if warning:
                    st.warning(warning)
                
                # Add assistant message to chat history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources,
                    "warning": warning,
                })


def render_disclaimer():
    """Render legal disclaimer at the bottom."""
    st.markdown("---")
    st.markdown(
        """
        <div style="background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #ffc107;">
        <h4 style="margin-top: 0; color: #856404;">⚠️ Legal Disclaimer</h4>
        <p style="margin-bottom: 0; color: #856404;">
        <strong>DOMULEX is an AI-powered research assistant, NOT a lawyer.</strong><br>
        The information provided here is for educational and informational purposes only and does not constitute 
        legal advice. Laws vary by jurisdiction and change frequently. Always consult a licensed attorney in your 
        jurisdiction for specific legal advice. DOMULEX and its creators assume no liability for actions taken 
        based on this information.
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Footer
    st.markdown(
        """
        <div style="text-align: center; margin-top: 2rem; color: #666;">
        <p>🏛️ <strong>DOMULEX</strong> | Global Real Estate Legal Tech Platform</p>
        <p style="font-size: 0.9rem;">Powered by Google Gemini 1.5 Pro • Qdrant Vector Database • FastAPI</p>
        <p style="font-size: 0.8rem;">Supported Jurisdictions: 🇩🇪 Germany • 🇺🇸 USA • 🇪🇸 Spain</p>
        </div>
        """,
        unsafe_allow_html=True
    )


# Reverse mappings for display
JURISDICTION_MAP_REVERSE = {v: k for k, v in JURISDICTION_MAP.items()}
LANGUAGE_MAP_REVERSE = {v: k for k, v in LANGUAGE_MAP.items()}


def display_contract_analysis(analysis: Dict):
    """
    Display contract analysis results with risk indicators.
    
    Args:
        analysis: Analysis result from backend API
    """
    if "error" in analysis:
        st.error(f"❌ {analysis['error']}")
        return
    
    # Overall summary
    st.subheader("📋 Contract Analysis Report")
    
    # Risk badge
    overall_risk = analysis.get("overall_risk", "YELLOW")
    risk_colors = {
        "GREEN": "🟢",
        "YELLOW": "🟡",
        "RED": "🔴",
    }
    risk_icon = risk_colors.get(overall_risk, "⚪")
    
    st.markdown(f"### {risk_icon} Overall Risk: **{overall_risk}**")
    st.info(analysis.get("summary", "No summary available"))
    
    # Statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Clauses", analysis.get("total_clauses_analyzed", 0))
    with col2:
        st.metric("🔴 Critical", analysis.get("red_flags", 0))
    with col3:
        st.metric("🟡 Warnings", analysis.get("yellow_flags", 0))
    with col4:
        st.metric("🟢 OK", analysis.get("green_flags", 0))
    
    st.markdown("---")
    
    # Detailed clause analysis
    clauses = analysis.get("clauses", [])
    
    if clauses:
        st.subheader("📝 Clause-by-Clause Analysis")
        
        for i, clause in enumerate(clauses, 1):
            risk = clause.get("risk_level", "YELLOW")
            icon = risk_colors.get(risk, "⚪")
            
            with st.expander(f"{icon} {i}. {clause.get('clause_type', 'Unknown Clause')} - **{risk}**"):
                # Contract text
                st.markdown("**📄 Contract Clause:**")
                st.text_area(
                    "Contract Text",
                    clause.get("clause_text", "N/A"),
                    height=80,
                    key=f"clause_{i}_text",
                    label_visibility="collapsed"
                )
                
                # Legal standard
                st.markdown("**⚖️ Legal Standard:**")
                st.markdown(clause.get("legal_standard", "No legal standard found"))
                
                if clause.get("source_title"):
                    st.caption(f"Source: [{clause['source_title']}]({clause.get('source_url', '#')})")
                
                # Comparison
                st.markdown("**🔍 Analysis:**")
                st.markdown(clause.get("comparison", "No comparison available"))
                
                # Recommendation
                if clause.get("recommendation"):
                    if risk == "RED":
                        st.error(f"⚠️ **Recommendation:** {clause['recommendation']}")
                    elif risk == "YELLOW":
                        st.warning(f"💡 **Recommendation:** {clause['recommendation']}")
                    else:
                        st.success(f"✅ **Recommendation:** {clause['recommendation']}")
    
    # Clear button
    if st.button("🗑️ Clear Analysis"):
        if "contract_analysis" in st.session_state:
            del st.session_state["contract_analysis"]
        st.rerun()


def render_lawyer_workbench(jurisdiction: str, language: str, sub_jurisdiction: Optional[str]):
    """
    Render the professional lawyer workbench with 2-column layout.
    
    Features:
    - Large text editor for drafting legal documents
    - Contextual research panel with "Analyze Selection" feature
    - Devil's Advocate mode for opposing counsel critique
    - Enhanced source citations with court-level filtering
    
    Args:
        jurisdiction: Target jurisdiction
        language: Response language
        sub_jurisdiction: Optional state/region
    """
    st.title("⚖️ DOMULEX Legal Workbench")
    st.markdown("### Professional Legal Research & Drafting Environment")
    st.markdown("---")
    
    # Initialize session state for lawyer mode
    if "lawyer_draft" not in st.session_state:
        st.session_state.lawyer_draft = ""
    if "research_results" not in st.session_state:
        st.session_state.research_results = []
    if "critique_results" not in st.session_state:
        st.session_state.critique_results = []
    if "selected_court_filter" not in st.session_state:
        st.session_state.selected_court_filter = "All Courts"
    
    # 2-Column Layout: Editor (3) + Intelligence Sidebar (2)
    col_editor, col_intelligence = st.columns([3, 2])
    
    with col_editor:
        st.subheader("📝 Document Editor")
        
        # Large text area for drafting
        draft_text = st.text_area(
            "Draft your legal document, motion, or brief",
            value=st.session_state.lawyer_draft,
            height=600,
            placeholder=(
                "Type or paste your legal text here...\n\n"
                "Highlight any section and use the 'Analyze Selection' button "
                "in the right panel to research supporting and opposing precedents."
            ),
            key="lawyer_editor"
        )
        
        # Update session state
        st.session_state.lawyer_draft = draft_text
        
        # Word count and character stats
        word_count = len(draft_text.split()) if draft_text else 0
        char_count = len(draft_text)
        
        st.caption(f"📊 {word_count:,} words · {char_count:,} characters")
    
    with col_intelligence:
        st.subheader("🧠 Legal Intelligence")
        
        # Tabs for different intelligence features
        tab_research, tab_critique, tab_precedents = st.tabs([
            "🔍 Research",
            "⚠️ Devil's Advocate",
            "📚 Precedents"
        ])
        
        with tab_research:
            st.markdown("**Contextual Legal Research**")
            st.markdown(
                "Highlight text in the editor and click below to find "
                "supporting AND conflicting rulings."
            )
            
            # Selection input
            selected_text = st.text_area(
                "Selected text to research",
                height=100,
                placeholder="Paste the text you want to research...",
                help="Copy text from the editor to analyze"
            )
            
            if st.button("🔍 Analyze Selection", type="primary", use_container_width=True):
                if selected_text and len(selected_text) > 10:
                    with st.spinner("⚖️ Researching case law and statutes..."):
                        # Query backend for research
                        response = query_backend(
                            query=f"Find legal precedents both supporting AND opposing this argument: {selected_text}",
                            role="LAWYER",
                            jurisdiction=jurisdiction,
                            language=language,
                            sub_jurisdiction=sub_jurisdiction,
                        )
                        
                        if "error" not in response:
                            st.session_state.research_results = response.get("sources", [])
                            st.success(f"✅ Found {len(st.session_state.research_results)} relevant sources")
                        else:
                            st.error(f"❌ Research failed: {response['error']}")
                else:
                    st.warning("⚠️ Please enter at least 10 characters to research.")
            
            # Display research results - CITATIONS ONLY
            if st.session_state.research_results:
                st.markdown("---")
                st.markdown("**📖 Citations Found:**")
                
                for i, source in enumerate(st.session_state.research_results, 1):
                    court = source.get("jurisdiction", "N/A")
                    date = source.get("publication_date", "N/A")
                    title = source.get("title", "Untitled")
                    url = source.get("source_url", "#")
                    
                    # Format as structured citation
                    st.markdown(
                        f"**{i}.** [{title}]({url})  \n"
                        f"&nbsp;&nbsp;&nbsp;&nbsp;{court} · {date}"
                    )
        
        with tab_critique:
            st.markdown("**👿 Opposing Counsel Perspective**")
            st.markdown(
                "Get a critical analysis from the opposing side's viewpoint. "
                "This helps identify weaknesses before they're exploited."
            )
            
            critique_text = st.text_area(
                "Argument to critique",
                height=100,
                placeholder="Paste your legal argument...",
                help="The AI will act as opposing counsel"
            )
            
            if st.button("⚔️ Attack This Argument", type="secondary", use_container_width=True):
                if critique_text and len(critique_text) > 10:
                    with st.spinner("👿 Analyzing from opposing counsel's perspective..."):
                        # Query backend with Devil's Advocate prompt
                        response = query_backend(
                            query=(
                                f"You are opposing counsel. Find all logical gaps, weak points, "
                                f"and counterarguments to this position: {critique_text}"
                            ),
                            role="LAWYER",
                            jurisdiction=jurisdiction,
                            language=language,
                            sub_jurisdiction=sub_jurisdiction,
                        )
                        
                        if "error" not in response:
                            critique_answer = response.get("answer", "")
                            st.session_state.critique_results = {
                                "critique": critique_answer,
                                "sources": response.get("sources", [])
                            }
                        else:
                            st.error(f"❌ Critique failed: {response['error']}")
                else:
                    st.warning("⚠️ Please enter at least 10 characters to critique.")
            
            # Display critique results
            if st.session_state.critique_results:
                st.markdown("---")
                st.error("⚠️ **Potential Weaknesses:**")
                st.markdown(st.session_state.critique_results.get("critique", ""))
                
                # Show sources used in critique
                critique_sources = st.session_state.critique_results.get("sources", [])
                if critique_sources:
                    with st.expander(f"📚 Opposing Arguments ({len(critique_sources)})"):
                        for i, source in enumerate(critique_sources, 1):
                            st.markdown(
                                f"**{i}.** {source.get('title', 'Untitled')}  \n"
                                f"&nbsp;&nbsp;&nbsp;&nbsp;[{source.get('source_url', 'N/A')}]({source.get('source_url', '#')})"
                            )
        
        with tab_precedents:
            st.markdown("**📚 Enhanced Source Display**")
            
            # Court level filter
            court_filter = st.selectbox(
                "Filter by court level",
                options=[
                    "All Courts",
                    "BGH (Germany Supreme)",
                    "BFH (Tax Court)",
                    "BVerfG (Constitutional)",
                    "Supreme Court (US)",
                    "Circuit Courts (US)",
                    "District Courts (US)",
                    "Tribunal Supremo (ES)",
                ],
                help="Filter precedents by court hierarchy"
            )
            st.session_state.selected_court_filter = court_filter
            
            # Display filtered sources
            all_sources = (
                st.session_state.research_results + 
                st.session_state.critique_results.get("sources", [])
            )
            
            if all_sources:
                # Remove duplicates based on URL
                unique_sources = {s.get("source_url"): s for s in all_sources}.values()
                
                # Filter by court if not "All Courts"
                if court_filter != "All Courts":
                    filtered_sources = [
                        s for s in unique_sources
                        if court_filter.split(" (")[0].upper() in s.get("title", "").upper()
                        or court_filter.split(" (")[0].upper() in s.get("jurisdiction", "").upper()
                    ]
                else:
                    filtered_sources = list(unique_sources)
                
                st.markdown(f"**Found {len(filtered_sources)} precedent(s):**")
                
                for i, source in enumerate(filtered_sources, 1):
                    with st.expander(f"📄 {i}. {source.get('title', 'Untitled')}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**Court:** {source.get('jurisdiction', 'N/A')}")
                            st.markdown(f"**Date:** {source.get('publication_date', 'N/A')}")
                        with col2:
                            st.markdown(f"**Type:** {source.get('document_type', 'Case Law')}")
                            st.markdown(f"**File No.:** {source.get('file_number', 'N/A')}")
                        
                        # Leitsatz (headnote) if available
                        if source.get("headnote"):
                            st.markdown("**📌 Leitsatz:**")
                            st.info(source["headnote"])
                        
                        st.markdown(f"**🔗 Source:** [{source.get('source_url', 'N/A')}]({source.get('source_url', '#')})")
            else:
                st.info("💡 No precedents loaded yet. Use the Research or Critique tabs to find cases.")


def main():
    """Main application function."""
    # Initialize session state
    init_session_state()
    
    # Render sidebar and get configuration
    role, jurisdiction, language, sub_jurisdiction = render_sidebar()
    
    # Check if user is in Lawyer mode
    if role == "LAWYER":
        # Show dedicated lawyer workbench
        render_lawyer_workbench(jurisdiction, language, sub_jurisdiction)
    else:
        # Create tabs for different modes (standard users)
        tab1, tab2 = st.tabs(["💬 Legal Assistant", "⚖️ Dispute Resolver"])
        
        with tab1:
            # Render main chat interface
            render_chat_interface(role, jurisdiction, language, sub_jurisdiction)
        
        with tab2:
            # Render dispute resolution interface
            render_dispute_resolver(jurisdiction, language)
    
    # Render disclaimer
    render_disclaimer()


def render_dispute_resolver(jurisdiction: str, language: str):
    """
    Render the dispute resolution interface.
    
    Args:
        jurisdiction: Target jurisdiction
        language: Response language
    """
    st.header("⚖️ Legal Dispute Resolver")
    st.markdown(
        """
        **Neutral mediation analysis for real estate disputes.**
        
        Enter both perspectives below, and our AI mediator will:
        - Analyze legal arguments for each side
        - Search relevant case law and precedents
        - Calculate litigation success probabilities
        - Recommend settlement or litigation strategy
        """
    )
    st.markdown("---")
    
    # Party labels
    col1, col2 = st.columns(2)
    with col1:
        party_a_label = st.text_input(
            "Party A Label",
            value="Landlord",
            help="e.g., Landlord, Seller, Owner"
        )
    with col2:
        party_b_label = st.text_input(
            "Party B Label",
            value="Tenant",
            help="e.g., Tenant, Buyer, Renter"
        )
    
    # Statement inputs
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"🔵 {party_a_label}'s Perspective")
        party_a_statement = st.text_area(
            f"{party_a_label}'s view",
            height=200,
            placeholder=f"Describe {party_a_label}'s perspective of the dispute...",
            help=f"Enter {party_a_label}'s side of the story in detail",
            label_visibility="collapsed"
        )
    
    with col2:
        st.subheader(f"🟠 {party_b_label}'s Perspective")
        party_b_statement = st.text_area(
            f"{party_b_label}'s view",
            height=200,
            placeholder=f"Describe {party_b_label}'s perspective of the dispute...",
            help=f"Enter {party_b_label}'s side of the story in detail",
            label_visibility="collapsed"
        )
    
    # Analyze button
    if st.button("🔍 Analyze Legal Situation", type="primary", use_container_width=True):
        if not party_a_statement or not party_b_statement:
            st.error("⚠️ Please provide both perspectives before analyzing.")
        elif len(party_a_statement) < 20 or len(party_b_statement) < 20:
            st.error("⚠️ Each perspective must be at least 20 characters.")
        else:
            with st.spinner("⚖️ Analyzing dispute from both perspectives..."):
                result = resolve_conflict_backend(
                    party_a_statement=party_a_statement,
                    party_b_statement=party_b_statement,
                    jurisdiction=jurisdiction,
                    party_a_label=party_a_label,
                    party_b_label=party_b_label,
                    language=language,
                )
            
            # Display results
            if "error" in result:
                st.error(f"❌ {result['error']}")
            else:
                display_conflict_resolution(result, party_a_label, party_b_label)


def display_conflict_resolution(analysis: Dict, party_a_label: str, party_b_label: str):
    """
    Display conflict resolution analysis results.
    
    Args:
        analysis: Analysis result from backend
        party_a_label: Label for party A
        party_b_label: Label for party B
    """
    st.markdown("---")
    st.subheader("📋 Mediation Analysis Report")
    
    # Dispute summary
    st.info(f"**Summary:** {analysis.get('dispute_summary', 'N/A')}")
    
    # Success probabilities
    st.markdown("### 📊 Litigation Success Probabilities")
    
    prob_a = analysis.get("success_probability_a", 50)
    prob_b = analysis.get("success_probability_b", 50)
    settlement = analysis.get("settlement_likelihood", 50)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            f"🔵 {party_a_label}",
            f"{prob_a:.0f}%",
            help="Probability of success if this goes to court"
        )
        st.progress(prob_a / 100)
    
    with col2:
        st.metric(
            f"🟠 {party_b_label}",
            f"{prob_b:.0f}%",
            help="Probability of success if this goes to court"
        )
        st.progress(prob_b / 100)
    
    with col3:
        st.metric(
            "🤝 Settlement",
            f"{settlement:.0f}%",
            help="Likelihood that settlement is the best option"
        )
        st.progress(settlement / 100)
    
    st.markdown("---")
    
    # Arguments for each party
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"### 🔵 Arguments for {party_a_label}")
        party_a_data = analysis.get("party_a_analysis", {})
        
        st.markdown("**Legal Basis:**")
        st.markdown(party_a_data.get("legal_arguments", "No arguments found"))
        
        st.markdown("**Strength Assessment:**")
        strength_a = party_a_data.get("strength_assessment", "Moderate")
        if "Strong" in strength_a:
            st.success(f"💪 {strength_a}")
        elif "Weak" in strength_a:
            st.error(f"⚠️ {strength_a}")
        else:
            st.warning(f"⚖️ {strength_a}")
        
        # Sources
        sources_a = party_a_data.get("supporting_sources", [])
        if sources_a:
            with st.expander(f"📚 Legal Sources ({len(sources_a)})"):
                for i, source in enumerate(sources_a, 1):
                    st.markdown(
                        f"**{i}. {source.get('title', 'Untitled')}**\n"
                        f"- [{source.get('source_url', 'N/A')}]({source.get('source_url', '#')})"
                    )
    
    with col2:
        st.markdown(f"### 🟠 Arguments for {party_b_label}")
        party_b_data = analysis.get("party_b_analysis", {})
        
        st.markdown("**Legal Basis:**")
        st.markdown(party_b_data.get("legal_arguments", "No arguments found"))
        
        st.markdown("**Strength Assessment:**")
        strength_b = party_b_data.get("strength_assessment", "Moderate")
        if "Strong" in strength_b:
            st.success(f"💪 {strength_b}")
        elif "Weak" in strength_b:
            st.error(f"⚠️ {strength_b}")
        else:
            st.warning(f"⚖️ {strength_b}")
        
        # Sources
        sources_b = party_b_data.get("supporting_sources", [])
        if sources_b:
            with st.expander(f"📚 Legal Sources ({len(sources_b)})"):
                for i, source in enumerate(sources_b, 1):
                    st.markdown(
                        f"**{i}. {source.get('title', 'Untitled')}**\n"
                        f"- [{source.get('source_url', 'N/A')}]({source.get('source_url', '#')})"
                    )
    
    st.markdown("---")
    
    # Neutral assessment
    st.markdown("### ⚖️ Neutral Legal Assessment")
    st.markdown(analysis.get("neutral_assessment", "No assessment available"))
    
    # Recommendation
    st.markdown("### 💡 Mediator's Recommendation")
    recommendation = analysis.get("recommendation", "No recommendation available")
    
    if settlement > 60:
        st.success(f"🤝 {recommendation}")
    elif prob_a > 70 or prob_b > 70:
        st.info(f"⚖️ {recommendation}")
    else:
        st.warning(f"⚠️ {recommendation}")


if __name__ == "__main__":
    main()
