# 🤖 LangGraph Article Writing & Review Agent

An AI-powered article writing and review agent built with **LangGraph, LangChain, Mistral AI, and Tavily**.

The system generates an article, reviews its content, searches the web when additional information is required, and improves the article using the retrieved information.

## 🚀 Key Features

* ✍️ AI-powered article generation
* 🔍 Automated article review
* 🌐 Web search using Tavily
* 🧠 LangGraph-based agent workflow
* 🛠️ LangChain tool integration
* 🔄 Iterative article improvement
* 🔐 Secure API key management using `.env`

## 🛠️ Tech Stack

**Python | LangGraph | LangChain | Mistral AI | Tavily | Python-dotenv**

## 🔄 Workflow

```text
User Request
     ↓
Write Article
     ↓
Review Article
     ↓
Need More Information?
   ↙          ↘
 Yes           No
  ↓             ↓
Tavily Search   Final Output
  ↓
Improve Article
  ↓
Review Again
```

## 📂 Project Structure

```text
LANGGRAPH/
│
├── main.py
├── README.md
├── requirements.txt
├── .gitignore
└── .env
```

> `.env` contains API keys and should never be uploaded to GitHub.

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Gargik283/langgraph-article-agent.git
cd langgraph-article-agent
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API keys

Create a `.env` file:

```env
MISTRALAI_API_KEY=your_mistral_api_key
TAVILY_API_KEY=your_tavily_api_key
```

### 5. Run

```bash
python main.py
```

## 💡 What This Project Demonstrates

* **Agentic AI workflows** using LangGraph
* **LLM integration** with Mistral AI
* **Tool calling** with LangChain
* **Real-time web search** using Tavily
* **State management** with LangGraph
* **Environment-based API security**

## 🎯 Use Case

This project demonstrates how an AI agent can combine **LLM generation, external tools, state management, and iterative reasoning** to create more informed content.

## 👩‍💻 Author

**Gargi Kundu**

Data Science / Data Analytics Fresher

GitHub: https://github.com/Gargik283
