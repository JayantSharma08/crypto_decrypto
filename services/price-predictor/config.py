from typing import Literal, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class TrainingConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file='training.settings.env')

    # feature view to read data form both at training time and prediction time
    feature_view_name: str = Field(description='The name of the feature view')
    feature_view_version: int = Field(description='The version of the feature view')

    pair_to_predict: str = Field(description='The pair to train the model on')
    candle_seconds: int = Field(description='The number of seconds per candle')
    prediction_seconds: int = Field(
        description='The number of seconds into the future to predict'
    )
    pairs_as_features: list[str] = Field(
        description='The pairs to use for the features'
    )
    technical_indicators_as_features: list[str] = Field(
        description='The technical indicators to use for from the technical_indicators feature group'
    )
    days_back: int = Field(
        description='The number of days to consider for the historical data'
    )
    llm_model_name_news_signals: str = Field(
        description='The name of the LLM model to use for the news signals'
    )

    # hyperparameter tuning
    hyperparameter_tuning_search_trials: Optional[int] = Field(
        default=0,
        description='The number of trials to perform for hyperparameter tuning',
    )
    hyperparameter_tuning_n_splits: Optional[int] = Field(
        default=3,
        description='The number of splits to perform for hyperparameter tuning',
    )

    # model registry
    model_status: Literal['Development', 'Staging', 'Production'] = Field(
        default='Development',
        description='The status of the model in the model registry',
    )


training_config = TrainingConfig()


class InferenceConfig(BaseSettings):
    """
    Configuration for the inference job

    These are the parameters that are used to load the model from the model registry
    and to generate the predictions

    Observe how most of the parameters from the trianing job are not here. Instead,
    they are loaded from the model registry. More precisely, from the experiment run
    that generated the model artifact we load from the registry.
    """

    model_config = SettingsConfigDict(env_file='inference.settings.env')

    pair_to_predict: str = Field(description='The pair to train the model on')
    candle_seconds: int = Field(description='The number of seconds per candle')
    prediction_seconds: int = Field(
        description='The number of seconds into the future to predict'
    )
    model_status: Literal['Development', 'Staging', 'Production'] = Field(
        description='The status of the model in the model registry that we want to use for inference'
    )


inference_config = InferenceConfig()


class HopsworksCredentials(BaseSettings):
    model_config = SettingsConfigDict(env_file='hopsworks_credentials.env')
    api_key: str
    project_name: str


class CometMlCredentials(BaseSettings):
    model_config = SettingsConfigDict(env_file='comet_ml_credentials.env')
    api_key: str
    project_name: str
    workspace: str


hopsworks_credentials = HopsworksCredentials()
comet_ml_credentials = CometMlCredentials()
