from app.config import settings


class AIService:
    """
    Optional LLM-powered message personalization.
    Falls back to template rendering if OPENAI_API_KEY is not set.
    """

    def __init__(self):
        self.enabled = bool(settings.OPENAI_API_KEY)

    async def personalize(
        self,
        template_body: str,
        recipient_context: dict,
    ) -> str:
        """
        Given a message template and recipient context (name, bio, recent post, etc.),
        returns a personalized version of the message.
        """
        if not self.enabled:
            # Plain variable substitution fallback
            body = template_body
            for k, v in recipient_context.items():
                body = body.replace(f"{{{{{k}}}}}", str(v))
            return body

        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

        system_prompt = (
            "You are a social media copywriter. Rewrite the given DM message template "
            "to feel warm, personal, and natural using the recipient context provided. "
            "Keep it concise (max 200 chars). Return ONLY the message text."
        )
        user_prompt = (
            f"Template: {template_body}\n"
            f"Recipient context: {recipient_context}\n"
            "Personalized message:"
        )

        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_prompt},
            ],
            max_tokens=150,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()

    async def classify_reply(self, reply_text: str) -> str:
        """
        Classify an incoming reply as: interested | not_interested | question | other
        Useful for prioritizing follow-up actions.
        """
        if not self.enabled:
            return "other"

        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "user",
                "content": (
                    f"Classify this DM reply into one of: interested, not_interested, question, other.\n"
                    f"Reply: \"{reply_text}\"\nRespond with only the category."
                ),
            }],
            max_tokens=10,
        )
        return response.choices[0].message.content.strip().lower()
