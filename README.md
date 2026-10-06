# Malini Voice 🎙️🏡
### Real-Time Voice Concierge & Booking Assistant for Malini Homes

An AI-powered, real-time voice concierge for **Malini Homes** — a premium government-registered homestay brand in Guwahati, Assam.

Guests talk over a live audio stream to **Malini Voice**, which:
- Answers property queries, amenities, tariffs, and room availability using RAG over PDF knowledge documents.
- Covers all 3 properties:
  - **Unit 1: Silpukhuri** (Central City Hub — Hummingbird Magic, Butterfly Effect rooms, or Full 2BHK)
  - **Unit 2: Zoo Road** (Upscale Urban Retreat — Serene Deluxe, Serene Delight, or Full 2BHK)
  - **Unit 3: Bhangagarh** (Healing Sanctuary near GMCH/hospitals — home-cooked Assamese meals & pet-friendly)
- Computes accurate quotes in Indian Rupees (₹).
- Provides Guwahati city guidance (Kamakhya Temple, Brahmaputra river cruises, ropeway, Sualkuchi, Pobitora).
- Collects booking inquiries and logs `MALINI-XXXXX` reservation tickets.
- Connects guests to human hosts via WhatsApp or direct escalation.

Built with **LiveKit Agents**, **LangChain + Groq**, **Docling**, and **Qdrant**.

---

## 🚀 Getting Started

### Prerequisites

- Python `>= 3.12`
- [LiveKit Cloud](https://livekit.io/) credentials (`LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`)
- [Groq](https://console.groq.com/keys) API Key (`GROQ_API_KEY`)

### Quick Setup

```bash
# 1. Activate virtual environment
source .venv/bin/activate  # or: uv sync

# 2. Configure credentials in .env
# LIVEKIT_URL=wss://your-project.livekit.cloud
# LIVEKIT_API_KEY=...
# LIVEKIT_API_SECRET=...
# GROQ_API_KEY=...

# 3. (Already done) Ingest knowledge documents into Qdrant
python ingest.py

# 4. Start Malini Voice in console mode
python -m voice_agent.main console
```

---

## 🗣️ Example Voice Prompts

| What You Say | What Malini Voice Does |
|---|---|
| *"What properties do you have in Guwahati?"* | Explains Silpukhuri, Zoo Road, and Bhangagarh with key highlights. |
| *"How much is the 2BHK in Silpukhuri for 3 nights?"* | Calls `calculate_stay_quote` and returns exact pricing in ₹. |
| *"Are pets allowed at any of your properties?"* | Uses RAG to explain pet-friendly policy at Bhangagarh (Unit 3). |
| *"How far is Kamakhya Temple from your homestay?"* | Pulls distances & tips from the Guwahati travel guide PDF. |
| *"I want to book Silpukhuri for next weekend. My number is 9876543210."* | Calls `create_booking_inquiry` and generates a `MALINI-xxxxx` ticket. |

---

## 📂 Project Architecture

- `docs/`: Auto-generated official knowledge base PDFs:
  - `malini-properties-and-pricing.pdf`
  - `malini-booking-policies-and-faq.pdf`
  - `malini-guwahati-guide-and-experiences.pdf`
- `generate_malini_pdfs.py`: Script that compiles website data into PDF format.
- `ingest.py`: Parses PDFs with **Docling**, embeds with `all-MiniLM-L6-v2`, and stores in **Qdrant**.
- `langchain_agent/`:
  - `rag.py`: Qdrant vector retrieval and Groq LLM synthesis.
  - `tools.py`: Domain tools (availability, stay quote calculator, inquiry generator, escalation) and system prompt.
- `voice_agent/`:
  - `main.py`: LiveKit voice pipeline with Deepgram STT, Inworld TTS, and speech-only token filtering.
