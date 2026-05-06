"""
Snowflake ACE Onboarding Hub
A Streamlit application for new Activation Engineers at Snowflake.
"""

import json
import streamlit as st

try:
    from snowflake.snowpark.context import get_active_session
    _session = get_active_session()
    IN_SNOWFLAKE = True
except Exception:
    _session = None
    IN_SNOWFLAKE = False

st.set_page_config(
    page_title="ACE Onboarding Hub",
    page_icon="\u2744\ufe0f",
    layout="wide",
    initial_sidebar_state="expanded",
)

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
        background: rgba(30,58,138,0.1); padding: 10px 16px; border-radius: 8px;
        margin: 24px 0 8px 0; border-left: 4px solid #29B5E8;
    }

    .stat-card {
        background: linear-gradient(135deg, rgba(41,181,232,0.15) 0%, rgba(30,58,138,0.1) 100%);
        border-left: 4px solid #29B5E8; border-radius: 8px;
        padding: 16px 20px; margin-bottom: 12px;
    }
    .stat-card .num { font-size: 2rem; font-weight: 700; color: #1E3A8A; }
    .stat-card .lbl { font-size: 0.85rem; color: #64748B; margin-top: 2px; }
    .stat-card a { color: #1E3A8A; text-decoration: none; }
    .stat-card a:hover { text-decoration: underline; }

    .phase-card {
        background: rgba(41,181,232,0.08); border: 1px solid rgba(41,181,232,0.3);
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
        background: linear-gradient(135deg, rgba(41,181,232,0.15) 0%, rgba(30,58,138,0.1) 100%);
        border-left: 4px solid #29B5E8;
        border-radius: 8px; padding: 14px 18px; margin-bottom: 12px;
    }
    .insight-box strong { color: #1E3A8A; }

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
    .tool-matrix tr:nth-child(even) { background: rgba(41,181,232,0.05); }
    .tool-matrix a { color: #1E40AF; text-decoration: none; font-weight: 600; }
    .tool-matrix a:hover { text-decoration: underline; }

    .flow-container {
        display: flex; flex-direction: column; align-items: center;
        gap: 0; padding: 28px 0; font-family: 'Source Sans Pro', sans-serif;
    }
    .flow-arrow { font-size: 1.4rem; color: #29B5E8; line-height: 1.2; }
    .flow-arrow-green { font-size: 1.4rem; color: #29B5E8; line-height: 1.2; }
    .flow-node {
        background: linear-gradient(135deg, rgba(41,181,232,0.15) 0%, rgba(30,58,138,0.1) 100%);
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
        background: linear-gradient(180deg, rgba(41,181,232,0.1) 0%, rgba(41,181,232,0.15) 100%);
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
        background: rgba(41,181,232,0.15); border: 2px solid #29B5E8; color: #1E3A8A;
        border-radius: 8px; padding: 8px 24px; font-weight: 600;
        font-size: 0.95rem; text-align: center;
    }
    .flow-phase-node-alt {
        background: rgba(41,181,232,0.12); border: 2px solid #93C5FD; color: #1E40AF;
        border-radius: 8px; padding: 8px 24px; font-weight: 600;
        font-size: 0.95rem; text-align: center;
    }
    .flow-phase-arrow { font-size: 1.2rem; color: #29B5E8; line-height: 1.2; }

    [data-testid="stChatMessage"] {
        background: rgba(41,181,232,0.08);
        border: 1px solid #DBEAFE;
        border-radius: 12px;
        padding: 12px 16px;
        margin-bottom: 8px;
    }
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
        color: #1E3A8A;
    }
    [data-testid="stChatInput"] {
        border-color: #29B5E8 !important;
    }
    [data-testid="stChatInput"]:focus-within {
        border-color: #1E3A8A !important;
        box-shadow: 0 0 0 1px #29B5E8 !important;
    }

    .home-card {
        background: linear-gradient(135deg, rgba(41,181,232,0.15) 0%, rgba(30,58,138,0.1) 100%);
        border: 2px solid #29B5E8; border-radius: 16px;
        padding: 32px 24px; text-align: center; cursor: pointer;
        transition: transform 0.2s, box-shadow 0.2s;
        min-height: 180px; display: flex; flex-direction: column;
        align-items: center; justify-content: center;
    }
    .home-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(41, 181, 232, 0.25);
    }
    .home-card h3 { color: #1E3A8A; margin: 0 0 8px 0; font-size: 1.3rem; }
    .home-card p { color: #1E40AF; margin: 0; font-size: 0.95rem; }

    .pre-phase {
        background: linear-gradient(135deg, rgba(41,181,232,0.15) 0%, rgba(30,58,138,0.1) 100%);
        border-left: 4px solid #29B5E8;
        border-radius: 8px; padding: 16px 20px; margin-bottom: 14px;
    }
    .pre-phase h4 { color: #1E3A8A; margin: 0 0 6px 0; font-size: 1.05rem; }
    .pre-phase ul { margin: 4px 0 0 0; padding-left: 20px; color: #1E3A8A; }
    .pre-phase li { margin-bottom: 4px; }
    .pre-phase a { color: #1E40AF; font-weight: 600; }

    .tip-note {
        background: rgba(41,181,232,0.08); border: 1px solid #BAE6FD;
        border-radius: 8px; padding: 10px 14px; margin: 12px 0;
        font-size: 0.85rem; color: #1E3A8A;
    }

    div.stButton > button {
        background: linear-gradient(135deg, #29B5E8 0%, #1E3A8A 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 12px 24px !important;
        border-radius: 8px !important;
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #1E3A8A 0%, #29B5E8 100%) !important;
        box-shadow: 0 4px 12px rgba(41, 181, 232, 0.4) !important;
    }
</style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "home"
if "prev_page" not in st.session_state:
    st.session_state.prev_page = "home"

def nav_to(page):
    st.session_state.prev_page = st.session_state.page
    st.session_state.page = page
    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()

with st.sidebar:
    st.markdown("### \u2744\ufe0f ACE Onboarding Hub")
    st.caption("Activation knowledge base for new account engineers")

if st.session_state.page != "home":
    nc1, nc2, nc3 = st.columns([1, 1, 14])
    with nc1:
        if st.button("\u2744\ufe0f", help="Home"):
            nav_to("home")
    with nc2:
        if st.button("\u2b05\ufe0f", help="Back"):
            nav_to(st.session_state.prev_page)

# =========================================================================
# HOME PAGE
# =========================================================================
if st.session_state.page == "home":
    st.markdown("## \u2744\ufe0f Snowflake ACE Onboarding Hub")
    st.caption("Welcome! Choose where you are in your onboarding journey.")
    st.markdown("---")

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown("""
<div class="home-card">
    <h3>Pre-Onboarding</h3>
    <p>New to Snowflake? Start here for your 30/60/90 day guide, SnowPro prep, and Boot Camp resources.</p>
</div>
""", unsafe_allow_html=True)
        if st.button("Pre-Onboarding", use_container_width=True):
            nav_to("pre")
    with c2:
        st.markdown("""
<div class="home-card">
    <h3>Post-Onboarding</h3>
    <p>Already onboarded? Access the activation playbook, expert FAQ, tools, and AI assistant.</p>
</div>
""", unsafe_allow_html=True)
        if st.button("Post-Onboarding", use_container_width=True):
            nav_to("post")


# =========================================================================
# PRE-ONBOARDING PAGE
# =========================================================================
elif st.session_state.page == "pre":
    st.markdown("## \u2744\ufe0f Pre-Onboarding")
    st.caption("Everything you need before your first day and through your first 90 days.")

    pre_tab1, pre_tab2, pre_tab3, pre_tab4, pre_tab5, pre_tab6, pre_tab7 = st.tabs([
        "ACE Onboarding Checklist",
        "Systems",
        "Slack Channels",
        "Helpful Bookmarks",
        "SnowPro Certification",
        "Boot Camp Guide",
        "Ask a Question",
    ])

    with pre_tab1:
        st.markdown('<div class="section-hdr">ACE Onboarding Checklist</div>', unsafe_allow_html=True)

        st.markdown("""
<table class="tool-matrix">
<tr><th colspan="3" style="background:#29B5E8; text-align:center; font-size:1.1rem;">DAYS 1 - 2: Tasks to be Completed within First 2 Days of joining Snowflake</th></tr>
<tr><th style="width:22%">TASK</th><th style="width:53%">TASK DETAILS</th><th style="width:20%">ESTIMATED TIME TO COMPLETE</th></tr>
<tr><td>New Hire Orientation</td><td>Attend Snowflake New Hire Orientation &amp; Laptop Setup calls</td><td>3 hours</td></tr>
<tr><td>Setup Day 1 Systems</td><td>Confirm &amp; configure access to required "Day 1" systems &amp; ACE tools listed in the "Systems" tab</td><td>3 hours</td></tr>
<tr><td>Access Raven GTM Assistant</td><td><a href="https://go/raven" target="_blank">Raven</a> is our internal AI Sales Assistant built on Snowflake Intelligence. We're asking all new hires to access Raven and ask at least one question to become familiar with working with the agent.<br><br>Instructions:<br>- Enter https://go/raven in your browser.<br>- Ask any snowflake sales related question such as "How do we win against Databricks?"</td><td>5 minutes</td></tr>
<tr><td>Subscribe to ACE Google Calendar</td><td><a href="https://calendar.google.com/calendar/embed?src=snowflake.com_ejjms14hdiuubitt5btqo1n08s%40group.calendar.google.com&ctz=America%2FNew_York" target="_blank">Subscribe to the ACE Google Calendar</a><br>Click on the "Add to Google Calendar" link in the bottom left hand corner to subscribe</td><td>2 minutes</td></tr>
<tr><td>Order a Snowflake Corporate Card</td><td>DAY 1 ACTION ITEM: <a href="https://docs.google.com/document/d/1puH8aGA_ZOjzx4ZUcHCOb3P3-wQu178icSt5Z81Z2SM/edit?usp=sharing" target="_blank">Request a Corporate Card</a> which is required for all hotel bookings/reservations at Snowflake. You must pay for the hotel using your Snowflake Corporate Card. If you have not received your Corporate Card in the mail within 7-10 business days, please email or Slack g.shaikmohammed@snowflake.com to expedite.<br><br>Flight bookings will be automatically charged to the Snowflake internal company card</td><td>10 minutes</td></tr>
<tr><td>Create Email Signature</td><td><a href="https://docs.google.com/document/d/1UwBOCVitAg_xuLnJy4HQWQKq5iBF1UotfqfDVWy2gOc/edit?tab=t.0" target="_blank">Create an email signature</a> that is Snowflake compliant signature &amp; download Snowflake Zoom backgrounds</td><td>5 minutes</td></tr>
<tr><td>New To Compass Instructions</td><td>Follow the <a href="https://snowflake.seismic.com/Link/Content/DCbfj7FgRpdGdGm2JGFGHmTdHb7G" target="_blank">Getting Started instructions on New To Compass</a>, syncing your Google Drive, updating your user profile, and then favorite the Support FAQ.</td><td>5 minutes</td></tr>
<tr><td>Download Assets Instructions</td><td>Follow the five steps on <a href="https://snowflake.seismic.com/Link/Content/DCB3P6HqMFdH2GmWW7T9Hdch37Vd" target="_blank">Download Compass Assets</a> so you are familiar with the steps to download and edit a Compass asset (after you complete the Google Drive sync above)</td><td>5 minutes</td></tr>
<tr><td>Check Global Holiday Schedule</td><td>Snowflake has company-wide and regional specific holidays. Check the <a href="https://lift.snowflake.com/lift?id=kb_article&table=kb_knowledge&sysparm_article=KB0010066&searchTerm=holiday%20calendar" target="_blank">Global Company Holidays</a> for the holidays in your region. Quickly add these to your Google Calendar by going to The Lift Home Page, and looking for the "Open in Google Calendar" link on the lower righthand side.</td><td>5 minutes</td></tr>
<tr><td>Join Slack Channels</td><td>Join Slack channels listed in the "Slack Channels" tab. Focus on the "Highly Recommended/Required" channels.</td><td>15 minutes</td></tr>
<tr><td>Setup Browser Bookmarks</td><td>Create browser bookmarks for locations / resources listed in the "Helpful Bookmarks" tab</td><td>15 minutes</td></tr>
</table>

<table class="tool-matrix">
<tr><th colspan="3" style="background:#29B5E8; text-align:center; font-size:1.1rem;">FIRST 30 DAYS: Tasks to be Completed within your First 30 Days at Snowflake</th></tr>
<tr><td colspan="3" style="background:rgba(41,181,232,0.15); font-weight:600; color:#1E3A8A; text-align:center;">***** Prioritize Completing these tasks. You will be reported on the completion of these requirements *****</td></tr>
<tr><th style="width:22%">TASK</th><th style="width:53%">TASK DETAILS</th><th style="width:20%">ESTIMATED TIME TO COMPLETE</th></tr>
<tr><td>Complete the Snowflake Partner Technical Foundations Class</td><td><a href="https://docs.google.com/presentation/d/18uGLo1JsuNozzaauSlXaq7juBHyepdMzDmYSsSrLIqA/edit?usp=sharing" target="_blank">Complete the Snowflake Partner Technical Foundations Class</a>.<br><br>Onboarding Team should've signed you up for this class during your Welcome Call. If not, you can follow the instructions using this link or slack #sales-boot-camp-support for assistance. You must complete this course within 30 Days after your hire date.<br><br>Follow these instructions to check that you are 100% complete with PTF.<br>Must be completed within 30 days from your Hire Date.</td><td>40 hours</td></tr>
<tr><td>Complete the ACE Onboarding eLearning Path</td><td><a href="https://snowflake.seismic.com/Link/Content/DCHbTdbHq7qmH8mDp3m6fFMCMg4V" target="_blank">Follow these instructions</a> to complete your ACE Onboarding eLearning Path.<br>Must be completed within 30 days from your Hire Date.</td><td>34 hours</td></tr>
<tr><td>Complete SQL and Python Assessments in Data Camp</td><td>Both Assessments are line items on the SE Onboarding ELearning Path. Access the Assessments through those links.<br><br>Refer to the ACE Data Camp Notes for more information. If you get stuck reach out to William Summerhill.<br><br>ACE Data Camp Notes<br>You must score at Intermediate Level or higher on both assessments.<br>Must be completed within 30 days from your Hire Date.</td><td>1 to 5 hours:<br>* 1 hr to take the 2 assessments (30 mins per)<br>* Additional 2-4 hours to prep if needed</td></tr>
<tr><td>"Why Snowflake?" Pitch &amp; Objection Handling Certification via Yoodli</td><td><a href="https://snowflake.seismic.com/Link/Content/DCHbTdbHq7qmH8mDp3m6fFMCMg4V" target="_blank">Follow these instructions</a> to complete your "Why Snowflake?" Pitch and Objection Handling Certification.<br>Must be completed within 30 days from your Hire Date.</td><td>1 to 2 hours:<br>* 1 hr to do the Certification<br>* Additional 1 hour to prep</td></tr>
<tr><td>Complete Required HR Training</td><td>Complete required HR training via <a href="https://wd5.myworkday.com/snowflake/learning" target="_blank">Snow Academy in Workday</a></td><td>4 hours</td></tr>
<tr><td>Setup and get familiar with CursorAI</td><td>Use the <a href="https://docs.google.com/document/d/14KYlW8P2zHeNm8O7GH9ArLjCPKGo57eNm12U9QIrxIQ/edit?tab=t.0" target="_blank">Cursor AI Essentials Guide</a> to install and get hands-on working with Cursor AI.<br><br>CursorAI is an intelligent assistant that helps you write or modify code that could be used to customize demos and POCs to your customers' specific needs. Highly recommend that you install Cursor and get familiar with using it.</td><td>1-2 hours</td></tr>
</table>

<table class="tool-matrix">
<tr><th colspan="3" style="background:#29B5E8; text-align:center; font-size:1.1rem;">BEFORE BOOT CAMP: These tasks must be completed BEFORE you arrive on Day One of your assigned Boot Camp</th></tr>
<tr><th style="width:22%">TASK</th><th style="width:53%">TASK DETAILS</th><th style="width:20%">ESTIMATED TIME TO COMPLETE</th></tr>
<tr><td>Complete "Pre-Boot Camp Exercises" in Boot Camp Exercise Guide</td><td>Review the <a href="https://docs.google.com/presentation/d/1LfA03BBYihWvGUGMyUmH2Az8uQi5FEtBTBf0NC6NjRc/edit?usp=sharing" target="_blank">Boot Camp Exercise Guide</a> for guidance on how to prepare for Boot Camp.<br>- See "Pre-Boot Camp Exercises" in the table of contents. Complete these exercises by the outlined due dates.</td><td>1 hour</td></tr>
<tr><td>Get your Demo Account Created</td><td><a href="https://docs.google.com/document/d/1dlO3_2oE6te308647cNMx8ZFzSxS72fNEoTEq_xMrL0/edit?usp=sharing" target="_blank">Follow these instructions</a> to get your first Demo Account setup in an AWS Region nearest you BEFORE arriving to Boot Camp. Note that once your demo account is provisioned you'll need to log in within 48 hours to set your own credentials up.</td><td>10 mins</td></tr>
<tr><td>Setup and practice the Marketing Data Foundations Starter v3 Demo</td><td><a href="https://docs.google.com/presentation/d/1LfA03BBYihWvGUGMyUmH2Az8uQi5FEtBTBf0NC6NjRc/edit?slide=id.g353afa13e96_0_10083" target="_blank">Setup Marketing Data Foundations Starter v3 demo</a> in your Demo account and practice the Demo BEFORE arriving to Boot Camp.<br><br>Refer to Demo Setup/Prep section of the Boot Camp Exercise Guide. This guide also includes instructions on requesting DataOps.Live access if you do not have it.</td><td>1 hour</td></tr>
<tr><td>Setup Week 1 Systems</td><td>Confirm &amp; configure access to required "Week 1" systems &amp; ACE tools listed in the "Systems" tab</td><td>2 hours</td></tr>
</table>

<table class="tool-matrix">
<tr><th colspan="3" style="background:#29B5E8; text-align:center; font-size:1.1rem;">FIRST 60-180 DAYS: Tasks to be Completed within your First 60-90 Days at Snowflake</th></tr>
<tr><td colspan="3" style="background:rgba(41,181,232,0.15); font-style:italic; color:#1E3A8A;">Ensure that your 30 Day Tasks are done before working these tasks.</td></tr>
<tr><th style="width:22%">TASK</th><th style="width:53%">TASK DETAILS</th><th style="width:20%">ESTIMATED TIME TO COMPLETE</th></tr>
<tr><td>Complete the ACE Capstone</td><td>You must complete the ACE Capstone Project within 60 days from your start date.<br><br>Refer to the <a href="https://docs.google.com/document/d/157iZQDFTznF7TVmyR0AZ0Aug_ni79usnduxvmTSDDO4/edit" target="_blank">High-Level Steps for Completing the Capstone</a> for Completing the Capstone document. This is a single doc with instructions and links to all information for getting the Capstone done. Remember to read through everything thoroughly.</td><td>NA</td></tr>
<tr><td>Study &amp; Pass the SnowPro Core Certification</td><td>You must pass the SnowPro Core Certification within 90 days from your start date.<br><br><a href="https://snowflake.seismic.com/Link/Content/DCHbTdbHq7qmH8mDp3m6fFMCMg4V" target="_blank">Click here for resources</a> on preparing for and taking the SnowPro Core Exam.</td><td>NA</td></tr>
<tr><td>ACE University</td><td>- Review the <a href="https://snowflake.seismic.com/Link/Content/DCHbTdbHq7qmH8mDp3m6fFMCMg4V" target="_blank">ACE University Page</a><br>- Talk with your manager about your college assignment. College must be assigned within 180 days of your hire date.<br>- Complete your college certification (within 1 year of your start date)</td><td>NA</td></tr>
</table>
""", unsafe_allow_html=True)

        st.markdown("""
<div class="tip-note">
    <strong>Note:</strong> If you go to bootcamp early, just focus on that and then capstone/SnowPro after.
    If bootcamp is closer to your 60-day mark, start the capstone earlier but still after the 30-day training requirements.
</div>
""", unsafe_allow_html=True)

    with pre_tab2:
        st.markdown('<div class="section-hdr">Systems Access</div>', unsafe_allow_html=True)
        st.caption("Follow access notes instructions carefully. Go in the order listed.")

        st.markdown('<div class="faq-category">Company Wide Systems & HR Tools</div>', unsafe_allow_html=True)
        st.markdown("""
<table class="tool-matrix">
<tr><th>Timeframe</th><th>System</th><th>What It's Used For</th><th>Access Notes</th></tr>
<tr><td>Day 1</td><td>1Password</td><td>Enterprise password management</td><td>Follow instructions in Configuration Notes to setup and configure 1Password</td></tr>
<tr><td>Day 1</td><td>Okta (snowbiz.okta.com)</td><td>Federated authentication for Snowflake enterprise applications + app launching pad</td><td>Access via snowbiz.okta.com. Multi-factor authentication is required</td></tr>
<tr><td>Day 1</td><td>The Lift</td><td>Onboarding, enterprise information / technical knowledge articles, service tickets</td><td>Provisioned automatically. Navigate to Okta > The Lift</td></tr>
<tr><td>Day 1</td><td>Slack</td><td>Real-time messaging and collaboration with internal Snowflake colleagues + select business partners and customers</td><td>Provisioned automatically. Access via standalone desktop and mobile app</td></tr>
<tr><td>Day 1</td><td>Google Workplace</td><td>Gmail, Calendar, Drive, Docs, Slides, etc.</td><td>Provisioned automatically via Okta</td></tr>
<tr><td>Day 1</td><td>Snowflake Brand Resources/Materials</td><td>Bookmark the Snowflake Brand Page</td><td>Includes deck templates, email signature template, LinkedIn headers & Zoom backgrounds</td></tr>
<tr><td>Day 1</td><td>Workday</td><td>Access and manage personal information, expense reports, PTO requests and org charts</td><td>Provisioned automatically. Navigate to Okta > Workday</td></tr>
<tr><td>Day 1</td><td>Snow Academy in Workday</td><td>Internal learning management system for corporate-wide HR training</td><td>Provisioned automatically. Navigate to Okta > Snow Academy</td></tr>
<tr><td>Day 1</td><td>Compass</td><td>One-stop shop for ALL Snowflake content, learning, and news</td><td>Provisioned automatically. Navigate to Okta > Compass</td></tr>
<tr><td>Day 1</td><td>Zoom</td><td>Enterprise web conferencing tool</td><td>Provisioned automatically via Okta</td></tr>
<tr><td>Day 1</td><td>Glean</td><td>Natural Language search across Enterprise tools (GDrive, Slack, etc.)</td><td>Provisioned automatically. Navigate to Okta > Glean</td></tr>
<tr><td>Day 1</td><td>Empyrean (US Only)</td><td>Benefits portal for health/welfare benefits</td><td>Provisioned automatically via Okta</td></tr>
<tr><td>Week 1</td><td>ADP (US Only)</td><td>Payroll information - paystubs, annual statements</td><td>Provisioned automatically via Okta</td></tr>
<tr><td>Week 1</td><td>Navan</td><td>Internal travel booking and management platform</td><td>Provisioned automatically. Navigate to Okta > Navan</td></tr>
<tr><td>Week 1</td><td>Snowflake University</td><td>Learning Management System for customers + partners training</td><td>Login via SeerTech Okta Tile</td></tr>
<tr><td>Week 1</td><td>Self Service</td><td>Desktop applications</td><td>Use Mac search icon to find the application</td></tr>
<tr><td>Optional</td><td>Gable</td><td>Global co-working platform</td><td>On demand desk/meeting room/event space booking</td></tr>
</table>
""", unsafe_allow_html=True)

        st.markdown('<div class="faq-category">Required Systems & Tools for ACE</div>', unsafe_allow_html=True)
        st.markdown("""
<table class="tool-matrix">
<tr><th>Timeframe</th><th>System</th><th>What It's Used For</th><th>Access Notes</th></tr>
<tr><td>Week 1</td><td>Salesforce</td><td>Customer and account management platform</td><td>Provisioned automatically. Navigate to Okta > Salesforce</td></tr>
<tr><td>Week 1</td><td>MaxIQ</td><td>Snowflake's forecasting tool for submitting forecasts and inspecting Opportunities/Use Cases</td><td>Provisioned automatically. Navigate to Okta > MaxIQ</td></tr>
<tr><td>Week 1</td><td>Duo</td><td>Multi-factor authentication for Production Deployments</td><td>Standalone mobile app. Configuration via invitation email from Duo</td></tr>
<tr><td>Week 1</td><td>Lucidchart / Lucidspark</td><td>Architecture diagrams</td><td>Provisioned automatically. Navigate to Okta > Lucidchart</td></tr>
<tr><td>Week 1</td><td>VPN - GlobalProtect</td><td>VPN for corporate resources and demo account access</td><td>Installation instructions - start at step 4</td></tr>
<tr><td>Week 1</td><td>Demo Account</td><td>Demo accounts hosted on production deployments</td><td>Follow instructions to request and set up your first demo account</td></tr>
<tr><td>Week 1</td><td>GitLab</td><td>Code repository manager for Snowflake</td><td>Navigate to Okta > GitLab. Fill out Lift Ticket for access</td></tr>
<tr><td>Week 1</td><td>Account 360 in Streamlit</td><td>Detailed deep-dive on an account including consumption, use cases, warehouse usage</td><td>Navigate to Okta > Account360</td></tr>
<tr><td>Week 1</td><td>SnowCLI Setup</td><td>Command-line interface for Snowflake</td><td>Requires DUO MFA for authentication</td></tr>
<tr><td>Week 1</td><td>Anaconda</td><td>Python environment management and Snowpark configuration</td><td>Follow Anaconda Setup for Solution Engineers instructions</td></tr>
<tr><td>Week 1</td><td>Confluence</td><td>Snowflake's Wiki platform</td><td>Provisioned automatically. Navigate to Okta > Confluence</td></tr>
<tr><td>Week 1</td><td>Snowflake Community</td><td>Main customer outreach portal</td><td>Navigate to Okta > Data Heroes tile</td></tr>
<tr><td>Week 1</td><td>Gong</td><td>Sales analytics - records, transcribes and analyzes sales calls</td><td>Sales analytics platform that records, transcribes and analyzes sales calls</td></tr>
<tr><td>Week 1</td><td>Ashby</td><td>Recruiting activities - Referrals, interview notes</td><td>Provisioned automatically via Okta</td></tr>
<tr><td>Week 1</td><td>DataOps.Live</td><td>Deploy and maintain demos created by Solution Innovation team</td><td>Should be provisioned automatically via Okta</td></tr>
<tr><td>Week 2</td><td>Glean</td><td>Snowflake enterprise search application</td><td>Provisioned automatically. Navigate to Okta > Glean</td></tr>
<tr><td>Week 2</td><td>Snowhouse</td><td>Data warehouse for customer account information</td><td>Follow Requesting Snowhouse Account & Access instructions</td></tr>
<tr><td>Week 2</td><td>Prod VPN - Viscosity Client</td><td>Prod VPN connectivity for Production deployments</td><td>Follow Prod VPN Access Instructions</td></tr>
<tr><td>Week 2</td><td>SnowCommand</td><td>Creating Customer Accounts, enrolling in Private Previews, managing configuration</td><td>Provisioned automatically. Navigate to Okta > SnowCommand</td></tr>
<tr><td>Week 2</td><td>AWS "SE Sandbox" Environment</td><td>AWS environment for creating services to support demos</td><td>NOT provisioned automatically. Submit AWS Sandbox Lift ticket</td></tr>
<tr><td>Week 2</td><td>Book of Business Dashboard</td><td>Comprehensive view of customer accounts and sales metrics</td><td>Access via direct link or go/bob</td></tr>
<tr><td>Week 2</td><td>Accounts 360 Active Trial/Eval</td><td>List of all active On Demand, Eval, and Trial accounts</td><td>Access via direct link</td></tr>
</table>
""", unsafe_allow_html=True)

    with pre_tab3:
        st.markdown('<div class="section-hdr">Slack Channels</div>', unsafe_allow_html=True)
        st.caption("Focus on joining the Highly Recommended/Required channels first.")

        st.markdown('<div class="faq-category">ACE Team Channels</div>', unsafe_allow_html=True)
        st.markdown("""
<table class="tool-matrix">
<tr><th>Channel</th><th>Description</th></tr>
<tr><td>#activation-all</td><td>Main channel for the entire Activation team — announcements, questions, collaboration</td></tr>
<tr><td>#ace-team-global</td><td>Global ACE team channel for cross-regional coordination and discussions</td></tr>
<tr><td>#ams-acquisition</td><td>Americas acquisition team channel for deal support and account discussions</td></tr>
</table>
""", unsafe_allow_html=True)

        st.markdown('<div class="faq-category">Highly Recommended / Required</div>', unsafe_allow_html=True)
        st.markdown("""
<table class="tool-matrix">
<tr><th>Channel</th><th>Description</th></tr>
<tr><td>#announcements-et</td><td>Enterprise Technology related News, Maintenance, and Announcements</td></tr>
<tr><td>#cx-announcements</td><td>Updates and news for Snowflake's CX organization</td></tr>
<tr><td>#everybody</td><td>Main Snowflake slack channel, for important / company wide topics</td></tr>
<tr><td>#feature-roadmap-notifications</td><td>Read Only Release Notifications for all major Snowflake features</td></tr>
<tr><td>#gtm-announcements</td><td>Central hub for key updates and announcements across GTM</td></tr>
<tr><td>#help-travel-and-expenses</td><td>Go-to resource for all travel (Navan) Q&A and updates</td></tr>
<tr><td>#new-sales-engineers</td><td>For newly-minted Snowflake sales engineers to ask questions</td></tr>
<tr><td>#partners</td><td>Discussions / questions for and amongst the larger Partner team</td></tr>
<tr><td>#sales</td><td>General channel across all of Sales and Solution Engineering</td></tr>
<tr><td>#snow-surge</td><td>Information about Mandatory Snow Surge enablement sessions</td></tr>
<tr><td>#solution-engineering</td><td>Discussions / questions for and amongst the SE team</td></tr>
</table>
""", unsafe_allow_html=True)

        st.markdown('<div class="faq-category">Highly Recommended</div>', unsafe_allow_html=True)
        st.markdown("""
<table class="tool-matrix">
<tr><th>Channel</th><th>Description</th></tr>
<tr><td>#demos</td><td>Information on anything related to Snowflake demos. Managed by Solution Innovation</td></tr>
<tr><td>#demo-support</td><td>Questions and help with demos, platforms, and hands-on labs</td></tr>
<tr><td>#team-et</td><td>Enterprise Technology (IT) team monitors this for general questions</td></tr>
</table>
""", unsafe_allow_html=True)

        st.markdown('<div class="faq-category">Nice to Have</div>', unsafe_allow_html=True)
        st.markdown("""
<table class="tool-matrix">
<tr><th>Channel</th><th>Description</th></tr>
<tr><td>#ask_sql_experts</td><td>Non-trivial SQL use cases, knowledge base</td></tr>
<tr><td>#change-control</td><td>System and account-wide parameters and settings tracked here</td></tr>
<tr><td>#competition</td><td>Discussions and questions about Snowflake competition</td></tr>
<tr><td>#customer-security-help</td><td>Anything Snowflake security related</td></tr>
<tr><td>#doc-discuss</td><td>Documentation team monitors for small documentation changes</td></tr>
<tr><td>#ecosystem</td><td>Discussions around the ecosystem (external 3rd party languages and tools)</td></tr>
<tr><td>#market-news</td><td>Articles, tweets, blogs relevant to the data platform market</td></tr>
<tr><td>#marketing</td><td>Insight from Snowflake's Marketing team and press releases</td></tr>
<tr><td>#prod-issues-discuss</td><td>Discussions around current production issues</td></tr>
<tr><td>#product</td><td>Product related questions and comments</td></tr>
<tr><td>#random</td><td>For "random" thoughts and musings</td></tr>
<tr><td>#releases</td><td>Information on Snowflake's upcoming releases</td></tr>
<tr><td>#snowflake-customer-support</td><td>Customer facing product support for the Snowflake service</td></tr>
<tr><td>#zoom-backgrounds</td><td>Images and videos useful as virtual Zoom backgrounds</td></tr>
</table>
""", unsafe_allow_html=True)

    with pre_tab4:
        st.markdown('<div class="section-hdr">Helpful Bookmarks</div>', unsafe_allow_html=True)
        st.caption("Create browser bookmarks for these key resources.")

        st.markdown("""
<table class="tool-matrix">
<tr><th>Item</th><th>Description</th></tr>
<tr><td><a href="https://snowflake.seismic.com/Link/Content/DCBp9M3p9R33C8cGbb437W2QmFWj" target="_blank">Communities of Practice</a></td><td>Facilitates distribution of knowledge across the SE org</td></tr>
<tr><td><a href="https://snowflake.seismic.com/Link/Content/DCPf8MjPM3hfH8MBJHWDcqGq23BV" target="_blank">Competitive Intelligence</a></td><td>Large library of competitive intelligence assets</td></tr>
<tr><td><a href="https://snowflakecomputing.atlassian.net/wiki" target="_blank">Confluence (Wiki) Home</a></td><td>Snowflake's Internal Wiki platform</td></tr>
<tr><td><a href="https://snowflake.seismic.com/Link/Content/DC6D4HQR4XCF6G2J6dmCdQbgVqp8" target="_blank">Customer References</a></td><td>Global Customer Reference in Compass</td></tr>
<tr><td>Feature Roadmap Application</td><td>Streamlit app that tracks new features and current status</td></tr>
<tr><td><a href="https://snowflakecomputing.atlassian.net/secure/BrowseProjects.jspa" target="_blank">JIRA</a></td><td>Main project & product management platform</td></tr>
<tr><td><a href="https://snowbiz.okta.com/app/UserHome" target="_blank">Okta (Business Systems)</a></td><td>Launching point for Salesforce, Workday, TripActions</td></tr>
<tr><td><a href="https://snowflake.okta.com/app/UserHome" target="_blank">Okta (Production Deployments)</a></td><td>Launching point for Snowhouse and production deployments</td></tr>
<tr><td><a href="https://snowflake.seismic.com/Link/Content/DCMT8bfTDHgmQ89RBcTRW8QFHMMj" target="_blank">Reference Architectures Hub</a></td><td>Reference Architectures</td></tr>
<tr><td><a href="https://www.snowflake.com/brand-guidelines/" target="_blank">Snowflake Brand Guidelines</a></td><td>Logos, fonts, colors, PowerPoint templates</td></tr>
<tr><td><a href="https://quickstarts.snowflake.com/" target="_blank">Snowflake Developer Guides</a></td><td>Guides with sample code for specific Snowflake use cases</td></tr>
<tr><td><a href="https://snowflake.seismic.com/Link/Content/DCbTgpPbQpgf2GF2X4T3jBDXgdm3" target="_blank">Snowflake Product Category Page</a></td><td>Snowflake Workload page in Compass</td></tr>
<tr><td><a href="https://status.snowflake.com/" target="_blank">Snowflake Status</a></td><td>Current operational status. Subscribe to get notifications</td></tr>
<tr><td><a href="https://community.snowflake.com/s/article/How-To-Submit-a-Support-Case-in-Snowfl" target="_blank">Snowflake Support Tickets</a></td><td>Step-by-step guide for customer support ticket submission</td></tr>
<tr><td><a href="https://snowflakecomputing.atlassian.net/wiki/spaces/EN/pages/565969462/Snowflak" target="_blank">Snowflake Terminology and Glossary</a></td><td>Glossary & dictionary of common acronyms and terms</td></tr>
<tr><td><a href="https://usergroups.snowflake.com/chapters/" target="_blank">Snowflake User Groups</a></td><td>Customer-led events to participate in</td></tr>
<tr><td><a href="https://snowflake.seismic.com/Link/Content/DC783F7q49297G9PJ9BF2C92jbMP" target="_blank">Solution Engineering Home Page</a></td><td>SE Home Page in Compass</td></tr>
<tr><td><a href="https://snowflake.seismic.com/Link/Content/DCdPc7C2c9VcT8MDh6Bd4GbJ6hH3" target="_blank">Solution Innovation Team</a></td><td>Demo content and industry specific demonstration resources</td></tr>
<tr><td><a href="https://docs.google.com/document/d/1-5MjkcAT2NCKCTdTZo5oojfSZdZkiop_qAOUTYKQ_l0/" target="_blank">Tips and Tricks for New Snowflake ACEs</a></td><td>Living document of tips and tricks encapsulating tribal knowledge</td></tr>
</table>
""", unsafe_allow_html=True)

    with pre_tab5:
        st.markdown('<div class="section-hdr">SnowPro Core Certification</div>', unsafe_allow_html=True)

        st.markdown("""
<div class="insight-box">
    <strong>Exam Details</strong><br>
    <strong>Exam:</strong> SnowPro Core COF-C03<br>
    <strong>Questions:</strong> 100 &nbsp;|&nbsp; <strong>Time:</strong> 115 minutes &nbsp;|&nbsp; <strong>Pass:</strong> 750/1000<br>
    <strong>Cost:</strong> $175 USD (use discount code below)<br>
    <strong>Domains:</strong> Architecture (25%), Security (20%), Performance (15%), Loading (10%), Transformations (20%), Sharing (10%)
</div>
""", unsafe_allow_html=True)

        st.markdown("""
<div class="insight-box">
    <strong>Employee Discount Code</strong><br>
    Use code <strong style="font-size:1.1rem; color:#1E3A8A;">SnowCatCore_SFEMP</strong> when registering for the SnowPro Core Certification Exam.
</div>
""", unsafe_allow_html=True)

        st.markdown("""
<div class="insight-box">
    <strong>Register for SnowPro Core Exam</strong><br>
    <a href="https://cp.certmetrics.com/snowflake/en/login" target="_blank">Certmetrics Registration Portal</a>
</div>
""", unsafe_allow_html=True)

        st.markdown("""
<div class="insight-box">
    <strong>SnowPro Certifications for Snowflake Employees</strong><br>
    <a href="https://lift.snowflake.com/lift?id=kb_article&table=kb_knowledge&sysparm_article=KB0012662&searchTerm=snowpro#mcetoc_1jmbhns8l62" target="_blank">Internal SnowPro Certification Info (The Lift)</a>
</div>
""", unsafe_allow_html=True)

        st.markdown("""
<div class="insight-box">
    <strong>Download Cheat Sheet (PDF)</strong><br>
    <a href="https://drive.google.com/file/d/1cckUXHACywME_Iqypc2FkMRa8d27NhAp/view?usp=sharing" target="_blank">SnowPro Core C03 Master Cheat Sheet</a>
</div>
""", unsafe_allow_html=True)

        st.markdown("""
<div class="insight-box">
    <strong>Official Exam Page</strong><br>
    <a href="https://learn.snowflake.com/en/certifications/snowpro-core-c03/" target="_blank">SnowPro Core COF-C03 Details</a>
</div>
""", unsafe_allow_html=True)

        st.markdown("""
<div class="tip-note">
    <strong>Tip:</strong> Give yourself at least a 2-week buffer before your target deadline so you have time to retake if needed.
</div>
""", unsafe_allow_html=True)

        st.markdown("""
<div class="tip-note">
    <strong>Tip:</strong> Take the official SnowPro Core practice tests before sitting for the real exam. You can expense as many practice tests as you need — they are a great way to identify knowledge gaps and build confidence.
</div>
""", unsafe_allow_html=True)

    with pre_tab6:
        st.markdown('<div class="section-hdr">Boot Camp Guide</div>', unsafe_allow_html=True)
        st.markdown("Tips and advice from experienced ACEs who have been through Boot Camp.")

        st.markdown("""
<div class="pre-phase">
    <h4>Logistics &amp; Travel</h4>
    <ul>
        <li>If you are staying in Redwood City, there is traffic &mdash; call your uber a little early to get to the office</li>
        <li>Book your flight for Thursday night/evening &mdash; everything wraps up around 3 PM on the last day</li>
        <li>Book travel through Navan</li>
        <li>The days are long &mdash; keep up with your self care!</li>
    </ul>
</div>

<div class="pre-phase">
    <h4>Product Exam</h4>
    <ul>
        <li>The product exam is very straightforward and directly from the study guide &mdash; don't stress about this piece too much</li>
    </ul>
</div>

<div class="pre-phase">
    <h4>Roleplay Tips</h4>
    <ul>
        <li>In the roleplay rooms there are 2 groups who present to one coach &mdash; <strong>volunteer to go first!</strong></li>
        <li><strong>Read the grading criteria</strong> for each roleplay session (these are in the bootcamp slides the enablement team will share with you) &mdash; seems obvious but a lot of teams don't do this!</li>
        <li>As a bootcamp team, spend time talking about your work styles/preferences &mdash; team chemistry is huge if you want to win
            <ul>
                <li>Do mini walkthrough sessions of each roleplay to practice transitions, who leads which slides/sections</li>
            </ul>
        </li>
        <li>Even though coaches change, it's meant to be one continuous sales cycle &mdash; you can say "based on what we heard last time..." and make stuff up as appropriate</li>
        <li>If you are asked a question, pretty much always ask a follow-up clarifying question or "how do you do that today?" type question</li>
        <li><strong>Time management</strong> is a big gotcha &mdash; don't get sucked down a rabbit hole of questions. Use "for the sake of time, we'll send follow-up documentation" &mdash; ask your AE teammates for help with time management</li>
        <li>Don't be afraid to step up and really carry the team &mdash; you'll get what you put into it! Embrace the roleplay even if teammates aren't as engaged</li>
    </ul>
</div>

<div class="pre-phase">
    <h4>Coaches &amp; Networking</h4>
    <ul>
        <li>Prep questions for coaches &mdash; they are a huge bootcamp highlight and have lots of experience!</li>
        <li>There are open bars almost every night &mdash; be safe/smart and find your hotel buddies!</li>
        <li>Network with your cohort &mdash; these are your future collaborators</li>
    </ul>
</div>

<div class="pre-phase">
    <h4>Tools &amp; Preparation</h4>
    <ul>
        <li>There will be a time when you need to use LucidChart and it's not really covered in the trainings &mdash; spend a little time getting familiar with it beforehand</li>
        <li>Complete all pre-boarding checklist items before Boot Camp</li>
        <li>Have all tools set up and working (Okta, Slack, Google Workspace)</li>
    </ul>
</div>

<div class="pre-phase">
    <h4>Activation-Specific Resources</h4>
    <ul>
        <li>Remember the onboarding process is built for regular solution engineers &mdash; check in with activation teammates for what is truly relevant for activation</li>
        <li>Activation Playbook calls &mdash; ask your manager for current links</li>
        <li>Activation Motion intro slides &mdash; deck you can use with customers when meeting for the first time</li>
    </ul>
</div>

<div class="pre-phase">
    <h4>After Boot Camp</h4>
    <ul>
        <li>Review your notes and identify knowledge gaps</li>
        <li>Begin applying what you learned to your first activations</li>
        <li>Start studying for SnowPro Core using the cheat sheet in the SnowPro tab</li>
    </ul>
</div>
""", unsafe_allow_html=True)


    with pre_tab7:
        st.markdown('<div class="section-hdr">Ask a Question</div>', unsafe_allow_html=True)
        st.markdown(
            "Ask anything about ACE onboarding, Snowflake tools, activation processes, or general Snowflake knowledge. "
            "Powered by Snowflake Cortex AI."
        )

        if "pre_chat_history" not in st.session_state:
            st.session_state.pre_chat_history = []

        PRE_SYSTEM_PROMPT = """You are the ACE Onboarding Hub assistant for Snowflake. You help new Account Engineers (ACEs) at Snowflake with onboarding, tools setup, SnowPro certification prep, Boot Camp preparation, and general Snowflake knowledge. Be friendly, concise, and knowledgeable."""

        def get_pre_cortex_response(user_question, chat_history):
            session = _session
            messages = [{"role": "system", "content": PRE_SYSTEM_PROMPT}]
            for msg in chat_history[-10:]:
                messages.append({"role": msg["role"], "content": msg["content"]})
            messages.append({"role": "user", "content": user_question})

            messages_json = json.dumps(messages)
            result = session.sql(
                "SELECT SNOWFLAKE.CORTEX.COMPLETE(?, PARSE_JSON(?), {})::STRING AS response",
                params=["mistral-large2", messages_json]
            ).collect()
            raw = result[0]["RESPONSE"]
            parsed = json.loads(raw)
            return parsed["choices"][0]["messages"]

        if "pre_pending_question" in st.session_state and st.session_state.pre_pending_question:
            user_input = st.session_state.pre_pending_question
            st.session_state.pre_pending_question = ""
            st.session_state.pre_chat_history.append({"role": "user", "content": user_input})

            with st.spinner("Thinking..."):
                try:
                    response = get_pre_cortex_response(user_input, st.session_state.pre_chat_history[:-1])
                except Exception as e:
                    response = f"Sorry, I encountered an error: {str(e)}. Try again or ask in #activation-all Slack channel."

            st.session_state.pre_chat_history.append({"role": "assistant", "content": response})

        for msg in st.session_state.pre_chat_history:
            if msg["role"] == "user":
                st.markdown(
                    f'<div style="background:rgba(41,181,232,0.15);border-radius:12px;padding:10px 16px;margin-bottom:8px;">'
                    f'<strong>You:</strong> {msg["content"]}</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div style="background:rgba(41,181,232,0.08);border:1px solid #DBEAFE;border-radius:12px;padding:10px 16px;margin-bottom:8px;">'
                    f'<strong>\u2744\ufe0f Assistant:</strong> {msg["content"]}</div>',
                    unsafe_allow_html=True,
                )

        def _on_pre_chat_submit():
            val = st.session_state.get("_pre_chat_input_val", "").strip()
            if val:
                st.session_state.pre_pending_question = val
                st.session_state._pre_chat_input_val = ""

        if IN_SNOWFLAKE:
            st.text_input("Type your question and press Enter...", key="_pre_chat_input_val", on_change=_on_pre_chat_submit)
        else:
            st.info("AI chat is available when running on Snowflake. For now, ask questions in #activation-all Slack channel.")


# =========================================================================
# POST-ONBOARDING PAGE
# =========================================================================
elif st.session_state.page == "post":
    st.markdown("## \u2744\ufe0f Snowflake ACE Onboarding Hub")
    st.caption("Consolidated activation knowledge for new account engineers.")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Executive Summary",
        "The ACE Journey",
        "Expert FAQ",
        "Tools & Systems",
        "Ask a Question",
    ])

    with tab1:

        st.markdown('<div class="section-hdr">At a Glance</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(
                '<div class="stat-card"><div class="num">90</div>'
                '<div class="lbl">Day Engagement Window</div></div>',
                unsafe_allow_html=True,
            )
            if st.button("View The ACE Journey", key="journey_90"):
                nav_to("journey")
        with c2:
            st.markdown(
                '<div class="stat-card"><div class="num">30/60/90</div>'
                '<div class="lbl">Phased Framework</div></div>',
                unsafe_allow_html=True,
            )
            if st.button("View The ACE Journey", key="journey_3060"):
                nav_to("journey")

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

<div class="phase-card">
    <span class="timeframe">PHASE 1 — FOUNDATIONS</span>
    <h4>Security & Account Setup</h4>
    <p>This is consistently the longest phase across all activations.</p>
    <ul>
        <li><strong>Cortex Code (Coco):</strong> Use Coco to accelerate technical tasks</li>
        <li><a href="https://docs.snowflake.com/en/user-guide/admin-security-fed-auth-overview">SSO</a> and <a href="https://docs.snowflake.com/en/user-guide/ui-snowsight-profile#label-snowsight-set-up-mfa">MFA</a> configuration</li>
        <li><a href="https://docs.snowflake.com/en/user-guide/scim-intro">SCIM</a> provisioning</li>
        <li><a href="https://docs.snowflake.com/en/user-guide/network-policies">Network policies</a> and private connectivity</li>
        <li><a href="https://docs.snowflake.com/en/user-guide/security-access-control-overview#role-hierarchy-and-privilege-inheritance">RBAC design</a></li>
        <li><a href="https://docs.snowflake.com/en/user-guide/resource-monitors">Resource monitors</a> and <a href="https://docs.snowflake.com/en/user-guide/cost-optimization-overview">cost optimization</a></li>
    </ul>
</div>

<div class="phase-card">
    <span class="timeframe">PHASE 2 — BUILD</span>
    <h4>Data Ingestion & Transformation</h4>
    <ul>
        <li>Ingestion patterns — staging, bulk loading, streaming</li>
        <li>Pipeline pattern selection — <a href="https://docs.snowflake.com/en/user-guide/dynamic-tables-about">dynamic tables</a>, stored procedures, tasks</li>
        <li>Data architecture design (Bronze, Silver, Gold layers)</li>
        <li>BI tool integration and validation</li>
        <li>Ongoing cost optimization and query performance review</li>
    </ul>
</div>

<div class="phase-card">
    <span class="timeframe">PHASE 3 — ACCELERATE</span>
    <h4>Advanced Use Cases & Go-Live</h4>
    <ul>
        <li>Advanced capabilities — AI, analytics, conversational interfaces</li>
        <li>Production readiness validation</li>
        <li>Explore additional use cases and expansion opportunities</li>
        <li>Performance tuning and final security/cost review</li>
    </ul>
</div>

<div class="phase-card">
    <span class="timeframe">HANDOFF & ROLL-OFF</span>
    <h4>Transition Back to Account Team</h4>
    <ul>
        <li>Notify the account team in advance</li>
        <li>Prepare handoff documentation</li>
        <li>Account team joins the final customer call</li>
        <li>Update Salesforce with final status and recommendations</li>
    </ul>
</div>
""", unsafe_allow_html=True)

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
- Has clear, well-qualified use cases
- Has an internal champion driving the effort
- Understands activation is a joint effort, not fully outsourced
""")

        with st.expander("What do we count as a successful activation?"):
            st.markdown("""
- At least one meaningful workload or use case live in production
- Strong foundational practices in place — security, access control, cost management
- Consumption growth toward the contract target
- Customer confidence — they understand the platform and can run it themselves
- Breadth of active users beyond a single champion
""")

        with st.expander("Where do customers get confused or frustrated?"):
            st.markdown("""
- Access control and role switching
- Cost management — surprised by bills
- Query and pipeline performance relative to expectations
- The compute vs. storage model
- Being sold on features not available in their edition
- Expecting activation to be hands-on rather than advisory
""")

        st.markdown('<div class="faq-category">Activation Process</div>', unsafe_allow_html=True)

        with st.expander("What are the reasons activations stall or drag?"):
            for r in [
                "Security and access approval delays",
                "Poor customer readiness — no engagement, no technical owner",
                "Unclear or unqualified use cases",
                "SI partner misalignment on scope or timelines",
                "Customer reorgs or priority shifts",
                "Data ingestion complexity",
                "Customer not following through on action items",
            ]:
                st.markdown(f"- {r}")

        with st.expander("What step takes the longest?"):
            st.markdown("""
**Security and access setup** — RBAC, SSO, SCIM, private connectivity, InfoSec approvals.
""")

        with st.expander("Who truly owns the activation plan?"):
            st.markdown("""
The **ACE owns and drives** the plan. The **customer owns** execution. The account team sets goals but doesn't run day-to-day.
""")

        st.markdown('<div class="faq-category">Handoff & Transitions</div>', unsafe_allow_html=True)

        with st.expander("What does a clean handoff look like?"):
            st.markdown("""
- Notify account team early
- Detailed documentation: goals, architecture, security, pending work
- Account team joins final call
- Salesforce fully updated
""")

        st.markdown('<div class="faq-category">Partner Collaboration</div>', unsafe_allow_html=True)

        with st.expander("When an SI partner is involved, what goes wrong?"):
            st.markdown("""
- Unclear scope — who owns what
- SI lacks technical depth
- Conflicting recommendations
- Variable engagement

**What helps:** Define swim lanes early, separate alignment meetings, document scope upfront.
""")

        st.markdown('<div class="faq-category">Engagement Variations</div>', unsafe_allow_html=True)

        with st.expander("What are the different types of activation motions?"):
            st.markdown("""
**Standard activation** — full 30/60/90 engagement.

**Cap N engagements** — customers approaching renewal. Focus on value demonstration, expansion, consumption trajectory.
""")

        st.markdown('<div class="faq-category">Metrics & Measurement</div>', unsafe_allow_html=True)

        with st.expander("What are the metrics that reflect value delivered?"):
            st.markdown("""
**Currently tracked:** Incremental consumption growth, use cases in production.

**Worth tracking:** Customer satisfaction, time-to-value, usage growth, breadth of active users.
""")

        with st.expander("What is a Go Live?"):
            st.markdown("""
A **Use Case Go-Live** is when a customer moves from testing or building to running a real workload in production on Snowflake. The simple way to explain it: "when a customer's first production workload is running on Snowflake, real users are consuming the output, and the customer can operate it independently."

It is when a client moves from idealization to "using" with real data. For example, if the use case is "AI chatbot," the customer has to bring in data, set up a semantic view, and deploy Cortex Agents. Can the customer open Snowflake Intelligence, ask questions, and get useful/valuable answers back? If yes, use case is live.

**Go Live does not equal perfection** — most projects can always be improved. It's the first value realization moment for a specific use case.

**Three components:**

1. **Production-grade deployment** — Real data is flowing, real queries are running, and the environment is configured for performance, cost control, and security.
2. **Business user adoption** — Someone outside of IT is actually using the output (a dashboard, a live pipeline, a model in production).
3. **Operational independence** — The customer can sustain, monitor, and troubleshoot the use case without ACE hand-holding.

**What it is NOT:**
- Account creation or basic security setup (that's onboarding)
- A successful POC (that's validation, not production)
- A demo environment with sample data
""")

        with st.expander("Recommendations for staying efficient"):
            st.markdown("""
- Block dedicated Salesforce time
- Use templates for emails and recaps
- Use Gong to record calls
- Leverage Cortex Code (Coco)
""")

        st.markdown('<div class="faq-category">Incremental Consumption</div>', unsafe_allow_html=True)

        with st.expander("What is incremental consumption?"):
            st.markdown("""
Measures credit usage change during/after activation vs. pre-activation baseline. Internal KPI — externally, focus on value delivered.

**Content pending** — further details after discussion with Daunte.
""")

    with tab4:
        st.markdown('<div class="section-hdr">Tools & Systems</div>', unsafe_allow_html=True)
        st.caption("All the tools the ACE team uses daily, organized by category.")

        st.markdown("""
<div class="insight-box">
    <strong>ACE Notes & Templates</strong> — Shared notes, templates, and engagement artifacts:<br>
    <a href="https://drive.google.com/drive/folders/1ZxEo6UdpIdZS2AmTWf3O-B6RafHVIkmA" target="_blank">ACE Shared Google Drive</a>
</div>
""", unsafe_allow_html=True)

        st.markdown("""
<div class="insight-box">
    <strong>Lunch & Learn Sessions</strong> — Continuous engagement sessions covering a wide variety of topics:<br>
    <a href="https://drive.google.com/drive/folders/12gpWHui1HUS7HEat_oOb4aXOSq3nnoyG?usp=drive_link" target="_blank">Lunch & Learn Recordings</a>
</div>
""", unsafe_allow_html=True)

        st.markdown('<div class="faq-category">Account Intelligence & CRM</div>', unsafe_allow_html=True)
        st.markdown("""
<table class="tool-matrix">
<tr><th>Tool</th><th>What It Does</th><th>Access</th></tr>
<tr><td><a href="https://app.snowflake.com" target="_blank">A360 (Account 360)</a></td><td>Deep-dive on account consumption, use cases, warehouse usage, user query analytics, and data sharing.</td><td>Okta</td></tr>
<tr><td><a href="https://app.snowflake.com/sfcogsops/snowhouse_aws_us_west_2/#/streamlit-apps/SALES.STREAMLIT_APPS.VSELJK9OL8LPOXV8" target="_blank">Book of Business (BoB)</a></td><td>Customer accounts view with sales metrics, consumption data, and account status.</td><td>Snowflake App</td></tr>
<tr><td><a href="https://snowflakecomputing.lightning.force.com" target="_blank">Salesforce</a></td><td>Track account history, log updates, handoff documentation.</td><td>Okta</td></tr>
<tr><td>Snowhouse</td><td>Internal data warehouse for customer account info.</td><td>Okta</td></tr>
<tr><td><a href="https://snowflake.elementum.io/work" target="_blank">Elementum</a></td><td>Territory Management Requests (TMR) — review, update, and manage activation requests.</td><td>Okta</td></tr>
</table>
""", unsafe_allow_html=True)

        st.markdown('<div class="faq-category">AI & Development</div>', unsafe_allow_html=True)
        st.markdown("""
<table class="tool-matrix">
<tr><th>Tool</th><th>What It Does</th><th>Access</th></tr>
<tr><td><a href="https://docs.snowflake.com/en/user-guide/ui-snowsight/cortex-code" target="_blank">Cortex Code (Coco)</a></td><td>AI coding assistant — RBAC scripts, config review, demos, troubleshooting.</td><td>Snowsight</td></tr>
<tr><td><a href="https://cursor.sh" target="_blank">Cursor</a></td><td>AI-powered code editor for building demos, scripts, and technical artifacts.</td><td>Download</td></tr>
<tr><td>GitLab</td><td>Code repository. Lift ticket (Category: Get Access to Gitlab, Group: Sales Engineering, Role: Developer).</td><td>Lift Ticket</td></tr>
<tr><td><a href="https://docs.google.com/document/d/18M6qmgG2o5871JhdssDv_SubO0W6oNLJqmyfnFLUYC0/edit?tab=t.0#heading=h.mj9nijiuvdoh" target="_blank">Blueprints</a></td><td>Reference architecture and engagement blueprints for activation workflows.</td><td>Google Doc</td></tr>
</table>
""", unsafe_allow_html=True)

        st.markdown('<div class="faq-category">Enterprise Search</div>', unsafe_allow_html=True)
        st.markdown("""
<table class="tool-matrix">
<tr><th>Tool</th><th>What It Does</th><th>Access</th></tr>
<tr><td><a href="https://app.glean.com" target="_blank">Glean</a></td><td>Natural language enterprise search across GDrive, Slack, Salesforce, and documentation.</td><td>Okta</td></tr>
<tr><td>Raven</td><td>Enterprise search alongside Glean.</td><td>Okta</td></tr>
</table>
""", unsafe_allow_html=True)

        st.markdown('<div class="faq-category">Communication & Collaboration</div>', unsafe_allow_html=True)
        st.markdown("""
<table class="tool-matrix">
<tr><th>Tool</th><th>What It Does</th><th>Access</th></tr>
<tr><td>Slack</td><td>Real-time messaging with customers and internal teams.</td><td>Okta</td></tr>
<tr><td>Google Workspace</td><td>Gmail, Calendar, Drive, Docs, Slides.</td><td>Okta</td></tr>
<tr><td>Zoom</td><td>Web conferencing.</td><td>Okta</td></tr>
<tr><td>Gong</td><td>Sales analytics — records, transcribes, analyzes calls.</td><td>Lift Ticket</td></tr>
<tr><td>Confluence</td><td>Wiki platform for internal documentation.</td><td>Okta</td></tr>
</table>
""", unsafe_allow_html=True)

        st.markdown('<div class="faq-category">Onboarding & HR</div>', unsafe_allow_html=True)
        st.markdown("""
<table class="tool-matrix">
<tr><th>Tool</th><th>What It Does</th><th>Access</th></tr>
<tr><td><a href="https://snowbiz.okta.com" target="_blank">Okta</a></td><td>Federated auth, MFA required, main app launcher.</td><td>Okta</td></tr>
<tr><td>The Lift</td><td>Onboarding portal, knowledge articles, service tickets.</td><td>Okta</td></tr>
<tr><td>Workday</td><td>Personal info, expenses, PTO, org charts.</td><td>Okta</td></tr>
</table>
""", unsafe_allow_html=True)

        st.markdown('<div class="faq-category">Security & Infrastructure</div>', unsafe_allow_html=True)
        st.markdown("""
<table class="tool-matrix">
<tr><th>Tool</th><th>What It Does</th><th>Access</th></tr>
<tr><td>1Password</td><td>Enterprise password manager.</td><td>Okta</td></tr>
<tr><td>Duo</td><td>MFA for Production Deployments.</td><td>Email Invite</td></tr>
<tr><td>GlobalProtect VPN</td><td>Corporate resources and demo account access.</td><td>Setup Guide</td></tr>
<tr><td>Viscosity Client</td><td>Prod VPN for production deployments.</td><td>Setup Guide</td></tr>
</table>
""", unsafe_allow_html=True)

        st.markdown('<div class="faq-category">Snowflake Platform Tools</div>', unsafe_allow_html=True)
        st.markdown("""
<table class="tool-matrix">
<tr><th>Tool</th><th>What It Does</th><th>Access</th></tr>
<tr><td>SnowCLI</td><td>Command-line interface. Requires Duo MFA.</td><td>Setup Guide</td></tr>
<tr><td>Demo Account</td><td>Personal demo account on production deployments.</td><td>Setup Guide</td></tr>
<tr><td>Anaconda/Conda</td><td>Python environment management.</td><td>Setup Guide</td></tr>
<tr><td>AWS SE Sandbox</td><td>AWS environment for demo services.</td><td>Lift Ticket</td></tr>
<tr><td>Snowflake Community</td><td>Customer outreach portal via Data Heroes Okta tile.</td><td>Okta</td></tr>
</table>
""", unsafe_allow_html=True)

        st.markdown('<div class="faq-category">Design</div>', unsafe_allow_html=True)
        st.markdown("""
<table class="tool-matrix">
<tr><th>Tool</th><th>What It Does</th><th>Access</th></tr>
<tr><td>Lucidchart / Lucidspark</td><td>Architecture diagrams.</td><td>Okta</td></tr>
</table>
""", unsafe_allow_html=True)

    with tab5:
        st.markdown('<div class="section-hdr">Ask a Question</div>', unsafe_allow_html=True)
        st.markdown(
            "Ask anything about ACE onboarding, Snowflake tools, activation processes, or general Snowflake knowledge. "
            "Powered by Snowflake Cortex AI."
        )

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        ACE_SYSTEM_PROMPT = """You are the ACE Onboarding Hub assistant for Snowflake. You help new Account Engineers (ACEs) at Snowflake with onboarding, activation processes, tools, systems, and general Snowflake knowledge. You are friendly, concise, and knowledgeable — like having a senior ACE mentor available 24/7.

You have deep knowledge of the ACE role, activation lifecycle, security & access setup, common stall reasons, handoff best practices, partner collaboration, engagement types, incremental consumption, and general Snowflake platform knowledge.

Response Guidelines:
- Be concise but thorough. Use markdown formatting.
- If unsure about internal details, suggest asking in #activation-all Slack channel.
- For Snowflake product questions, provide accurate technical answers.
- Always be helpful and encouraging to new ACEs."""

        def get_cortex_response(user_question, chat_history):
            session = _session
            messages = [{"role": "system", "content": ACE_SYSTEM_PROMPT}]
            for msg in chat_history[-10:]:
                messages.append({"role": msg["role"], "content": msg["content"]})
            messages.append({"role": "user", "content": user_question})

            messages_json = json.dumps(messages)
            result = session.sql(
                "SELECT SNOWFLAKE.CORTEX.COMPLETE(?, PARSE_JSON(?), {})::STRING AS response",
                params=["mistral-large2", messages_json]
            ).collect()
            raw = result[0]["RESPONSE"]
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
                    f'<div style="background:rgba(41,181,232,0.15);border-radius:12px;padding:10px 16px;margin-bottom:8px;">'
                    f'<strong>You:</strong> {msg["content"]}</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div style="background:rgba(41,181,232,0.08);border:1px solid #DBEAFE;border-radius:12px;padding:10px 16px;margin-bottom:8px;">'
                    f'<strong>\u2744\ufe0f Assistant:</strong> {msg["content"]}</div>',
                    unsafe_allow_html=True,
                )

        def _on_chat_submit():
            val = st.session_state.get("_chat_input_val", "").strip()
            if val:
                st.session_state.pending_question = val
                st.session_state._chat_input_val = ""

        st.text_input("Type your question and press Enter...", key="_chat_input_val", on_change=_on_chat_submit)


# =========================================================================
# ACE JOURNEY PAGE (standalone, linked from stat cards)
# =========================================================================
elif st.session_state.page == "journey":
    st.markdown("## \u2744\ufe0f The ACE Journey")
    st.caption("The consolidated chronological roadmap every activation follows.")

    st.markdown('<div class="section-hdr">The Activation Lifecycle</div>', unsafe_allow_html=True)
    st.markdown(
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

<div class="phase-card">
    <span class="timeframe">PHASE 1 — FOUNDATIONS (Days 1-30)</span>
    <h4>Security & Account Setup</h4>
    <p>This is consistently the longest phase across all activations.</p>
    <ul>
        <li><strong>Cortex Code (Coco):</strong> Use Coco to accelerate technical tasks</li>
        <li><a href="https://docs.snowflake.com/en/user-guide/admin-security-fed-auth-overview">SSO</a> and <a href="https://docs.snowflake.com/en/user-guide/ui-snowsight-profile#label-snowsight-set-up-mfa">MFA</a> configuration</li>
        <li><a href="https://docs.snowflake.com/en/user-guide/scim-intro">SCIM</a> provisioning</li>
        <li><a href="https://docs.snowflake.com/en/user-guide/network-policies">Network policies</a> and private connectivity</li>
        <li><a href="https://docs.snowflake.com/en/user-guide/security-access-control-overview#role-hierarchy-and-privilege-inheritance">RBAC design</a></li>
        <li><a href="https://docs.snowflake.com/en/user-guide/resource-monitors">Resource monitors</a> and <a href="https://docs.snowflake.com/en/user-guide/cost-optimization-overview">cost optimization</a></li>
    </ul>
</div>

<div class="phase-card">
    <span class="timeframe">PHASE 2 — BUILD (Days 30-60)</span>
    <h4>Data Ingestion & Transformation</h4>
    <ul>
        <li>Ingestion patterns — staging, bulk loading, streaming</li>
        <li>Pipeline pattern selection — <a href="https://docs.snowflake.com/en/user-guide/dynamic-tables-about">dynamic tables</a>, stored procedures, tasks</li>
        <li>Data architecture design (Bronze, Silver, Gold layers)</li>
        <li>BI tool integration and validation</li>
        <li>Ongoing cost optimization and query performance review</li>
    </ul>
</div>

<div class="phase-card">
    <span class="timeframe">PHASE 3 — ACCELERATE (Days 60-90)</span>
    <h4>Advanced Use Cases & Go-Live</h4>
    <ul>
        <li>Advanced capabilities — AI, analytics, conversational interfaces</li>
        <li>Production readiness validation</li>
        <li>Explore additional use cases and expansion opportunities</li>
        <li>Performance tuning and final security/cost review</li>
    </ul>
</div>

<div class="phase-card">
    <span class="timeframe">HANDOFF & ROLL-OFF</span>
    <h4>Transition Back to Account Team</h4>
    <ul>
        <li>Notify the account team in advance</li>
        <li>Prepare handoff documentation</li>
        <li>Account team joins the final customer call</li>
        <li>Update Salesforce with final status and recommendations</li>
    </ul>
</div>
""", unsafe_allow_html=True)
