import os
from dotenv import load_dotenv

load_dotenv()

# Optional cloud provider support.
# If OPENAI_API_KEY is not configured, EduGenie automatically uses
# a deterministic local educational engine so the project still runs.
async def generate_answer(question: str, mode: str = "simple") -> str:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()

    if api_key:
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=api_key)
            system = (
                "You are EduGenie, a helpful educational assistant. "
                "Explain concepts accurately and safely for students. "
                "Use simple language, examples, and bullet points when useful. "
                f"Answer in {mode} mode."
            )
            response = await client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": question}
                ],
                temperature=0.3,
            )
            return response.choices[0].message.content
        except Exception:
            pass

    return local_answer(question, mode)


def local_answer(question: str, mode: str) -> str:
    q = question.lower().strip()

    known = {
        "largest ocean": (
            "The Pacific Ocean is the largest ocean on Earth. "
            "It covers more area than any other ocean and stretches "
            "between Asia/Australia and North and South America."
        ),
        "python": (
            "Python is a high-level, general-purpose programming language. "
            "It is popular for web development, automation, data science, "
            "artificial intelligence, and scripting. Example: print('Hello')."
        ),
        "photosynthesis": (
            "Photosynthesis is the process by which green plants use sunlight, "
            "water, and carbon dioxide to produce glucose and oxygen. "
            "It mainly occurs in chloroplasts using chlorophyll."
        ),
        "pithagoras": (
            "The Pythagorean theorem relates the sides of a right triangle: "
            "the square of the hypotenuse equals the sum of the squares of "
            "the other two sides. It is commonly written as a² + b² = c²."
        ),
        "pythagoras": (
            "The Pythagorean theorem relates the sides of a right triangle: "
            "the square of the hypotenuse equals the sum of the squares of "
            "the other two sides. It is commonly written as a² + b² = c²."
        ),
        "sql": (
            "SQL stands for Structured Query Language. It is used to create, "
            "read, update, and delete data in relational databases. Start with "
            "SELECT, WHERE, ORDER BY, GROUP BY, JOIN, subqueries, and indexing."
        ),
        "operating system": (
            "An operating system is system software that manages computer "
            "hardware and provides services to applications. Examples include "
            "Windows, Linux, macOS, Android, and iOS."
        ),
        "machine learning": (
            "Machine learning is a branch of AI in which algorithms learn "
            "patterns from data to make predictions or decisions without "
            "being explicitly programmed for every case."
        ),
    }

    for key, value in known.items():
        if key in q:
            return value

    return (
        "EduGenie local mode is active. I can provide educational help, but "
        "this lightweight offline engine has a limited knowledge base. "
        "For broader generative answers, add OPENAI_API_KEY to the .env file "
        "and restart the server.\n\n"
        f"Your question: {question}\n\n"
        "Try asking about Python, SQL, photosynthesis, Pythagoras theorem, "
        "machine learning, operating systems, or the largest ocean."
    )
