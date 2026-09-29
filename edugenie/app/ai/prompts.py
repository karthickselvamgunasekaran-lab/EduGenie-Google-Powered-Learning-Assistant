SYSTEM = """You are EduGenie, a patient educational AI tutor.
Use clear language appropriate for a student. Be accurate, concise, and structured.
Do not invent citations or claim to have browsed the web unless browsing was actually performed.
When a topic is ambiguous, state the assumption briefly.
"""

EXPLANATION = """Explain the topic below in simple, clear language for a school student.
Use a short definition, an intuitive explanation, and one everyday example when useful.
Topic: {topic}
"""

QNA = """Answer the student's question clearly.
Give the direct answer first, then a brief explanation.
Question: {question}
"""

SUMMARY = """Summarize the following passage in simple language.
Keep the important ideas and remove repetition.
Return a short paragraph followed by 3 bullet points when the source is long.
Passage:
{text}
"""

LEARNING = """Create an adaptive learning path for the requested topic.
Organize it as Beginner, Intermediate, and Advanced where appropriate.
For each level include key topics, a sensible learning order, practice ideas, and resource types.
Do not invent specific URLs.
Topic: {topic}
"""

QUIZ = """Create exactly 5 multiple-choice questions from the passage.
Each question must have exactly 4 distinct options and exactly one correct answer.
Return ONLY valid JSON with this shape:
[
  {{
    "question": "string",
    "options": ["string", "string", "string", "string"],
    "answer": "string"
  }}
]
The answer must exactly equal one of the four options.
Passage:
{text}
"""
