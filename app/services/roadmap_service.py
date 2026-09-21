import os, json

async def generate_roadmap(topic: str, level: str, weeks: int):
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if api_key:
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=api_key)
            prompt = f"""
Create a {weeks}-week learning roadmap for {topic}.
Learner level: {level}.
Return ONLY valid JSON array with exactly {weeks} objects.
Each object: week, title, topics (array), practice, milestone.
"""
            response = await client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
            )
            data = json.loads(response.choices[0].message.content)
            if isinstance(data, list):
                return data[:weeks]
        except Exception:
            pass

    if topic.lower() == "sql":
        topics = [
            ("Database Fundamentals", ["Databases", "Tables", "Rows and columns"], "Create a sample database."),
            ("SELECT Basics", ["SELECT", "WHERE", "ORDER BY"], "Write 10 SELECT queries."),
            ("Functions and Aggregation", ["COUNT", "SUM", "AVG", "GROUP BY"], "Analyze a small dataset."),
            ("Joins", ["INNER JOIN", "LEFT JOIN", "Relationships"], "Combine two related tables."),
            ("Advanced SQL", ["Subqueries", "Views", "Indexes"], "Optimize sample queries."),
            ("Project", ["Schema design", "CRUD", "Reporting"], "Build a mini student database.")
        ]
    else:
        topics = [
            ("Fundamentals", [f"{topic} basics", "Terminology", "Core concepts"], "Write a one-page summary."),
            ("Core Concepts", [f"{topic} concepts", "Examples", "Common patterns"], "Solve 10 practice questions."),
            ("Practice", ["Guided exercises", "Debugging", "Case studies"], "Complete a mini exercise."),
            ("Intermediate", ["Intermediate concepts", "Best practices"], "Build a small practical task."),
            ("Advanced", ["Advanced concepts", "Optimization", "Real-world use"], "Analyze a real-world case."),
            ("Project", ["Project planning", "Implementation", "Review"], f"Build a mini {topic} project.")
        ]

    return [
        {"week": i+1, "title": topics[i % len(topics)][0],
         "topics": topics[i % len(topics)][1],
         "practice": topics[i % len(topics)][2],
         "milestone": "Review notes and test your understanding."}
        for i in range(weeks)
    ]
