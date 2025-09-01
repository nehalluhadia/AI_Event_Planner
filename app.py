import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

from core.ideas import generate_event_ideas
from core.invitation import generate_invitations
from core.timeline import make_timeline

load_dotenv()  # Loads OPENAI_API_KEY from .env

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret")  # for flash messages


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        event_type = request.form.get("event_type", "Block Party").strip()
        guests = int(request.form.get("guests", "50") or 50)
        budget = request.form.get("budget", "Moderate").strip()
        location = request.form.get("location", "").strip()
        organizing_group = request.form.get("organizing_group", "").strip()
        event_date = request.form.get("event_date", "").strip()
        event_time = request.form.get("event_time", "").strip()
        venue = request.form.get("venue", "").strip()
        tone = request.form.get("tone", "casual").strip()

        # OpenAI-powered generation (with graceful fallbacks in each function)
        ideas = generate_event_ideas(event_type, guests, budget, location)
        invitations = generate_invitations(
            event_type, organizing_group, event_date, event_time, venue, tone
        )
        timeline = make_timeline(event_type, event_date)

        # Render results page
        return render_template(
            "results.html",
            invitations=invitations,
            ideas=ideas,
            timeline=timeline,
        )

    return render_template("index.html")


if __name__ == "__main__":
    # Debug on for local dev
    app.run(debug=True)







'''import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

from core.ideas import generate_event_ideas
from core.invitation import generate_invitations
from core.timeline import make_timeline

load_dotenv()  # Loads OPENAI_API_KEY from .env

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret")  # for flash messages


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        event_type = request.form.get("event_type", "Birthday").strip()
        guests = int(request.form.get("guests", "50") or 50)
        budget = request.form.get("budget", "Moderate").strip()
        location = request.form.get("location", "").strip()
        host_names = request.form.get("host_names", "").strip()
        event_date = request.form.get("event_date", "").strip()
        event_time = request.form.get("event_time", "").strip()
        venue = request.form.get("venue", "").strip()
        tone = request.form.get("tone", "casual").strip()

        # OpenAI-powered generation (with graceful fallbacks in each function)
        ideas = generate_event_ideas(event_type, guests, budget, location)
        invitations = generate_invitations(
            event_type, host_names, event_date, event_time, venue, tone
        )
        timeline = make_timeline(event_type, event_date)

        # Render results page (no PDF)
        return render_template(
            "results.html",
            invitations=invitations,
            ideas=ideas,
            timeline=timeline,
        )

    return render_template("index.html")


if __name__ == "__main__":
    # Debug on for local dev
    app.run(debug=True)
'''







'''
import os
from flask import Flask, render_template, request, url_for
from dotenv import load_dotenv

from core.ideas import generate_event_ideas
from core.invitation import generate_invitations
from core.timeline import make_timeline
from core.pdf_export import export_to_pdf

# Load environment variables (for OPENAI_API_KEY, etc.)
load_dotenv()

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Collect form inputs
        event_type = request.form["event_type"]
        guests = request.form["guests"]
        budget = request.form["budget"]
        location = request.form.get("location", "")
        host_names = request.form["host_names"]
        event_date = request.form["event_date"]
        event_time = request.form["event_time"]
        venue = request.form["venue"]
        tone = request.form["tone"]

        # Generate ideas (dict of categories)
        ideas = generate_event_ideas(event_type, guests, budget, location)
        if not isinstance(ideas, dict):  # fallback to dict
            ideas = {"Themes": [], "Food": [], "Activities": []}

        # Generate multiple invitations
        invitations = generate_invitations(
            event_type, host_names, event_date, event_time, venue, tone
        )
        if not isinstance(invitations, list):
            invitations = [str(invitations)]

        # Generate timeline (list of steps)
        timeline = make_timeline(event_type, event_date)
        if not isinstance(timeline, list):
            timeline = []
        

        # right before export_to_pdf(...)
        inv_texts = [f"{i['title']}\n\n{i['body']}" for i in invitations]
        pdf_file = export_to_pdf("event_plan", inv_texts, ideas, timeline)


        # Export full plan to PDF (saved in static/)
        pdf_file = export_to_pdf("event_plan", invitations, ideas, timeline)
        pdf_url = url_for("static", filename=pdf_file)

        # Show results page
        return render_template(
            "results.html",
            invitations=invitations,
            ideas=ideas,
            timeline=timeline,
            pdf_file=pdf_url,
        )

    # First visit → show form
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)



'''












'''import streamlit as st
from datetime import date

from core.ideas import generate_event_ideas
from core.invitation import generate_invitation
from core.timeline import make_timeline
from core.pdf_export import export_to_pdf

st.title("🎉 Simple Event Planner")

with st.form("event_form"):
    event_type = st.selectbox("Event Type", ["Wedding", "Birthday", "Corporate", "Custom"])
    host_names = st.text_input("Host(s)", "John & Jane")
    event_date = st.date_input("Event Date", value=date.today())
    event_time = st.text_input("Event Time", "6:00 PM")
    venue = st.text_input("Venue", "City Hall")
    guests = st.number_input("Guests", min_value=1, value=50)
    budget = st.selectbox("Budget", ["Shoestring", "Moderate", "Premium"])
    location = st.text_input("Location", "New York")
    tone = st.selectbox("Invitation Tone", ["Formal", "Casual", "Playful", "Elegant"])

    submitted = st.form_submit_button("Generate Plan")

if submitted:
    st.subheader("📜 Invitation")
    invitation = generate_invitation(event_type, host_names, event_date, event_time, venue, tone)
    st.write(invitation)

    st.subheader("💡 Event Ideas")
    ideas = generate_event_ideas(event_type, guests, budget, location)
    for section, items in ideas.items():
        st.write(f"**{section}:**")
        for item in items:
            st.write(f"- {item}")

    st.subheader("📅 Timeline")
    timeline = make_timeline(event_type, event_date)
    for d, task in timeline:
        st.write(f"**{d}** - {task}")

    st.subheader("⬇️ Export")
    if st.button("Export as PDF"):
        file_path = export_to_pdf("event_plan", invitation, ideas, timeline)
        with open(file_path, "rb") as f:
            st.download_button("Download PDF", f, file_name=file_path)
'''