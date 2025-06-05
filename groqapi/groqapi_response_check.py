import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OLD_GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"  # Replace with your old endpoint

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "You're a kind, motivational assistant who helps people stay mentally strong and productive. "
        "Given the user's emotional and activity state, respond with a short, uplifting message that speaks directly to them. "
        "Format your message as 3 clear lines like a poem or affirmation, no preface or formatting, just the 3-line quote."
    )
}

def fetch_motivational_quote(user_state):
    user_prompt = {
        "role": "user",
        "content": (
            f"The user is feeling {user_state['emotion']}. "
            f"They are currently using {user_state['activity']['active_window']} with a typing speed of "
            f"{user_state['activity']['typing_speed']} keys/sec and a mouse speed of "
            f"{user_state['activity']['mouse_speed']} px/sec. Please provide an encouraging, personal motivational message."
        )
    }

    data = {
        "model": "llama3-8b-8192",
        "messages": [SYSTEM_PROMPT, user_prompt],
        "temperature": 0.9
    }

    start_time = time.time()
    response = requests.post(OLD_GROQ_URL, headers=HEADERS, json=data)
    elapsed_time = time.time() - start_time

    if response.status_code == 200:
        quote = response.json()['choices'][0]['message']['content'].strip()
        return quote, elapsed_time
    else:
        raise Exception(f"API Error {response.status_code}: {response.text}")

# Example usage
if __name__ == "__main__":
    example_user_state = {
        "emotion": "stressed",
        "activity": {
            "active_window": "Visual Studio Code",
            "typing_speed": 40,
            "mouse_speed": 300
        }
    }
    quote, time_taken = fetch_motivational_quote(example_user_state)
    print(f"Quote:\n{quote}\n\nResponse time: {time_taken:.3f} seconds")
