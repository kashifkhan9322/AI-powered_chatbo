import os
import unittest
from app import app
from chatbot import ChatbotEngine, load_intents

ROOT = os.path.dirname(os.path.dirname(__file__))

class ChatbotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = ChatbotEngine(load_intents(os.path.join(ROOT, "intents.json")))

    def test_exact_greeting(self):
        result = self.engine.respond("hello")
        self.assertTrue(result["matched"])
        self.assertEqual(result["intent"], "greeting")

    def test_greeting_variation(self):
        result = self.engine.respond("Hi there")
        self.assertEqual(result["intent"], "greeting")

    def test_pricing(self):
        self.assertEqual(self.engine.respond("How much do you charge?")["intent"], "pricing")

    def test_business_hours(self):
        self.assertEqual(self.engine.respond("What time do you close?")["intent"], "business_hours")

    def test_unknown_question_fallback(self):
        result = self.engine.respond("Explain quantum chromodynamics")
        self.assertFalse(result["matched"])
        self.assertEqual(result["intent"], "fallback")

    def test_health_endpoint(self):
        response = app.test_client().get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "ok")

    def test_chat_api_success(self):
        response = app.test_client().post("/api/chat", json={"message": "hello"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["intent"], "greeting")

    def test_empty_message(self):
        self.assertEqual(app.test_client().post("/api/chat", json={"message": " "}).status_code, 400)

    def test_non_json_request(self):
        response = app.test_client().post("/api/chat", data="bad", content_type="text/plain")
        self.assertEqual(response.status_code, 400)

    def test_long_message(self):
        self.assertEqual(app.test_client().post("/api/chat", json={"message": "x"*1001}).status_code, 413)

    def test_suggestions(self):
        data = app.test_client().get("/api/intents").get_json()
        self.assertGreater(len(data["suggestions"]), 0)

if __name__ == "__main__":
    unittest.main(verbosity=2)
