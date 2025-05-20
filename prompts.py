# prompts.py

SUMMARIZE_TEXT_PROMPT_TEMPLATE = """
You are an AI assistant skilled at summarizing text.
Please provide a concise summary of the following text. The summary should capture the main points and key information.
Aim for a summary that is approximately {summary_length_preference} of the original text's length, or a few key sentences.

Text to summarize:
---
{text_to_summarize}
---

Concise Summary:
"""

EXTRACT_KEYWORDS_PROMPT_TEMPLATE = """
You are an AI assistant skilled at identifying key topics and keywords from a piece of text.
From the following text, please extract the most important keywords or key phrases.
Provide them as a comma-separated list. Aim for 5-10 key terms.

Text to analyze:
---
{text_to_analyze}
---

Keywords (comma-separated):
""" 