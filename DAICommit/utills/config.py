import json
import os
from enum import Enum

defaultConfigPath = os.path.join(os.path.expanduser("~"), ".aicommit")

DEFAULT_SETTINGS = {
    "AI_PROVIDER": "openai",
    "API_KEY": "any",
    "API_URL": "https://api.openai.com/v1/",
    "TOKENS_MAX_INPUT": 40960,
    "MAX_TOKENS_OUTPUT": 4096,
    "EMOJI": False,
    "MODEL": "gpt-3.5-turbo",
    "LANGUAGE": "en",
    "ONE_LINE_COMMIT": False,
    "DESCRIPTION": True
}

MODEL_LIST = {
    'openai': [
        'gpt-4o-mini',
        'gpt-3.5-turbo',
        'gpt-3.5-turbo-instruct',
        'gpt-3.5-turbo-0613',
        'gpt-3.5-turbo-0301',
        'gpt-3.5-turbo-1106',
        'gpt-3.5-turbo-0125',
        'gpt-3.5-turbo-16k',
        'gpt-3.5-turbo-16k-0613',
        'gpt-3.5-turbo-16k-0301',
        'gpt-4',
        'gpt-4-0314',
        'gpt-4-0613',
        'gpt-4-1106-preview',
        'gpt-4-0125-preview',
        'gpt-4-turbo-preview',
        'gpt-4-vision-preview',
        'gpt-4-1106-vision-preview',
        'gpt-4-turbo',
        'gpt-4-turbo-2024-04-09',
        'gpt-4-32k',
        'gpt-4-32k-0314',
        'gpt-4-32k-0613',
        'gpt-4o',
        'gpt-4o-2024-05-13',
        'gpt-4o-mini-2024-07-18'
    ],
    'anthropic': [
        'claude-3-5-sonnet-20240620',
        'claude-3-opus-20240229',
        'claude-3-sonnet-20240229',
        'claude-3-haiku-20240307'
    ],
    'gemini': [
        'gemini-1.5-flash',
        'gemini-1.5-pro',
        'gemini-1.0-pro',
        'gemini-pro-vision',
        'text-embedding-004'
    ],
}

class DefaultTokenLimits:
    DEFAULT_MAX_TOKENS_INPUT = 40960
    DEFAULT_MAX_TOKENS_OUTPUT = 4096

class AiProviderEnum(Enum):
    OPENAI = 'openai'
    ANTHROPIC = 'anthropic'
    GEMINI = 'gemini'

def set_config_value(key, value):
    config = DEFAULT_SETTINGS.copy()

    if os.path.exists(defaultConfigPath):
        try:
            with open(defaultConfigPath, 'r') as file:
                config = json.load(file)

                for setting in DEFAULT_SETTINGS:
                    if setting not in config:
                        config[setting] = DEFAULT_SETTINGS[setting]
        except (json.JSONDecodeError, IOError):
            config = DEFAULT_SETTINGS.copy()

    config[key] = value
    with open(defaultConfigPath, 'w') as file:
        json.dump(config, file, indent=4)


def get_config_value(key):
    config = DEFAULT_SETTINGS.copy()

    if os.path.exists(defaultConfigPath):
        try:
            with open(defaultConfigPath, 'r') as file:
                config = json.load(file)

                for setting in DEFAULT_SETTINGS:
                    if setting not in config:
                        config[setting] = DEFAULT_SETTINGS[setting]
        except (json.JSONDecodeError, IOError):
            pass

    return config.get(key, DEFAULT_SETTINGS.get(key))

def get_config():
    config = DEFAULT_SETTINGS.copy()

    if os.path.exists(defaultConfigPath):
        try:
            with open(defaultConfigPath, 'r') as file:
                config = json.load(file)
        except (json.JSONDecodeError, IOError):
            config = DEFAULT_SETTINGS.copy()

    return config
