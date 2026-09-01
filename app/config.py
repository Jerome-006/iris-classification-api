from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODEL_PATH: str = "ml/saved_model/model.joblib"
    MODEL_METADATA_PATH: str = "ml/saved_model/metadata.json"
    LOG_LEVEL: str = "INFO"
    MAX_BATCH_SIZE: int = 10
    API_TITLE: str = "Iris Classification API"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()