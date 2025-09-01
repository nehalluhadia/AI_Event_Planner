import os
import json
from openai import OpenAI
from typing import Dict, List

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

def _fallback_ideas(event_type: str, guests: int, budget: str, location: str) -> Dict[str, List[str]]:
    # Safe fallback for community events
    return {
        "Themes": [
            "Outdoor Movie Night",
            "Cultural Food Fair",
            "Neighborhood BBQ"
        ],
        "Food": [
            "Potluck-style shared dishes",
            "Local vendor stalls",
            "Snacks and lemonade stand"
        ],
        "Activities": [
            "Kids’ games and relay races",
            "Open mic or talent show",
            "Community raffle and cleanup crew"
        ],
    }

def generate_event_ideas(event_type: str, guests: int, budget: str, location: str) -> Dict[str, List[str]]:
    """
    Returns a dict:
    {
      "Themes": [.. up to 6],
      "Food":   [.. up to 6],
      "Activities": [.. up to 6]
    }
    """
    try:
        client = OpenAI()
        system = (
            "You are a neighborhood event planning assistant. "
            "Respond ONLY as strict JSON with keys: Themes, Food, Activities. "
            "Each value must be an array of 3-6 short, practical ideas. "
            "Keep suggestions family-friendly, inclusive, and affordable. "
            "Encourage collaboration (potlucks, cultural sharing, talent shows, cleanup drives). "
            "No prose, no markdown, no extra keys."
        )
        user = (
            f"Event type: {event_type}\n"
            f"Expected neighbors: {guests}\n"
            f"Budget: {budget}\n"
            f"Location: {location}\n"
            "Return JSON with 3 arrays: Themes, Food, Activities."
        )
        resp = client.chat.completions.create(
            model=MODEL,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0.7,
        )
        raw = resp.choices[0].message.content
        data = json.loads(raw)
        # normalize
        return {
            "Themes": [str(x).strip() for x in data.get("Themes", [])][:6],
            "Food": [str(x).strip() for x in data.get("Food", [])][:6],
            "Activities": [str(x).strip() for x in data.get("Activities", [])][:6],
        }
    except Exception:
        return _fallback_ideas(event_type, guests, budget, location)






'''import os
import json
from openai import OpenAI
from typing import Dict, List

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

def _fallback_ideas(event_type: str, guests: int, budget: str, location: str) -> Dict[str, List[str]]:
    # Safe, tidy fallback
    return {
        "Themes": [
            "Modern Minimal",
            "Garden Party",
            "Retro Disco"
        ],
        "Food": [
            "Mixed buffet with local dishes",
            "Finger foods & small plates",
            "Mocktail station"
        ],
        "Activities": [
            "Photo booth",
            "Trivia game",
            "Curated playlist and dance corner"
        ],
    }

def generate_event_ideas(event_type: str, guests: int, budget: str, location: str) -> Dict[str, List[str]]:
    """
    Returns a dict:
    {
      "Themes": [.. up to 6],
      "Food":   [.. up to 6],
      "Activities": [.. up to 6]
    }
    """
    try:
        client = OpenAI()
        system = (
            "You are an event-planning assistant. "
            "Respond ONLY as strict JSON with keys: Themes, Food, Activities. "
            "Each value must be an array of 3-6 short bullet ideas. "
            "No prose, no markdown, no extra keys."
        )
        user = (
            f"Event type: {event_type}\n"
            f"Guests: {guests}\n"
            f"Budget: {budget}\n"
            f"Location: {location}\n"
            "Return JSON with 3 arrays: Themes, Food, Activities."
        )
        resp = client.chat.completions.create(
            model=MODEL,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0.7,
        )
        raw = resp.choices[0].message.content
        data = json.loads(raw)
        # normalize
        return {
            "Themes": [str(x).strip() for x in data.get("Themes", [])][:6],
            "Food": [str(x).strip() for x in data.get("Food", [])][:6],
            "Activities": [str(x).strip() for x in data.get("Activities", [])][:6],
        }
    except Exception:
        return _fallback_ideas(event_type, guests, budget, location)
'''






'''
import json
from utils.config import get_openai_client, MODEL

def _fallback_ideas():
    return {
        "Themes": [
            "Masquerade Ball — elegant masks, candlelight, deep colors",
            "Bollywood Night — posters, playlist, glam outfits",
            "Garden Party — fairy lights, florals, picnic tables",
        ],
        "Food": [
            "Fusion buffet (Indian + Continental)",
            "Dessert bar with pastries & themed cake",
            "Mocktail station (mango mint cooler, rose fizz, etc.)",
        ],
        "Activities": [
            "Photo booth with props",
            "Karaoke or dance-off",
            "Trivia/ice-breaker games with small prizes",
        ],
    }

def generate_event_ideas(event_type, guests, budget, location):
    """
    Returns a dict: { 'Themes': [..], 'Food': [..], 'Activities': [..] }
    """
    # Ensure guests is an int if possible
    try:
        guests_int = int(guests)
    except Exception:
        guests_int = guests

    client = get_openai_client()
    if not client:
        return _fallback_ideas()

    system = (
        "You are an event planning assistant. "
        "Return STRICT JSON with keys Themes, Food, Activities. "
        "Each value is an array of 3-6 short, practical bullets. "
        "Keep items concrete and region-aware if a location is provided. "
        "No markdown, no extra keys."
    )
    user = (
        f"event_type: {event_type}\n"
        f"guests: {guests_int}\n"
        f"budget: {budget}\n"
        f"location: {location}"
    )

    try:
        resp = client.chat.completions.create(
            model=MODEL,
            response_format={"type": "json_object"},
            temperature=0.5,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        data = json.loads(resp.choices[0].message.content)
        out = {
            "Themes": list(data.get("Themes", []))[:6],
            "Food": list(data.get("Food", []))[:6],
            "Activities": list(data.get("Activities", []))[:6],
        }
        # basic sanitation
        for k in out:
            out[k] = [str(x).strip() for x in out[k] if str(x).strip()]
        if not any(out.values()):
            raise ValueError("Empty ideas")
        return out
    except Exception:
        return _fallback_ideas()

'''




'''
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # <-- this loads .env file

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_event_ideas(event_type, guests, budget, location=None):
    prompt = f"""
    Suggest creative ideas for a {event_type} with {guests} guests.
    Budget level: {budget}.
    Location: {location if location else "not specified"}.

    Provide suggestions for:
    - Themes
    - Food
    - Activities
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )

    text = response.choices[0].message.content
    sections = {"Themes": [], "Food": [], "Activities": []}

    current_section = None
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue
        if "theme" in line.lower():
            current_section = "Themes"
        elif "food" in line.lower():
            current_section = "Food"
        elif "activity" in line.lower():
            current_section = "Activities"
        elif current_section:
            sections[current_section].append(line.strip("-• "))

    return sections
'''





