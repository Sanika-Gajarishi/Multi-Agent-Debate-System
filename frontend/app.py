import streamlit as st
from streamlit_mic_recorder import speech_to_text
from api_client import (
    create_debate,
    get_debates,
    get_debate,
)
from voice.speech_to_text import audio_to_text
from voice.text_to_speech import text_to_audio_bytes

def speak_text(
    text: str,
    key: str,
):
    try:

        audio = text_to_audio_bytes(text)

        st.audio(
            audio,
            format="audio/mp3",
        )

    except Exception as exc:

        st.warning(
            f"Audio generation failed: {exc}"
        )


def render_voice_playback(result: dict):
    st.subheader("🎙️ Voice Debate Presentation")

    st.write(
        "Listen to the different stages of the debate."
    )

    debate_history = result.get(
        "debate_history",
        []
    )

    for index, item in enumerate(debate_history):

        speaker = item.get(
            "speaker",
            "UNKNOWN"
        )

        statement_type = item.get(
            "type",
            "statement"
        )

        content = item.get(
            "content",
            ""
        )

        if not content:
            continue

        st.markdown(
            f"### 🎙️ {speaker} — {statement_type.title()}"
        )

        st.write(content)

        try:
            audio = text_to_audio_bytes(content)

            st.audio(
                audio,
                format="audio/mp3",
            )

        except Exception as exc:
            st.warning(
                f"Voice generation failed for "
                f"{speaker} {statement_type}: {exc}"
            )


def render_analysis_voice(result: dict):
    st.subheader("🔊 Analysis & Verdict Audio")

    sections = [
        (
            "🔬 Research Analysis",
            result.get("research_analysis", "")
        ),
        (
            "🧐 Critic Analysis",
            result.get("critique", "")
        ),
        (
            "⚖️ Final Verdict",
            result.get(
                "judge_result",
                {}
            ).get(
                "final_verdict",
                ""
            )
        ),
    ]

    for title, text in sections:

        if not text:
            continue

        st.markdown(f"### {title}")

        st.write(text)

        try:
            audio = text_to_audio_bytes(text)

            st.audio(
                audio,
                format="audio/mp3",
            )

        except Exception as exc:
            st.warning(
                f"Voice generation failed: {exc}"
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

mode = st.radio(
    "Choose Debate Mode",
    options=[
        "📝 Text Mode",
        "🎙️ Voice Mode",
    ],
    horizontal=True,
)

voice_mode_type = st.radio(
    "Choose Voice Experience",
    [
        "No Voice Experience",
        "🎙️ Voice Debate",
        "🗣️ Interactive Voice Presentation"
    ],
    index=0,
)

def render_interactive_voice_presentation(result: dict):

    st.subheader("🗣️ Interactive Voice Presentation")

    st.write(
        "Listen to the debate one speaker at a time."
    )

    debate_history = result.get(
        "debate_history",
        []
    )

    if not debate_history:
        st.info(
            "No debate conversation is available."
        )
        return

    for index, item in enumerate(debate_history):

        speaker = item.get(
            "speaker",
            "UNKNOWN"
        )

        statement_type = item.get(
            "type",
            "statement"
        )

        content = item.get(
            "content",
            ""
        )

        if not content.strip():
            continue

        if speaker == "PRO":
            speaker_name = "🟢 Pro Agent"
        elif speaker == "CON":
            speaker_name = "🔴 Con Agent"
        else:
            speaker_name = f"🎙️ {speaker}"

        st.markdown(
            f"### {speaker_name}"
        )

        st.caption(
            statement_type.title()
        )

        with st.expander(
            "View transcript",
            expanded=False
        ):
            st.write(content)

        try:

            audio = text_to_audio_bytes(
                content,
                language="en"
            )

            st.audio(
                audio,
                format="audio/mp3"
            )

        except Exception as exc:

            st.warning(
                f"Unable to generate audio: {exc}"
            )


def render_interactive_analysis(result: dict):

    st.subheader("🧠 AI Analysis")

    analysis_sections = [
        (
            "🔬 Research Agent",
            result.get(
                "research_analysis",
                ""
            )
        ),
        (
            "🧐 Critic Agent",
            result.get(
                "critique",
                ""
            )
        ),
        (
            "⚖️ Judge Agent",
            result.get(
                "judge_result",
                {}
            ).get(
                "final_verdict",
                ""
            )
        ),
    ]

    for title, content in analysis_sections:

        if not content:
            continue

        st.markdown(
            f"### {title}"
        )

        with st.expander(
            "View analysis",
            expanded=False
        ):
            st.write(content)

        try:

            audio = text_to_audio_bytes(
                content,
                language="en"
            )

            st.audio(
                audio,
                format="audio/mp3"
            )

        except Exception as exc:

            st.warning(
                f"Unable to generate audio: {exc}"
            )


if voice_mode_type == "🗣️ Interactive Voice Presentation":

    result = st.session_state.get(
        "current_debate",
        {}
    )

    if not result:
        st.info(
            "Start a debate to enable interactive voice presentation."
        )
    else:
        render_interactive_voice_presentation(
            result
        )

        render_interactive_analysis(
            result
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

voice_playback = st.sidebar.toggle(
    "🔊 Enable Voice Playback",
    value=False,
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

if mode == "📝 Text Mode":

    st.subheader("Start a Debate")

    text_rounds = st.selectbox(
        "Rebuttal rounds",
        options=[1, 2, 3, 4, 5],
        index=0,
        key="text_rounds",
    )

    topic = st.text_area(
        "Debate Topic",
        placeholder=(
            "Example: Should AI replace software developers?"
        ),
        height=100,
    )

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
                "Please provide a more meaningful debate topic."
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
                        rounds=text_rounds,
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

else:

    st.subheader("🎙️ Voice Debate Mode")

    st.info(
        """
        Voice Mode allows you to speak your debate topic
        instead of typing it.

        Your speech is converted to text and sent through
        the same multi-agent debate pipeline.
        """
    )

    st.write(
        "Speak your debate topic and the system "
        "will convert your speech into text."
    )

    audio = speech_to_text(
        start_prompt="🎙️ Start Speaking",
        stop_prompt="⏹️ Stop Recording",
        just_once=True,
        use_container_width=True,
        language="en",
    )

    if audio:

        try:

            voice_topic = audio_to_text(audio)

            st.session_state[
                "voice_topic"
            ] = voice_topic

        except Exception as exc:

            st.error(
                f"Voice input failed: {exc}"
            )

    if "voice_topic" in st.session_state:

        st.success(
            "Speech recognized successfully."
        )

        st.text_area(
            "Recognized Debate Topic",
            value=st.session_state[
                "voice_topic"
            ],
            height=100,
            disabled=True,
        )

    voice_rounds = st.selectbox(
        "Rebuttal rounds",
        options=[1, 2, 3, 4, 5],
        index=0,
        key="voice_rounds",
    )

    voice_start = st.button(
        "🎙️ Start Voice Debate",
        type="primary",
        use_container_width=True,
    )

    if voice_start:

        voice_topic = st.session_state.get(
            "voice_topic",
            "",
        )

        if not voice_topic.strip():

            st.warning(
                "Please speak a debate topic first."
            )

        else:

            try:

                with st.status(
                    "Running voice debate...",
                    expanded=True,
                ) as status:

                    st.write("🤖 Pro Agent preparing...")
                    st.write("🤖 Con Agent preparing...")
                    st.write("🔄 Running debate rounds...")
                    st.write("🔎 Research Agent analyzing...")
                    st.write("🧐 Critic Agent evaluating...")
                    st.write("⚖️ Judge Agent deciding...")

                    result = create_debate(
                        topic=voice_topic.strip(),
                        rounds=voice_rounds,
                    )

                    st.session_state[
                        "current_debate"
                    ] = result

                    status.update(
                        label="Voice debate completed!",
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

            if voice_playback:

                if st.button(
                    "🔊 Listen",
                    key=(
                        f"listen_"
                        f"{speaker}_"
                        f"{round_number}_"
                        f"{statement_type}"
                    ),
                ):

                    speak_text(
                        text=content,
                        key=(
                            f"{speaker}_"
                            f"{round_number}_"
                            f"{statement_type}"
                        ),
                    )

    st.divider()

    st.header("🔎 Research Analysis")

    with st.expander(
        "View Research Agent Analysis",
        expanded=False,
    ):
        research_text = result[
             "research_analysis"
        ]

        st.write(research_text)

        if voice_playback:

            if st.button(
                "🔊 Listen to Research",
                key="listen_research",
            ):

                speak_text(
                    text=research_text,
                    key="research",
                )

    st.header("🧐 Critic Analysis")

    with st.expander(
        "View Critic Agent Analysis",
        expanded=False,
    ):
        critic_text = result[
            "critique"
        ]

        st.write(critic_text)

        if voice_playback:

            if st.button(
                "🔊 Listen to Critic",
                key="listen_critic",
            ):

                speak_text(
                    text=critic_text,
                    key="critic",
                )

    st.divider()

    st.header("⚖️ Final Verdict")

    judge = result["judge_result"]

    spoken_verdict = f"""
The final verdict is {judge["winner"]}.

The Pro side received a score of
{judge["pro_score"]}.

The Con side received a score of
{judge["con_score"]}.

Confidence in the verdict is
{judge["confidence"]:.0%}.

The strongest Pro argument was:

{judge["strongest_pro_argument"]}

The strongest Con argument was:

{judge["strongest_con_argument"]}

The judge's reasoning was:

{judge["reasoning"]}

Final verdict:

{judge["final_verdict"]}
"""

    if voice_playback:

        if st.button(
            "🔊 Listen to Final Verdict",
            key="listen_final_verdict",
        ):

            speak_text(
                text=spoken_verdict,
                key="final_verdict",
            )

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

    if voice_playback:
        render_voice_playback(result)

        render_analysis_voice(result)

st.sidebar.divider()







