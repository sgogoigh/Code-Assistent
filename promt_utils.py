# prompt_utils.py
import json
from typing import Tuple

def build_review_prompt(code: str, filename: str | None = None, language: str | None = None) -> str:
    """
    Returns a prompt asking Gemini to return a JSON object with specific keys.
    Keep the instruction explicit to maximize structured JSON output.
    """
    meta = {
        "filename": filename or "",
        "language": language or ""
    }

    prompt = f"""
You are an expert senior software engineer and code reviewer.
Analyze the provided source code for:

1. Readability
2. Modularity / structure
3. Potential bugs or security issues
4. Performance concerns (if applicable)
5. Testability
6. Specific, actionable suggestions and prioritized fixes

Return your answer ONLY as a VALID JSON OBJECT (no surrounding explanation). The object must have these keys:
- summary: short (1-2 sentences)
- readability: list of observations (strings)
- modularity: list of observations (strings)
- potential_bugs: list of observations (strings)
- suggestions: list of objects with keys { "line": string_or_null, "severity": "low|medium|high", "suggestion": string }
- confidence: short explanation of any uncertainty

Also include an optional key "raw_notes" for any free-form commentary.

If you are unable to produce JSON, return {"error": "explain reason"}.

Here is context metadata (do not make this part of the analysis text):
{json.dumps(meta)}

Now analyze the code below (do not hallucinate extra files):

---CODE START---
{code}
---CODE END---
"""
    return prompt
