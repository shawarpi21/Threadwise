import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

# ---------- PAGE CONFIGURATION ----------

st.set_page_config(
    page_title="Threadwise | Reliability Studio",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

# ---------- THEME COLORS ----------

theme = st.session_state.theme

if theme == "Dark":
    BG = "#0C1120"
    PANEL = "#141C2E"
    TEXT = "#F0F3FA"
    MUTED = "#9CAAC0"
    BORDER = "#29354B"
    ACCENT = "#B8F0DE"
    SECONDARY = "#A9A0FF"
    SIDEBAR = "#101727"
else:
    BG = "#F5F4FA"
    PANEL = "#FFFFFF"
    TEXT = "#25263D"
    MUTED = "#70738C"
    BORDER = "#E2DFF0"
    ACCENT = "#287D68"
    SECONDARY = "#6554C0"
    SIDEBAR = "#FBFAFF"

# ---------- CUSTOM STYLING ----------

st.markdown(
    f"""
    <style>
    .stApp {{
        background:
            radial-gradient(
                ellipse at 90% 0%,
                {"#242044" if theme == "Dark" else "#E7E1FF"},
                transparent 38%
            ),
            {BG};
        color: {TEXT};
    }}

    [data-testid="stSidebar"] {{
        background: {SIDEBAR};
        border-right: 1px solid {BORDER};
    }}

    [data-testid="stHeader"] {{
        background: transparent;
    }}

    .block-container {{
        padding-top: 2.2rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }}

    .brand {{
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px 0 18px;
    }}

    .brand-mark {{
        width: 46px;
        height: 46px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #C9F0E5;
        border-radius: 15px;
        flex-shrink: 0;
    }}

    .brand-name {{
        font-size: 23px;
        font-weight: 700;
        letter-spacing: -1.1px;
        color: {TEXT};
        line-height: 1.2;
    }}

    .brand-caption {{
        font-size: 9px;
        letter-spacing: 1.5px;
        margin-top: 5px;
        color: {MUTED};
    }}

    h1, h2, h3, p, label {{
        color: {TEXT};
    }}

    [data-testid="stMetric"] {{
        background: {PANEL};
        padding: 20px;
        border: 1px solid {BORDER};
        border-radius: 16px;
    }}

    [data-testid="stMetricLabel"] {{
        color: {MUTED};
    }}

    [data-testid="stMetricValue"] {{
        color: {TEXT};
    }}

    .hero {{
        background: linear-gradient(
            115deg,
            {"#242442, #153644" if theme == "Dark" else "#E7E0FF, #DDF5EE"}
        );
        border: 1px solid {BORDER};
        border-radius: 22px;
        padding: 28px 30px;
        margin-bottom: 24px;
    }}

    .hero-eyebrow {{
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 2px;
        color: {SECONDARY};
        margin-bottom: 12px;
    }}

    .hero-title {{
        font-size: clamp(26px, 3vw, 38px);
        font-weight: 700;
        letter-spacing: -1.5px;
        color: {TEXT};
        line-height: 1.2;
    }}

    .hero-subtitle {{
        font-size: 14px;
        color: {MUTED};
        margin-top: 10px;
        line-height: 1.7;
    }}

    .section-label {{
        color: {MUTED};
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1.8px;
        margin-bottom: 12px;
    }}

    .surface {{
        background: {PANEL};
        border: 1px solid {BORDER};
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 16px;
    }}

    .surface-title {{
        font-size: 15px;
        font-weight: 650;
        color: {TEXT};
        margin-bottom: 8px;
    }}

    .surface-caption {{
        color: {MUTED};
        font-size: 12px;
        line-height: 1.7;
    }}

    .status-dot {{
        display: inline-block;
        width: 8px;
        height: 8px;
        background: {ACCENT};
        border-radius: 50%;
        margin-right: 8px;
    }}

    .stButton button {{
        border-radius: 10px;
        border: 1px solid {BORDER};
    }}

    div[data-testid="stDataFrame"] {{
        border: 1px solid {BORDER};
        border-radius: 12px;
        overflow: hidden;
    }}

    [data-testid="stSidebar"] [data-testid="stRadio"] label {{
        padding-top: 5px;
        padding-bottom: 5px;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- DATA HELPERS ----------

def fetch_records(endpoint):
    """Fetch records from the Threadwise API."""
    response = requests.get(
        f"{API_URL}/{endpoint}",
        timeout=5,
    )
    response.raise_for_status()
    return response.json()


def show_empty_state(title, description):
    """Show a consistent empty-state panel."""
    st.markdown(
        f"""
        <div class="surface">
            <div class="surface-title">{title}</div>
            <div class="surface-caption">{description}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------- SIDEBAR ----------

with st.sidebar:
    st.markdown(
        """
        <div class="brand">
            <div class="brand-mark">
                <svg viewBox="0 0 40 40" width="34" height="34">
                    <path
                        d="M5 12 C14 12 14 28 21 28 S28 12 35 12"
                        stroke="#172B35"
                        stroke-width="2.4"
                        fill="none"
                        stroke-linecap="round"
                    />
                    <path
                        d="M5 20 C14 20 14 12 21 12 S28 28 35 28"
                        stroke="#5268A8"
                        stroke-width="2.4"
                        fill="none"
                        stroke-linecap="round"
                    />
                    <circle cx="5" cy="20" r="2.5" fill="#172B35"/>
                    <circle cx="35" cy="20" r="2.5" fill="#172B35"/>
                </svg>
            </div>
            <div>
                <div class="brand-name">threadwise</div>
                <div class="brand-caption">MEMORY THAT LEARNS</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()
    st.caption("WORKSPACE")

    page = st.radio(
        "Navigate",
        [
            "Pulse",
            "Intent paths",
            "Memory archive",
            "Failure signals",
            "Diagnostics",
        ],
        label_visibility="collapsed",
    )

    st.divider()
    st.caption("PREFERENCES")

    selected_theme = st.selectbox(
        "Appearance",
        ["Dark", "Light"],
        index=0 if theme == "Dark" else 1,
    )

    if selected_theme != st.session_state.theme:
        st.session_state.theme = selected_theme
        st.rerun()

    st.divider()

    st.markdown(
        """
        <div class="surface">
            <div class="surface-caption">PROJECT STATUS</div>
            <div class="surface-title">
                <span class="status-dot"></span>Local workspace
            </div>
            <div class="surface-caption">
                Threadwise · Development
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------- PAGE HEADER ----------

hero_title = (
    "Your system, in perspective."
    if page == "Pulse"
    else page + "."
)

hero_subtitle = (
    "Track intent, preserve verified knowledge, and learn from failure."
    if page == "Pulse"
    else "Explore the records and signals behind your AI reliability system."
)

st.markdown(
    f"""
    <div class="hero">
        <div class="hero-eyebrow">THREADWISE / RELIABILITY STUDIO</div>
        <div class="hero-title">{hero_title}</div>
        <div class="hero-subtitle">{hero_subtitle}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- REFRESH ----------

if st.button("↻  Refresh records", type="secondary"):
    st.rerun()

# ---------- LOAD DATA AND DISPLAY PAGES ----------

try:
    goals = fetch_records("goals")
    lessons = fetch_records("lessons")
    failures = fetch_records("failures")

    # ---------- PULSE / OVERVIEW ----------

    if page == "Pulse":
        st.markdown(
            '<div class="section-label">CURRENT SNAPSHOT</div>',
            unsafe_allow_html=True,
        )

        col1, col2, col3 = st.columns(3)

        col1.metric("Intent records", len(goals))
        col2.metric("Verified memories", len(lessons))
        col3.metric("Failure records", len(failures))

        st.write("")

        # Reliability activity chart
        st.markdown("### Reliability activity")
        st.caption("A quick comparison of the records stored by Threadwise.")

        chart_data = pd.DataFrame(
            {
                "Record type": [
                    "Goals",
                    "Verified memories",
                    "Failures",
                ],
                "Count": [
                    len(goals),
                    len(lessons),
                    len(failures),
                ],
            }
        ).set_index("Record type")

        st.bar_chart(
            chart_data,
            color=SECONDARY,
        )

        st.write("")

        left, right = st.columns([1.1, 0.9])

        with left:
            st.markdown("### Intent paths")
            st.caption(
                "The goals and constraints your system is preserving."
            )

            if goals:
                display_goals = [
                    {
                        "ID": item["id"],
                        "Goal": item["goal"],
                        "Approval needed": item["approval_required"],
                    }
                    for item in goals[-5:][::-1]
                ]

                st.dataframe(
                    display_goals,
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                show_empty_state(
                    "No intent records yet",
                    "Save a goal through the Threadwise API to begin.",
                )

        with right:
            st.markdown("### Reliability signals")
            st.caption(
                "Recorded failures that can guide future improvements."
            )

            if failures:
                for item in failures[-3:][::-1]:
                    st.markdown(
                        f"""
                        <div class="surface">
                            <div class="surface-title">
                                {item["action_description"]}
                            </div>
                            <div class="surface-caption">
                                {item["failure_reason"]}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            else:
                show_empty_state(
                    "No failures recorded",
                    "Failure records will appear here when available.",
                )

        st.markdown("### Memory archive")

        if lessons:
            st.dataframe(
                [
                    {
                        "ID": item["id"],
                        "Title": item["title"],
                        "Verified": item["verified"],
                    }
                    for item in lessons[-5:][::-1]
                ],
                use_container_width=True,
                hide_index=True,
            )
        else:
            show_empty_state(
                "No verified memories yet",
                "Verified lessons will appear here.",
            )

    # ---------- INTENT PATHS ----------

    
    # ---------- INTENT PATHS ----------

    elif page == "Intent paths":
        st.markdown("### Preserved user intent")
        st.caption("Create and review the goals your AI agent must follow.")

        with st.form("create_goal_form"):
            goal_text = st.text_input(
                "Goal",
                placeholder="Example: Help users find reliable information",
            )

            constraints_text = st.text_area(
                "Constraints",
                placeholder="Enter one constraint per line",
            )

            approval_required = st.checkbox(
                "Require approval before sensitive actions",
                value=True,
            )

            submitted = st.form_submit_button("Save goal")

            if submitted:
                if len(goal_text.strip()) < 5:
                    st.error("Goal must contain at least 5 characters.")
                else:
                    payload = {
                        "goal": goal_text.strip(),
                        "constraints": [
                            line.strip()
                            for line in constraints_text.splitlines()
                            if line.strip()
                        ],
                        "approval_required": approval_required,
                    }

                    try:
                        response = requests.post(
                            f"{API_URL}/goals",
                            json=payload,
                            timeout=5,
                        )

                        if response.status_code in (200, 201):
                            st.success("Goal saved successfully.")
                            st.rerun()
                        else:
                            st.error(
                                f"Could not save goal: {response.text}"
                            )

                    except requests.RequestException:
                        st.error("Could not connect to the Threadwise API.")

        st.divider()
        st.markdown("### Stored goals")

        if goals:
            search = st.text_input(
                "Search goals",
                placeholder="Search by goal or constraint...",
            )

            filtered_goals = [
                item for item in goals
                if search.lower() in (
                    item["goal"]
                    + " "
                    + " ".join(item.get("constraints", []))
                ).lower()
            ]

            st.dataframe(
                filtered_goals,
                use_container_width=True,
                hide_index=True,
            )
        else:
            show_empty_state(
                "Nothing stored yet",
                "Create your first goal using the form above.",
            )


    # ---------- MEMORY ARCHIVE ----------

    elif page == "Memory archive":
        st.markdown("### Verified memory archive")
        st.caption(
            "Only lessons returned by the verified-lessons API are displayed."
        )

        if lessons:
            search = st.text_input(
                "Search memories",
                placeholder="Search titles, descriptions, or evidence...",
            )

            filtered_lessons = [
                item
                for item in lessons
                if search.lower() in (
                    item["title"]
                    + " "
                    + item["description"]
                    + " "
                    + item["evidence"]
                ).lower()
            ]

            if filtered_lessons:
                for item in filtered_lessons:
                    with st.expander(
                        f'{item["title"]} · Memory #{item["id"]}'
                    ):
                        st.write("**What was learned**")
                        st.write(item["description"])

                        st.write("**Evidence recorded**")
                        st.write(item["evidence"])

                        st.caption("Status: Verified in database")
            else:
                show_empty_state(
                    "No matching memories",
                    "Try a different search term.",
                )
        else:
            show_empty_state(
                "The archive is waiting",
                "Add and verify a lesson through the API to see it here.",
            )

    # ---------- FAILURE SIGNALS ----------

   
    # ---------- FAILURE SIGNALS ----------

    elif page == "Failure signals":
        st.markdown("### Failure signals")
        st.caption(
            "Capture mistakes so your AI reliability system "
            "has records to learn from."
        )

        with st.form("record_failure_form"):
            action_description = st.text_input(
                "Action that failed",
                placeholder="Example: Agent gave an unsupported answer",
            )

            failure_reason = st.text_area(
                "Why did it fail?",
                placeholder="Describe what went wrong...",
            )

            expected_behavior = st.text_area(
                "Expected behavior",
                placeholder="Describe what the agent should have done...",
            )

            submitted = st.form_submit_button("Record failure")

            if submitted:
                if (
                    len(action_description.strip()) < 5
                    or len(failure_reason.strip()) < 5
                    or len(expected_behavior.strip()) < 5
                ):
                    st.error(
                        "Please provide at least 5 characters "
                        "in each field."
                    )
                else:
                    payload = {
                        "action_description": action_description.strip(),
                        "failure_reason": failure_reason.strip(),
                        "expected_behavior": expected_behavior.strip(),
                    }

                    try:
                        response = requests.post(
                            f"{API_URL}/failures",
                            json=payload,
                            timeout=5,
                        )

                        if response.status_code in (200, 201):
                            st.success("Failure record saved.")
                            st.rerun()
                        else:
                            st.error(
                                f"Could not save failure: {response.text}"
                            )

                    except requests.RequestException:
                        st.error(
                            "Could not connect to the Threadwise API."
                        )

        st.divider()
        st.markdown("### Recorded failures")

        if failures:
            search = st.text_input(
                "Search failure records",
                placeholder="Search actions, reasons, or expected behavior...",
            )

            filtered_failures = [
                item for item in failures
                if search.lower() in (
                    item["action_description"]
                    + " "
                    + item["failure_reason"]
                    + " "
                    + item["expected_behavior"]
                ).lower()
            ]

            st.metric("Matching records", len(filtered_failures))

            if filtered_failures:
                for item in filtered_failures[::-1]:
                    with st.expander(
                        f'Failure #{item["id"]}: '
                        f'{item["action_description"]}'
                    ):
                        st.write("**Why it failed**")
                        st.write(item["failure_reason"])

                        st.write("**Expected behavior**")
                        st.write(item["expected_behavior"])
            else:
                show_empty_state(
                    "No matching failures",
                    "Try a different search term.",
                )
        else:
            show_empty_state(
                "No failure signals yet",
                "Use the form above to record your first failure.",
            )


    # ---------- DIAGNOSTICS ----------

    elif page == "Diagnostics":
        st.markdown("### System diagnostics")
        st.caption(
            "Check whether the Threadwise API is responding."
        )

        try:
            health = requests.get(
                f"{API_URL}/health",
                timeout=5,
            )
            health.raise_for_status()
            health_data = health.json()

            st.success(
                f'API responded successfully: '
                f'{health_data.get("status", "unknown")}'
            )

            col1, col2 = st.columns(2)

            col1.metric("API", "Reachable")
            col2.metric(
                "Stored records",
                len(goals) + len(lessons) + len(failures),
            )

            st.markdown("#### Health response")
            st.json(health_data)

        except requests.RequestException:
            st.error(
                "The API health endpoint could not be reached."
            )

        st.markdown("#### Data retrieval")

        st.write(f"Goals retrieved: {len(goals)}")
        st.write(f"Verified lessons retrieved: {len(lessons)}")
        st.write(f"Failure records retrieved: {len(failures)}")

except requests.RequestException:
    st.error(
        "Threadwise API is unavailable. Start the FastAPI server, "
        "then refresh the dashboard."
    )

    st.code(
        "python -m uvicorn app.main:app --reload",
        language="bash",
    )

# ---------- FOOTER ----------

st.divider()

st.caption(
    "THREADWISE  /  Memory, intent & reliability  /  Local development"
)
