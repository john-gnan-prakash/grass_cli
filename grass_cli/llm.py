import json
import requests
from typing import Dict, Any

OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5-coder:14b"  # <-- Updated to include the exact tag

SYSTEM_PROMPT = """You are an offline outdoor trail planner AI.
Your job is to generate outdoor itineraries based on user queries.
You MUST respond STRICTLY in raw JSON matching the requested schema.
Do not include any intro, outtro, or markdown codeblocks like ```json.
"""

TRAIL_SCHEMA = """
{
  "trail_name": "String",
  "summary": "String",
  "difficulty": "Easy | Moderate | Hard",
  "estimated_duration_mins": Integer,
  "distance_km": Float,
  "elevation_gain_m": Integer,
  "waypoints": [
    {
      "step": Integer,
      "name": "String",
      "type": "start | water_stop | scenic_view | end",
      "description": "String",
      "latitude": Float,
      "longitude": Float
    }
  ],
  "packing_list": ["String"]
}
"""

def generate_trail_plan(user_query: str) -> Dict[str, Any]:
    prompt = f"""
{SYSTEM_PROMPT}

JSON Schema to follow:
{TRAIL_SCHEMA}

User Request: "{user_query}"

Generate a realistic trail plan matching the request. Provide approximate coordinates (lat/lon) near reasonable default hiking areas.
Output raw JSON only:
"""

    try:
        response = requests.post(
            OLLAMA_ENDPOINT,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "format": "json",
                "stream": False,
                "options": {
                    "temperature": 0.2  # Low temperature for strict schema adherence
                }
            },
            timeout=360
        )
        response.raise_for_status()
        
        result_text = response.json().get("response", "")
        return json.loads(result_text)

    except requests.exceptions.ConnectionError:
        raise RuntimeError("Could not connect to Ollama. Make sure Ollama is running locally on port 11434.")
    except json.JSONDecodeError:
        raise ValueError(f"Model failed to output valid JSON. Raw output was:\n{result_text}")