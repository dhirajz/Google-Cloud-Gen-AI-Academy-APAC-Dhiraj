# Google-Cloud-Gen-AI-Academy-APAC-Dhiraj Amin
Here’s a **complete, clean, professional `README.md`** for your project 👇

---

# 🔌 Smart EV Multi-Agent System

An **AI-powered EV ecosystem platform** that enhances both **user experience** and **infrastructure efficiency** using a **multi-agent architecture**.

The system provides intelligent solutions for:

* 🚗 EV users (charger discovery, trip planning)
* 🏢 EV operators (analytics, demand insights, expansion planning)

---

## 🚀 Features

### 🚗 Customer Features

* Smart charger discovery with real-time availability
* Slot booking and cost optimization
* AI-based trip planning with optimized charging stops
* Emergency low-battery assistance
* Navigation using Maps integration

### 🏢 Company Features

* Station utilization analytics
* Demand pattern and peak hour insights
* Location intelligence for expansion
* Revenue and performance analysis
* Data-driven recommendations

### ⚙️ Platform Capabilities

* Multi-agent intelligent workflows
* Parallel + sequential execution
* BigQuery + Maps integration (via MCP)
* Efficient database operations (querying, aggregation, analytics)
* Scalable, real-time architecture

---

## 🏗️ Architecture

The system uses a **dual-API + multi-agent architecture**:

* `/chat/customer` → Handles EV user queries
* `/chat/company` → Handles operator analytics

### Key Components

* **FastAPI Backend** (deployed on Cloud Run)
* **Google ADK** for multi-agent orchestration
* **Gemini LLM** for reasoning and decision-making
* **MCP Integration** for tool access

### Agent Design

#### Customer Agents

* Root Agent
* Router Agent
* Sequential Pipeline

  * EV Solver Agent
  * EV Presenter Agent
* Parallel Pipeline

  * Route Agent
  * Charger Agent
  * Synthesizer Agent

#### Company Agent

* LLM Root Agent

  * BigQuery MCP Tool (analytics)
  * Maps MCP Tool (geospatial insights)

---

## 🔄 Workflow

### Customer Flow

User → API → Router Agent →

* Sequential Flow (Charger Search)
* Parallel Flow (Trip Planning)

### Company Flow

User → API → LLM Agent → BigQuery + Maps → Insights

---

## ☁️ Technologies Used

### Core Stack

* Google ADK (Agent Development Kit)
* Gemini LLM
* FastAPI

### Google Cloud

* Cloud Run (deployment)
* BigQuery (analytics)
* Google Maps MCP (routing & location intelligence)
* Firestore / In-memory sessions

### System Design

* Multi-Agent Architecture
* MCP (Model Context Protocol)
* Parallel & Sequential Workflows

---

## 📡 API Endpoints

### Customer API

```
POST /chat/customer
```

**Example Request**

```json
{
  "user_id": "user_001",
  "session_id": "session_001",
  "prompt": "Find fast chargers near Mumbai for tonight"
}
```

---

### Company API

```
POST /chat/company
```

**Example Request**

```json
{
  "user_id": "admin_001",
  "session_id": "session_admin_001",
  "prompt": "What is the utilization of charging stations in Mumbai?"
}
```

---

### Health Check

```
GET /health
```

---

## ▶️ Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
python main.py
```

Server will run at:

```
http://localhost:8000
```

---

## 📊 Example Use Cases

### Customer

* Find nearby chargers
* Plan EV trips with charging stops
* Handle low battery scenarios

### Company

* Analyze station utilization
* Identify high-demand locations
* Optimize infrastructure expansion

---

## ⚡ USP

* Dual-agent system (Customer + Company)
* Multi-agent intelligent workflows
* Real-time data + geospatial intelligence
* End-to-end EV ecosystem optimization

---

## 👨‍💻 Contributors

* Dhiraj Amin

---

## 📄 License

MIT License

---
