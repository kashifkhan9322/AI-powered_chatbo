# Architecture

```mermaid
flowchart TD
 A[Website visitor] --> B[Chat widget: HTML/CSS/JS]
 B -->|POST JSON| C[Flask API]
 C --> D[Validate message]
 D --> E[Normalize text]
 E --> F[Compare with intents.json patterns]
 F --> G{Score above threshold?}
 G -->|Yes| H[Return approved intent answer]
 G -->|No| I[Return fallback]
 H --> J[Render response as text]
 I --> J
```

## Components
- Browser widget: sends messages to the API and uses `textContent` to display returned text.
- Flask API: serves the page and provides `/api/chat`, `/api/intents`, and `/health`.
- Chatbot engine: normalizes input and scores predefined patterns using token overlap and string similarity.
- `intents.json`: curated patterns and responses.
- Tests: cover matching and API input validation.

The current design is low-cost and explainable. Its scores are heuristics, not probabilities. Chat history is not stored server-side by default.
