# 🤖 Multi-Agent Debate System

An AI-powered **Multi-Agent Debate System** that simulates a structured debate between multiple specialized AI agents. The agents argue opposing sides, exchange rebuttals, analyze factual claims, critique the debate, and produce a structured final verdict.

The system uses **Anthropic**, **LangGraph**, **FastAPI**, **SQLAlchemy**, **SQLite**, and **Streamlit**, and supports both **text-based and voice-based interaction**. Users can enter a debate topic by typing or speaking, and listen to the generated debate using AI-powered text-to-speech.

---

## 📌 Overview

Instead of asking a single AI model to generate an entire debate, this system separates responsibilities across multiple specialized agents:

- 🟢 **Pro Agent** — argues in favor of the topic
- 🔴 **Con Agent** — argues against the topic
- 🔬 **Research Agent** — analyzes factual claims, assumptions, and evidence requirements
- 🧐 **Critic Agent** — evaluates the quality of arguments and rebuttals
- ⚖️ **Judge Agent** — evaluates the complete debate and produces the final verdict

For a given topic:

1. The Pro Agent argues in favor of the topic.
2. The Con Agent argues against the topic.
3. Both agents exchange rebuttals for the selected number of rounds.
4. The Research Agent analyzes the complete debate.
5. The Critic Agent evaluates both sides.
6. The Judge Agent produces a structured final verdict.
7. The debate is stored in a SQLite database.
8. The Streamlit frontend displays the transcript and analysis.
9. Optional voice input and playback let users speak topics and listen to the debate.

---

## 🎯 Project Objectives

- Build a real-world multi-agent AI system
- Demonstrate agent specialization
- Use LangGraph for agent orchestration
- Implement multi-round AI debates
- Maintain complete debate history
- Perform post-debate research analysis
- Critique arguments and rebuttals
- Generate a structured final verdict
- Store completed debates in a database
- Provide REST APIs using FastAPI
- Build a user interface using Streamlit
- Support both text and voice interaction
- Convert spoken topics into text
- Convert AI-generated responses into speech

---

## 🏗️ System Architecture

```text
                         ┌──────────────────────┐
                         │         USER         │
                         └──────────┬───────────┘
                                    │
                         ┌──────────▼───────────┐
                         │  Streamlit Frontend  │
                         │   Text / Voice Mode  │
                         └──────────┬───────────┘
                                    │ HTTP
                                    ▼
                         ┌──────────────────────┐
                         │    FastAPI Backend   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    Debate Service    │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ LangGraph Orchestrator│
                         └──────────┬───────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
        ┌───────────┐         ┌───────────┐        ┌──────────────┐
        │ Pro Agent │         │ Con Agent │        │Research Agent│
        └─────┬─────┘         └─────┬─────┘        └──────────────┘
              │                     │
              └──────────┬──────────┘
                         ▼
                  ┌─────────────┐
                  │  Rebuttals  │
                  │ Multi-round │
                  └──────┬──────┘
                         │
                         ▼
                  ┌─────────────┐
                  │ Critic Agent│
                  └──────┬──────┘
                         │
                         ▼
                  ┌─────────────┐
                  │ Judge Agent │
                  └──────┬──────┘
                         │
             ┌───────────┴────────────┐
             ▼                        ▼
      ┌──────────────┐        ┌──────────────┐
      │  SQLite DB   │        │ Final Result │
      └──────────────┘        └──────────────┘
```

---

## 🔄 Debate Workflow

For a topic such as:

> Should artificial intelligence be used in education?

the workflow is:

```text
User enters topic
        ↓
Pro Agent generates opening argument
        ↓
Con Agent generates opening argument
        ↓
Pro Agent generates rebuttal
        ↓
Con Agent generates rebuttal
        ↓
Additional rebuttal rounds
        ↓
Research Agent analyzes complete debate
        ↓
Critic Agent evaluates both sides
        ↓
Judge Agent evaluates the debate
        ↓
Structured final verdict
        ↓
Debate saved to SQLite
        ↓
Results displayed in Streamlit
```

---

## 🧠 AI Agents

### 🟢 Pro Agent

Responsible for arguing in favor of the debate topic.

**Responsibilities:**

- Construct a clear opening argument
- Provide logical reasoning
- Give relevant examples
- Anticipate counterarguments
- Respond to the Con Agent during rebuttals
- Defend the Pro position

**Example:**

```text
Topic: Should AI be used in education?

Pro Agent: AI can personalize learning experiences, automate repetitive
tasks, provide immediate feedback, and make educational resources
more accessible.
```

### 🔴 Con Agent

Responsible for arguing against the debate topic.

**Responsibilities:**

- Construct a clear opposing argument
- Identify risks and limitations
- Challenge assumptions
- Provide logical reasoning and counterexamples
- Anticipate counterarguments
- Respond to the Pro Agent during rebuttals

**Example:**

```text
Topic: Should AI be used in education?

Con Agent: Over-reliance on AI may reduce human interaction, introduce
biases, and create privacy and dependency concerns.
```

### 🔬 Research Agent

Analyzes the complete debate rather than taking one side.

**It identifies:**

- Major factual claims
- Claims requiring external evidence
- Unsupported or questionable claims
- Important assumptions
- Factual inconsistencies
- Logical weaknesses
- Whether rebuttals address opposing arguments
- Claims that became stronger or weaker
- Missing evidence

> **Note:** The Research Agent is currently an LLM-based debate analysis agent. It identifies claims that require verification, but the current implementation does not independently retrieve external sources. It does not select a winner.

### 🧐 Critic Agent

Evaluates the quality of the debate.

**It analyzes:**

- Pro opening strengths and weaknesses
- Con opening strengths and weaknesses
- Pro rebuttal quality
- Con rebuttal quality
- Logical issues
- Unsupported assumptions
- Overlooked points
- Effectiveness of responses

The Critic Agent does not act as the final judge.

### ⚖️ Judge Agent

The Judge receives:

```text
Complete Debate History
        +
Research Analysis
        +
Critic Analysis
```

It produces structured JSON:

```json
{
    "winner": "PRO | CON | DRAW",
    "pro_score": 0,
    "con_score": 0,
    "confidence": 0,
    "strongest_pro_argument": "",
    "strongest_con_argument": "",
    "pro_weaknesses": [],
    "con_weaknesses": [],
    "reasoning": "",
    "final_verdict": ""
}
```

This allows the frontend to display a structured final result instead of relying on unstructured text.

**Example output:**

```json
{
    "winner": "PRO",
    "pro_score": 82,
    "con_score": 76,
    "confidence": 0.84,
    "strongest_pro_argument": "AI can provide personalized learning.",
    "strongest_con_argument": "AI introduces privacy and dependency risks.",
    "pro_weaknesses": ["Limited discussion of privacy concerns"],
    "con_weaknesses": ["Limited evidence for some claims"],
    "reasoning": "The Pro side provided stronger overall reasoning...",
    "final_verdict": "The Pro position was stronger based on the arguments presented."
}
```

---

## 🕸️ LangGraph Orchestration

LangGraph controls the complete debate workflow.

```text
START
  │
  ▼
PRO OPENING
  │
  ▼
CON OPENING
  │
  ▼
PRO REBUTTAL
  │
  ▼
CON REBUTTAL
  │
  ▼
Check Round Count
  │
  ├── More rounds ──► PRO REBUTTAL
  │
  └── Finished ─────► RESEARCH
                         │
                         ▼
                       CRITIC
                         │
                         ▼
                       JUDGE
                         │
                         ▼
                        END
```

---


## 📚 Debate History

Every statement is stored in a structured format:

```json
{
    "round": 1,
    "speaker": "PRO",
    "type": "rebuttal",
    "content": "AI can improve personalized learning..."
}
```

This allows the Research, Critic, and Judge agents to analyze the complete conversation instead of only the latest argument.

---

## 🗃️ Database

The project uses **SQLite** with **SQLAlchemy** as the ORM.

Database file: `debates.db`

The `debates` table stores:

| Column | Description |
|---|---|
| `id` | Debate ID |
| `topic` | Debate topic |
| `rounds` | Number of rebuttal rounds |
| `debate_history` | Complete debate history |
| `research_analysis` | Research Agent output |
| `critique` | Critic Agent output |
| `judge_result` | Judge Agent structured result |
| `created_at` | Creation timestamp |

This allows completed debates to be retrieved later through the API.

---

## 🔌 Backend API

The backend is built using **FastAPI**.

Base URL during local development:

```text
http://127.0.0.1:8000
```

### Root

```http
GET /
```

Response:

```json
{
    "message": "Multi-Agent Debate System API",
    "status": "running"
}
```

### Health Check

```http
GET /health
```

Response:

```json
{
    "status": "healthy"
}
```

### Create Debate

```http
POST /api/debate
```

Request:

```json
{
    "topic": "Should artificial intelligence be used in education?",
    "rounds": 1
}
```

Supported rounds: `1`, `2`, `3`, `4`, `5`

### Get Debate List

```http
GET /api/debates
```

Returns stored debate summaries.

### Get Specific Debate

```http
GET /api/debates/{debate_id}
```

Returns the complete stored debate, including topic, number of rounds, debate history, research analysis, critique, and judge result.

### API Documentation

When the backend is running, interactive Swagger documentation is available at:

```text
http://127.0.0.1:8000/docs
```

---

## 🎙️ Voice Features

Voice is an additional option and does **not** replace text functionality.

```text
              Debate Input
                   │
          ┌────────┴────────┐
          │                 │
       📝 Text           🎙️ Voice
          │                 │
          │           Speech-to-Text
          │                 │
          └────────┬────────┘
                   │
                   ▼
              Debate System
                   │
                   ▼
              Text Results
                   │
                   ▼
             Text-to-Speech
                   │
                   ▼
              🔊 Audio
```

### Voice Input

Users can speak their debate topic. The system converts speech into text before sending the topic to the backend. The debate itself still uses the same Pro, Con, Research, Critic, and Judge agents.

```text
Microphone
    ↓
SpeechRecognition
    ↓
Text Topic
    ↓
FastAPI
```

**Technology:** SpeechRecognition, Google Speech Recognition, Streamlit microphone component

### Voice Playback

Generated debate content can be converted to speech for:

- Pro arguments
- Con arguments
- Rebuttals
- Research analysis
- Critic analysis
- Final verdict

```text
AI Generated Text
       ↓
      gTTS
       ↓
   MP3 Audio
       ↓
Streamlit Audio Player
```

**Technology:** gTTS, Streamlit `st.audio()`

The application also provides an **interactive voice presentation** where users can listen to the debate speaker by speaker.

---

## 🖥️ Frontend

The frontend is built using **Streamlit** and supports two modes:

- 📝 **Text Mode**
- 🎙️ **Voice Mode**

Voice Mode includes additional experiences:

- 🎙️ **Voice Debate**
- 🗣️ **Interactive Voice Presentation**

The normal text transcript and analysis remain available regardless of the selected mode.

---

## ⚙️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Anthrophic | Large Language Model |
| LangGraph | Multi-agent orchestration |
| FastAPI | Backend REST API |
| Uvicorn | ASGI server |
| Pydantic | API validation |
| SQLAlchemy | Database ORM |
| SQLite | Database |
| python-dotenv | Environment variable management |
| Streamlit | Frontend UI |
| Requests | Frontend–backend communication |
| SpeechRecognition | Speech-to-text |
| streamlit-mic-recorder | Microphone input |
| gTTS | Text-to-speech |
| Pytest | Testing |

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone <https://github.com/Sanika-Gajarishi/Multi-Agent-Debate-System>
cd Multi-Agent-Debate-System
```

### 2. Backend Setup

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it (Windows):

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configure Anthropic API Key

Create a `.env` file inside the `backend` folder:

```env
ANTHROPIC_API_KEY=your_anthropic_api_key
```


### 4. Frontend Setup

Open a second terminal:

```bash
cd frontend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

---

## ▶️ Running the Backend

From the `backend` directory:

```bash
.venv\Scripts\activate
python -m uvicorn app.main:app --reload
```

- Backend: `http://127.0.0.1:8000`
- Swagger docs: `http://127.0.0.1:8000/docs`

---

## ▶️ Running the Frontend

From the `frontend` directory (in a second terminal):

```bash
streamlit run app.py
```

Streamlit will open in your browser, typically at `http://localhost:8501`.

---

## 🧪 Testing

Run backend tests from the `backend` directory:

```bash
pytest -v
```

Or run a specific folder:

```bash
pytest tests/
```

### Agent Tests

- Pro Agent
- Con Agent
- Research Agent
- Critic Agent
- Judge Agent

### Graph Tests

- Opening arguments
- Rebuttal flow
- Multi-round routing
- Research stage
- Critic stage
- Judge stage

### Service Tests

- Topic validation
- Round validation
- Debate execution
- Database persistence
- Debate retrieval

### API Tests

- `GET /`
- `GET /health`
- `POST /api/debate`
- `GET /api/debates`
- `GET /api/debates/{debate_id}`

### End-to-End Testing

A complete test should verify:

```text
User
 ↓
Streamlit
 ↓
FastAPI
 ↓
DebateService
 ↓
LangGraph
 ↓
All Agents
 ↓
SQLite
 ↓
FastAPI Response
 ↓
Streamlit Results
 ↓
Optional Voice Playback
```

---


## 💡 Why Multi-Agent Architecture?

A single LLM could generate both sides of a debate, but a multi-agent architecture separates responsibilities.

Instead of:

```text
User → Single LLM → Debate
```

this project uses:

```text
                 Debate Topic
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
      Pro Agent               Con Agent
          │                       │
          └───────────┬───────────┘
                      ▼
                Debate Rounds
                      │
                      ▼
               Research Agent
                      │
                      ▼
                Critic Agent
                      │
                      ▼
                 Judge Agent
```

This makes it possible to experiment with agent specialization, state management, orchestration, iterative reasoning, and multi-agent workflows.

---

## 👩‍💻 Author

**Sanika Gajarishi**

---

## 📄 License

This project is created for educational, learning, and portfolio purposes.




