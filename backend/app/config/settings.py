from pydantic_settings import BaseSettings
from sqlalchemy.engine import URL

class Settings(BaseSettings):

    database_url: URL = URL.create(
        drivername="postgresql+asyncpg",
        username="endeavor",
        password="Ende@vor1990$",
        host="localhost",
        database="endeavor",
        port=5432
    )
    
    echo_sql: bool = False
    test: bool = False
    title: str = "Endeavor"
    description:str = "Voyager 3.0"
    oauth_token_secret: str = "my_dev_secret"

settings = Settings()