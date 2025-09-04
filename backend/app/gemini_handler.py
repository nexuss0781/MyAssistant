import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from a .env file located in the 'backend' directory
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# Define models in order of preference (most capable/fastest first)
GEMINI_MODELS = [
    "gemini-1.5-flash-latest",
    "gemini-pro"  # Fallback model
]
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"

def call_gemini(prompt: str):
    """
    Calls the Gemini API with a given prompt, featuring graceful fallback to other models.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")

    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": prompt}]}]}

    for model in GEMINI_MODELS:
        url = f"{BASE_URL}/{model}:generateContent?key={api_key}"
        print(f"Attempting to use model: {model}...")
        
        try:
            response = requests.post(url, headers=headers, data=json.dumps(data), timeout=120)
            
            # Raise an exception for bad status codes (4xx or 5xx)
            response.raise_for_status()

            result = response.json()
            
            # Safely extract content. If response is valid but content is blocked, try next model.
            if "candidates" in result and result["candidates"]:
                print(f"Successfully received response from {model}.")
                return result['candidates'][0]['content']['parts'][0]['text']
            else:
                print(f"Warning: Model {model} returned a valid response but no content (possibly due to safety filters). Trying next model.")
                continue

        except requests.exceptions.HTTPError as e:
            # Specifically check for rate limiting to decide if we should try the next model
            if e.response.status_code == 429:
                print(f"Rate limit hit for {model}. Trying next model...")
                continue
            else:
                print(f"HTTP Error with {model}: {e}. Trying next model...")
                continue
        except requests.exceptions.RequestException as e:
            print(f"Request failed for {model}: {e}. Trying next model...")
            continue

    # If the loop completes without returning, all models have failed.
    raise Exception("All Gemini models failed to provide a response.")
