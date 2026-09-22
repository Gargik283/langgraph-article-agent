# 🤖 LangGraph Article Writing & Review Agent

A practical **AI-powered article writing and review agent** built with **LangGraph, LangChain, Mistral AI, and Tavily**.

This project demonstrates how to build a stateful AI workflow where an LLM can:

1. ✍️ Generate an article based on a user's request.
2. 🔍 Review the generated article.
3. 🌐 Search the Internet when additional information is required.
4. 🧠 Use the retrieved information to improve the article.
5. 🔄 Continue the workflow through a LangGraph state-based architecture.

---

## 📌 Project Overview

This project uses **LangGraph** to create a structured AI workflow instead of making a single LLM API call.

The workflow consists of three main nodes:

* **Write Article** — Generates the initial article using Mistral AI.
* **Review Article** — Reviews the generated article and determines whether additional information is needed.
* **Internet Search** — Uses Tavily to retrieve information from the Internet when requested by the AI.

The retrieved information is then passed back into the article-writing stage.

### Workflow

```text
                    ┌─────────────────────┐
                    │       START         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Write Article     │
                    │    Mistral AI       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Review Article    │
                    │  Mistral + Tools    │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
              Tool required?          No tool
                    │                     │
                   Yes                    ▼
                    │                   END
                    ▼
          ┌─────────────────────┐
          │   Internet Search   │
          │       Tavily        │
          └──────────┬──────────┘
                     │
                     ▼
          ┌─────────────────────┐
          │   Write Article     │
          │   with new info     │
          └──────────┬──────────┘
                     │
                     ▼
                Review Again
```

---

## ✨ Features

* 🤖 AI-powered article generation
* 📝 Automated article review
* 🌐 Internet search using Tavily
* 🔗 LangGraph state-based workflow
* 🛠️ LangChain tool integration
* 🔄 Conditional workflow routing
* 🧠 Tool calling with Mistral AI
* 💬 Structured message handling
* 🔐 Environment-variable based API-key management
* 🐍 Built entirely with Python

---

## 🧰 Technologies Used

| Technology        | Purpose                             |
| ----------------- | ----------------------------------- |
| Python            | Programming language                |
| LangGraph         | Agent workflow and state management |
| LangChain         | LLM and tool integration            |
| Mistral AI        | Large Language Model                |
| Tavily            | Internet search                     |
| python-dotenv     | Environment variable management     |
| typing-extensions | Typed state definition              |

---

## 📂 Project Structure

```text
LANGGRAPH/
│
├── main.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── venv/
│   └── ...
│
└── .env
```

### Important

The following files/folders should **not** be uploaded to GitHub:

```text
.env
venv/
__pycache__/
```

Your `.gitignore` file should prevent them from being committed.

---

## ⚙️ How the Project Works

### 1. User Input

The workflow starts with a user request such as:

```text
Write an article about the benefits of meditation.
```

The request is stored inside the LangGraph state.

---

### 2. Write Article Node

The `write_article_node` sends the messages stored in the state to the Mistral AI model.

```python
def write_article_node(state: State):
    response = model.invoke(state["messages"])

    return {"messages": [response]}
```

Mistral generates the initial article.

---

### 3. Review Article Node

The generated article is then passed to the review node.

The reviewer is instructed to:

* Review the article.
* Provide feedback.
* Use the Internet search tool if additional information is required.

The project uses a tool-enabled Mistral model:

```python
model_with_tools = model.bind_tools(tools)
```

---

### 4. Conditional Decision

LangGraph checks whether the model requested a tool.

```python
def decide_internet_search(state: State):
    last_message = state["messages"][-1]
    
    if last_message.tool_calls:
        return "internet_search"
    else:
        return END
```

If the model does not request a tool:

```text
Review → END
```

If the model requests Internet information:

```text
Review → Internet Search
```

---

### 5. Internet Search

The project uses Tavily to search the Internet.

```python
client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
response = client.search(query)
```

The result is returned to LangGraph as a `ToolMessage`.

This allows the LLM to associate the search result with the corresponding tool call.

---

### 6. Article Improvement

After receiving the Internet information, the workflow returns to:

```text
Internet Search
       ↓
Write Article
```

The article-writing node can then use the additional information to generate an improved response.

---

## 🧠 LangGraph State

The project uses a typed state:

```python
class State(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
```

The `messages` list stores the conversation and tool interactions throughout the workflow.

`operator.add` allows messages generated by different nodes to be accumulated in the graph state.

---

## 🔧 Tool Used in the Project

The project defines an Internet-search tool using LangChain's `@tool` decorator:

```python
@tool
def get_information(query: str) -> str:
    """Use this tool for information from the Internet"""
```

The tool is then bound to the Mistral model:

```python
model_with_tools = model.bind_tools(tools)
```

This enables the model to decide when it needs external information.

---

# 🚀 Getting Started

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
```

Move into the project directory:

```bash
cd LANGGRAPH
```

---

## 2. Create a Virtual Environment

### Windows

```bash
py -m venv venv
```

Activate the virtual environment:

```bash
venv\Scripts\activate
```

---

## 3. Install Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

---

## 4. Configure API Keys

Create a `.env` file in the project root:

```text
MISTRALAI_API_KEY=your_mistral_api_key
TAVILY_API_KEY=your_tavily_api_key
```

The application loads these variables using:

```python
load_dotenv()
```

### 🔐 Security

**Never upload your `.env` file to GitHub.**

Never place your actual API keys directly inside `main.py`.

Use:

```python
os.getenv("MISTRALAI_API_KEY")
```

and:

```python
os.getenv("TAVILY_API_KEY")
```

instead.

---

## 5. Run the Application

After activating the virtual environment:

```bash
python main.py
```

The LangGraph workflow will execute and generate the article.

---

# 📦 requirements.txt

A basic `requirements.txt` for this project can contain:

```text
langgraph
langchain
langchain-core
langchain-mistralai
tavily-python
python-dotenv
typing-extensions
```

Install everything with:

```bash
pip install -r requirements.txt
```

---

# 🛡️ .gitignore

Create a `.gitignore` file containing:

```gitignore
venv/
.env
__pycache__/
*.pyc
```

This prevents your virtual environment, environment variables, and Python cache files from being uploaded.

---

# 🧪 Example

### Input

```text
Write an article about the benefits of meditation.
```

### Workflow

```text
User Request
     ↓
Write Article
     ↓
Review Article
     ↓
Does the reviewer need more information?
     ↓
   Yes ──────────────→ Tavily Internet Search
                           ↓
                    Retrieved Information
                           ↓
                      Write Article
                           ↓
                     Review Article
                           ↓
                          END
```

---

# 📚 Key Concepts Demonstrated

This project was created to practice several important concepts in modern AI application development.

### LangGraph

Used to create a structured, stateful workflow consisting of multiple nodes and conditional transitions.

### LLM Tool Calling

Mistral can determine when external information is required and request the appropriate tool.

### Tool Integration

Tavily is integrated as an Internet-search tool through LangChain.

### State Management

LangGraph maintains the messages exchanged between the different nodes.

### Conditional Routing

The workflow dynamically determines whether to:

```text
END
```

or:

```text
INTERNET SEARCH
```

based on the model's tool calls.

### Environment Variables

API credentials are loaded securely from `.env` rather than being hard-coded.

---

# 🎯 Learning Objectives

Through this project, the following concepts are demonstrated:

* Understanding LangGraph fundamentals
* Creating a `StateGraph`
* Defining graph states
* Creating LangGraph nodes
* Creating graph edges
* Creating conditional edges
* Working with `START` and `END`
* Integrating Mistral AI with LangChain
* Binding tools to an LLM
* Handling tool calls
* Working with `ToolMessage`
* Integrating Tavily
* Managing API keys with environment variables
* Building an agentic AI workflow

---

# 🔮 Future Improvements

Possible improvements for future versions include:

* [ ] Add a Streamlit user interface
* [ ] Add article length controls
* [ ] Add different writing styles
* [ ] Add source citations to generated articles
* [ ] Add article fact-checking
* [ ] Add multiple Internet-search tools
* [ ] Add persistent conversation memory
* [ ] Add human approval before publishing
* [ ] Add LangGraph checkpoints
* [ ] Add error handling and retries
* [ ] Add logging and monitoring
* [ ] Deploy the application as a web application

---

# ⚠️ Important Notes

This project requires valid API credentials for:

* Mistral AI
* Tavily

API availability, rate limits, model availability, and usage restrictions are controlled by the respective service providers.

If an API returns an error such as a rate-limit response, the issue may be related to the external API rather than the LangGraph workflow itself.

---

# 🔐 API Key Safety

Never commit API keys to GitHub.

Do **not** upload:

```text
.env
```

If an API key is accidentally exposed publicly, revoke or rotate the key immediately.

---

# 👩‍💻 Author

**Gargi Kundu**

Data Science & Analytics | Python | SQL | Power BI | Machine Learning | Generative AI

GitHub:
https://github.com/Gargik283

---

# ⭐ Acknowledgements

This project uses the following technologies and services:

* LangGraph
* LangChain
* Mistral AI
* Tavily
* Python

---

# 📄 License

This project is available for educational and portfolio purposes.

If you reuse or modify the project, please provide appropriate attribution to the original repository.

---

## ⭐ If You Find This Project Useful

If this project helped you understand LangGraph, LLM tool calling, or agentic workflows, consider giving the repository a ⭐ on GitHub.
