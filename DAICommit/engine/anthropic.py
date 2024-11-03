import time
from typing import Any, Dict, List, Optional

from anthropic import Anthropic

from .Engine import AiEngineConfig

from ..utills.cli import outro
from ..utills.tokenCount import token_count
from ..utills import generateCommitMessageFromGitDiff



class AnthropicEngine:
    def __init__(self, config: AiEngineConfig):
        self.config = config

        self.client = Anthropic(api_key=self.config.apiKey)

    def generate_commit_message(self, messages: List[Dict[str, Any]]) -> Optional[str]:
        system_message = next((msg['content'] for msg in messages if msg['role'] == 'system'), None)

        rest_messages = [msg for msg in messages if msg['role'] != 'system']

        try:
            request_tokens = sum(token_count(msg['content']) + 4 for msg in messages)

            if request_tokens > (self.config.maxTokensInput - self.config.maxTokensOutput):
                raise RuntimeError(generateCommitMessageFromGitDiff.GenerateCommitMessageErrorEnum.TOO_MUCH_TOKENS)

            data = self.client.messages.create(
                model=self.config.model,
                system=system_message,
                messages=rest_messages,
                temperature=0,
                top_p=0.1,
                max_tokens=self.config.maxTokensOutput
            )

            return data.content
        except Exception as error:
            outro(str(error), 'red')
            exit(0)
