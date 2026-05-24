# evaluator.py
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL  = "llama-3.1-8b-instant"

# ── EVALUATION PROMPT ───────────────────────────────────────────
def build_eval_prompt(original, neutralized, technique):
    return f"""You are an expert evaluator of text neutralization quality.

Propaganda technique that was detected: {technique}

Original text:
\"{original}\"

Neutralized text:
\"{neutralized}\"

Score the neutralized text on these three criteria.
Each score is strictly between 1 and 5.

1. Factual Preservation (1-5)
   Does the neutralized text keep all the same facts as the original?
   5 = all facts preserved, 1 = facts changed or lost

2. Rhetoric Removal (1-5)
   Is the propaganda technique successfully removed?
   5 = completely neutral, 1 = still heavily propagandistic

3. Fluency (1-5)
   Is the neutralized text natural and readable?
   5 = perfectly natural, 1 = awkward or broken

Return ONLY a JSON object in this exact format, nothing else:
{{
  "factual_preservation": <score>,
  "rhetoric_removal": <score>,
  "fluency": <score>,
  "overall": <average of three scores>,
  "reasoning": "<one sentence explanation>"
}}"""


# ── EVALUATE ────────────────────────────────────────────────────
def evaluate(original, neutralized, technique):
    prompt = build_eval_prompt(original, neutralized, technique)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,    # zero temp for consistent scoring
        max_tokens=256,
    )

    raw = response.choices[0].message.content.strip()

    # parse JSON response
    import json
    try:
        # strip markdown fences if model adds them
        clean = raw.replace("```json", "").replace("```", "").strip()
        scores = json.loads(clean)
    except json.JSONDecodeError:
        print(f"Warning: Could not parse scores. Raw response:\n{raw}")
        scores = {
            "factual_preservation" : 0,
            "rhetoric_removal"     : 0,
            "fluency"              : 0,
            "overall"              : 0,
            "reasoning"            : "Parse error"
        }

    return scores


# ── EVALUATE PIPELINE OUTPUT ────────────────────────────────────
def evaluate_pipeline(pipeline_result):
    original    = pipeline_result["original"]
    neutralized = pipeline_result["neutralized"]
    techniques  = pipeline_result["techniques"]

    # skip if no technique detected or text unchanged
    if not techniques or original == neutralized:
        print("Skipping evaluation — no technique detected or text unchanged.")
        return None

    top_technique = techniques[0]["technique"]
    scores        = evaluate(original, neutralized, top_technique)

    print(f"\nEVALUATION SCORES")
    print(f"  Factual Preservation : {scores.get('factual_preservation')}/5")
    print(f"  Rhetoric Removal     : {scores.get('rhetoric_removal')}/5")
    print(f"  Fluency              : {scores.get('fluency')}/5")
    print(f"  Overall              : {scores.get('overall')}/5")
    print(f"  Reasoning            : {scores.get('reasoning')}")

    return scores


# ── TEST ────────────────────────────────────────────────────────
if __name__ == "__main__":
    # simulate a pipeline result
    test_result = {
        "original"   : "The radical left is destroying everything our ancestors built.",
        "neutralized": "The left-wing political group has implemented policies that some argue conflict with traditional values.",
        "techniques" : [{"technique": "Loaded_Language", "confidence": 0.84}]
    }

    evaluate_pipeline(test_result)