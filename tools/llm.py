import time

from dotenv import load_dotenv
import os

from httpx import HTTPStatusError
from network.client import client
import re
from logger.log_config import logger
load_dotenv()

class LLMConfig:
    api=os.getenv("GEMINI_API")
    url=f"{os.getenv('GEMINI_URL')}/{os.getenv('GEMINI_MODEL')}:generateContent"
    temperature=os.getenv("GEMINI_TEMPERATURE", 0.2)



def escape_control_chars_in_json_strings(text: str) -> str:
    out = []
    in_string = False
    escaped = False

    for ch in text:
        if in_string:
            if escaped:
                out.append(ch)
                escaped = False
                continue

            if ch == '\\':
                out.append(ch)
                escaped = True
                continue

            if ch == '"':
                out.append(ch)
                in_string = False
                continue

            if ch == '\n':
                out.append('\\n')
            elif ch == '\r':
                out.append('\\r')
            elif ch == '\t':
                out.append('\\t')
            elif ord(ch) < 0x20:
                out.append(f'\\u{ord(ch):04x}')
            else:
                out.append(ch)
        else:
            out.append(ch)
            if ch == '"':
                in_string = True
                escaped = False

    return ''.join(out)

def clean_string(text):
    cleaned = text.strip()
    #remove surronding markdown fences if present
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)

    return cleaned

async def send_llm_request(prompt: str, system_prompt="You are a helpful assistant."):
    api_key = LLMConfig.api
    url = LLMConfig.url
    payload = {
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "contents": [{"role":"user","parts": [{"text": prompt}]}],
        "generationConfig":{
            "temperature": LLMConfig.temperature
        }
    }
    header = {
        "Content-Type":"application/json",
        "x-goog-api-key": api_key
    }
    for _ in range(3):
        try:
            response = await client.post(url, headers=header, json=payload)
            response.raise_for_status()
            data = response.json()
            if "candidates" in data and len(data["candidates"]) > 0:
                rawtext = data["candidates"][0]["content"]["parts"][0]["text"]
                if "usageMetadata" in data:
                    total_tokens = data["usageMetadata"].get("totalTokenCount", 0)
                    logger.info(f"Total tokens used: {total_tokens}")
                cleaned_text = escape_control_chars_in_json_strings(clean_string(rawtext))
                return cleaned_text
            else:
                raise ValueError("No candidates found in the response")
        except HTTPStatusError as e:
            logger.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            time.sleep(1)