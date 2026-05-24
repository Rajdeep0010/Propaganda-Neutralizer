#imports
import os 
from groq import Groq
from dotenv import load_dotenv

#load the api key
load_dotenv()
client=Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.1-8b-instant"


#Technique
TECHNIQUE_DEFINITIONS = {
    "Loaded_Language"               : "Uses emotionally charged words to influence instead of inform.",
    "Name_Calling"                  : "Attaches a negative label to a person or group to dismiss them.",
    "Labeling"                      : "Reduces a complex person or group to a single dismissive tag.",
    "Appeal_to_fear-prejudice"      : "Exploits fear or prejudice to push a viewpoint.",
    "Appeal_to_Authority"           : "Uses authority figures to validate a claim without evidence.",
    "Exaggeration"                  : "Overstates facts beyond what evidence supports.",
    "Minimisation"                  : "Downplays significant facts to reduce their perceived importance.",
    "Flag-Waving"                   : "Exploits national or group pride to justify a position.",
    "Doubt"                         : "Questions credibility of a person or source without evidence.",
    "Causal_Oversimplification"     : "Assigns a single cause to a complex problem.",
    "Black-and-White_Fallacy"       : "Presents only two options when more exist.",
    "Repetition"                    : "Repeats a message excessively to make it seem true.",
    "Bandwagon"                     : "Pressures to follow the crowd rather than think independently.",
    "Reductio_ad_hitlerum"          : "Discredits by comparing to Hitler or Nazis.",
    "Red_Herring"                   : "Introduces irrelevant information to distract from the issue.",
    "Straw_Men"                     : "Misrepresents someone's argument to make it easier to attack.",
    "Slogans"                       : "Uses a catchy phrase to replace actual argument.",
    "Thought-terminating_Cliches"   : "Uses a cliche to shut down critical thinking.",
    "Whataboutism"                  : "Deflects criticism by pointing to someone else's faults.",
}

#Build prompt
def build_prompt(context, snippet, technique):
    definition = TECHNIQUE_DEFINITIONS.get(technique, "A propaganda technique.")

    return f"""You are a neutral text editor. Your job is to rewrite propaganda text into factual, neutral language.

Propaganda technique detected: {technique}
Definition: {definition}

Original context:
\"\"\"{context}\"\"\"

Propaganda span:
\"{snippet}\"

Your task:
1. Rewrite the full context removing the propaganda technique
2. Keep all factual information intact
3. Use neutral, objective language
4. Do not add new facts or opinions
5. Keep the same sentence structure where possible

Return ONLY the rewritten text. No explanation, no preamble.

Neutralized version:"""

#Neutralize
def neutralize(context, snippet, technique):
    prompt = build_prompt(context, snippet, technique)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,    # low temp = more consistent, less creative
        max_tokens=512,
    )

    return response.choices[0].message.content.strip()

#Test
# ── TEST ────────────────────────────────────────────────────────
if __name__ == "__main__":
    context   = "The radical left is destroying everything our ancestors built."
    snippet   = "radical left is destroying everything"
    technique = "Loaded_Language"

    print(f"Technique  : {technique}")
    print(f"Original   : {context}")
    print(f"\nNeutralizing...\n")

    result = neutralize(context, snippet, technique)
    print(f"Neutralized: {result}")