from flask import current_app
from openai import OpenAI


class AIService:
    def __init__(self):
        api_key = current_app.config["OPENAI_API_KEY"]
        self.model = current_app.config["OPENAI_MODEL"]
        self.client = OpenAI(api_key=api_key) if api_key else None

    def answer_bible_question(self, question):
        system_prompt = (
            "You are a pastoral AI church assistant. Answer Bible questions with "
            "warmth, humility, and scriptural grounding. Avoid claiming certainty "
            "where traditions differ, and encourage users to speak with church leaders "
            "for sensitive pastoral care."
        )
        return self._complete(system_prompt, question, fallback=self._fallback_bible_answer(question))

    def generate_sermon(self, topic, scripture=None, mode="outline"):
        scripture_line = f"Primary scripture: {scripture}" if scripture else "Suggest fitting scripture references."
        if mode == "full":
            user_prompt = (
                f"Write a complete sermon on '{topic}'. {scripture_line} Include title, "
                "introduction, 3-5 main points, illustrations, application, and closing prayer."
            )
        else:
            user_prompt = (
                f"Create a sermon outline on '{topic}'. {scripture_line} Include title, "
                "theme, key texts, main points, illustrations, and practical applications."
            )
        system_prompt = "You help pastors prepare biblically faithful, practical sermon material."
        return self._complete(system_prompt, user_prompt, fallback=self._fallback_sermon(topic, scripture, mode))

    def _complete(self, system_prompt, user_prompt, fallback):
        if not self.client:
            return fallback

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()

    def _fallback_bible_answer(self, question):
        return (
            "AI provider is not configured yet. Once OPENAI_API_KEY is set, this question "
            f"will receive a full pastoral response: {question}"
        )

    def _fallback_sermon(self, topic, scripture, mode):
        text_type = "Full sermon" if mode == "full" else "Sermon outline"
        passage = scripture or "Select a primary passage during preparation"
        return (
            f"{text_type}: {topic}\n\n"
            f"Scripture: {passage}\n"
            "1. Introduce the need and biblical theme.\n"
            "2. Explain the passage in context.\n"
            "3. Apply the truth to family, work, community, and discipleship.\n"
            "4. Invite prayerful response and practical obedience."
        )
