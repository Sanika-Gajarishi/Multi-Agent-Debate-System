import streamlit as st

from api_client import (
    create_debate,
    get_debates,
    get_debate,
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Multi-Agent Debate System",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# TITLE
# ============================================================

st.title("⚖️ Multi-Agent Debate System")

st.write(
    "Enter a topic and let multiple AI agents debate it "
    "from different perspectives."
)


# ============================================================
# SIDEBAR — PREVIOUS DEBATES
# ============================================================

st.sidebar.divider()

st.sidebar.header("📚 Previous Debates")

try:
    previous_debates = get_debates()

except Exception:
    previous_debates = []

if not isinstance(previous_debates, list):
    previous_debates = []

if previous_debates:

    debate_options = {
        (
            f'#{debate["debate_id"]} — '
            f'{debate["topic"][:40]}'
        ): debate["debate_id"]
        for debate in previous_debates
        if isinstance(debate, dict)
        and "debate_id" in debate
        and "topic" in debate
    }

    if debate_options:

        debate_options = {
            label: debate_id
            for label, debate_id in debate_options.items()
        }

        selected_label = st.sidebar.selectbox(
            "Select a debate",
            options=list(debate_options.keys()),
        )

        selected_id = debate_options[selected_label]

        if st.sidebar.button(
            "📖 Load Selected Debate",
            use_container_width=True,
        ):

            try:
                selected_debate = get_debate(selected_id)

                st.session_state[
                    "current_debate"
                ] = selected_debate
                st.rerun()

            except Exception as exc:

                st.sidebar.error(
                    f"Could not load debate: {exc}"
                )

    else:
        st.sidebar.info("No saved debates yet.")

else:
    st.sidebar.info("No saved debates yet.")

st.sidebar.title("⚙️ Debate Settings")

st.sidebar.markdown(
    "Configure your debate before starting."
)

rounds = st.sidebar.selectbox(
    "Rebuttal rounds",
    options=[1, 2, 3, 5],
    index=0,
)

st.sidebar.caption(
    "Openings happen once. Each selected round adds "
    "one Pro + Con rebuttal cycle."
)

if st.sidebar.button(
    "🆕 New Debate",
    use_container_width=True,
):

    st.session_state.pop(
        "current_debate",
        None,
    )

    st.rerun()
# ============================================================
# NEW DEBATE
# ============================================================

st.subheader("Start a New Debate")

topic = st.text_area(
    "Debate Topic",
    placeholder="Example: Should AI replace software developers?",
    height=100,
)


rounds = st.selectbox(
    "Number of Debate Rounds",
    options=[1, 2, 3, 5],
    index=0,
)


# ============================================================
# START DEBATE BUTTON
# ============================================================

start_debate = st.button(
    "🚀 Start Debate",
    type="primary",
    use_container_width=True,
)

if start_debate:

    if not topic.strip():

        st.warning(
            "Please enter a debate topic first."
        )

    elif len(topic.strip()) < 5:

        st.warning(
            "Please enter a more meaningful debate topic."
        )

    else:

        try:

            with st.status(
                "Running multi-agent debate...",
                expanded=True,
            ) as status:

                st.write("🤖 Pro Agent preparing argument...")
                st.write("🤖 Con Agent preparing argument...")
                st.write("🔄 Running debate rounds...")
                st.write("🔎 Research Agent analyzing claims...")
                st.write("🧐 Critic Agent evaluating arguments...")
                st.write("⚖️ Judge Agent preparing verdict...")

                result = create_debate(
                    topic=topic.strip(),
                    rounds=rounds,
                )

                st.session_state[
                    "current_debate"
                ] = result

                status.update(
                    label="Debate completed!",
                    state="complete",
                    expanded=False,
                )

        except Exception as exc:

            st.error(
                "Unable to complete the debate."
            )

            st.caption(
                f"Backend error: {exc}"
            )

# ============================================================
# DISPLAY CURRENT DEBATE
# ============================================================

if "current_debate" in st.session_state:

    result = st.session_state[
        "current_debate"
    ]

    st.divider()

    st.header("📋 Debate Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Debate ID",
            result["debate_id"],
        )

    with col2:
        st.metric(
            "Rebuttal Rounds",
            result["rounds"],
        )

    with col3:
        st.metric(
            "Total Statements",
            len(result["debate_history"]),
        )

    st.markdown(
        f"### Topic\n{result['topic']}"
    )

    st.divider()

    st.header("💬 Debate Transcript")

    for item in result["debate_history"]:

        speaker = item["speaker"]
        statement_type = item["type"]
        round_number = item["round"]
        content = item["content"]

        if statement_type == "opening":
            title = f"{speaker} — Opening"
        else:
            title = (
                f"Round {round_number} — "
                f"{speaker} — Rebuttal"
            )

        with st.expander(
            title,
            expanded=False,
        ):
            st.write(content)

    st.divider()

    st.header("🔎 Research Analysis")

    with st.expander(
        "View Research Agent Analysis",
        expanded=False,
    ):
        st.write(
            result["research_analysis"]
        )

    st.header("🧐 Critic Analysis")

    with st.expander(
        "View Critic Agent Analysis",
        expanded=False,
    ):
        st.write(result["critique"])

    st.divider()

    st.header("⚖️ Final Verdict")

    judge = result["judge_result"]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Winner", judge["winner"])

    with col2:
        st.metric("Pro Score", judge["pro_score"])

    with col3:
        st.metric("Con Score", judge["con_score"])

    st.write(
        f"**Confidence:** "
        f"{judge['confidence']:.2f}"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Strongest Pro Argument")
        st.write(judge["strongest_pro_argument"])

    with col2:
        st.subheader("Strongest Con Argument")
        st.write(judge["strongest_con_argument"])

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Pro Weaknesses")
        for weakness in judge["pro_weaknesses"]:
            st.write(f"• {weakness}")

    with col2:
        st.subheader("Con Weaknesses")
        for weakness in judge["con_weaknesses"]:
            st.write(f"• {weakness}")

    st.subheader("🧠 Judge Reasoning")
    st.write(judge["reasoning"])

    st.subheader("📝 Final Verdict")
    st.info(judge["final_verdict"])

st.sidebar.divider()

