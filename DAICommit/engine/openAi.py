
from typing import Any, Dict, List, Optional

from openai import OpenAI

from .Engine import AiEngineConfig
from ..utills.cli import outro
from ..utills.tokenCount import token_count
from ..utills import generateCommitMessageFromGitDiff


class OpenAiEngine:
    def __init__(self, config: AiEngineConfig):
        self.config = config

        if config.baseURL == '':
            self.client = OpenAI(api_key=config.apiKey)
        else:
            self.client = OpenAI(api_key=config.apiKey, base_url=config.baseURL)

    def generate_commit_message(self, messages: List[Dict[str, Any]]) -> Optional[str]:
        params = {
            "model": self.config.model,
            "messages": messages,
            "temperature": 0,
            "top_p": 0.1,
            "max_tokens": self.config.maxTokensOutput
        }

        try:
            request_tokens = sum(token_count(msg['content']) + 4 for msg in messages)

            if request_tokens > self.config.maxTokensInput - self.config.maxTokensOutput:
                raise RuntimeError(generateCommitMessageFromGitDiff.GenerateCommitMessageErrorEnum.TOO_MUCH_TOKENS)

            completion = self.client.chat.completions.create(**params)

            message = completion.choices[0].message
            return message.content
        except Exception as error:
            outro(str(error), 'red')
            exit(0)
