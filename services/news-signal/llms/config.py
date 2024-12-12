from pydantic_settings import BaseSettings, SettingsConfigDict


class AnthropicConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file='anthropic_credentials.env')
    model_name: str = 'claude-3-5-sonnet-20240620'
    api_key: str
