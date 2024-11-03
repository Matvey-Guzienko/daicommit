from ..engine.Engine import AiEngineConfig
from ..engine.anthropic import AnthropicEngine
from ..engine.gemini import GeminiEngine
from ..engine.openAi import OpenAiEngine

from .config import AiProviderEnum, get_config


def get_engine():
    global_config = get_config()
    provider = global_config['AI_PROVIDER']

    default_config = {
        'model': global_config['MODEL'],
        'maxTokensOutput': global_config['MAX_TOKENS_OUTPUT'],
        'maxTokensInput': global_config['TOKENS_MAX_INPUT'],
        'baseURL': global_config['API_URL'],
        'apiKey': global_config['API_KEY']
    }

    if provider == AiProviderEnum.ANTHROPIC.value:
        return AnthropicEngine(AiEngineConfig(**default_config))
    elif provider == AiProviderEnum.GEMINI.value:
        return GeminiEngine(AiEngineConfig(**default_config))
    else:
        return OpenAiEngine(AiEngineConfig(**default_config))
