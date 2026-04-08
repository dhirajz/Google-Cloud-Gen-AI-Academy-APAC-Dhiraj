from google.adk.agents import Agent, LlmAgent, SequentialAgent, ParallelAgent
from google.adk.tools import FunctionTool

Model = "gemini-2.5-flash"  # Balanced model for routing decisions

# -----------------------------
# 1️⃣ Dataset
# -----------------------------
CHARGERSEV = [
    {"id": 1, "name": "VoltEdge Mumbai Central", "company": "ElectroGo", "location": "Mumbai", "type": "Fast", "price": 25, "availability": {"00:00-06:00": 3,"06:00-09:00": 1,"09:00-12:00": 2,"12:00-15:00": 2,"15:00-18:00": 2,"18:00-21:00": 1,"21:00-24:00": 3}},
    {"id": 2, "name": "ChargeHub Andheri", "company": "GreenCharge", "location": "Mumbai", "type": "Slow", "price": 15, "availability": {"00:00-06:00": 5,"06:00-09:00": 3,"09:00-12:00": 4,"12:00-15:00": 4,"15:00-18:00": 4,"18:00-21:00": 3,"21:00-24:00": 5}},
    {"id": 3, "name": "EcoBoost Charger Bandra", "company": "EcoVolt", "location": "Mumbai", "type": "Fast", "price": 22, "availability": {"00:00-06:00": 2,"06:00-09:00": 1,"09:00-12:00": 2,"12:00-15:00": 2,"15:00-18:00": 1,"18:00-21:00": 1,"21:00-24:00": 2}},
    {"id": 4, "name": "RapidVolt Thane West", "company": "ElectroGo", "location": "Thane", "type": "Fast", "price": 23, "availability": {"00:00-06:00": 2,"06:00-09:00": 1,"09:00-12:00": 2,"12:00-15:00": 2,"15:00-18:00": 2,"18:00-21:00": 1,"21:00-24:00": 2}},
    {"id": 5, "name": "PowerNest Navi Mumbai", "company": "ChargePoint", "location": "Navi Mumbai", "type": "Slow", "price": 14, "availability": {"00:00-06:00": 4,"06:00-09:00": 3,"09:00-12:00": 4,"12:00-15:00": 4,"15:00-18:00": 3,"18:00-21:00": 2,"21:00-24:00": 4}},
    {"id": 6, "name": "VoltEdge Kalyan", "company": "GreenCharge", "location": "Kalyan", "type": "Fast", "price": 20, "availability": {"00:00-06:00": 2,"06:00-09:00": 1,"09:00-12:00": 2,"12:00-15:00": 2,"15:00-18:00": 1,"18:00-21:00": 1,"21:00-24:00": 2}},
    {"id": 7, "name": "ChargeHub Dadar", "company": "EcoVolt", "location": "Mumbai", "type": "Slow", "price": 12, "availability": {"00:00-06:00": 5,"06:00-09:00": 3,"09:00-12:00": 4,"12:00-15:00": 4,"15:00-18:00": 3,"18:00-21:00": 2,"21:00-24:00": 5}},
    {"id": 8, "name": "EcoBoost Charger Borivali", "company": "ChargePoint", "location": "Mumbai", "type": "Fast", "price": 24, "availability": {"00:00-06:00": 3,"06:00-09:00": 1,"09:00-12:00": 2,"12:00-15:00": 2,"15:00-18:00": 2,"18:00-21:00": 1,"21:00-24:00": 3}},
    {"id": 9, "name": "RapidVolt Pimpri", "company": "ElectroGo", "location": "Pimpri-Chinchwad", "type": "Fast", "price": 21, "availability": {"00:00-06:00": 2,"06:00-09:00": 1,"09:00-12:00": 2,"12:00-15:00": 2,"15:00-18:00": 1,"18:00-21:00": 1,"21:00-24:00": 2}},
    {"id": 10, "name": "PowerNest Pune Central", "company": "GreenCharge", "location": "Pune", "type": "Slow", "price": 16, "availability": {"00:00-06:00": 4,"06:00-09:00": 3,"09:00-12:00": 4,"12:00-15:00": 4,"15:00-18:00": 3,"18:00-21:00": 2,"21:00-24:00": 4}},
    {"id": 11, "name": "VoltEdge Lonavala", "company": "EcoVolt", "location": "Lonavala", "type": "Fast", "price": 26, "availability": {"00:00-06:00": 2,"06:00-09:00": 1,"09:00-12:00": 2,"12:00-15:00": 2,"15:00-18:00": 1,"18:00-21:00": 1,"21:00-24:00": 2}},
    {"id": 12, "name": "ChargeHub Hinjewadi", "company": "ChargePoint", "location": "Pune", "type": "Fast", "price": 23, "availability": {"00:00-06:00": 3,"06:00-09:00": 1,"09:00-12:00": 2,"12:00-15:00": 2,"15:00-18:00": 2,"18:00-21:00": 1,"21:00-24:00": 3}},
    {"id": 13, "name": "EcoBoost Charger Kharghar", "company": "ElectroGo", "location": "Navi Mumbai", "type": "Slow", "price": 15, "availability": {"00:00-06:00": 4,"06:00-09:00": 3,"09:00-12:00": 4,"12:00-15:00": 4,"15:00-18:00": 3,"18:00-21:00": 2,"21:00-24:00": 4}},
    {"id": 14, "name": "RapidVolt Thane East", "company": "GreenCharge", "location": "Thane", "type": "Fast", "price": 22, "availability": {"00:00-06:00": 2,"06:00-09:00": 1,"09:00-12:00": 2,"12:00-15:00": 2,"15:00-18:00": 1,"18:00-21:00": 1,"21:00-24:00": 2}},
    {"id": 15, "name": "PowerNest Aundh", "company": "EcoVolt", "location": "Pune", "type": "Slow", "price": 14, "availability": {"00:00-06:00": 4,"06:00-09:00": 3,"09:00-12:00": 4,"12:00-15:00": 4,"15:00-18:00": 3,"18:00-21:00": 2,"21:00-24:00": 4}},
    {"id": 16, "name": "VoltEdge Navi Mumbai", "company": "ChargePoint", "location": "Navi Mumbai", "type": "Fast", "price": 25, "availability": {"00:00-06:00": 3,"06:00-09:00": 1,"09:00-12:00": 2,"12:00-15:00": 2,"15:00-18:00": 2,"18:00-21:00": 1,"21:00-24:00": 3}},
    {"id": 17, "name": "ChargeHub Mulund", "company": "ElectroGo", "location": "Mumbai", "type": "Slow", "price": 13, "availability": {"00:00-06:00": 5,"06:00-09:00": 3,"09:00-12:00": 4,"12:00-15:00": 4,"15:00-18:00": 3,"18:00-21:00": 2,"21:00-24:00": 5}},
    {"id": 18, "name": "EcoBoost Charger Vashi", "company": "GreenCharge", "location": "Navi Mumbai", "type": "Fast", "price": 22, "availability": {"00:00-06:00": 3,"06:00-09:00": 1,"09:00-12:00": 2,"12:00-15:00": 2,"15:00-18:00": 2,"18:00-21:00": 1,"21:00-24:00": 3}},
    {"id": 19, "name": "RapidVolt Thane West", "company": "EcoVolt", "location": "Thane", "type": "Fast", "price": 21, "availability": {"00:00-06:00": 2,"06:00-09:00": 1,"09:00-12:00": 2,"12:00-15:00": 2,"15:00-18:00": 1,"18:00-21:00": 1,"21:00-24:00": 2}},
    {"id": 20, "name": "PowerNest Pimpri-Chinchwad", "company": "ChargePoint", "location": "Pimpri-Chinchwad", "type": "Slow", "price": 16, "availability": {"00:00-06:00": 4,"06:00-09:00": 3,"09:00-12:00": 4,"12:00-15:00": 4,"15:00-18:00": 3,"18:00-21:00": 2,"21:00-24:00": 4}},
    {"id": 21, "name": "VoltEdge Kothrud", "company": "ElectroGo", "location": "Pune", "type": "Fast", "price": 23, "availability": {"00:00-06:00": 3,"06:00-09:00": 1,"09:00-12:00": 2,"12:00-15:00": 2,"15:00-18:00": 2,"18:00-21:00": 1,"21:00-24:00": 3}},
    {"id": 22, "name": "ChargeHub Vile Parle", "company": "GreenCharge", "location": "Mumbai", "type": "Slow", "price": 14, "availability": {"00:00-06:00": 5,"06:00-09:00": 3,"09:00-12:00": 4,"12:00-15:00": 4,"15:00-18:00": 3,"18:00-21:00": 2,"21:00-24:00": 5}},
    {"id": 23, "name": "EcoBoost Panvel", "company": "EcoVolt", "location": "Navi Mumbai", "type": "Fast", "price": 24, "availability": {"00:00-06:00": 2,"06:00-09:00": 1,"09:00-12:00": 1,"12:00-15:00": 1,"15:00-18:00": 1,"18:00-21:00": 1,"21:00-24:00": 2}},
    {"id": 24, "name": "RapidVolt Chembur", "company": "ElectroGo", "location": "Mumbai", "type": "Fast", "price": 22, "availability": {"00:00-06:00": 3,"06:00-09:00": 2,"09:00-12:00": 2,"12:00-15:00": 1,"15:00-18:00": 2,"18:00-21:00": 1,"21:00-24:00": 3}},
    {"id": 25, "name": "PowerNest Worli", "company": "ChargePoint", "location": "Mumbai", "type": "Slow", "price": 13, "availability": {"00:00-06:00": 4,"06:00-09:00": 4,"09:00-12:00": 3,"12:00-15:00": 3,"15:00-18:00": 4,"18:00-21:00": 2,"21:00-24:00": 4}},
    {"id": 26, "name": "VoltEdge Baner", "company": "GreenCharge", "location": "Pune", "type": "Fast", "price": 21, "availability": {"00:00-06:00": 2,"06:00-09:00": 1,"09:00-12:00": 2,"12:00-15:00": 2,"15:00-18:00": 1,"18:00-21:00": 1,"21:00-24:00": 2}},
    {"id": 27, "name": "ChargeHub Airoli", "company": "EcoVolt", "location": "Navi Mumbai", "type": "Slow", "price": 11, "availability": {"00:00-06:00": 6,"06:00-09:00": 4,"09:00-12:00": 4,"12:00-15:00": 4,"15:00-18:00": 4,"18:00-21:00": 3,"21:00-24:00": 6}},
    {"id": 28, "name": "EcoBoost Kandivali", "company": "ChargePoint", "location": "Mumbai", "type": "Fast", "price": 23, "availability": {"00:00-06:00": 3,"06:00-09:00": 1,"09:00-12:00": 2,"12:00-15:00": 1,"15:00-18:00": 2,"18:00-21:00": 1,"21:00-24:00": 3}},
    {"id": 29, "name": "RapidVolt Wakad", "company": "ElectroGo", "location": "Pune", "type": "Fast", "price": 22, "availability": {"00:00-06:00": 2,"06:00-09:00": 1,"09:00-12:00": 2,"12:00-15:00": 2,"15:00-18:00": 1,"18:00-21:00": 1,"21:00-24:00": 2}},
    {"id": 30, "name": "PowerNest Dombivli", "company": "GreenCharge", "location": "Kalyan", "type": "Slow", "price": 12, "availability": {"00:00-06:00": 5,"06:00-09:00": 3,"09:00-12:00": 4,"12:00-15:00": 4,"15:00-18:00": 3,"18:00-21:00": 2,"21:00-24:00": 5}},
    {"id": 31, "name": "VoltEdge Santacruz", "company": "EcoVolt", "location": "Mumbai", "type": "Fast", "price": 25, "availability": {"00:00-06:00": 2,"06:00-09:00": 1,"09:00-12:00": 2,"12:00-15:00": 1,"15:00-18:00": 1,"18:00-21:00": 1,"21:00-24:00": 2}},
    {"id": 32, "name": "ChargeHub Hadapsar", "company": "ChargePoint", "location": "Pune", "type": "Slow", "price": 14, "availability": {"00:00-06:00": 4,"06:00-09:00": 3,"09:00-12:00": 4,"12:00-15:00": 4,"15:00-18:00": 3,"18:00-21:00": 2,"21:00-24:00": 4}},
    {"id": 33, "name": "EcoBoost Belapur", "company": "ElectroGo", "location": "Navi Mumbai", "type": "Fast", "price": 23, "availability": {"00:00-06:00": 3,"06:00-09:00": 1,"09:00-12:00": 2,"12:00-15:00": 2,"15:00-18:00": 2,"18:00-21:00": 1,"21:00-24:00": 3}},
    {"id": 34, "name": "RapidVolt Mira Road", "company": "GreenCharge", "location": "Thane", "type": "Fast", "price": 20, "availability": {"00:00-06:00": 2,"06:00-09:00": 1,"09:00-12:00": 1,"12:00-15:00": 2,"15:00-18:00": 1,"18:00-21:00": 1,"21:00-24:00": 2}},
    {"id": 35, "name": "PowerNest Viman Nagar", "company": "EcoVolt", "location": "Pune", "type": "Slow", "price": 15, "availability": {"00:00-06:00": 4,"06:00-09:00": 3,"09:00-12:00": 4,"12:00-15:00": 4,"15:00-18:00": 3,"18:00-21:00": 2,"21:00-24:00": 4}},
    {"id": 36, "name": "VoltEdge Ghodbunder", "company": "ChargePoint", "location": "Thane", "type": "Fast", "price": 24, "availability": {"00:00-06:00": 3,"06:00-09:00": 2,"09:00-12:00": 2,"12:00-15:00": 2,"15:00-18:00": 2,"18:00-21:00": 1,"21:00-24:00": 3}},
    {"id": 37, "name": "ChargeHub Malad", "company": "ElectroGo", "location": "Mumbai", "type": "Slow", "price": 12, "availability": {"00:00-06:00": 5,"06:00-09:00": 4,"09:00-12:00": 4,"12:00-15:00": 4,"15:00-18:00": 3,"18:00-21:00": 2,"21:00-24:00": 5}},
    {"id": 38, "name": "EcoBoost Pashan", "company": "GreenCharge", "location": "Pune", "type": "Fast", "price": 22, "availability": {"00:00-06:00": 3,"06:00-09:00": 1,"09:00-12:00": 2,"12:00-15:00": 2,"15:00-18:00": 2,"18:00-21:00": 1,"21:00-24:00": 3}},
    {"id": 39, "name": "RapidVolt Seawoods", "company": "EcoVolt", "location": "Navi Mumbai", "type": "Fast", "price": 23, "availability": {"00:00-06:00": 2,"06:00-09:00": 1,"09:00-12:00": 2,"12:00-15:00": 2,"15:00-18:00": 1,"18:00-21:00": 1,"21:00-24:00": 2}},
    {"id": 40, "name": "PowerNest Kalwa", "company": "ChargePoint", "location": "Thane", "type": "Slow", "price": 13, "availability": {"00:00-06:00": 4,"06:00-09:00": 3,"09:00-12:00": 4,"12:00-15:00": 4,"15:00-18:00": 3,"18:00-21:00": 2,"21:00-24:00": 4}},
    {"id": 41, "name": "VoltEdge Chakan", "company": "ElectroGo", "location": "Pune", "type": "Fast", "price": 20, "availability": {"00:00-06:00": 3,"06:00-09:00": 1,"09:00-12:00": 2,"12:00-15:00": 2,"15:00-18:00": 2,"18:00-21:00": 1,"21:00-24:00": 3}},
    {"id": 42, "name": "ChargeHub Ghatkopar", "company": "GreenCharge", "location": "Mumbai", "type": "Slow", "price": 14, "availability": {"00:00-06:00": 5,"06:00-09:00": 3,"09:00-12:00": 4,"12:00-15:00": 4,"15:00-18:00": 3,"18:00-21:00": 2,"21:00-24:00": 5}},
    {"id": 43, "name": "EcoBoost Karve Nagar", "company": "EcoVolt", "location": "Pune", "type": "Fast", "price": 21, "availability": {"00:00-06:00": 2,"06:00-09:00": 1,"09:00-12:00": 1,"12:00-15:00": 1,"15:00-18:00": 1,"18:00-21:00": 1,"21:00-24:00": 2}},
    {"id": 44, "name": "RapidVolt Ulhasnagar", "company": "ElectroGo", "location": "Kalyan", "type": "Fast", "price": 19, "availability": {"00:00-06:00": 3,"06:00-09:00": 2,"09:00-12:00": 2,"12:00-15:00": 2,"15:00-18:00": 2,"18:00-21:00": 1,"21:00-24:00": 3}},
    {"id": 45, "name": "PowerNest Nerul", "company": "ChargePoint", "location": "Navi Mumbai", "type": "Slow", "price": 12, "availability": {"00:00-06:00": 4,"06:00-09:00": 4,"09:00-12:00": 4,"12:00-15:00": 4,"15:00-18:00": 3,"18:00-21:00": 2,"21:00-24:00": 4}},
    {"id": 46, "name": "VoltEdge Shivaji Nagar", "company": "GreenCharge", "location": "Pune", "type": "Fast", "price": 24, "availability": {"00:00-06:00": 2,"06:00-09:00": 1,"09:00-12:00": 2,"12:00-15:00": 2,"15:00-18:00": 1,"18:00-21:00": 1,"21:00-24:00": 2}},
    {"id": 47, "name": "ChargeHub Byculla", "company": "EcoVolt", "location": "Mumbai", "type": "Slow", "price": 13, "availability": {"00:00-06:00": 5,"06:00-09:00": 3,"09:00-12:00": 4,"12:00-15:00": 4,"15:00-18:00": 4,"18:00-21:00": 3,"21:00-24:00": 5}},
    {"id": 48, "name": "EcoBoost Sanpada", "company": "ChargePoint", "location": "Navi Mumbai", "type": "Fast", "price": 22, "availability": {"00:00-06:00": 3,"06:00-09:00": 1,"09:00-12:00": 2,"12:00-15:00": 1,"15:00-18:00": 2,"18:00-21:00": 1,"21:00-24:00": 3}},
    {"id": 49, "name": "RapidVolt Bibwewadi", "company": "ElectroGo", "location": "Pune", "type": "Fast", "price": 21, "availability": {"00:00-06:00": 2,"06:00-09:00": 1,"09:00-12:00": 2,"12:00-15:00": 2,"15:00-18:00": 1,"18:00-21:00": 1,"21:00-24:00": 2}},
    {"id": 50, "name": "PowerNest Kanjurmarg", "company": "GreenCharge", "location": "Mumbai", "type": "Slow", "price": 14, "availability": {"00:00-06:00": 4,"06:00-09:00": 3,"09:00-12:00": 4,"12:00-15:00": 4,"15:00-18:00": 3,"18:00-21:00": 2,"21:00-24:00": 4}}
]

# -----------------------------
# 2️⃣ Tools
# -----------------------------
def dataset_tool(prompt: str):
    """Return the full charger dataset as string for LLM reasoning."""
    return str(CHARGERSEV)

dataset_function_tool = FunctionTool(dataset_tool)

# -----------------------------
# 3️⃣ Sub-Agents
# -----------------------------

# Step 1: EV Solver Agent
ev_solver_agent = LlmAgent(
    name="EVSolverAgent",
    model=Model,
    instruction=(
        "Parse the user's query for location, charger type (Fast/Slow), and time period. "
        "Time can be exact (09:00-12:00) or natural (morning, afternoon, evening, night, late night). "
        "Default time is 00:00-24:00 if unspecified. "
        "Check the CHARGERSEV dataset provided by the tool, compute available slots, and rank by slots → price. "
        "Return up to 3 top chargers as JSON with fields: "
        "name, company, location, type, price, available_slots, time_period. "
        "Handle edge cases (no matches, missing info, overlapping time)."
    ),
    tools=[dataset_function_tool],
    output_key="charger_results"
)

# Step 2: EV Presenter Agent
ev_presenter_agent = LlmAgent(
    name="EVPresenterAgent",
    model=Model,
    instruction=(
        "Receive 'charger_results' JSON from the solver agent. "
        "Format it into a polite, readable message using bullet points. "
        "Include name, company, location, type, price, available slots, and time period. "
        "If the list is empty, politely inform the user that no chargers match their query. "
        "Do not add or remove chargers."
    ),
    tools=[],
    output_key="formatted_message"
)

# -----------------------------
# 4️⃣ Sequential Agent
# -----------------------------
EVSequentialPipeline = SequentialAgent(
    name="EVSequentialPipeline",
    sub_agents=[ev_solver_agent, ev_presenter_agent],  # List style works in ADK v1
    description="First solve the EV query, then format the results for the user."
)

# -----------------------------
# 1️⃣ Dataset (Mumbai ↔ Pune)
# -----------------------------
ROUTES = [
    {
        "origin": "Mumbai",
        "destination": "Pune",
        "distance_km": 150,
        "eta_hr": 3,
        "traffic": "Heavy",
        "route_name": "Mumbai–Pune Expressway"
    }
]

CHARGERS = [
    {
        "name": "ChargeZone Khalapur",
        "location": "Khalapur (Expressway Midpoint)",
        "type": "Fast",
        "slots": 4,
        "amenities": ["Food Court", "Restrooms"]
    },
    {
        "name": "Tata Power Charging Lonavala",
        "location": "Lonavala",
        "type": "Fast",
        "slots": 3,
        "amenities": ["Cafe", "Parking"]
    },
    {
        "name": "Statiq Pune City",
        "location": "Pune",
        "type": "Slow",
        "slots": 6,
        "amenities": ["Mall", "Restrooms"]
    },
    {
        "name": "EVRE Charging Hub Panvel",
        "location": "Panvel",
        "type": "Fast",
        "slots": 2,
        "amenities": ["Parking"]
    }
]
import json
# -----------------------------
# 2️⃣ Tools (ONLY DATA PROVIDERS)
# -----------------------------
def route_dataset_tool(prompt: str):
    """Return all route data."""
    return str(ROUTES)

def charger_dataset_tool(prompt: str):
    """Return all charger data."""
    return str(CHARGERS)

route_tool = FunctionTool(route_dataset_tool)
charger_tool = FunctionTool(charger_dataset_tool)

# -----------------------------
# 3️⃣ Sub-Agents (LLM DOES LOGIC)
# -----------------------------

# Route Agent
route_agent = LlmAgent(
    name="RouteAgent",
    model=Model,
    instruction=(
        "Extract origin and destination from user query. "
        "Use the route dataset tool to find the best matching route. "
        "Return selected route as JSON with: origin, destination, distance_km, eta_hr, traffic."
    ),
    tools=[route_tool],
    output_key="route_data"
)

# Charger Agent
charger_agent = LlmAgent(
    name="ChargerAgent",
    model=Model,
    instruction=(
        "Analyze the route_data and user query. "
        "Use charger dataset tool to find relevant charging stations along the route. "
        "Prefer fast chargers with higher availability. "
        "Return top 2 chargers as JSON list with: name, location, type, slots."
    ),
    tools=[charger_tool],
    output_key="charger_info"
)

# Synthesizer Agent (LLM reasoning step)
synth_agent = LlmAgent(
    name="TripSynthesizerAgent",
    model=Model,
    instruction=(
        "You are an EV trip planner.\n"
        "Input:\n"
        "- route_data\n"
        "- charger_info\n"
        "- user battery level\n\n"
        "Task:\n"
        "1. Estimate when charging is needed based on distance and battery.\n"
        "2. Insert optimal charging stops.\n"
        "3. Create a human-friendly itinerary.\n\n"
        "Output:\n"
        "A clear travel plan with route summary and charging stops."
    ),
    tools=[],
    output_key="final_plan"
)

# -----------------------------
# 4️⃣ Parallel Layer (Fan-Out)
# -----------------------------
parallel_layer = ParallelAgent(
    name="RouteChargerParallel",
    sub_agents=[route_agent, charger_agent]
)

# -----------------------------
# 5️⃣ Sequential Pipeline (Fan-In)
# -----------------------------
EVTripPipeline = SequentialAgent(
    name="EVTripPipeline",
    sub_agents=[parallel_layer, synth_agent],
    description="Fetch route + chargers in parallel, then synthesize plan"
)


# -----------------------------
# Router Agent for EV Queries (with examples)
# -----------------------------
router_agent = LlmAgent(
    name="EVRouterAgent",
    model=Model,
    instruction="""
You are an intelligent EV query router.

Task:
1. Analyze the user query deeply.
2. Determine if the user wants:
   - A local EV charger lookup (within a city) → delegate to EVSequentialPipeline
   - A trip planning query (route, distance, charging stops, multi-city) → delegate to EVTripPipeline

Guidelines:
- Look for hints like city names, charger type, time, or 'near me' for local queries.
- Look for multi-city, route, distance, ETA, battery, or travel itinerary hints for trip queries.
- If ambiguous, prefer asking the user for clarification.
- Respond with JSON containing a single field:
    {"delegate_agent": "<agent_name>"}
  where <agent_name> is either "EVSequentialPipeline" or "EVTripPipeline".

Examples:
1. "Find fast chargers near Mumbai for tonight" → EVSequentialPipeline
2. "Show me slow chargers in Thane tomorrow afternoon" → EVSequentialPipeline
3. "Where can I charge my EV around Navi Mumbai this evening?" → EVSequentialPipeline
4. "Plan my Mumbai to Pune trip with charging stops" → EVTripPipeline
5. "I need an itinerary from Bangalore to Chennai including EV chargers" → EVTripPipeline
6. "What are the available chargers along the Mumbai–Pune Expressway?" → EVTripPipeline
7. "Find all fast chargers near Bandra and Andheri" → EVSequentialPipeline
8. "Estimate ETA and charging points for a trip from Mumbai to Goa" → EVTripPipeline
9. "List chargers with parking and amenities in Thane" → EVSequentialPipeline
10. "Create a travel plan from Pune to Nashik with stops for charging and lunch" → EVTripPipeline
"""
    ,
    sub_agents=[EVSequentialPipeline, EVTripPipeline],  # local sequential, trip planning sequential
    output_key="selected_agent"
)

# Root Agent
root_agent = LlmAgent(
    name="Root",
    model=Model,  # entry point can use a balanced model
    instruction="""
You are the main entry assistant.

Delegate all requests to the Router agent.
""",
    sub_agents=[router_agent]
)
