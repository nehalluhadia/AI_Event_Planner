import os
import json
from datetime import datetime, timedelta
from typing import List, Dict
from openai import OpenAI

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

def _fallback_timeline(event_type: str, event_date: str) -> List[Dict]:
    return [
        {"period": "6–4 Weeks Before", "tasks": [
            "Form volunteer committee",
            "Apply for permits if required",
            "Set event budget & attendance goals"
        ]},
        {"period": "4–2 Weeks Before", "tasks": [
            "Design and distribute flyers",
            "Confirm potluck sign-ups or food vendors",
            "Plan group activities and entertainment"
        ]},
        {"period": "1 Week Before", "tasks": [
            "Finalize equipment rentals (tables, chairs)",
            "Confirm volunteer roles",
            "Purchase supplies"
        ]},
        {"period": "Event Day", "tasks": [
            "Set up booths, tables, and greeting station",
            "Coordinate food and activity areas",
            "Enjoy the community gathering & cleanup"
        ]},
    ]

def _date_window_labels(event_date: str) -> List[str]:
    try:
        d = datetime.strptime(event_date, "%Y-%m-%d")
    except Exception:
        return ["6–4 Weeks Before", "4–2 Weeks Before", "1 Week Before", "Event Day"]
    return [
        f"{(d - timedelta(days=42)).strftime('%b %d')} – {(d - timedelta(days=28)).strftime('%b %d')}",
        f"{(d - timedelta(days=28)).strftime('%b %d')} – {(d - timedelta(days=14)).strftime('%b %d')}",
        f"{(d - timedelta(days=7)).strftime('%b %d')} – {(d - timedelta(days=1)).strftime('%b %d')}",
        d.strftime("%b %d (Event Day)"),
    ]

def make_timeline(event_type: str, event_date: str) -> List[Dict]:
    """
    Returns: [{ "period": "label", "tasks": ["...", "..."] }, ...]  (4–6 periods)
    """
    try:
        labels = _date_window_labels(event_date)
        client = OpenAI()
        system = (
            "You are a community event timeline planner. "
            "Return ONLY JSON with key 'timeline' which is an array of 4-6 objects. "
            "Each object has 'period' (string label) and 'tasks' (array of 3-6 short items). "
            "No extra text, no markdown."
        )
        user = (
            f"Generate a planning timeline for a neighborhood/community event: {event_type}, on {event_date}.\n"
            f"Include early tasks (permissions, flyers, volunteer committees), mid-term tasks (confirm food, activities, vendors), and event-day setup.\n"
            f"Suggested period labels: {labels}\nReturn JSON only."
        )
        resp = client.chat.completions.create(
            model=MODEL,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0.6,
        )
        data = json.loads(resp.choices[0].message.content)
        tl = data.get("timeline", [])
        out = []
        for block in tl[:6]:
            period = str(block.get("period", "")).strip()
            tasks = [str(t).strip() for t in block.get("tasks", [])][:6]
            if not period:
                continue
            if not tasks:
                continue
            out.append({"period": period, "tasks": tasks})
        return out or _fallback_timeline(event_type, event_date)
    except Exception:
        return _fallback_timeline(event_type, event_date)






'''import os
import json
from datetime import datetime, timedelta
from typing import List, Dict
from openai import OpenAI

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

def _fallback_timeline(event_type: str, event_date: str) -> List[Dict]:
    return [
        {"period": "6–4 Weeks Before", "tasks": [
            "Set budget & guest list",
            "Shortlist venues and vendors",
            "Define theme"
        ]},
        {"period": "4–2 Weeks Before", "tasks": [
            "Send invitations & collect RSVPs",
            "Finalize menu & activities",
            "Book entertainment"
        ]},
        {"period": "1 Week Before", "tasks": [
            "Confirm vendors and logistics",
            "Create seating or flow plan",
            "Prepare supplies"
        ]},
        {"period": "Event Day", "tasks": [
            "Setup venue & décor",
            "Coordinate with vendors",
            "Enjoy the event!"
        ]},
    ]

def _date_window_labels(event_date: str) -> List[str]:
    # Human-friendly labels based on real date (optional helper)
    try:
        d = datetime.strptime(event_date, "%Y-%m-%d")
    except Exception:
        return ["6–4 Weeks Before", "4–2 Weeks Before", "1 Week Before", "Event Day"]
    return [
        f"{(d - timedelta(days=42)).strftime('%b %d')} – {(d - timedelta(days=28)).strftime('%b %d')}",
        f"{(d - timedelta(days=28)).strftime('%b %d')} – {(d - timedelta(days=14)).strftime('%b %d')}",
        f"{(d - timedelta(days=7)).strftime('%b %d')} – {(d - timedelta(days=1)).strftime('%b %d')}",
        d.strftime("%b %d (Event Day)"),
    ]

def make_timeline(event_type: str, event_date: str) -> List[Dict]:
    """
    Returns: [{ "period": "label", "tasks": ["...", "..."] }, ...]  (4–6 periods)
    """
    try:
        labels = _date_window_labels(event_date)
        client = OpenAI()
        system = (
            "You are an event timeline planner. "
            "Return ONLY JSON with key 'timeline' which is an array of 4-6 objects. "
            "Each object has 'period' (string label) and 'tasks' (array of 3-6 short items). "
            "No extra text, no markdown."
        )
        user = (
            f"Create a preparation timeline for a {event_type} on {event_date}.\n"
            f"Suggested period labels: {labels}\n"
            "Return JSON only."
        )
        resp = client.chat.completions.create(
            model=MODEL,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0.6,
        )
        data = json.loads(resp.choices[0].message.content)
        tl = data.get("timeline", [])
        out = []
        for block in tl[:6]:
            period = str(block.get("period", "")).strip()
            tasks = [str(t).strip() for t in block.get("tasks", [])][:6]
            if not period:
                continue
            if not tasks:
                continue
            out.append({"period": period, "tasks": tasks})
        return out or _fallback_timeline(event_type, event_date)
    except Exception:
        return _fallback_timeline(event_type, event_date)
'''






'''
import json
from utils.config import get_openai_client, MODEL

def _fallback_timeline(event_type, event_date):
    return [
        {"period": "4–6 Weeks Before", "tasks": [
            "Set budget & guest list",
            "Book venue & confirm date",
            "Pick theme and high-level plan",
        ]},
        {"period": "2–3 Weeks Before", "tasks": [
            "Finalize menu and vendors",
            "Order cake / desserts",
            "Design & send invitations",
        ]},
        {"period": "Week Of Event", "tasks": [
            "Confirm RSVPs & quantities",
            "Finalize playlist and schedule",
            "Buy remaining supplies",
        ]},
        {"period": "Event Day", "tasks": [
            "Set up décor & AV",
            "Welcome guests",
            "Enjoy the celebration 🎉",
        ]},
    ]

def make_timeline(event_type, event_date):
    """
    Returns a list of { 'period': str, 'tasks': [str, ...] }
    """
    client = get_openai_client()
    if not client:
        return _fallback_timeline(event_type, event_date)

    system = (
        "You are a project scheduler. Build a concise planning timeline for an event. "
        "Output STRICT JSON with the shape:\n"
        "{ \"timeline\": [ {\"period\": string, \"tasks\": [string, ...]}, ... ] }\n"
        "Return 4–6 periods max; 3–6 tasks each; no dates calculation needed; no markdown."
    )
    user = f"event_type: {event_type}\nevent_date: {event_date}"

    try:
        resp = client.chat.completions.create(
            model=MODEL,
            response_format={"type": "json_object"},
            temperature=0.3,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        data = json.loads(resp.choices[0].message.content)
        items = data.get("timeline", [])
        cleaned = []
        for it in items:
            period = (it.get("period") or "").strip()
            tasks = [str(t).strip() for t in (it.get("tasks") or []) if str(t).strip()]
            if period and tasks:
                cleaned.append({"period": period, "tasks": tasks[:6]})
        if not cleaned:
            raise ValueError("Empty timeline")
        return cleaned[:6]
    except Exception:
        return _fallback_timeline(event_type, event_date)
'''







'''
import os
from openai import OpenAI
from datetime import timedelta

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def make_timeline(event_type, event_date):
    prompt = f"""
    Create a preparation timeline for a {event_type} happening on {event_date}.
    Include tasks starting weeks before the event until the event day.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )

    text = response.choices[0].message.content
    timeline = []
    for line in text.split("\n"):
        if "-" in line:
            parts = line.split("-", 1)
            date = parts[0].strip()
            task = parts[1].strip()
            timeline.append((date, task))
    return timeline
'''









'''
from utils.config import client

def generate_timeline(event_type: str, event_date: str):
    prompt = f"""
    Create a preparation timeline for a {event_type}.
    Event date: {event_date}.
    Break it down into milestones (planning, booking, invitations, catering, final touches).
    Return 6-8 steps with dates leading up to the event.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400
    )
    return response.choices[0].message.content.split("\n\n")


'''







'''from datetime import date, timedelta

def make_timeline(event_type: str, event_date: date):
    tasks = [
        (12, "Set budget & guest list"),
        (10, "Choose venue"),
        (8, "Finalize theme & vendors"),
        (6, "Send save-the-date"),
        (4, "Confirm catering & entertainment"),
        (2, "Send invitations"),
        (1, "Finalize logistics"),
        (0, "Event day 🎉"),
    ]
    timeline = []
    for weeks, task in tasks:
        d = event_date - timedelta(weeks=weeks) if weeks > 0 else event_date
        timeline.append((d.strftime("%b %d, %Y"), task))
    return timeline
'''