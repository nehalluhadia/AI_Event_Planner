import os
import json
from openai import OpenAI
from typing import List, Dict

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

def _fallback_invitations(event_type, organizing_group, event_date, event_time, venue, tone) -> List[Dict[str, str]]:
    base = f"{event_type} organized by {organizing_group}"
    return [
        {
            "title": "Invitation 1",
            "body": (
                f"Dear neighbors, you are warmly invited to {base}.\n\n"
                f"Date: {event_date}\nTime: {event_time}\nLocation: {venue}\n\n"
                "We look forward to celebrating our community together!"
            ),
        },
        {
            "title": "Invitation 2",
            "body": (
                f"Please join us for our community {event_type} at {venue} on {event_date}. "
                f"Festivities begin at {event_time}. Bring family, food, and friends to share."
            ),
        },
        {
            "title": "Invitation 3",
            "body": (
                f"Celebrate {base} with us!\n\nWhen: {event_date} at {event_time}\n"
                f"Where: {venue}\n\nAll are welcome — let’s make it a great neighborhood gathering!"
            ),
        },
    ]

def generate_invitations(event_type, organizing_group, event_date, event_time, venue, tone) -> List[Dict[str, str]]:
    """
    Returns a list of 3 dicts: [{"title": "...", "body": "..."}, ...]
    Body should be plain text (no markdown).
    """
    try:
        client = OpenAI()
        system = (
            "You write concise community invitation messages. "
            "Return ONLY JSON with key 'invitations' which is an array of exactly 3 objects. "
            "Each object has 'title' and 'body' (plain text, no markdown)."
        )
        user = (
            f"Generate 3 friendly, community-focused invitations for a {event_type}.\n"
            f"Organized by: {organizing_group}\nDate: {event_date}\n"
            f"Time: {event_time}\nLocation: {venue}\nTone: {tone}\n"
            "Make them warm and inclusive, suitable for neighbors. Return JSON only."
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
        data = json.loads(resp.choices[0].message.content)
        invites = data.get("invitations", [])
        # Normalize
        out = []
        for i, inv in enumerate(invites[:3], start=1):
            out.append({
                "title": str(inv.get("title", f"Invitation {i}")).strip(),
                "body": str(inv.get("body", "")).strip(),
            })
        # Guarantee 3
        while len(out) < 3:
            out.append({"title": f"Invitation {len(out)+1}", "body": ""})
        return out
    except Exception:
        return _fallback_invitations(event_type, organizing_group, event_date, event_time, venue, tone)






'''import os
import json
from openai import OpenAI
from typing import List, Dict

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

def _fallback_invitations(event_type, host_names, event_date, event_time, venue, tone) -> List[Dict[str, str]]:
    base = f"{event_type} hosted by {host_names}"
    return [
        {
            "title": "Invitation 1",
            "body": (
                f"You are warmly invited to {base}.\n\n"
                f"Date: {event_date}\nTime: {event_time}\nVenue: {venue}\n\n"
                "We look forward to celebrating together!"
            ),
        },
        {
            "title": "Invitation 2",
            "body": (
                f"Please join us for {base} at {venue} on {event_date}. "
                f"Festivities begin at {event_time}. Your presence would mean a lot."
            ),
        },
        {
            "title": "Invitation 3",
            "body": (
                f"Celebrate {base} with us!\n\nWhen: {event_date} at {event_time}\n"
                f"Where: {venue}\n\nRSVP appreciated. See you there!"
            ),
        },
    ]

def generate_invitations(event_type, host_names, event_date, event_time, venue, tone) -> List[Dict[str, str]]:
    """
    Returns a list of 3 dicts: [{"title": "...", "body": "..."}, ...]
    Body should be plain text (no markdown).
    """
    try:
        client = OpenAI()
        system = (
            "You write concise invitation messages. "
            "Return ONLY JSON with key 'invitations' which is an array of exactly 3 objects. "
            "Each object has 'title' and 'body' (plain text, no markdown)."
        )
        user = (
            f"Create 3 invitation messages for a {tone} tone.\n"
            f"Event: {event_type}\nHost(s): {host_names}\nDate: {event_date}\n"
            f"Time: {event_time}\nVenue: {venue}\n"
            "Keep them short, warm, and natural. Return JSON only."
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
        data = json.loads(resp.choices[0].message.content)
        invites = data.get("invitations", [])
        # Normalize
        out = []
        for i, inv in enumerate(invites[:3], start=1):
            out.append({
                "title": str(inv.get("title", f"Invitation {i}")).strip(),
                "body": str(inv.get("body", "")).strip(),
            })
        # Guarantee 3
        while len(out) < 3:
            out.append({"title": f"Invitation {len(out)+1}", "body": ""})
        return out
    except Exception:
        return _fallback_invitations(event_type, host_names, event_date, event_time, venue, tone)
'''



'''import json
from utils.config import get_openai_client, MODEL

def _fallback_invitations(event_type, host_names, event_date, event_time, venue, tone):
    # Compact, well-formed fallback content
    return [
        {
            "title": "Invitation 1",
            "body": (
                f"You are warmly invited to {host_names}'s {event_type}.\n\n"
                f"Date: {event_date}\nTime: {event_time}\nVenue: {venue}\n\n"
                "We look forward to celebrating together!"
            ),
        },
        {
            "title": "Invitation 2",
            "body": (
                f"Please join us for {host_names}'s {event_type} at {venue} on {event_date}."
                f" Festivities begin at {event_time}. Your presence would mean a lot."
            ),
        },
        {
            "title": "Invitation 3",
            "body": (
                f"Celebrate {host_names}'s {event_type} with us!\n\n"
                f"When: {event_date} at {event_time}\nWhere: {venue}\n\n"
                "RSVP appreciated. See you there!"
            ),
        },
    ]

def generate_invitations(event_type, host_names, event_date, event_time, venue, tone):
    """
    Returns a list of {title:str, body:str} generated by OpenAI in strict JSON.
    """
    client = get_openai_client()
    if not client:
        return _fallback_invitations(event_type, host_names, event_date, event_time, venue, tone)

    system = (
        "You are a concise event invitation copywriter. "
        "Write THREE distinct invitation messages for the provided event details. "
        "Match the requested tone (Formal/Casual/Playful/Elegant). "
        "Output STRICT JSON with this exact shape:\n"
        "{ \"invitations\": [ {\"title\": string, \"body\": string}, { ... }, { ... } ] }\n"
        "Do not include markdown, backticks, or extra keys. No placeholders like [Name]."
    )

    user = (
        f"event_type: {event_type}\n"
        f"host_names: {host_names}\n"
        f"event_date: {event_date}\n"
        f"event_time: {event_time}\n"
        f"venue: {venue}\n"
        f"tone: {tone}"
    )

    try:
        resp = client.chat.completions.create(
            model=MODEL,
            response_format={"type": "json_object"},
            temperature=0.7,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        data = json.loads(resp.choices[0].message.content)
        invitations = data.get("invitations", [])
        # Normalize
        cleaned = []
        for inv in invitations[:3]:
            title = (inv.get("title") or "Invitation").strip()
            body = (inv.get("body") or "").strip()
            if body:
                cleaned.append({"title": title, "body": body})
        if len(cleaned) < 3:
            raise ValueError("Model returned too few items")
        return cleaned
    except Exception:
        return _fallback_invitations(event_type, host_names, event_date, event_time, venue, tone)

'''




'''import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_invitations(event_type, host_names, event_date, event_time, venue, tone):
    prompt = f"""
    Write 3 different invitation messages for a {event_type}.
    Hosts: {host_names}
    Date: {event_date}
    Time: {event_time}
    Venue: {venue}
    Tone: {tone}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )

    text = response.choices[0].message.content
    return text.split("\n\n")

'''

'''from utils.config import get_openai_client

def _fallback_invitation(event_type, host_names, date, time, venue, tone="Formal"):
    return (
        f"{host_names} invite you to a {event_type}.\n\n"
        f"Date & Time: {date} at {time}\nVenue: {venue}\n\n"
        f"Tone: {tone}\nWe look forward to seeing you!"
    )

def generate_invitation(event_type, host_names, date, time, venue, tone="Formal"):
    client = get_openai_client()
    if not client:
        return _fallback_invitation(event_type, host_names, date, time, venue, tone)

    prompt = f"""
    Write a {tone.lower()} invitation for a {event_type} hosted by {host_names}.
    Event on {date} at {time}, Venue: {venue}.
    Keep it under 120 words, suitable for a message card.
    """

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=220,
        )
        return resp.choices[0].message.content.strip()
    except Exception:
        return _fallback_invitation(event_type, host_names, date, time, venue, tone)
'''