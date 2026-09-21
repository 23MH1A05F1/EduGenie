import os
import json
from app.services.ai_service import generate_answer

async def generate_quiz(topic: str, difficulty: str, count: int):
    api_key = os.getenv("OPENAI_API_KEY", "").strip()

    if api_key:
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=api_key)
            prompt = f"""
Create exactly {count} multiple-choice educational questions about {topic}.
Difficulty: {difficulty}.
Return ONLY valid JSON as an array. Each object must have:
question, options (array of 4 strings), answer (the exact correct option),
explanation.
"""
            response = await client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
            )
            data = json.loads(response.choices[0].message.content)
            if isinstance(data, list) and data:
                return data[:count]
        except Exception:
            pass

    return local_quiz(topic, difficulty, count)


def local_quiz(topic, difficulty, count):
    t = topic.lower()
    banks = {
        "python": [
            ("Which keyword defines a function in Python?",
             ["def", "func", "function", "define"], "def",
             "Python uses the def keyword to define a function."),
            ("Which data type stores True or False?",
             ["str", "bool", "list", "tuple"], "bool",
             "bool represents Boolean values."),
            ("Which symbol starts a Python comment?",
             ["//", "#", "/*", "--"], "#",
             "A single-line Python comment starts with #."),
            ("Which function displays output?",
             ["input()", "display()", "print()", "show()"], "print()",
             "print() writes output to the console."),
            ("Which collection is mutable?",
             ["tuple", "string", "list", "frozenset"], "list",
             "Python lists are mutable.")
        ],
        "sql": [
            ("Which command retrieves data from a table?",
             ["SELECT", "PUSH", "FETCHALL", "GET"], "SELECT",
             "SELECT is used to retrieve rows."),
            ("Which clause filters rows?",
             ["WHERE", "ORDER", "GROUP", "SORT"], "WHERE",
             "WHERE applies row-level conditions."),
            ("Which clause sorts query results?",
             ["ORDER BY", "SORT BY", "ARRANGE", "GROUP BY"], "ORDER BY",
             "ORDER BY sorts returned rows."),
            ("Which SQL operation combines related tables?",
             ["JOIN", "MERGEFILE", "CONNECT", "BIND"], "JOIN",
             "JOIN combines rows from related tables."),
            ("Which command changes existing rows?",
             ["UPDATE", "CHANGE", "ALTERROW", "MODIFY"], "UPDATE",
             "UPDATE changes values in existing rows.")
        ]
    }
    bank = banks.get(t, [
        (f"What is the main purpose of studying {topic}?",
         ["To understand concepts and apply them", "To avoid practice",
          "To memorize without understanding", "None of these"],
         "To understand concepts and apply them",
         "Learning is most useful when concepts can be understood and applied."),
        (f"Which approach is useful when learning {topic}?",
         ["Practice and review", "Never revise", "Skip examples", "Avoid questions"],
         "Practice and review", "Practice reinforces understanding."),
        (f"What should a learner do after making a mistake in {topic}?",
         ["Analyze the mistake", "Ignore it", "Stop learning", "Delete notes"],
         "Analyze the mistake", "Mistakes can identify areas for improvement."),
        (f"How can progress in {topic} be improved?",
         ["Set goals and practice", "Avoid exercises", "Study randomly", "Skip feedback"],
         "Set goals and practice", "Structured practice supports progress."),
        (f"What is a good way to test understanding of {topic}?",
         ["Solve problems or quizzes", "Only reread titles", "Avoid examples", "Do nothing"],
         "Solve problems or quizzes", "Active recall and practice test understanding.")
    ])

    result = []
    for i in range(count):
        q = bank[i % len(bank)]
        result.append({
            "question": q[0],
            "options": q[1],
            "answer": q[2],
            "explanation": q[3]
        })
    return result
