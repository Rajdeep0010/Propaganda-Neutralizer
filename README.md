```
markdown
# Propaganda Neutralizer

An end-to-end NLP pipeline that detects propaganda techniques in text and rewrites them into neutral, factual language — with a before/after comparison and AI-powered quality scores.

---

## What It Does

Most tools only flag suspicious text. This tool goes further:

- Identifies the **specific propaganda technique** being used
- **Rewrites** the text neutrally while keeping all original facts
- **Scores** the rewrite on Factual Preservation, Rhetoric Removal, and Fluency

---

## Demo

**Input:**
> The radical left is destroying everything our ancestors built.

**Detected Technique:** Loaded Language (89% confidence)

**Neutralized:**
> Some critics argue that certain left-wing policies conflict with traditional values.

**Quality Scores:** Factual Preservation 4/5 · Rhetoric Removal 5/5 · Fluency 5/5

---

## Propaganda Techniques Detected (19 total)

| Technique | Description |
|---|---|
| Loaded Language | Emotionally charged words used to manipulate |
| Name Calling | Negative labels applied to dismiss someone |
| Appeal to Fear | Exploits fear to push a viewpoint |
| Exaggeration | Overstates facts beyond evidence |
| Bandwagon | Pressures following the crowd |
| Black and White Fallacy | Presents only two extreme options |
| Flag Waving | Exploits national pride without argument |
| Doubt | Questions credibility without evidence |
| Causal Oversimplification | Blames complex problems on one cause |
| Repetition | Repeats message to make it feel true |
| and 9 more... | |

---

## Architecture

```
Input Text + Span
       ↓
DeBERTa-v3-small (fine-tuned)
— detects technique + confidence
       ↓
Llama 3.1 8B via Groq API
— rewrites neutrally using technique-aware prompt
       ↓
Llama 3.1 8B via Groq API
— scores rewrite quality (1-5 per dimension)
       ↓
Before / After + Quality Scores
```

---

## Model Performance

Trained on the SemEval 2020 Propaganda Techniques dataset (18 techniques, span-level annotation).

| Metric | Score |
|---|---|
| Micro F1 | 0.56 |
| Macro F1 | 0.41 |
| Weighted F1 | 0.60 |
| Exact Match | 0.40 |

Core techniques (Loaded Language, Name Calling, Labeling) achieve F1 of 0.74+.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Detection Model | DeBERTa-v3-small (fine-tuned) |
| Training | PyTorch, HuggingFace Transformers |
| Rewriter | Llama 3.1 8B via Groq API |
| Evaluator | Llama 3.1 8B via Groq API |
| Interface | Streamlit |
| Environment | Python 3.11 |

---

## Project Structure

```
propaganda_project/
├── model/                  # fine-tuned model weights (not in git)
│   ├── config.json
│   ├── model.safetensors
│   ├── tokenizer files
│   ├── mlb.pkl
│   └── thresholds.pkl
├── detector.py             # loads model, runs prediction
├── neutralizer.py          # calls Groq API to rewrite
├── evaluator.py            # scores the rewrite quality
├── pipeline.py             # chains all three together
├── app.py                  # Streamlit UI
├── requirements.txt
├── .gitignore
└── .env                    # API keys (not in git)
```

---

## Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/yourusername/propaganda-neutralizer.git
cd propaganda-neutralizer
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Add your API key**

Create a `.env` file:
```
GROQ_API_KEY=your_groq_api_key_here
```

**4. Add the model folder**

Download the fine-tuned model files and place them in `./model/`.
The folder needs: `config.json`, `model.safetensors`, `tokenizer.json`,
`tokenizer_config.json`, `spm.model`, `mlb.pkl`, `thresholds.pkl`.

**5. Run**
```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## Dataset

SemEval 2020 Task 11 — Detection of Propaganda Techniques in News Articles.
Fragment-level span annotations across 18 propaganda technique labels.

---

## Key Design Decisions

**Why DeBERTa-v3 over a generative model**
Encoder-only models are more accurate and efficient for classification. Using a generative model for 18-class classification introduces label hallucination.

**Why per-class thresholds**
Fixed threshold of 0.5 caused precision collapse on rare classes. Per-class optimization improved Micro F1 from 0.41 to 0.56.

**Why technique-aware prompting**
Injecting the detected technique definition into the rewrite prompt forces the LLM to target the specific manipulation pattern rather than doing a generic paraphrase.
```