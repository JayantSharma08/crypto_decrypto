from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class TrainingConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file='training.settings.env')

    pair_to_predict: str = Field(description='The pair to train the model on')
    candle_seconds: int = Field(description='The number of seconds per candle')
    prediction_seconds: int = Field(
        description='The number of seconds into the future to predict'
    )
    pairs_as_features: list[str] = Field(
        description='The pairs to use for the features'
    )
    days_back: int = Field(
        description='The number of days to consider for the historical data'
    )


training_config = TrainingConfig()


class HopsworksCredentials(BaseSettings):
    model_config = SettingsConfigDict(env_file='hopsworks_credentials.env')
    hopsworks_api_key: str
    hopsworks_project_name: str


hopsworks_credentials = HopsworksCredentials()
