from pydantic import BaseModel

class AiEngineConfig(BaseModel):
    apiKey: str
    model: str
    maxTokensOutput: int
    maxTokensInput: int
    baseURL: str = None
