from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Postgres settings
    db_name: str
    db_url: str 
    admin_db_url: str 

    class Config:
        env_file = ".env"

