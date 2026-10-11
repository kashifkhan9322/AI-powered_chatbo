"""Explainable retrieval-based intent matching; no paid AI API is required."""
import json
import re
from difflib import SequenceMatcher

TOKEN_RE = re.compile(r"[a-z0-9']+")

def normalize(text):
    return " ".join(TOKEN_RE.findall(text.lower()))

def load_intents(path):
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
    intents = data.get("intents")
    if not isinstance(intents, list) or not intents:
        raise ValueError("intents.json must contain a non-empty 'intents' list")
    for item in intents:
        if not all(k in item for k in ("tag", "patterns", "responses")) or not item["patterns"] or not item["responses"]:
            raise ValueError("Every intent needs a tag, non-empty patterns, and non-empty responses")
    return intents

class ChatbotEngine:
    def __init__(self, intents, threshold=0.52):
        self.intents, self.threshold = intents, threshold

    @staticmethod
    def score(message, pattern):
        a, b = normalize(message), normalize(pattern)
        if not a or not b:
            return 0.0
        if a == b:
            return 1.0
        at, bt = set(a.split()), set(b.split())
        overlap = len(at & bt) / max(1, len(at | bt))
        sequence = SequenceMatcher(None, a, b).ratio()
        return max(0.68 * overlap + 0.32 * sequence, sequence * 0.88)

    def respond(self, message):
        best_score, best_intent = 0.0, None
        for intent in self.intents:
            for pattern in intent["patterns"]:
                score = self.score(message, pattern)
                if score > best_score:
                    best_score, best_intent = score, intent
        if best_intent is None or best_score < self.threshold:
            return {"reply": "I'm not certain I understood that. Try asking about services, pricing, business hours, refunds, or contact support.",
                    "intent": "fallback", "confidence": round(best_score, 3), "matched": False}
        import random
        return {"reply": random.choice(best_intent["responses"]), "intent": best_intent["tag"],
                "confidence": round(best_score, 3), "matched": True}
