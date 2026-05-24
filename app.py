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
    .technique-card {
        background: #1e1e2e;
        border-left: 4px solid #e63946;
        padding: 0.8rem 1rem;
        border-radius: 6px;
        margin-bottom: 0.5rem;
    }
    .score-label { font-size: 0.8rem; color: #aaa; margin-bottom: 2px; }
    .score-value { font-size: 1.6rem; font-weight: 700; color: #4ade80; }
    .help-box {
        background: #1e1e2e;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        margin-bottom: 1rem;
        font-size: 0.85rem;
        color: #ccc;
    }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE — fixes vanishing text on button click ─────────
# Streamlit reruns the whole script on every interaction.
# Without session_state, example values reset to "" on rerun.
# We store context and snippet in session_state so they persist.
if "context" not in st.session_state:
    st.session_state.context = ""
if "snippet" not in st.session_state:
    st.session_state.snippet = ""

# ── SIDEBAR ──────────────────────────────────────────────────────
with st.sidebar:
    st.title("About")
    st.markdown("""
    This tool detects **propaganda techniques** in text and rewrites them into neutral, factual language.

    **How to use:**
    1. Paste the full sentence in **Context**
    2. Paste the suspicious phrase in **Span**
    3. Click **Analyze & Neutralize**

    **Or pick an example below ↓**
    """)
    st.divider()
    st.markdown("**Detects 19 techniques including:**")
    for t in [
        "🔴 Loaded Language", "🔴 Name Calling",
        "🔴 Appeal to Fear",  "🔴 Exaggeration",
        "🔴 Bandwagon",       "🔴 Black & White Fallacy",
        "🔴 Flag Waving",     "🔴 Doubt", "... and 11 more"
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
st.title("🔍 Propaganda Neutralizer")
st.markdown("Paste any text below to detect propaganda techniques and get a neutralized rewrite.")
st.divider()

# ── EXAMPLE BUTTONS ──────────────────────────────────────────────
st.markdown("**Quick Examples:**")
cols = st.columns(len(EXAMPLES))
for i, (label, data) in enumerate(EXAMPLES.items()):
    if cols[i].button(label, use_container_width=True):
        # store in session_state so values survive the rerun
        st.session_state.context = data["context"]
        st.session_state.snippet = data["snippet"]

# ── FIELD EXPLANATIONS ───────────────────────────────────────────
st.markdown("")
col_help1, col_help2 = st.columns(2)

with col_help1:
    st.markdown("""
    <div class="help-box">
    📄 <b>What is Full Context?</b><br>
    The complete sentence or paragraph containing the suspicious text.
    This gives the model surrounding information to understand the meaning
    and rewrite it accurately.
    <br><br>
    <i>Example: "The radical left is destroying everything our ancestors built."</i>
    </div>
    """, unsafe_allow_html=True)

with col_help2:
    st.markdown("""
    <div class="help-box">
    🎯 <b>What is Propaganda Span?</b><br>
    The specific word or phrase inside the context that you think
    contains propaganda. This is the exact fragment the model
    will classify and the neutralizer will focus on removing.
    <br><br>
    <i>Example: "radical left is destroying everything"</i>
    </div>
    """, unsafe_allow_html=True)

# ── INPUT FIELDS ─────────────────────────────────────────────────
col1, col2 = st.columns(2)
with col1:
    context = st.text_area(
        "📄 Full Context",
        value=st.session_state.context,    # reads from session_state
        placeholder="Paste the full sentence or paragraph here...",
        height=130
    )
with col2:
    snippet = st.text_area(
        "🎯 Propaganda Span",
        value=st.session_state.snippet,    # reads from session_state
        placeholder="Paste the specific suspicious phrase here...",
        height=130
    )

# update session_state when user types manually
st.session_state.context = context
st.session_state.snippet = snippet

st.markdown("")
run_btn = st.button("🔍 Analyze & Neutralize", type="primary", use_container_width=True)

# ── RUN PIPELINE ─────────────────────────────────────────────────
if run_btn:
    if not context.strip() or not snippet.strip():
        st.warning("⚠️ Please fill in both fields before analyzing.")
    else:
        with st.spinner("Analyzing text and generating neutral rewrite..."):
            result = run_pipeline(context, snippet)

        st.divider()

        # ── DETECTED TECHNIQUES ──────────────────────────────────
        st.subheader("🎯 Detected Propaganda Techniques")
        if not result["techniques"]:
            st.success("✅ No propaganda technique detected — this text appears clean.")
        else:
            for d in result["techniques"]:
                confidence_pct = int(d["confidence"] * 100)
                color = "#e63946" if confidence_pct > 70 else "#f4a261"
                st.markdown(f"""
                <div class="technique-card">
                    <b>{d['technique']}</b>
                    <span style="float:right; color:{color}; font-weight:700;">{confidence_pct}% confidence</span>
                    <br><small style="color:#aaa;">Detected in: <i>"{snippet}"</i></small>
                </div>
                """, unsafe_allow_html=True)

        st.divider()

        # ── BEFORE / AFTER ───────────────────────────────────────
        st.subheader("📝 Before / After Comparison")
        col3, col4 = st.columns(2)
        with col3:
            st.markdown("**🔴 Original (with propaganda)**")
            st.error(context)
        with col4:
            st.markdown("**🟢 Neutralized (rhetoric removed)**")
            st.success(result["neutralized"])

        st.divider()

        # ── EVALUATION SCORES ────────────────────────────────────
        if result.get("scores"):
            st.subheader("📊 Rewrite Quality Scores")
            scores = result["scores"]
            c1, c2, c3, c4 = st.columns(4)

            def score_color(s):
                return "#4ade80" if s >= 4 else "#f4a261" if s >= 3 else "#e63946"

            for col, label, key in [
                (c1, "Factual Preservation", "factual_preservation"),
                (c2, "Rhetoric Removal",     "rhetoric_removal"),
                (c3, "Fluency",              "fluency"),
                (c4, "Overall",              "overall"),
            ]:
                val = scores.get(key, 0)
                col.markdown(f"""
                <div style="text-align:center; padding:1rem; background:#1e1e2e;
                            border-radius:8px; border:1px solid #333;">
                    <div class="score-label">{label}</div>
                    <div class="score-value" style="color:{score_color(val)};">{val}/5</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("")
            st.info(f"💬 **Evaluator says:** {scores.get('reasoning')}")