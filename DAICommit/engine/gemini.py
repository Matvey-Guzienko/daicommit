import time
from typing import Any, Dict, List, Optional
import google.generativeai as genai
from google.generativeai import GenerationConfig
from google.generativeai.types import HarmCategory, HarmBlockThreshold, ContentDict, PartDict


from .Engine import AiEngineConfig
from ..utills import outro


class GeminiEngine:
    def __init__(self, config: AiEngineConfig):
        self.config = config

        genai.configure(api_key=config.apiKey)
        self.client = genai.GenerativeModel()


    def generate_commit_message(self, messages: List[Dict[str, Any]]) -> Optional[str]:
        system_instruction = "\n".join(m['content'] for m in messages if m['role'] == 'system')
        gemini = self.client = genai.GenerativeModel(self.config.model, system_instruction=system_instruction)
        contents = [
            ContentDict(parts=[PartDict(text=m['content'])], role='user' if m['role'] == 'user' else 'model')
            for m in messages if m['role'] != 'system'
        ]

        attempts = 0
        while True:
            attempts += 1
            try:
                result = gemini.generate_content(
                    contents,
                    safety_settings={
                        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE
                    },
                    generation_config=GenerationConfig(
                        max_output_tokens=self.config.maxTokensOutput,
                        temperature=0,
                        top_p=0.1
                    )
                )

                return result.text
            except Exception as error:
                if ('400 API key expired. Please renew the API key.' in str(error) or '429 Resource has been exhausted (e.g. check quota)' in str(error)) and attempts < 50:
                    time.sleep(1)
                else:
                    outro(str(error), 'red')
                    exit(0)
