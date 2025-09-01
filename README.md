# 🎉 Neighborhood Event Planner

A Flask-based web app that helps communities plan neighborhood events.
It uses OpenAI to generate event ideas, invitation messages, and planning timelines, with graceful fallbacks when AI is unavailable.

## ✨ Features

- 📝 Event Form: Input event details (type, date, time, budget, location, etc.).

- 💡 AI-Powered Event Ideas: Suggestions for themes, food, and activities.

- 📜 Invitations: Generates 3 friendly invitation messages.

- 📅 Timeline Planner: Creates a preparation schedule with key tasks.

- 🎨 Modern UI: Styled with responsive CSS and banner support.

- ⚡ Fallback Mode: Works even if OpenAI API is unavailable.

## 📂 Project Structure
.
├── app.py            # Flask app entry point
├── utils
|   ├──  config.py         # Handles API keys and OpenAI client
├── core
│   ├── ideas.py          # Generates event ideas
│   ├── invitation.py     # Generates invitation messages
│   └── timeline.py       # Builds event preparation timeline
├── templates/
│   ├── index.html    # Input form page
│   └── results.html  # (to be added) displays generated results
├── static/
│   ├── static.css    # Styling
│   └── images/
│       └── community_banner.jpg
└── .env.example      # Example environment variables

## ⚙️ Setup & Installation

1. Clone the repository

git clone https://github.com/yourusername/neighborhood-event-planner.git
cd neighborhood-event-planner


2. Create a virtual environment

python -m venv .venv
source .venv/bin/activate   # (Linux/Mac)
.venv\Scripts\activate      # (Windows)


3. Install dependencies

pip install -r requirements.txt


4. Environment variables
Create a .env file in the project root:

OPENAI_API_KEY=your_openai_api_key
FLASK_SECRET_KEY=your_flask_secret
OPENAI_MODEL=gpt-4o-mini   # (default, can change)
USE_OPENAI=true

## ▶️ Running the App
python app.py


Then open http://127.0.0.1:5000
 in your browser.

## 🔎 How It Works

1. Fill the Event Form

   - On the homepage, you choose the event type (Block Party, Potluck, Cleanup Drive, etc.), expected guests, budget, location, date, time, venue, and tone of invitation.
   - This form is defined in index.html.

2. Submit & Process
   - When you click “Generate Plan”, your details are sent to app.py
   - app.py calls three helper functions:
      - generate_event_ideas() → from ideas.py
      - generate_invitations() → from invitation.py
      - make_timeline() → from timeline.py

3. AI Generation (with Fallbacks)

   - Each helper function tries to use OpenAI’s API to generate content:
      - Ideas → themes, food, activities.
      -  Invitations → 3 short messages.
      - Timeline → checklist of tasks.

   - If the API isn’t available (or key missing), it switches to hardcoded fallback suggestions, so the app always works.

4. Render Results

   - The generated plan is displayed on a results page (currently you need a results.html template).
   - The UI is styled with static.css for a clean, modern look.

5. Future Enhancements

    - Exporting the entire plan to PDF.
    - Saving event plans.
    - Sharing invitations directly via email/social.
    
## 📸 Screenshots

(Add screenshots of the form and results page here for better presentation.)


## 🛠 Tech Stack

#### Frontend

- HTML5 – form inputs & structure (index.html, results.html)
- CSS3 – responsive design & styling (static.css)

#### Backend

- Python 3.9+
- Flask – lightweight web framework (app.py)
- Jinja2 – templating engine (for rendering HTML with Flask)

#### AI / External Services

- OpenAI API – generates event ideas, invitations, and timelines
- dotenv – loads API keys & secrets from .env

#### Other Utilities

- os / json / datetime – standard Python modules used in helpers
- Fallback Mode – predefined suggestions if OpenAI API is not available


## 📜 License

This project is for educational & demo purposes. Check individual APIs for their respective terms of use.