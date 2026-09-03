import os

from dotenv import load_dotenv

load_dotenv()


APP_NAME = "LedgerPilot AI"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
)


print("================================")
print("Gemini API Key Loaded:",
      bool(GEMINI_API_KEY))

if GEMINI_API_KEY:
    print(
        "Gemini Key Prefix:",
        GEMINI_API_KEY[:8] + "..."
    )

print("Gemini Model:", GEMINI_MODEL)
print("================================")