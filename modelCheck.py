from google import genai
import config

client = genai.Client(api_key=config.GEMINI_API_KEY)

for model in client.models.list():
    if "generateContent" in model.supported_actions:
        print(model.name)