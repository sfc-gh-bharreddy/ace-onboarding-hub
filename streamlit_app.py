"""
Snowflake ACE Onboarding Hub
A Streamlit application for new Activation Engineers at Snowflake.
"""

import json
import os
import streamlit as st

def _get_snowflake_connection():
    try:
        from snowflake.snowpark.context import get_active_session
        return "sis", get_active_session()
    except Exception:
        pass
    import snowflake.connector
    conn = snowflake.connector.connect(
        account=st.secrets["snowflake"]["account"],
        user=st.secrets["snowflake"]["user"],
        password=st.secrets["snowflake"]["password"],
        warehouse=st.secrets["snowflake"]["warehouse"],
        role=st.secrets["snowflake"].get("role", "ACCOUNTADMIN"),
    )
    return "connector", conn

st.set_page_config(
    page_title="ACE Onboarding Hub",
    page_icon="\u2744\ufe0f",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    html, body, [class*="css"] { font-family: 'Source Sans Pro', sans-serif; }

    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { padding: 10px 20px; font-weight: 600; }
    .stTabs [aria-selected="true"] { border-bottom: 3px solid #29B5E8; }

    .section-hdr {
        font-size: 1.5rem; font-weight: 700; color: #1E3A8A;
        border-bottom: 3px solid #29B5E8; padding-bottom: 6px;
        margin-top: 1.5rem; margin-bottom: 1rem;
    }

    .faq-category {
        font-size: 1.05rem; font-weight: 700; color: #1E40AF;
        background: #EFF6FF; padding: 10px 16px; border-radius: 8px;
        margin: 24px 0 8px 0; border-left: 4px solid #29B5E8;
    }

    .stat-card {
        background: linear-gradient(135deg, #E0F2FE 0%, #F0F9FF 100%);
        border-left: 4px solid #29B5E8; border-radius: 8px;
        padding: 16px 20px; margin-bottom: 12px;
    }
    .stat-card .num { font-size: 2rem; font-weight: 700; color: #1E3A8A; }
    .stat-card .lbl { font-size: 0.85rem; color: #475569; margin-top: 2px; }

    .phase-card {
        background: #F8FAFC; border: 1px solid #CBD5E1;
        border-radius: 10px; padding: 20px; margin-bottom: 16px;
        border-top: 4px solid #29B5E8;
    }
    .phase-card h4 { color: #1E3A8A; margin: 0 0 8px 0; }
    .phase-card .timeframe {
        display: inline-block; background: #1E3A8A; color: #FFFFFF;
        padding: 2px 10px; border-radius: 12px; font-size: 0.8rem;
        font-weight: 600; margin-bottom: 8px;
    }

    .insight-box {
        background: linear-gradient(135deg, #E0F2FE 0%, #F0F9FF 100%);
        border-left: 4px solid #29B5E8;
        border-radius: 8px; padding: 14px 18px; margin-bottom: 12px;
    }
    .insight-box strong { color: #1E3A8A; }

    .commission-placeholder {
        background: #F0FDF4; border: 2px dashed #86EFAC;
        border-radius: 10px; padding: 32px; text-align: center;
        color: #166534;
    }

    .tool-matrix {
        width: 100%; border-collapse: collapse; margin: 12px 0;
    }
    .tool-matrix th {
        background: #1E3A8A; color: #FFFFFF; padding: 10px 14px;
        text-align: left; font-size: 0.9rem;
    }
    .tool-matrix td {
        padding: 10px 14px; border-bottom: 1px solid #E2E8F0;
        font-size: 0.9rem;
    }
    .tool-matrix tr:nth-child(even) { background: #F8FAFC; }
    .tool-matrix a { color: #1E40AF; text-decoration: none; font-weight: 600; }
    .tool-matrix a:hover { text-decoration: underline; }

    .flow-container {
        display: flex; flex-direction: column; align-items: center;
        gap: 0; padding: 28px 0; font-family: 'Source Sans Pro', sans-serif;
    }
    .flow-arrow { font-size: 1.4rem; color: #29B5E8; line-height: 1.2; }
    .flow-arrow-green { font-size: 1.4rem; color: #29B5E8; line-height: 1.2; }
    .flow-node {
        background: linear-gradient(135deg, #E0F2FE 0%, #F0F9FF 100%);
        border: 2px solid #29B5E8; color: #1E3A8A; border-radius: 8px;
        padding: 10px 32px; font-weight: 600; font-size: 0.95rem;
        text-align: center;
    }
    .flow-start {
        background: linear-gradient(135deg, #29B5E8 0%, #1E3A8A 100%);
        border: 2px solid #1E3A8A; color: #FFFFFF; border-radius: 50%;
        width: 120px; height: 120px; display: flex; align-items: center;
        justify-content: center; font-weight: 700; font-size: 0.95rem;
        text-align: center;
    }
    .flow-end {
        background: linear-gradient(135deg, #29B5E8 0%, #1E3A8A 100%);
        border: 3px solid #1E3A8A; color: #FFFFFF; border-radius: 50%;
        width: 120px; height: 120px; display: flex; align-items: center;
        justify-content: center; font-weight: 700; font-size: 1.1rem;
        text-align: center;
    }
    .flow-phase {
        border: 2px dashed #29B5E8; border-radius: 12px;
        background: linear-gradient(180deg, #F0F9FF 0%, #E0F2FE 100%);
        padding: 18px 36px; display: flex; flex-direction: column;
        align-items: center; gap: 0; min-width: 280px;
    }
    .flow-phase-label {
        color: #1E3A8A; font-weight: 700; font-size: 0.85rem;
        margin-bottom: 10px; letter-spacing: 0.5px;
        background: #29B5E8; color: #FFFFFF; padding: 3px 14px;
        border-radius: 12px;
    }
    .flow-phase-node {
        background: #FFFFFF; border: 2px solid #29B5E8; color: #1E3A8A;
        border-radius: 8px; padding: 8px 24px; font-weight: 600;
        font-size: 0.95rem; text-align: center;
    }
    .flow-phase-node-alt {
        background: #FFFFFF; border: 2px solid #93C5FD; color: #1E40AF;
        border-radius: 8px; padding: 8px 24px; font-weight: 600;
        font-size: 0.95rem; text-align: center;
    }
    .flow-diamond {
        background: #DBEAFE; border: 2px solid #1E3A8A; color: #1E3A8A;
        border-radius: 6px; padding: 6px 18px; font-weight: 700;
        font-size: 0.9rem; transform: rotate(45deg); width: 60px;
        height: 60px; display: flex; align-items: center;
        justify-content: center; margin: 10px 0;
    }
    .flow-diamond span { transform: rotate(-45deg); }
    .flow-decision {
        display: flex; gap: 28px; font-size: 0.85rem; font-weight: 600;
        margin-top: 4px;
    }
    .flow-yes { color: #29B5E8; }
    .flow-no { color: #F59E0B; }
    .flow-phase-arrow { font-size: 1.2rem; color: #29B5E8; line-height: 1.2; }

    [data-testid="stChatMessage"] {
        background: #F0F9FF;
        border: 1px solid #DBEAFE;
        border-radius: 12px;
        padding: 12px 16px;
        margin-bottom: 8px;
    }
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
        color: #1E293B;
    }
    [data-testid="stChatMessage"] .stAvatar > div {
        background: linear-gradient(135deg, #29B5E8 0%, #1E3A8A 100%) !important;
        color: #FFFFFF !important;
    }
    [data-testid="stChatInput"] {
        border-color: #29B5E8 !important;
    }
    [data-testid="stChatInput"]:focus-within {
        border-color: #1E3A8A !important;
        box-shadow: 0 0 0 1px #29B5E8 !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### \u2744\ufe0f ACE Onboarding Hub")
    st.caption("Activation knowledge base for new account engineers")

# ---------------------------------------------------------------------------
# Title
# ---------------------------------------------------------------------------
st.markdown("## \u2744\ufe0f Snowflake ACE Onboarding Hub")
st.caption("Consolidated activation knowledge for new account engineers.")

# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Executive Summary",
    "The ACE Journey",
    "Expert FAQ",
    "Incremental Consumption",
    "Ask a Question",
])

# =========================================================================
# TAB 1: EXECUTIVE SUMMARY
# =========================================================================
with tab1:

    st.markdown('<div class="section-hdr">At a Glance</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            '<div class="stat-card"><div class="num">90</div>'
            '<div class="lbl">Day Engagement Window</div></div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            '<div class="stat-card"><div class="num">30/60/90</div>'
            '<div class="lbl">Phased Framework</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-hdr">Key Insights</div>', unsafe_allow_html=True)

    insights = [
        ("Security is the #1 bottleneck",
         "RBAC, SSO, SCIM, PrivateLink, and network policies are consistently the longest phase. "
         "Getting security and access approvals moving early is the highest-leverage action."),
        ("Customer readiness determines outcome",
         "An engaged customer with a clear use case, dedicated technical resources, and urgency "
         "is the strongest predictor of a smooth activation."),
        ("Tribal knowledge is the norm",
         "Security setup, partner engagement, cost optimization, and escalation patterns "
         "largely live in people's heads rather than in a documented playbook."),
        ("Incremental consumption matters but isn't the only measure",
         "Incremental consumption is a key internal KPI for tracking activation impact, but time-to-value, "
         "customer satisfaction, and usage growth are equally important signals of success. "
         "Note: externally, focus on value delivered to the customer, not on driving consumption."),
        ("Cortex Code (Coco) accelerates every phase",
         "Use Coco throughout the activation lifecycle to generate scripts, review configurations, "
         "troubleshoot issues, build demos, and answer technical questions faster. "
         "It's your AI pair-programmer for every phase of the engagement."),
    ]
    for title, body in insights:
        st.markdown(
            f'<div class="insight-box"><strong>{title}.</strong> {body}</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-hdr">The Activation Cycle</div>', unsafe_allow_html=True)

    st.markdown("""
<div class="flow-container">

  <div class="flow-start">Customer<br>Signed</div>
  <div class="flow-arrow">&#x25BC;</div>

  <div class="flow-node">ACE Assigned</div>
  <div class="flow-arrow">&#x25BC;</div>

  <div class="flow-node">Kickoff &amp; Discovery</div>
  <div class="flow-arrow">&#x25BC;</div>

  <div class="flow-phase">
    <div class="flow-phase-label">PHASE 1: FOUNDATIONS</div>
    <div class="flow-phase-node">Onboarding</div>
    <div class="flow-phase-arrow">&#x25BC;</div>
    <div class="flow-phase-node-alt">Security &amp; Networking</div>
  </div>
  <div class="flow-arrow-green">&#x25BC;</div>

  <div class="flow-phase">
    <div class="flow-phase-label">PHASE 2: BUILD</div>
    <div class="flow-phase-node">Enablement</div>
    <div class="flow-phase-arrow">&#x25BC;</div>
    <div class="flow-phase-node-alt">Snowflake 101<br>Data Eng &amp; Architecture</div>
  </div>
  <div class="flow-arrow-green">&#x25BC;</div>

  <div class="flow-phase">
    <div class="flow-phase-label">PHASE 3: OPTIMIZE</div>
    <div class="flow-phase-node">Best Practices &amp; Cost Mgmt</div>
    <div class="flow-phase-arrow">&#x25BC;</div>
    <div class="flow-phase-node-alt">FinOps &amp; Governance</div>
  </div>
  <div class="flow-arrow-green">&#x25BC;</div>

  <div class="flow-phase">
    <div class="flow-phase-label">PHASE 4: ACCELERATE</div>
    <div class="flow-phase-node">Acceleration</div>
    <div class="flow-phase-arrow">&#x25BC;</div>
    <div class="flow-phase-node-alt">POCs &amp; Pilots</div>
  </div>
  <div class="flow-arrow-green">&#x25BC;</div>

  <div class="flow-end">Go Live!</div>
  <div class="flow-arrow">&#x25BC;</div>

  <div class="flow-node">Handoff to Account Team</div>

</div>
""", unsafe_allow_html=True)


# =========================================================================
# TAB 2: THE ACE JOURNEY
# =========================================================================
with tab2:
    st.markdown('<div class="section-hdr">The Activation Lifecycle</div>', unsafe_allow_html=True)
    st.markdown(
        "This is the consolidated chronological roadmap every activation follows. "
        "Each customer is unique, but these phases and checkpoints are consistent."
    )

    st.markdown("""
<div class="phase-card">
    <span class="timeframe">PRE-ENGAGEMENT</span>
    <h4>Internal Prep & Account Research</h4>
    <ul>
        <li><strong>Step 1 — Review the TMR:</strong> Log in to
            <a href="https://snowflake.elementum.io/work" target="_blank">Elementum</a>
            and review the submitted Territory Management Request</li>
        <li><strong>Step 2 — Use Case Hygiene:</strong> Update the TMR as needed, then complete
            <a href="https://docs.google.com/presentation/d/1MxmNM6c_15_ZloQE4og3ubQPwtyxoOQ4wwSlmFdVDZE/edit?slide=id.g1ed82e8067d_0_2803" target="_blank">use case hygiene</a>
            before moving forward:
            <ul>
                <li>Confirm each use case has a clear business objective and defined scope</li>
                <li>Verify the customer has a technical owner identified for each use case</li>
                <li>Ensure use cases align with Snowflake's activation motion</li>
                <li>Flag anything out-of-scope or requiring further qualification</li>
                <li>Prioritize use cases by readiness and business impact</li>
            </ul>
        </li>
        <li>Research the account: review consumption data, user analytics, and Salesforce history</li>
        <li>Schedule an internal sync with the account team to cover:
            <ul>
                <li>Activation goals and expectations</li>
                <li>Deal context and key constraints</li>
                <li>Customer champions and technical contacts</li>
                <li>Partner involvement and key dates</li>
            </ul>
        </li>
    </ul>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="phase-card">
    <span class="timeframe">INTRODUCTION & KICKOFF</span>
    <h4>First Contact & Setting the Foundation</h4>
    <ul>
        <li><strong>Intro Call:</strong> Joint call with the account team and customer stakeholders
            to make introductions and schedule the kickoff</li>
        <li><strong>Kickoff Call (activation-led):</strong>
            <ul>
                <li>Present the activation motion and phased framework</li>
                <li>Discover use cases, current stack, constraints, and owners</li>
                <li>Set communication preferences and recurring cadence</li>
                <li>Align on initial action items and expectations</li>
            </ul>
        </li>
    </ul>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="phase-card">
    <span class="timeframe">PHASE 1 — FOUNDATIONS</span>
    <h4>Security & Account Setup</h4>
    <p>This is consistently the longest phase across all activations.</p>
    <ul>
        <li><strong>Cortex Code (Coco):</strong> Use Coco to accelerate technical tasks — generating scripts, reviewing configurations, troubleshooting issues, and answering questions faster</li>
        <li><a href="https://docs.snowflake.com/en/user-guide/admin-security-fed-auth-overview">SSO</a> and <a href="https://docs.snowflake.com/en/user-guide/ui-snowsight-profile#label-snowsight-set-up-mfa">MFA</a> configuration with the customer's identity provider</li>
        <li><a href="https://docs.snowflake.com/en/user-guide/scim-intro">SCIM</a> provisioning for automated user management</li>
        <li><a href="https://docs.snowflake.com/en/user-guide/network-policies">Network policies</a> and private connectivity(<a href="https://docs.snowflake.com/en/user-guide/private-connectivity-inbound">inbound</a>/<a href="https://docs.snowflake.com/en/user-guide/private-connectivity-outbound">outbound</a>) setup if required</li>
        <li><a href="https://docs.snowflake.com/en/user-guide/security-access-control-overview#role-hierarchy-and-privilege-inheritance">RBAC design</a> — roles, users, groups, grants, object ownership</li>
        <li><a href="https://docs.snowflake.com/en/sql-reference/identifiers">Environment and naming convention guidance</a></li>
        <li><a href="https://docs.snowflake.com/en/user-guide/resource-monitors">Resource monitors</a> and initial cost management tooling</li>
        <li><a href="https://docs.snowflake.com/en/user-guide/warehouses-considerations">Warehouse right-sizing</a> and <a href="https://docs.snowflake.com/en/user-guide/cost-optimization-overview">cost optimization</a> baseline</li>
    </ul>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="phase-card">
    <span class="timeframe">PHASE 2 — BUILD</span>
    <h4>Data Ingestion & Transformation</h4>
    <ul>
        <li>Ingestion patterns — <a href="https://docs.snowflake.com/en/user-guide/data-load-considerations-stage">staging</a>, bulk loading (<a href="https://docs.snowflake.com/en/user-guide/data-load-azure">Azure</a>,<a href="https://docs.snowflake.com/en/user-guide/data-load-s3">AWS</a>, <a href="https://docs.snowflake.com/en/user-guide/data-load-gcs">GCP</a>), <a href="https://docs.snowflake.com/en/user-guide/snowpipe-streaming/data-load-snowpipe-streaming-overview">streaming</a></li>
        <li>Pipeline pattern selection — evaluate tradeoffs between <a href="https://docs.snowflake.com/en/user-guide/dynamic-tables-about">dynamic tables</a>,
            <a href="https://docs.snowflake.com/en/developer-guide/stored-procedure/stored-procedures-overview">stored procedures</a>, and <a href="https://docs.snowflake.com/en/user-guide/tasks-intro">tasks</a></li>
        <li>Data architecture design (Bronze, Silver, Gold layers)</li>
        <li><a href="https://docs.snowflake.com/en/sql-reference/ddl-database">Schema and database structure decisions</a></li>
        <li><a href="https://docs.snowflake.com/en/user-guide/ecosystem-bi">BI tool</a> integration and validation</li>
        <li>Ongoing <a href="https://docs.snowflake.com/en/user-guide/budgets">cost optimization</a> and <a href="https://docs.snowflake.com/en/guides-overview-performance">query performance</a> review</li>
        <li><strong>Cortex Code (Coco):</strong> Use Coco to accelerate technical tasks — generating scripts, reviewing configurations, troubleshooting issues, and answering questions faster</li>
    </ul>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="phase-card">
    <span class="timeframe">PHASE 3 — ACCELERATE</span>
    <h4>Advanced Use Cases & Go-Live</h4>
    <ul>
        <li>Advanced capabilities — <a href="https://docs.snowflake.com/en/guides-overview-ai-features">AI</a>, analytics, <a href="https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst">conversational interfaces</a></li>
        <li>Production readiness validation</li>
        <li>Explore additional use cases and expansion opportunities</li>
        <li>Performance tuning for critical workloads</li>
        <li>Final cost and security posture review</li>
        <li><strong>Cortex Code (Coco):</strong> Use Coco to accelerate technical tasks — generating scripts, reviewing configurations, troubleshooting issues, and answering questions faster</li>
    </ul>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="phase-card">
    <span class="timeframe">HANDOFF & ROLL-OFF</span>
    <h4>Transition Back to Account Team</h4>
    <ul>
        <li>Notify the account team in advance that the engagement is ending</li>
        <li>Prepare handoff documentation:
            <ul>
                <li>Goals, use cases, and success criteria achieved</li>
                <li>Architecture and environment decisions</li>
                <li>Security and access posture</li>
                <li>Completed vs. pending work with clear next steps</li>
            </ul>
        </li>
        <li>Account team joins the final customer call for a smooth transition</li>
        <li>Update Salesforce with final status and recommendations</li>
    </ul>
</div>
""", unsafe_allow_html=True)


# =========================================================================
# TAB 3: EXPERT FAQ
# =========================================================================
with tab3:
    st.markdown('<div class="section-hdr">Expert FAQ</div>', unsafe_allow_html=True)
    st.caption("Consolidated answers organized by topic. Click to expand.")

    st.markdown('<div class="faq-category">The ACE Role</div>', unsafe_allow_html=True)

    with st.expander("What are the behaviors of a successful ACE?"):
        st.markdown("""
- **Customer-first mindset** — great customer service, empathy, building trust
- **Deep listening and curiosity** — ask probing questions, meet the customer where they are
- **Problem-solving and follow-through** — be determined to find the right answer and follow up
- **Have opinions** — you are the expert; it's okay to be prescriptive when it helps
- **Organization and documentation** — good note-taking, structured calls, clear action items
- **Comfortable saying "I don't know"** — then find out and get back to the customer
- **Technical breadth** — general knowledge across security, data engineering, cost optimization
- **Leverage internal resources** — know who to ask, which channels to use, when to bring in specialists
""")

    st.markdown('<div class="faq-category">Customer Success</div>', unsafe_allow_html=True)

    with st.expander("What does a good Activation customer look like?"):
        st.markdown("""
**A good customer:**
- Eager, engaged, and shows up to calls
- Has dedicated technical resources with hands on keyboard
- Has clear, well-qualified use cases — not just exploring
- Has an internal champion driving the effort
- Understands activation is a joint effort, not fully outsourced

**A successful activation from the customer's perspective:**
- Real, tangible progress on their priority use cases
- Noticeable improvements in cost and performance
- A secure, well-governed environment they can operate themselves
- Feeling supported by a responsive, trusted technical partner
- Knowing how to use the platform and manage costs going forward
""")

    with st.expander("What do we count as a successful activation?"):
        st.markdown("""
Success is defined jointly by the activation engineer, leadership, and the account team. Key markers:

- At least one meaningful workload or use case live in production
- Strong foundational practices in place — security, access control, cost management
- Consumption growth toward the contract target set by leadership
- Customer confidence — they understand the platform and can run it themselves
- Breadth of active users beyond a single champion
""")

    with st.expander("Where do customers get confused or frustrated?"):
        st.markdown("""
- Access control and role switching — which option is right for them
- Cost management — not having a good handle on spend, surprised by bills
- Query and pipeline performance relative to expectations
- The compute vs. storage model — new to many coming from on-prem
- Being sold on features not available in their edition
- Expecting the activation team to be hands-on rather than advisory
""")

    with st.expander("What do customers underestimate when starting an activation?"):
        st.markdown("""
- Time and effort required for security and access approvals
- Need for dedicated technical resources who can execute
- The time commitment to building a proper data platform before advanced use cases
- The impact of moving from on-prem to cloud architecture
- Importance of early environment and access control design to avoid rework
""")

    st.markdown('<div class="faq-category">Activation Process</div>', unsafe_allow_html=True)

    with st.expander("What are the reasons activations stall or drag?"):
        for r in [
            "Security and access approval delays (RBAC, SSO, networking, compliance)",
            "Poor customer readiness — no engagement, no technical owner, no urgency",
            "Unclear or unqualified use cases going into the engagement",
            "SI partner misalignment on scope, ownership, or timelines",
            "Customer reorgs, priority shifts, or leadership changes",
            "Data ingestion complexity or capacity constraints",
            "Customer not following through on action items between sessions",
        ]:
            st.markdown(f"- {r}")

    with st.expander("Walk me through a typical activation — what are the steps and where does it slow down?"):
        st.markdown("""
**Typical flow:**

1. **Internal prep** — research the account, sync with the account team on context and goals
2. **Kickoff** — meet the customer, run discovery on use cases, stack, and constraints
3. **Security and access** — SSO, SCIM, network policies, RBAC design and provisioning
4. **Cost setup** — resource monitors, warehouse sizing, initial optimization review
5. **Data ingestion** — staging, loading, pipeline pattern selection
6. **Transformation and modeling** — build the data architecture, validate BI integrations
7. **Advanced use cases** — AI, analytics, or additional workloads once foundations are stable
8. **Handoff** — document everything, transition back to the account team

**Where it typically slows down:**
- Security validation and access approvals (most common)
- Waiting on the customer's internal teams (networking, InfoSec, identity)
- Discovery and remediation of expensive query or warehouse patterns
- Customer resource constraints or shifting priorities
""")

    with st.expander("What step takes you the longest?"):
        st.markdown("""
**Security and access setup** is consistently the longest phase:
- RBAC design and provisioning (users, roles, grants, object ownership)
- SSO and SCIM integration with corporate identity providers
- Private connectivity and network policy configuration
- InfoSec and compliance approvals, especially in regulated industries

**Other common delays:**
- Stakeholder alignment across the customer, SI partners, and internal teams
- Data ingestion when source systems are complex or poorly documented
""")

    with st.expander("What forces a late rework?"):
        st.markdown("""
- **Not having the right people in the room early** — late discovery of the actual technical owner
- **Hidden security or access requirements** — compliance constraints not surfaced during discovery
- **Incorrect pipeline pattern choice** — picking the wrong approach without proper evaluation
- **Late environment or naming decisions** — refactoring databases and schemas mid-stream
- **Poorly configured warehouses** — cost spikes or performance issues discovered after build has started
- **SI partner not prepared** — scope and ownership changes forced late
""")

    with st.expander("Who truly owns the activation plan once the kickoff happens?"):
        st.markdown("""
The **ACE owns and drives** the plan and ongoing guidance.
The **customer owns** internal resourcing and completing their action items — the ACE
operates in an advisory capacity only.
The account team sets goals but does not run day-to-day execution.
When an SI is involved, the ACE often coordinates between all parties.
""")

    st.markdown('<div class="faq-category">Handoff & Transitions</div>', unsafe_allow_html=True)

    with st.expander("What does a clean handoff look like after an ACE cycle?"):
        st.markdown("""
- Notify the account team early — don't surprise them at the end
- Prepare detailed documentation: goals achieved, architecture decisions, security posture,
  completed vs. pending work, and clear next steps
- Run an internal sync with the receiving team before the final call
- Account team joins the final customer call for a smooth transition
- Salesforce is fully updated with status and recommendations
- The receiving team can continue without needing to re-discover anything
""")

    with st.expander("What does a bad handoff look like today in practice?"):
        st.markdown("""
- Account team doesn't join the final call — context is lost
- Too much time passes between steps — momentum dies
- Incomplete or inaccurate notes — the next team has to re-discover everything
- Poor initial handoff into activation — no architecture, no use cases, no customer context provided
- Too many people involved with unclear roles — communication breaks down
- Earlier teams over-promised — customer expectations are misaligned from the start
""")

    st.markdown('<div class="faq-category">Partner Collaboration</div>', unsafe_allow_html=True)

    with st.expander("When an SI partner is involved, what goes wrong most frequently?"):
        st.markdown("""
- **Unclear scope** — who owns access control? Data modeling? Data movement? Each party assumes the other handles it
- **SI lacks technical depth** — not truly hands-on, leading to stalled progress
- **Conflicting recommendations** between the SI and the activation team
- **Variable engagement** — inconsistent responsiveness from the SI side
- **SI passes off work** — misunderstanding that activation is advisory, not hands-on

**What helps:** Define swim lanes early, have separate alignment meetings with the SI
and the customer, and document scope agreements upfront.
""")

    with st.expander("What does a successful SI/PS partner motion look like?"):
        st.markdown("""
**Best practices for working with SI and PS partners:**
- **Define swim lanes upfront** — document who owns what (access control, data modeling, data movement, testing) before the first joint call
- **Hold separate alignment sessions** — meet with the SI/PS team independently from the customer to align on approach, timelines, and escalation paths
- **Set shared milestones** — agree on checkpoints and deliverables so progress is visible to all parties
- **Establish a single communication channel** — avoid fragmented threads; use one shared Slack channel or Teams group

**What a successful motion looks like:**
- The SI handles day-to-day implementation with the customer
- The ACE provides architectural guidance, reviews, and Snowflake-specific recommendations
- Both teams attend joint calls but the customer sees a unified front
- Handoff documentation captures both the ACE's and the partner's contributions
- The customer is self-sufficient after the engagement because both teams invested in enablement
""")

    with st.expander("How should I navigate difficult partner interactions?"):
        st.markdown("""
- **Stay professional and collaborative** — even when the partner is underperforming, maintain a constructive tone
- **Escalate through the right channels** — if the SI is blocking progress, raise it with your manager and the account team, not directly with the customer
- **Document everything** — keep a record of agreed scope, action items, and who owns what to avoid he-said-she-said situations
- **Redirect, don't override** — if the partner gives incorrect guidance, correct it as a collaborative suggestion rather than a contradiction
- **Loop in your manager early** — if you sense misalignment, don't wait until it becomes a crisis
""")

    st.markdown('<div class="faq-category">Engagement Variations</div>', unsafe_allow_html=True)

    with st.expander("What are the different types of activation motions?"):
        st.markdown("""
**Standard activation** — the full 30/60/90 engagement with a new or expanding customer, covering foundations through go-live.

**Cap N engagements** — focused on customers approaching contract renewal. The emphasis shifts to:
- Demonstrating value delivered during the contract period
- Identifying expansion opportunities and new use cases
- Ensuring consumption trajectory supports renewal discussions
- Working closely with the account team on renewal strategy

**Key differences to keep in mind:**
- Cap N engagements are shorter and more outcome-focused
- The depth and duration of each motion depends on deal size, complexity, and customer readiness
""")

    st.markdown('<div class="faq-category">Tools & Metrics</div>', unsafe_allow_html=True)

    with st.expander("What do you need to keep general templates of?"):
        st.markdown("""
- Security discovery checklists (SSO, SCIM, private connectivity, network policies)
- RBAC patterns and role design templates
- Initial account setup scripts
- Recap and follow-up email templates
- Cost optimization review steps
- Data ingestion setup patterns
- Environment and naming convention guidance
- Discovery question lists
- Activation overview decks
- Project plan templates
""")

    with st.expander("What are the metrics today that actually reflect value delivered?"):
        st.markdown("""
**Currently tracked:**
- Incremental consumption growth (before vs. after activation)
- Number of use cases unlocked and moved to production

**Worth keeping in mind (not formally tracked by leadership):**
- Customer satisfaction at the end of the engagement
- Time-to-value (time to first meaningful workload live)
- Usage growth trends over time
- Quality of use case qualification entering activation
- Breadth of active users beyond a single champion
""")

    with st.expander("What tools do you rely on daily?"):
        st.markdown("""
<table class="tool-matrix">
<tr><th>Category</th><th>Tool</th><th>How the ACE Uses It</th></tr>
<tr><td>Account Intelligence</td><td><a href="https://app.snowflake.com" target="_blank">A360 (Account 360)</a></td><td>Deep-dive on account consumption, use cases, warehouse usage, user query analytics, and data sharing. Keep it open during calls to reference specific data and build trust.</td></tr>
<tr><td>Enterprise Search</td><td><a href="https://app.glean.com" target="_blank">Glean</a> / Raven</td><td>Searches across internal communication, Salesforce, and documentation</td></tr>
<tr><td>CRM</td><td><a href="https://snowflakecomputing.lightning.force.com" target="_blank">Salesforce</a></td><td>Track account history, log updates, handoff documentation. Update at least weekly with a focus on next steps and concerns.</td></tr>
<tr><td>AI Code Assistant</td><td><a href="https://docs.snowflake.com/en/user-guide/ui-snowsight/cortex-code" target="_blank">Cortex Code (Coco)</a></td><td>Documentation, code examples, technical troubleshooting, RBAC script generation, security configuration review</td></tr>
<tr><td>Code Editor</td><td>Snowwork / <a href="https://cursor.sh" target="_blank">Cursor</a></td><td>Building demos, scripts, and technical artifacts</td></tr>
<tr><td>Internal Messaging</td><td>Slack</td><td>Real-time communication with customers and internal teams</td></tr>
</table>
""", unsafe_allow_html=True)

    with st.expander("Recommendations for staying efficient"):
        st.markdown("""
- **Block dedicated Salesforce time** — schedule 15–20 minutes at the end of each day or after calls to update notes, next steps, and status
- **Use templates** — keep email, recap, and follow-up templates ready to reduce overhead
- **Use Gong to record calls** — review transcripts for action items and share key moments with your team
- **Leverage Cortex Code (Coco)** — use it for generating scripts, reviewing configurations, and accelerating technical tasks
""")


# =========================================================================
# TAB 4: INCREMENTAL CONSUMPTION
# =========================================================================
with tab4:
    st.markdown('<div class="section-hdr">Incremental Consumption</div>', unsafe_allow_html=True)
    st.info("Content coming soon \u2014 pending discussion with Daunte.")


# =========================================================================
# TAB 5: ASK A QUESTION
# =========================================================================
with tab5:
    st.markdown('<div class="section-hdr">Ask a Question</div>', unsafe_allow_html=True)
    st.markdown(
        "Ask anything about ACE onboarding, Snowflake tools, activation processes, or general Snowflake knowledge. "
        "Powered by Snowflake Cortex AI."
    )

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    ACE_SYSTEM_PROMPT = """You are the ACE Onboarding Hub assistant for Snowflake. You help new Account Engineers (ACEs) at Snowflake with onboarding, activation processes, tools, systems, and general Snowflake knowledge. You are friendly, concise, and knowledgeable — like having a senior ACE mentor available 24/7.

You have deep knowledge of:

## The ACE Role
- ACE = Activation & Customer Engagement. ACEs drive customer activation — helping customers move from contract signing to production workloads.
- Successful ACE behaviors: customer-first mindset, deep listening, problem-solving, being prescriptive, organization, leveraging internal resources.
- ACEs operate in an advisory capacity — they guide and coach but the customer owns execution.

## The Activation Lifecycle
1. **Pre-Engagement**: Review TMR in Elementum, use case hygiene, account research (A360, Salesforce), internal sync with account team.
2. **Introduction & Kickoff**: Joint intro call, then activation-led kickoff covering use cases, constraints, cadence, action items.
3. **Phase 1 — Foundations (longest phase)**: Security & account setup — SSO, MFA, SCIM, network policies, private connectivity, RBAC design, environment/naming conventions, resource monitors, warehouse right-sizing, cost optimization baseline. Use Cortex Code (Coco) throughout.
4. **Phase 2 — Build**: Data ingestion (staging, bulk loading, streaming), pipeline patterns (dynamic tables, stored procedures, tasks), Bronze/Silver/Gold architecture, schema design, BI tool integration, cost optimization.
5. **Phase 3 — Accelerate**: Advanced use cases (AI, analytics, conversational interfaces), production readiness, expansion opportunities, performance tuning, final security/cost review.
6. **Handoff & Roll-off**: Notify account team early, prepare documentation (goals, architecture, security, pending work), account team joins final call, update Salesforce.

## Security & Access (Phase 1 Detail)
- **SSO**: Single Sign-On with customer's identity provider (Okta, Azure AD, etc.). Configured via SAML 2.0 integration in Snowflake.
- **SCIM**: System for Cross-domain Identity Management — automated user provisioning/deprovisioning from the customer's IdP to Snowflake. Eliminates manual user management.
- **MFA**: Multi-factor authentication, required for all Snowflake accounts.
- **Network Policies**: IP allowlisting/blocklisting to restrict Snowflake access. Can be set at account or user level.
- **Private Connectivity**: PrivateLink (AWS), Private Endpoints (Azure), Private Service Connect (GCP) — private network paths to Snowflake.
- **RBAC**: Role-Based Access Control — roles, users, groups, grants, object ownership. Use templates and Coco to accelerate.
- **Resource Monitors**: Track and control credit usage with alerts and auto-suspend.

## Common Stall Reasons
- Security approval delays, poor customer readiness, unqualified use cases, SI misalignment, customer reorgs, data ingestion complexity, lack of follow-through.

## Handoff Best Practices
- Clean handoff: notify account team early, detailed documentation, internal sync, account team joins final call, Salesforce updated.
- Bad handoff: account team absent from final call, incomplete notes, too much time between steps, over-promised expectations.

## Partner Collaboration (SI/PS)
- Define swim lanes upfront, separate alignment sessions, shared milestones, single communication channel.
- Common issues: unclear scope, SI lacks depth, conflicting recommendations, variable engagement.

## Engagement Types
- Standard activation: full 30/60/90 engagement.
- Cap N: customers approaching renewal — focus on value demonstration, expansion, consumption trajectory.

## Incremental Consumption
- Measures credit usage change during/after activation vs. pre-activation baseline.
- Internal metric — externally, focus on value delivered.
- Currently tracked: incremental consumption growth, use cases in production, partner engagement.

## Tools & Systems (40+)
- **Okta** (snowbiz.okta.com): Federated auth, MFA required, main app launcher. Day 1.
- **Slack**: Real-time messaging. Day 1. Authenticate through Okta.
- **Google Workspace**: Gmail, Calendar, Drive, Docs, Slides. Day 1.
- **1Password**: Enterprise password manager. Day 1.
- **Zoom**: Web conferencing. Day 1.
- **Navan**: Travel booking. Fill traveler info before Boot Camp.
- **The Lift**: Onboarding portal, knowledge articles, service tickets.
- **Workday**: Personal info, expenses, PTO, org charts.
- **Snow Academy**: Internal LMS in Workday.
- **Compass**: One-stop shop for ALL Snowflake content, learning, news. Sync Google Drive first.
- **Salesforce**: CRM — accounts, cases, subscriptions, contracts, opportunities.
- **A360 (Account 360)**: Deep-dive on account consumption, use cases, warehouse usage, user analytics, data sharing.
- **Glean**: Natural language enterprise search across GDrive, Slack, etc.
- **Raven**: Enterprise search alongside Glean.
- **Cortex Code (Coco)**: AI coding assistant — RBAC scripts, config review, demos, troubleshooting. Access via Snowsight.
- **Cursor**: AI-powered code editor for demos and scripts. Pair with Snowwork.
- **Vivun**: SE platform for opportunities, solutions assessments, technical risks.
- **MaxIQ**: Forecasting tool — forecasts, opportunities, go-live info.
- **Gong**: Sales analytics — records, transcribes, analyzes calls. Lift ticket for access.
- **GitLab**: Code repository. Lift ticket for access (Category: Get Access to Gitlab, Group: Sales Engineering, Role: Developer).
- **Snowhouse**: Internal data warehouse for customer account info.
- **SnowCommand**: Create customer accounts, Private Previews, configuration.
- **SnowCLI**: Command-line interface. Requires Duo MFA.
- **Anaconda/Conda**: Python environment management. Follow SE setup guide.
- **Duo**: MFA for Production Deployments. Phone app + invitation email.
- **GlobalProtect VPN**: Corporate resources and demo account access. Start at step 4.
- **Viscosity Client**: Prod VPN for production deployments.
- **Demo Account**: Personal demo account on production deployments. Week 1 setup.
- **Lucidchart/Lucidspark**: Architecture diagrams. Check SE folder access.
- **Confluence**: Wiki platform.
- **Snowflake Community**: Customer outreach portal via Data Heroes Okta tile.
- **AWS SE Sandbox**: AWS environment for demo services. Lift ticket for access.
- **DataOps.Live**: Deploy demos (Tasty Bytes, Marketing Data Foundations).
- **Book of Business (BoB)**: Customer accounts view with sales metrics. go/bob.
- **Gable**: Global co-working platform for desks and meeting rooms.
- **Xactly**: Commission statements. Okta > Xactly (Production).
- **Empyrean**: US benefits portal.
- **ADP**: US payroll.
- **Self Service**: Mac app for pushing pre-installed applications.
- **Ashby**: Recruiting activities and referrals.
- **Snowflake University**: LMS via SeerTech Okta tile.
- **Brand Resources**: Deck templates, email signatures, logos, images.

## General Snowflake Knowledge
You also have broad knowledge of Snowflake's platform, features, and architecture. You can answer questions about:
- Snowflake architecture (storage, compute, cloud services layers)
- Warehouses, databases, schemas, tables, views
- Data loading, Snowpipe, streaming, stages
- Dynamic tables, tasks, streams, stored procedures
- Cortex AI functions, Cortex Search, Cortex Analyst, Cortex Agents
- Snowpark (Python, Java, Scala)
- Data sharing, Marketplace, listings
- Security features (encryption, data masking, row access policies, network policies)
- Cost management and optimization
- Performance tuning and query optimization

## Response Guidelines
- Be concise but thorough. Use markdown formatting (bold, bullets, headers) for readability.
- If the question is about a specific tool, include how to access it (Okta tile, Lift ticket, etc.).
- If you're unsure about internal Snowflake-specific details, say so and suggest asking in #activation-all Slack channel.
- For Snowflake product questions, provide accurate technical answers.
- Always be helpful and encouraging to new ACEs."""

    def get_cortex_response(user_question, chat_history):
        messages = [{"role": "system", "content": ACE_SYSTEM_PROMPT}]
        for msg in chat_history[-10:]:
            messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": user_question})
        messages_json = json.dumps(messages)

        conn_type, conn = _get_snowflake_connection()
        if conn_type == "sis":
            result = conn.sql(
                "SELECT SNOWFLAKE.CORTEX.COMPLETE(?, PARSE_JSON(?), {})::STRING AS response",
                params=["mistral-large2", messages_json]
            ).collect()
            raw = result[0]["RESPONSE"]
        else:
            cur = conn.cursor()
            cur.execute(
                "SELECT SNOWFLAKE.CORTEX.COMPLETE(%s, PARSE_JSON(%s), {})::STRING AS response",
                ("mistral-large2", messages_json)
            )
            raw = cur.fetchone()[0]
            cur.close()
            conn.close()

        parsed = json.loads(raw)
        return parsed["choices"][0]["messages"]

    if "pending_question" in st.session_state and st.session_state.pending_question:
        user_input = st.session_state.pending_question
        st.session_state.pending_question = ""
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        with st.spinner("Thinking..."):
            try:
                response = get_cortex_response(user_input, st.session_state.chat_history[:-1])
            except Exception as e:
                response = f"Sorry, I encountered an error: {str(e)}. Try again or ask in #activation-all Slack channel."

        st.session_state.chat_history.append({"role": "assistant", "content": response})

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(
                f'<div style="background:#E0F2FE;border-radius:12px;padding:10px 16px;margin-bottom:8px;">'
                f'<strong>You:</strong> {msg["content"]}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div style="background:#F0F9FF;border:1px solid #DBEAFE;border-radius:12px;padding:10px 16px;margin-bottom:8px;">'
                f'<strong>\u2744\ufe0f Assistant:</strong> {msg["content"]}</div>',
                unsafe_allow_html=True,
            )

    def _on_chat_submit():
        val = st.session_state.get("_chat_input_val", "").strip()
        if val:
            st.session_state.pending_question = val
            st.session_state._chat_input_val = ""

    st.text_input("Type your question and press Enter...", key="_chat_input_val", on_change=_on_chat_submit)
