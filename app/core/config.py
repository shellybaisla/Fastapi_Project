from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env",extra="ignore")

    DB_CONNECTION:str
    SECRET_KEY : str
    ALGORITHM : str
    EXP_TIME : int

settings = Settings()

#Basesetting ek special pydantic class hai jo hume environment variables ko  extract karne me help krti hai.
