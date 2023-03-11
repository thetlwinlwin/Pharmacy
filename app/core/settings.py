from pydantic import BaseSettings


class Settings(BaseSettings):
    db_hostname: str
    db_port: int
    db_password: str
    db_name: str
    db_username: str
    secret_key: str
    algorithm: str
    admin_limits: int
    access_token_expire_mins: int
    refresh_token_expire_days: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings: Settings = Settings()
