import os
from app.services.ai_service import generate_answer

async def summarize_text(text: str):
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if api_key:
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=api_key)
            response = await client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[{
                    "role": "user",
                    "content": (
                        "Summarize the following educational material. "
                        "Return sections: Short Summary, Key Points, Important Terms.\n\n"
                        + text
                    )
                }],
                temperature=0.2,
            )
            return response.choices[0].message.content
        except Exception:
            pass

    sentences = [s.strip() for s in text.replace("\n", " ").split(".") if s.strip()]
    selected = sentences[:5]
    bullets = "\n".join(f"• {s}." for s in selected)
    return f"SHORT SUMMARY\n{bullets}\n\nKEY POINTS\n• Review the main ideas in the text.\n• Identify important terms and definitions.\n• Use active recall and practice questions to test understanding."
