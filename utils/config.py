import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")  # change if you prefer
USE_OPENAI = os.getenv("USE_OPENAI", "1").lower() in {"1", "true", "yes"}

def get_openai_client():
    """Create the OpenAI client only when needed. Returns None if key missing or disabled."""
    if not USE_OPENAI:
        return None
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    return OpenAI(api_key=api_key)






'''
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load .env variables
load_dotenv()

# Get API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("⚠️ OPENAI_API_KEY not found in .env file")

# Create reusable OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)



'''







'''import os
from openai import OpenAI
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

def get_openai_client():
    """Return an OpenAI client if API key is set, else None."""
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        return None
    return OpenAI(api_key=key)
'''