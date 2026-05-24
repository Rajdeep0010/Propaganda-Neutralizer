# app.py
import streamlit as st
from pipeline import run_pipeline

st.set_page_config(
    page_title="Propaganda Neutralizer",
    page_icon="🔍",
    layout="wide"
)

st.markdown("""
<style>
    .main { padding: 2rem; }
    .stButton>button { border-radius: 8px; font-weight: 600; }

    .help-box {
        background: #1a1a2e;
        border: 1px solid #333;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin-bottom: 1rem;
        font-size: 0.85rem;
        color: #ccc;
        line-height: 1.6;
    }
    .help-box b { color: #fff; font-size: 0.95rem; }

    .technique-card {
        background: #1a1a2e;
        border-left: 4px solid #e63946;
        padding: 0.9rem 1.1rem;
        border-radius: 8px;
        margin-bottom: 0.6rem;
    }
    .technique-name { font-size: 1rem; font-weight: 700; color: #fff; }
    .technique-snippet { font-size: 0.8rem; color: #aaa; margin-top: 4px; }

    .score-card {
        text-align: center;
        padding: 1.2rem 1rem;
        background: #1a1a2e;
        border-radius: 10px;
        border: 1px solid #2a2a3e;
    }
    .score-label { font-size: 0.85rem; color: #aaa; margin-bottom: 4px; font-weight: 600; }
    .score-value { font-size: 2rem; font-weight: 800; }
    .score-desc  { font-size: 0.75rem; color: #888; margin-top: 6px; line-height: 1.4; }

    .section-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #fff;
        margin-bottom: 1rem;
        margin-top: 0.5rem;
    }
    .before-box {
        background: #2a1a1a;
        border: 1px solid #e63946;
        border-radius: 10px;
        padding: 1.2rem;
        color: #ffcdd2;
        font-size: 1rem;
        line-height: 1.7;
    }
    .after-box {
        background: #1a2a1a;
        border: 1px solid #4ade80;
        border-radius: 10px;
        padding: 1.2rem;
        color: #c8e6c9;
        font-size: 1rem;
        line-height: 1.7;
    }
    .box-label {
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    .evaluator-box {
        background: #1a1a2e;
        border: 1px solid #3a3a5e;
        border-radius: 10px;
        padding: 1rem 1.4rem;
        color: #ccc;
        font-size: 0.9rem;
        line-height: 1.6;
        margin-top: 1rem;
    }
    .clean-badge {
        background: #1a2a1a;
        border: 1px solid #4ade80;
        border-radius: 8px;
        padding: 1rem 1.4rem;
        color: #4ade80;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ────────────────────────────────────────────────
if "context" not in st.session_state:
    st.session_state.context = ""
if "snippet" not in st.session_state:
    st.session_state.snippet = ""

# ── SIDEBAR ──────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## Propaganda Neutralizer")
    st.markdown("""
    This tool detects propaganda techniques in text
    and rewrites them into neutral, factual language
    using AI.

    **How to use:**
    1. Paste the full sentence in Context
    2. Paste the suspicious phrase in Span
    3. Click Analyze and Neutralize

    Or pick a quick example below.
    """)
    st.divider()
    st.markdown("**Detects 19 techniques including:**")
    for t in [
        "Loaded Language", "Name Calling",
        "Appeal to Fear",  "Exaggeration",
        "Bandwagon",       "Black and White Fallacy",
        "Flag Waving",     "Doubt", "and 11 more..."
    ]:
        st.markdown(f"- {t}")

# ── EXAMPLES ─────────────────────────────────────────────────────
EXAMPLES = {
    "Loaded Language": {
        "context": "The radical left is destroying everything our ancestors built.",
        "snippet": "radical left is destroying everything"
    },
    "Appeal to Fear": {
        "context": "These criminal immigrants are flooding our borders and stealing jobs from hardworking citizens.",
        "snippet": "criminal immigrants are flooding our borders"
    },
    "Conspiracy": {
        "context": "The globalist elite are secretly controlling our economy and pulling the strings of every government.",
        "snippet": "globalist elite are secretly controlling our economy"
    },
    "Name Calling": {
        "context": "The fake news media is the enemy of the people and cannot be trusted on anything.",
        "snippet": "fake news media is the enemy of the people"
    },
    "Clean Text": {
        "context": "The minister announced a new education policy for rural schools.",
        "snippet": "new education policy for rural schools"
    },
}

# ── HEADER ───────────────────────────────────────────────────────
st.markdown("# Propaganda Neutralizer")
st.markdown("Paste any text to detect hidden propaganda techniques and get a clean, neutral rewrite instantly.")
st.divider()

# ── EXAMPLE BUTTONS ──────────────────────────────────────────────
st.markdown("**Try a quick example:**")
cols = st.columns(len(EXAMPLES))
for i, (label, data) in enumerate(EXAMPLES.items()):
    if cols[i].button(label, use_container_width=True):
        st.session_state.context = data["context"]
        st.session_state.snippet = data["snippet"]

st.markdown("")

# ── FIELD EXPLANATIONS ───────────────────────────────────────────
col_help1, col_help2 = st.columns(2)
with col_help1:
    st.markdown("""
    <div class="help-box">
        <b>What is Full Context?</b><br><br>
        The complete sentence or paragraph that contains the text
        you want to analyze. Providing the full sentence helps the
        AI understand the surrounding meaning and produce a more
        accurate rewrite.<br><br>
        <span style="color:#888;">Example: "The radical left is destroying
        everything our ancestors built."</span>
    </div>
    """, unsafe_allow_html=True)

with col_help2:
    st.markdown("""
    <div class="help-box">
        <b>What is a Propaganda Span?</b><br><br>
        The specific word or short phrase inside your sentence that
        sounds suspicious, emotionally charged, or manipulative.
        This is the exact fragment the AI will classify and remove
        the propaganda from.<br><br>
        <span style="color:#888;">Example: "radical left is destroying
        everything"</span>
    </div>
    """, unsafe_allow_html=True)

# ── INPUT FIELDS ─────────────────────────────────────────────────
col1, col2 = st.columns(2)
with col1:
    context = st.text_area(
        "Full Context",
        value=st.session_state.context,
        placeholder="Paste the full sentence or paragraph here...",
        height=130
    )
with col2:
    snippet = st.text_area(
        "Propaganda Span",
        value=st.session_state.snippet,
        placeholder="Paste the specific suspicious phrase here...",
        height=130
    )

st.session_state.context = context
st.session_state.snippet = snippet

st.markdown("")
run_btn = st.button("Analyze and Neutralize", type="primary", use_container_width=True)

# ── RUN PIPELINE ─────────────────────────────────────────────────
if run_btn:
    if not context.strip() or not snippet.strip():
        st.warning("Please fill in both fields before analyzing.")
    else:
        with st.spinner("Analyzing text and generating neutral rewrite..."):
            result = run_pipeline(context, snippet)

        st.divider()

        # ── DETECTED TECHNIQUES ──────────────────────────────────
        st.markdown('<div class="section-title">Detected Propaganda Techniques</div>',
                    unsafe_allow_html=True)

        TECHNIQUE_MEANINGS = {
            "Loaded_Language"              : "Words chosen specifically to trigger an emotional reaction rather than convey facts.",
            "Name_Calling"                 : "Attacking a person or group with a negative label instead of addressing their argument.",
            "Labeling"                     : "Reducing a complex person or group to a single dismissive tag.",
            "Appeal_to_fear-prejudice"     : "Using fear or prejudice to push an opinion without providing real evidence.",
            "Appeal_to_Authority"          : "Claiming something is true simply because an authority figure said so.",
            "Exaggeration"                 : "Overstating facts or outcomes far beyond what the evidence actually supports.",
            "Minimisation"                 : "Downplaying a significant event or fact to make it seem less important.",
            "Flag-Waving"                  : "Exploiting national or group pride to justify a position without argument.",
            "Doubt"                        : "Questioning someone's credibility or motives without providing real proof.",
            "Causal_Oversimplification"    : "Blaming a complex problem on a single cause while ignoring other factors.",
            "Black-and-White_Fallacy"      : "Presenting only two extreme options when many other possibilities exist.",
            "Repetition"                   : "Repeating a message over and over to make it feel true through familiarity.",
            "Bandwagon"                    : "Pressuring people to follow the crowd rather than think for themselves.",
            "Reductio_ad_hitlerum"         : "Discrediting someone by comparing them to Hitler or the Nazis.",
            "Red_Herring"                  : "Introducing an irrelevant topic to distract from the real issue.",
            "Straw_Men"                    : "Misrepresenting someone's position to make it easier to attack.",
            "Slogans"                      : "Using a catchy phrase as a substitute for a real argument.",
            "Thought-terminating_Cliches"  : "Using a familiar phrase to shut down critical thinking and discussion.",
            "Whataboutism"                 : "Deflecting criticism by pointing to someone else's wrongdoing instead.",
        }

        if not result["techniques"]:
            st.markdown("""
            <div class="clean-badge">
                No propaganda technique detected. This text appears factual and neutral.
            </div>
            """, unsafe_allow_html=True)
        else:
            for d in result["techniques"]:
                confidence_pct = int(d["confidence"] * 100)
                color          = "#e63946" if confidence_pct > 70 else "#f4a261"
                meaning        = TECHNIQUE_MEANINGS.get(d["technique"], "")
                st.markdown(f"""
                <div class="technique-card">
                    <div class="technique-name">
                        {d['technique'].replace('_', ' ')}
                        <span style="float:right; color:{color}; font-size:0.9rem;">
                            {confidence_pct}% confidence
                        </span>
                    </div>
                    <div class="technique-snippet">
                        What this means: {meaning}
                    </div>
                    <div class="technique-snippet" style="margin-top:6px;">
                        Detected in: "{snippet}"
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.divider()

        # ── BEFORE / AFTER ───────────────────────────────────────
        st.markdown('<div class="section-title">Before and After Comparison</div>',
                    unsafe_allow_html=True)
        col3, col4 = st.columns(2)
        with col3:
            st.markdown("""
            <div class="box-label" style="color:#e63946;">Original — contains propaganda</div>
            """, unsafe_allow_html=True)
            st.markdown(f'<div class="before-box">{context}</div>',
                        unsafe_allow_html=True)
        with col4:
            st.markdown("""
            <div class="box-label" style="color:#4ade80;">Neutralized — rhetoric removed</div>
            """, unsafe_allow_html=True)
            st.markdown(f'<div class="after-box">{result["neutralized"]}</div>',
                        unsafe_allow_html=True)

        st.divider()

        # ── EVALUATION SCORES ────────────────────────────────────
        if result.get("scores"):
            st.markdown('<div class="section-title">Rewrite Quality Scores</div>',
                        unsafe_allow_html=True)

            SCORE_DESCRIPTIONS = {
                "factual_preservation": (
                    "Factual Preservation",
                    "Did the rewrite keep all the original facts intact without adding or removing information?"
                ),
                "rhetoric_removal": (
                    "Rhetoric Removal",
                    "Was the propaganda technique successfully removed? Is the rewritten text free of manipulation?"
                ),
                "fluency": (
                    "Fluency",
                    "Does the rewritten text read naturally? Is it grammatically correct and easy to understand?"
                ),
                "overall": (
                    "Overall Score",
                    "The average score across all three criteria above."
                ),
            }

            scores = result["scores"]
            c1, c2, c3, c4 = st.columns(4)

            def score_color(s):
                return "#4ade80" if s >= 4 else "#f4a261" if s >= 3 else "#e63946"

            for col, key in zip([c1, c2, c3, c4], SCORE_DESCRIPTIONS):
                val   = scores.get(key, 0)
                label, desc = SCORE_DESCRIPTIONS[key]
                col.markdown(f"""
                <div class="score-card">
                    <div class="score-label">{label}</div>
                    <div class="score-value" style="color:{score_color(val)};">{val}/5</div>
                    <div class="score-desc">{desc}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="evaluator-box">
                <b>What the AI evaluator says:</b><br>
                {scores.get("reasoning")}
            </div>
            """, unsafe_allow_html=True)