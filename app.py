
import json
import streamlit as st

from services.gemini_service import GeminiService
from services.prompt_service import PromptService
from services.evaluation_service import EvaluationService
from database.db_manager import DatabaseManager
from utils.export import export_pdf, export_txt
from prompts.templates import PROMPTS


# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AI Writing Assistant Pro",
    page_icon="",
    layout="wide"
)


# ==========================================
# 2. INITIALIZE SERVICES
# ==========================================

@st.cache_resource
def initialize_services():

    return (
        GeminiService(),
        PromptService(),
        EvaluationService(),
        DatabaseManager()
    )


try:
    gemini, prompt_service, evaluator, database = (
        initialize_services()
    )

except Exception as error:
    st.error(f"Initialization failed: {error}")
    st.stop()


# ==========================================
# 3. SESSION STATE
# ==========================================

defaults = {
    "generated_text": "",
    "user_input": "",
    "last_task": "",
    "last_tone": "Professional",
    "last_length": "Medium",
    "generation_id": None,
    "evaluation": None,
    "latency": 0.0,
    "conversation": []
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


def clear_content():

    st.session_state.generated_text = ""
    st.session_state.user_input = ""
    st.session_state.generation_id = None
    st.session_state.evaluation = None
    st.session_state.conversation = []
    st.session_state.latency = 0.0


# ==========================================
# 4. SIDEBAR NAVIGATION
# ==========================================

with st.sidebar:

    st.title(" AI Writer")

    st.write("Your AI-powered writing companion.")

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Content Generator",
            "AI Evaluation",
            "Generation History",
            "Analytics",
            "About Project"
        ]
    )

    st.divider()

    st.subheader("Available Tools")

    st.markdown("""
    -  Blog Writer
    -  Email Drafter
    -  Code Explainer
    -  Social Media Writer
    """)

    st.divider()

    st.subheader("About Project")

    st.write(
        "Generative AI application built using "
        "Python, Streamlit and Google's Gemini API."
    )

    st.caption("Skill Nexis | Generative AI Internship")


# ==========================================
# 5. CONTENT GENERATOR
# ==========================================

if page == "Content Generator":

    st.title("AI Writing Assistant")

    st.write(
        "Create blogs, professional emails, "
        "code explanations and social media content."
    )

    st.divider()

    col1, col2 = st.columns([2, 1])

    with col1:

        task = st.selectbox(
            "Choose your writing task",
            list(PROMPTS.keys())
        )

    with col2:

        output_format = st.selectbox(
            "Output Format",
            ["Markdown", "Plain Text"]
        )

    descriptions = {
        "Blog Writer": "Create informative and engaging blog articles.",
        "Email Drafter": "Write professional and personalized emails.",
        "Code Explainer": "Understand programming code step by step.",
        "Social Media Writer": "Generate engaging social media content."
    }

    st.info(descriptions.get(task, "Choose a writing task."))

    col1, col2 = st.columns(2)

    with col1:

        tone = st.selectbox(
            "Writing Tone",
            [
                "Professional",
                "Friendly",
                "Creative",
                "Formal",
                "Persuasive",
                "Simple"
            ]
        )

    with col2:

        length = st.selectbox(
            "Output Length",
            ["Short", "Medium", "Long"]
        )

    user_input = st.text_area(
        "Enter your topic or instructions",
        key="user_input",
        height=150,
        placeholder="Describe what you want the AI to generate..."
    )

    temperature = st.slider(
        "Creativity Level",
        0.0,
        1.0,
        0.7,
        0.1
    )

    use_memory = st.checkbox(
        "Use previous conversation context",
        value=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        generate_clicked = st.button(
            " Generate Content",
            use_container_width=True
        )

    with col2:

        regenerate_clicked = st.button(
            " Regenerate",
            use_container_width=True,
            disabled=not bool(st.session_state.generated_text)
        )

    with col3:

        st.button(
            " Clear",
            use_container_width=True,
            on_click=clear_content
        )

    # GENERATION LOGIC

    if generate_clicked or regenerate_clicked:

        if not user_input.strip():

            st.warning("Please enter your instructions.")

        else:

            try:

                context = ""

                if use_memory:

                    context = "\n".join(
                        st.session_state.conversation[-6:]
                    )

                prompt = prompt_service.build_prompt(
                    task=task,
                    user_input=user_input,
                    tone=tone,
                    length=length,
                    context=context
                )

                with st.spinner("Generating content..."):

                    result = gemini.generate_content(
                        prompt=prompt,
                        temperature=temperature
                    )

                content = result["content"]

                generation_id = database.save_generation(
                    task=task,
                    user_input=user_input,
                    generated_content=content,
                    tone=tone,
                    output_length=length,
                    latency=result["latency"],
                    model=result["model"]
                )

                st.session_state.generated_text = content
                st.session_state.generation_id = generation_id
                st.session_state.last_task = task
                st.session_state.last_tone = tone
                st.session_state.last_length = length
                st.session_state.latency = result["latency"]
                st.session_state.evaluation = None

                st.session_state.conversation.extend([
                    f"User: {user_input}",
                    f"Assistant: {content}"
                ])

                st.success("Content generated successfully!")

            except Exception as error:

                st.error(f"Generation failed: {error}")

    # DISPLAY GENERATED CONTENT

    if st.session_state.generated_text:

        st.divider()

        st.subheader(" Generated Content")

        st.caption(
            f"Writing Mode: {st.session_state.last_task}"
        )

        content = st.session_state.generated_text

        if output_format == "Markdown":
            st.markdown(content)
        else:
            st.text(content)

        word_count = len(content.split())

        character_count = len(content)

        reading_time = max(1, round(word_count / 200))

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Words", word_count)

        col2.metric("Characters", character_count)

        col3.metric("Reading Time", f"{reading_time} min")

        col1, col2 = st.columns(2)

        with col1:

            st.download_button(
                "⬇ Download TXT",
                data=export_txt(content),
                file_name="AI_Generated_Content.txt",
                mime="text/plain",
                use_container_width=True
            )

        with col2:

            st.download_button(
                " Download PDF",
                data=export_pdf(content),
                file_name="AI_Generated_Content.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        st.caption(
            f"Generation ID: {st.session_state.generation_id} "
            f"| Response time: {st.session_state.latency}s"
        )


# ==========================================
# 6. AI EVALUATION
# ==========================================

elif page == "AI Evaluation":

    st.title("AI Content Quality Evaluation")

    st.write(
        "Evaluate generated content using an AI-powered assessment engine."
    )

    content = st.session_state.generated_text

    if not content:

        st.info(
            "Generate content first using the Content Generator section."
        )

    else:

        st.subheader("Content Preview")

        st.text_area(
            "Generated Content",
            value=content,
            height=180,
            disabled=True
        )

        if st.button("Evaluate Content", use_container_width=True):

            try:

                with st.spinner("Evaluating content quality..."):

                    evaluation = evaluator.evaluate_content(
                        user_request=st.session_state.user_input,
                        generated_content=content
                    )

                database.update_evaluation(
                    st.session_state.generation_id,
                    evaluation
                )

                st.session_state.evaluation = evaluation

                st.success("Evaluation completed and saved!")

            except Exception as error:

                st.error(f"Evaluation failed: {error}")

        evaluation = st.session_state.evaluation

        if evaluation:

            st.divider()

            st.caption(
                "Scores are AI-generated assessments, not objective measurements."
            )

            st.metric(
                "Overall Quality Score",
                f"{evaluation['overall_score']}/10"
            )

            scores = {
                "Relevance": evaluation["relevance"],
                "Clarity": evaluation["clarity"],
                "Completeness": evaluation["completeness"],
                "Instruction Following": evaluation["instruction_following"]
            }

            st.subheader("Quality Breakdown")

            for label, score in scores.items():

                st.write(f"**{label}: {score}/10**")

                st.progress(score / 10)

            col1, col2 = st.columns(2)

            with col1:

                st.subheader("Strengths")

                for item in evaluation["strengths"]:
                    st.write(f" {item}")

            with col2:

                st.subheader("Improvements")

                for item in evaluation["improvements"]:
                    st.write(f" {item}")

            st.info(evaluation["feedback"])


# ==========================================
# 7. GENERATION HISTORY
# ==========================================

elif page == "Generation History":

    st.title("Generation History")

    st.write("View and search your previously generated content.")

    keyword = st.text_input(
        "Search by topic, task or content"
    )

    try:

        if keyword.strip():

            history = database.search_history(keyword)

        else:

            history = database.get_history(limit=100)

        if not history:

            st.info("No generation records found.")

        else:

            st.caption(f"Total records displayed: {len(history)}")

            for item in history:

                with st.expander(
                    f"#{item['id']} | {item['task']} | {item['created_at']}"
                ):

                    st.write("**Original Instructions**")

                    st.write(item["user_input"])

                    st.write("**Generated Content**")

                    st.markdown(item["generated_content"])

                    st.write("Tone:", item["tone"])

                    st.write("Length:", item["output_length"])

                    st.write("Latency:", item["latency"], "seconds")

                    if item["evaluation"]:

                        saved_evaluation = json.loads(
                            item["evaluation"]
                        )

                        st.write(
                            "Overall Evaluation:",
                            saved_evaluation["overall_score"],
                            "/10"
                        )

                    col1, col2 = st.columns(2)

                    with col1:

                        st.download_button(
                            "Download TXT",
                            data=export_txt(item["generated_content"]),
                            file_name=f"generation_{item['id']}.txt",
                            key=f"txt_{item['id']}"
                        )

                    with col2:

                        st.download_button(
                            "Download PDF",
                            data=export_pdf(item["generated_content"]),
                            file_name=f"generation_{item['id']}.pdf",
                            key=f"pdf_{item['id']}"
                        )

    except Exception as error:

        st.error(f"History loading failed: {error}")


# ==========================================
# 8. ANALYTICS DASHBOARD
# ==========================================

elif page == "Analytics":

    st.title("Application Analytics")

    st.write(
        "Monitor application usage and generation performance."
    )

    try:

        history = database.get_history(limit=1000)

        if not history:

            st.info(
                "Generate some content to see analytics."
            )

        else:

            total = len(history)

            average_latency = sum(
                item["latency"] or 0
                for item in history
            ) / total

            task_counts = {}

            evaluated_scores = []

            for item in history:

                task_name = item["task"]

                task_counts[task_name] = (
                    task_counts.get(task_name, 0) + 1
                )

                if item["evaluation"]:

                    saved = json.loads(item["evaluation"])

                    evaluated_scores.append(
                        saved["overall_score"]
                    )

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Total Generations",
                total
            )

            col2.metric(
                "Average Response Time",
                f"{average_latency:.2f}s"
            )

            col3.metric(
                "Evaluated Generations",
                len(evaluated_scores)
            )

            st.divider()

            st.subheader("Usage by Writing Task")

            st.bar_chart(task_counts)

            if evaluated_scores:

                st.subheader("Average AI Quality Score")

                average_score = sum(
                    evaluated_scores
                ) / len(evaluated_scores)

                st.metric(
                    "Average Quality",
                    f"{average_score:.2f}/10"
                )

            else:

                st.info(
                    "Evaluate some generated content to see quality analytics."
                )

    except Exception as error:

        st.error(f"Analytics error: {error}")


# ==========================================
# 9. ABOUT PROJECT
# ==========================================

elif page == "About Project":

    st.title("About AI Writing Assistant Pro")

    st.write("""
    An AI-powered writing and content evaluation platform
    developed using Python, Streamlit and Google's Gemini API.

    Key Features:

    - Multiple AI writing modes
    - Dynamic prompt engineering
    - Tone and output length controls
    - Conversation context
    - AI-based content evaluation
    - SQLite generation history
    - PDF and TXT downloads
    - Usage analytics
    - API response latency monitoring
    """)

    st.info(
        "Developed as part of the Skill Nexis "
        "Generative AI & LLMs Internship."
    )


# ==========================================
# 10. FOOTER
# ==========================================

st.divider()

st.caption(
    "AI Writing Assistant Pro | "
    "Python • Streamlit • Gemini API • SQLite | "
    "Skill Nexis Internship"
)
