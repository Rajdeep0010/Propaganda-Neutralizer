# Propaganda Neutralizer

Propaganda Neutralizer is an AI-powered tool that detects propaganda techniques in text and rewrites them into neutral, objective language while preserving the original meaning.

## Features

* Detects 19 propaganda techniques
* Rewrites biased or manipulative text into neutral language
* Evaluates rewrite quality using AI
* Simple and interactive Streamlit interface

## Tech Stack

* Python
* PyTorch
* Hugging Face Transformers
* Groq API (Llama 3.1 8B)
* Streamlit

## How It Works

1. **Detect** propaganda techniques using a fine-tuned Transformer model.
2. **Neutralize** the detected rhetoric using an LLM.
3. **Evaluate** the rewritten text for factual preservation, rhetoric removal, and fluency.

## Run Locally

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key
```

Start the application:

```bash
streamlit run app.py
```

## Example

**Original:**

> The radical left is destroying everything our ancestors built.

**Neutralized:**

> Some critics argue that certain left-wing policies conflict with traditional values.

