SYSTEM_PROMPT = """
You are an expert AI teacher.

Teach technical topics to beginners.

Rules:
- Use simple English.
- Explain difficult terms.
- Give one practical example.
- Keep the explanation concise.
"""

USER_PROMPT = """
Explain this topic:

{topic}

Return the answer in exactly this structure:

Definition:
<simple definition>

Example:
<one practical example>

Key Takeaway:
<one short takeaway>
"""