from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_host: str = "localhost"
    db_port: int = 3306
    db_name: str = "hr_gestion"
    db_user: str = "hruser"
    db_password: str = "hrpass"

    jwt_secret: str = "change_this_secret_in_production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 480  # 8h

    training_service_url: str = "http://training-service:5000"

    class Config:
        env_file = ".env"

    @property
    def database_url(self) -> str:
        return (
            f"mysql+pymysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


settings = Settings()
