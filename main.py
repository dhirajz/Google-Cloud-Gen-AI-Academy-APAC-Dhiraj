

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from contextlib import asynccontextmanager

from google.genai import types
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from ev_customer_agent.agent import root_agent
from ev_company_agent.agent import root_agent as company_root_agent
from ev_company_data_agent.agent import root_agent as company_data_root_agent



ev_customer_name = "ev_customer_agent"
ev_company_name = "ev_company_agent"
ev_company_data_name = "ev_company_data_agent"


# Initialize global services and Runner
session_service = InMemorySessionService()
adk_customer_runner = None
adk_company_runner = None
adk_company_data_runner = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global adk_customer_runner,adk_company_runner,adk_company_data_runner
    print("Initializing ADK Runner...")

    adk_company_runner = Runner(
        agent=company_root_agent,
        app_name=ev_company_name,
        session_service=session_service
    )

    adk_customer_runner = Runner(
        agent=root_agent,
        app_name=ev_customer_name,
        session_service=session_service
    )
    adk_company_data_runner = Runner(
        agent=company_data_root_agent,
        app_name=ev_company_data_name,
        session_service=session_service
    )

    yield

    print("Shutting down ADK Runner...")

app = FastAPI(title="EV Agent API", lifespan=lifespan)

# Request/Response models
class ChatRequest(BaseModel):
    user_id: str
    session_id: str
    prompt: str

class ChatResponse(BaseModel):
    response: str




@app.post("/chat/company/data", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    if not adk_company_data_runner:
        raise HTTPException(status_code=500, detail="adk_company_data_runner is not initialized")

    agent_response = "Sorry, I couldn't generate a response."

    try:
        # ✅ Correct way to fetch session
        session = await session_service.get_session(
            app_name=ev_company_data_name,
            user_id=request.user_id,
            session_id=request.session_id
        )

        # ✅ Create session if it doesn't exist
        if not session:
            session = await session_service.create_session(
                session_id=request.session_id,
                state={},
                app_name=ev_company_data_name,
                user_id=request.user_id
            )

        # ✅ Convert prompt to ADK Content format
        content = types.Content(
            role="user",
            parts=[types.Part(text=request.prompt)]
        )

        # ✅ Correct runner call
        events = adk_company_data_runner.run_async(
            user_id=session.user_id,
            session_id=session.id,
            new_message=content
        )

        # ✅ Extract final response
        async for event in events:
            if event.is_final_response():
                if event.content and event.content.parts:
                    agent_response = event.content.parts[0].text

        return ChatResponse(response=agent_response)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/company", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    if not adk_company_runner:
        raise HTTPException(status_code=500, detail="adk_company_runner is not initialized")

    agent_response = "Sorry, I couldn't generate a response."

    try:
        # ✅ Correct way to fetch session
        session = await session_service.get_session(
            app_name=ev_company_name,
            user_id=request.user_id,
            session_id=request.session_id
        )

        # ✅ Create session if it doesn't exist
        if not session:
            session = await session_service.create_session(
                session_id=request.session_id,
                state={},
                app_name=ev_company_name,
                user_id=request.user_id
            )

        # ✅ Convert prompt to ADK Content format
        content = types.Content(
            role="user",
            parts=[types.Part(text=request.prompt)]
        )

        # ✅ Correct runner call
        events = adk_company_runner.run_async(
            user_id=session.user_id,
            session_id=session.id,
            new_message=content
        )

        # ✅ Extract final response
        async for event in events:
            if event.is_final_response():
                if event.content and event.content.parts:
                    agent_response = event.content.parts[0].text

        return ChatResponse(response=agent_response)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat/cutomer", response_model=ChatResponse)
async def customer_chat_endpoint(request: ChatRequest):
    if not adk_customer_runner:
        raise HTTPException(status_code=500, detail="adk_customer_runner is not initialized")

    agent_response = "Sorry, I couldn't generate a response."

    try:
        # ✅ Correct way to fetch session
        session = await session_service.get_session(
            app_name=ev_customer_name,
            user_id=request.user_id,
            session_id=request.session_id
        )

        # ✅ Create session if it doesn't exist
        if not session:
            session = await session_service.create_session(
                session_id=request.session_id,
                state={},
                app_name=ev_customer_name,
                user_id=request.user_id
            )

        # ✅ Convert prompt to ADK Content format
        content = types.Content(
            role="user",
            parts=[types.Part(text=request.prompt)]
        )

        # ✅ Correct runner call
        events = adk_customer_runner.run_async(
            user_id=session.user_id,
            session_id=session.id,
            new_message=content
        )

        # ✅ Extract final response
        async for event in events:
            if event.is_final_response():
                if event.content and event.content.parts:
                    agent_response = event.content.parts[0].text

        return ChatResponse(response=agent_response)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@app.get("/", response_class=HTMLResponse)
async def root():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Smart EV Multi-Agent System</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; line-height: 1.6; color: #333; background-color: #f9f9f9; }
            .container { max-width: 900px; margin: auto; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
            h1, h2, h3 { color: #2c3e50; }
            h1 { text-align: center; border-bottom: 2px solid #3498db; padding-bottom: 15px; margin-bottom: 10px; }
            .participant { text-align: center; font-style: italic; color: #7f8c8d; margin-bottom: 30px; font-size: 1.1em; }
            .section { margin-bottom: 25px; }
            .highlight { background-color: #e8f4f8; padding: 20px; border-left: 5px solid #3498db; border-radius: 4px; margin-bottom: 10px; }
            pre { background: #282c34; color: #e0e6ed; padding: 15px; border-radius: 6px; overflow-x: auto; font-family: 'Courier New', Courier, monospace; margin-top: 10px; margin-bottom: 0; font-size: 0.9em; box-shadow: inset 0 1px 4px rgba(0,0,0,0.3); }
            .response { background: #f4fdf4; padding: 20px; border-left: 5px solid #2ecc71; border-radius: 4px; margin-bottom: 30px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
            .response pre { background: #1e1e1e; color: #a6e22e; border: none; box-shadow: inset 0 1px 4px rgba(0,0,0,0.5); }
            ul { margin-top: 5px; }
            a { color: #3498db; text-decoration: none; font-weight: bold; }
            a:hover { text-decoration: underline; }
            code { background: #f4f4f4; padding: 2px 5px; border-radius: 3px; color: #c0392b; font-family: 'Courier New', Courier, monospace; font-size: 0.9em; }
            pre code { background: transparent; color: inherit; padding: 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔌 Smart EV Multi-Agent System</h1>
            <div class="participant">Developed by: [Your Name / Team Name Here]</div>
            
            <div class="section">
                <h2>🎯 Problem Statement</h2>
                <p>Develop a Smart EV Multi-Agent System that enhances the electric vehicle ecosystem by solving two critical challenges:</p>
                <ul>
                    <li><strong>Customer Side:</strong> Enable EV users to easily find, book, and navigate to charging stations with real-time availability, cost optimization, and intelligent trip planning.</li>
                    <li><strong>Company Side:</strong> Provide EV operators with advanced analytics, utilization insights, and location intelligence to optimize infrastructure, improve efficiency, and support data-driven expansion decisions.</li>
                </ul>
            </div>

            <div class="highlight">
                <strong>Objective:</strong> Build a scalable, AI-powered solution using multi-agent architecture that combines real-time data, geospatial intelligence, and intelligent decision-making to improve both user experience and business operations in the EV ecosystem.
            </div>

            <div class="section">
                <h2>🧠 Dual-Agent Approach & Technology</h2>
                <p>The platform uses a single API entry point for both the customer and company interfaces, leveraging intelligent routing where queries are classified and handled by specialized agents.</p>
                <ul>
                    <li>🚗 <strong>Customer Agent:</strong> Finds nearby chargers, checks availability, books slots, plans trips with optimized stops, and handles emergency low-battery scenarios.</li>
                    <li>🏢 <strong>Company Agent:</strong> Analyzes station utilization, identifies demand patterns, optimizes operations, and aids in data-driven expansion.</li>
                </ul>
                <p><strong>Tech Stack:</strong> Multi-agent architecture (ADK), LLM-based reasoning (Gemini), and MCP integrations (BigQuery, Maps).</p>
            </div>

            <div class="section">
                <h2>📚 API Documentation</h2>
                <p>Interactive API documentation is generated automatically: <a href="/docs">Swagger UI (/docs)</a> | <a href="/redoc">ReDoc (/redoc)</a></p>
            </div>

            <div class="section">
                <h2>🚀 API Endpoints & Sample Tests</h2>
                
                <h3>1. Customer Agent Endpoint (<code>POST /chat/customer</code>)</h3>
                <p>Handles requests from EV users to find chargers, check availability, and plan trips.</p>
                
                <div class="highlight">
                    <strong>Sample Request (cURL): Local Charger Lookup</strong>
                    <pre><code>curl -X 'POST' 'http://localhost:8000/chat/customer' \\
    -H 'accept: application/json' \\
    -H 'Content-Type: application/json' \\
    -d '{
      "user_id": "user_001",
      "session_id": "session_001",
      "prompt": "Find fast chargers near Mumbai for tonight"
    }'</code></pre>
                </div>
                <div class="response">
                    <strong>Expected JSON Output:</strong>
                    <pre><code>{
  "response": "✅ VoltEdge Mumbai Central (ElectroGo) is available in Mumbai with 3 slots at price ₹25 for the 18:00-24:00 time period."
}</code></pre>
                </div>

                <div class="highlight">
                    <strong>Sample Request (cURL): Trip Planning</strong>
                    <pre><code>curl -X 'POST' 'http://localhost:8000/chat/customer' \\
    -H 'accept: application/json' \\
    -H 'Content-Type: application/json' \\
    -d '{
      "user_id": "user_002",
      "session_id": "session_002",
      "prompt": "Plan my Mumbai to Pune trip with charging stops"
    }'</code></pre>
                </div>
                <div class="response">
                    <strong>Expected JSON Output:</strong>
                    <pre><code>{
  "response": "Route: Mumbai to Pune (150 km, ETA: 3 hrs). Suggested charging stop: ChargeZone Khalapur (Fast Charger, 4 slots available)."
}</code></pre>
                </div>

                <h3>2. Company Agent Endpoint (<code>POST /chat/company</code>)</h3>
                <p>Handles requests from EV operators for analytics, utilization insights, and internal data.</p>
                
                <div class="highlight">
                    <strong>Sample Request (cURL): Utilization Insights</strong>
                    <pre><code>curl -X 'POST' 'http://localhost:8000/chat/company' \\
    -H 'accept: application/json' \\
    -H 'Content-Type: application/json' \\
    -d '{
      "user_id": "admin_001",
      "session_id": "session_admin_001",
      "prompt": "What is the utilization of our charging stations in Mumbai?"
    }'</code></pre>
                </div>
                <div class="response">
                    <strong>Expected JSON Output:</strong>
                    <pre><code>{
  "response": "Based on the latest BigQuery analytics, Mumbai stations are currently running at 85% utilization during peak hours."
}</code></pre>
                </div>

                <h3>3. Health Check (<code>/health</code>)</h3>
                <div class="highlight">
                    <strong>Sample Request (cURL)</strong>
                    <pre><code>curl -X 'GET' 'http://localhost:8000/health'</code></pre>
                </div>
                <div class="response">
                    <strong>Expected JSON Output:</strong>
                    <pre><code>{
  "status": "healthy"
}</code></pre>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)




@app.get("/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
