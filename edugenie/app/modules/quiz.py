from app.ai.gemini import gemini_service
from app.ai.prompts import QUIZ


def _demo_quiz(text: str) -> list[dict]:
    return [
        {
            "question": "What is the main purpose of studying the supplied passage?",
            "options": [
                "Understand the key ideas",
                "Ignore the main ideas",
                "Remove all examples",
                "Avoid asking questions",
            ],
            "answer": "Understand the key ideas",
        },
        {
            "question": "Which approach best supports learning from a passage?",
            "options": [
                "Read and practice",
                "Skip the content",
                "Memorize random words",
                "Avoid review",
            ],
            "answer": "Read and practice",
        },
        {
            "question": "What should a good quiz question have?",
            "options": [
                "One clearly correct answer",
                "No options",
                "Only unrelated choices",
                "Multiple identical answers",
            ],
            "answer": "One clearly correct answer",
        },
        {
            "question": "What can practice questions help a student do?",
            "options": [
                "Check understanding",
                "Delete knowledge",
                "Guarantee a grade",
                "Replace all learning",
            ],
            "answer": "Check understanding",
        },
        {
            "question": "What should a learner do after finding an incorrect answer?",
            "options": [
                "Review the concept",
                "Ignore it forever",
                "Delete the notes",
                "Stop learning",
            ],
            "answer": "Review the concept",
        },
    ]


def _validate_questions(data) -> list[dict]:
    if not isinstance(data, list):
        raise ValueError("Quiz response must be a JSON array.")

    questions = []
    for item in data[:5]:
        if not isinstance(item, dict):
            continue
        question = str(item.get("question", "")).strip()
        options = item.get("options", [])
        answer = str(item.get("answer", "")).strip()
        if (
            question
            and isinstance(options, list)
            and len(options) == 4
            and all(str(x).strip() for x in options)
            and answer in [str(x).strip() for x in options]
        ):
            questions.append(
                {
                    "question": question,
                    "options": [str(x).strip() for x in options],
                    "answer": answer,
                }
            )

    if len(questions) < 3:
        raise ValueError("Model did not return enough valid quiz questions.")
    return questions


def generate_quiz(text: str) -> list[dict]:
    if not gemini_service.available:
        return _demo_quiz(text)

    raw = gemini_service.generate(QUIZ.format(text=text))
    data = gemini_service.extract_json(raw)
    return _validate_questions(data)
