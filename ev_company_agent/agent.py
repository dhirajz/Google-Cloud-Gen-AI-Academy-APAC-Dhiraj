
import os
import dotenv
from ev_company_agent import tools
from google.adk.agents import LlmAgent

dotenv.load_dotenv()

PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT', 'project_not_set')

maps_toolset = tools.get_maps_mcp_toolset()
bigquery_toolset = tools.get_bigquery_mcp_toolset()



root_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='root_agent',
    instruction=f"""
                Help the user answer questions by combining insights from two sources:

                1. **BigQuery toolset:** 
                   Access EV charging analytics data from the `ev_charging` dataset ONLY.
                   This includes:
                   - charging_stations (station info, charger types, operators)
                   - charging_sessions (energy usage, session duration, cost)
                   - station_utilization (utilization %, peak hours)

                   Use this data to:
                   - Analyze station performance
                   - Identify high-demand locations
                   - Calculate revenue in Indian Rupees and usage trends
                   - Compare charger types and efficiency

                   IMPORTANT:
                   - Do NOT use any dataset other than `ev_charging`
                   - Run all queries using project id: {PROJECT_ID}

                2. **Maps Toolset:**
                   Use this for real-world EV infrastructure insights:
                   - Find nearby charging stations
                   - Analyze competitor networks (e.g., ChargePoint, EVgo)
                   - Evaluate geographic coverage and accessibility
                   - Calculate routes and distances for EV users

                   Include a hyperlink to an interactive map when relevant.


                Your goal:
                Provide actionable insights for EV users, operators, or planners by combining data analytics with real-world location intelligence.
            """,
    tools=[maps_toolset, bigquery_toolset]
)
