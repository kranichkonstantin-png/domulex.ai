# Lawyer Mode - Professional Legal Workbench

## Overview
DOMULEX Lawyer Mode provides a professional-grade legal research and drafting environment designed specifically for attorneys handling real estate cases across multiple jurisdictions (Germany, Spain, United States).

## Features

### 1. **2-Column Productivity Layout**
- **Left Panel (60%)**: Large document editor with 600px height for drafting legal briefs, motions, and documents
- **Right Panel (40%)**: Tabbed intelligence sidebar with research tools

### 2. **Document Editor**
- Full-featured text area for legal drafting
- Real-time word count and character statistics
- Persistent draft storage in session state
- Optimized for long-form legal writing

### 3. **Contextual Research Tab** 🔍
**Purpose**: Find both supporting AND opposing precedents for selected text

**Workflow**:
1. Highlight/copy text from your draft
2. Paste into "Selected text to research" field
3. Click "Analyze Selection"
4. Receive structured citations (no summaries)

**Output Format**:
```
1. BGH VIII ZR 30/20 - Mietrecht: Schönheitsreparaturen
   DE · 2021-03-15

2. AG München 412 C 5678/20
   DE · 2020-11-22
```

**Backend Integration**:
- Uses existing `/query` endpoint with role="LAWYER"
- Prompt: "Find legal precedents both supporting AND opposing this argument: {text}"
- Returns `sources` array with court, date, title, URL

### 4. **Devil's Advocate Tab** ⚠️
**Purpose**: Expose weaknesses before opposing counsel does

**Workflow**:
1. Paste your legal argument
2. Click "Attack This Argument"
3. AI assumes opposing counsel role
4. Identifies logical gaps, counterarguments, and risks

**Prompt Template**:
```
You are opposing counsel. Find all logical gaps, weak points, 
and counterarguments to this position: {argument}
```

**Display**:
- Critique shown in red error box (`st.error()`)
- Supporting sources listed below with expander
- Helps strengthen arguments before filing

### 5. **Precedents Tab** 📚
**Enhanced Source Display with Court Filtering**

**Court Filter Options**:
- All Courts (default)
- BGH (Germany Supreme Court)
- BFH (Federal Tax Court)
- BVerfG (Constitutional Court)
- Supreme Court (US)
- Circuit Courts (US)
- District Courts (US)
- Tribunal Supremo (Spain)

**Precedent Card Structure**:
```
📄 1. BGH VIII ZR 30/20 - Schönheitsreparaturen

Court: DE                    Type: Case Law
Date: 2021-03-15             File No.: VIII ZR 30/20

📌 Leitsatz:
[Headnote/summary if available]

🔗 Source: https://...
```

**Features**:
- Deduplication (same URL = same case)
- Combined sources from Research + Critique tabs
- Court-level hierarchy filtering
- Structured metadata (Court, Date, File Number, Headnote)

## Activation

### Frontend
Select "⚖️ Lawyer" from the role dropdown in sidebar. This replaces the standard chat/dispute tabs with the workbench interface.

### Backend
The `LAWYER` role is now defined in `models/legal.py`:
```python
class UserRole(str, Enum):
    INVESTOR = "INVESTOR"
    LANDLORD = "LANDLORD"
    TENANT = "TENANT"
    OWNER = "OWNER"
    MANAGER = "MANAGER"
    MEDIATOR = "MEDIATOR"
    LAWYER = "LAWYER"  # Professional legal workbench mode
```

## Technical Architecture

### Session State Variables
```python
st.session_state.lawyer_draft = ""            # Current document text
st.session_state.research_results = []        # Array of source objects
st.session_state.critique_results = {}        # {critique: str, sources: []}
st.session_state.selected_court_filter = ""   # Active court filter
```

### API Integration
All features use the existing `/query` endpoint with:
- `role="LAWYER"`
- Custom prompts for research vs. critique
- Standard RAG pipeline with strict grounding (temp=0.0)

### Layout Code
```python
col_editor, col_intelligence = st.columns([3, 2])

with col_editor:
    # 600px text area

with col_intelligence:
    tab_research, tab_critique, tab_precedents = st.tabs([...])
```

## Differences from Standard User Modes

| Feature | Standard Users | Lawyer Mode |
|---------|---------------|-------------|
| **Interface** | Chat-based Q&A | 2-column workbench |
| **Citations** | In expandable sections | Structured cards with metadata |
| **Critique** | Not available | Devil's Advocate mode |
| **Court Filtering** | Not available | Hierarchy-based filtering |
| **Editor** | Chat input (1 line) | Full document editor (600px) |
| **Research** | Question → Answer | Selection → Citations only |

## Use Cases

### 1. **Motion Drafting**
- Draft motion in left panel
- Research each argument in right panel
- Test arguments with Devil's Advocate
- Insert citations directly into draft

### 2. **Case Preparation**
- Paste opposing counsel's argument
- Use Devil's Advocate to find their strongest points
- Research counter-precedents
- Filter by supreme court rulings only

### 3. **Client Memo Writing**
- Draft memo in editor
- Research supporting case law
- Check critique for risks
- Cite filtered BGH/BFH precedents

### 4. **Cross-Jurisdiction Analysis**
- Switch jurisdiction in sidebar
- Compare Florida vs. NY vs. German law
- Filter by Circuit Court level
- Get German explanations of US law (cultural bridge)

## Future Enhancements

### Planned Features
1. **Citation Export**: Copy all citations to clipboard in Bluebook/German format
2. **Precedent Comparison**: Side-by-side view of conflicting rulings
3. **Leitsatz Extraction**: AI-generated headnotes for sources without them
4. **Brief Templates**: Pre-filled templates for common motions
5. **Opposing Counsel Simulation**: Full dialogue with AI devil's advocate

### Integration Opportunities
1. **Document Assembly**: Merge research into draft with citation footnotes
2. **Collaboration**: Share workbench state with colleagues
3. **Version Control**: Track draft changes over time
4. **External Databases**: Integrate with Westlaw/LexisNexis APIs

## Testing

### Manual Testing Steps
1. Start backend: `uvicorn main:app --reload`
2. Start frontend: `streamlit run frontend_app.py`
3. Select "⚖️ Lawyer" role in sidebar
4. Verify 2-column layout appears
5. Type text in editor → verify word count updates
6. Test Research tab with sample legal argument
7. Test Devil's Advocate with same argument
8. Check Precedents tab shows both sets of sources
9. Test court filter (select "BGH" → verify filtering)

### Test Cases
```python
# Test 1: Research Query
Selection: "Tenant refuses to pay Schönheitsreparaturen"
Expected: 3-5 sources with BGH/AG cases
Verify: Citations in format "Court · Date"

# Test 2: Devil's Advocate
Argument: "Landlord can charge full deposit for minor wear"
Expected: Critique mentioning BGB §538, normal wear exclusion
Verify: Red error box with risks

# Test 3: Court Filter
Filter: "BGH (Germany Supreme)"
Expected: Only BGH cases shown
Verify: No AG (lower court) cases visible
```

## Production Readiness

### ✅ Completed
- [x] LAWYER role added to backend enum
- [x] LAWYER role added to frontend ROLE_MAP
- [x] 2-column layout implemented
- [x] Document editor with stats
- [x] Contextual research feature
- [x] Devil's Advocate critique mode
- [x] Enhanced source display
- [x] Court-level filtering
- [x] Session state management
- [x] Error handling for API calls

### ⏳ Pending
- [ ] Streamlit module installation
- [ ] End-to-end testing with backend
- [ ] Mobile responsiveness check
- [ ] Performance testing with large drafts (10,000+ words)
- [ ] Citation export feature
- [ ] Document save/load functionality

## Documentation
- **Code**: `frontend_app.py` → `render_lawyer_workbench()`
- **Models**: `backend/models/legal.py` → `UserRole.LAWYER`
- **This File**: Architecture and user guide

---

**Status**: ✅ Feature Complete - Ready for Testing
**Last Updated**: 2024 (Implementation)
**Developed By**: DOMULEX Engineering Team
