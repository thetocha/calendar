from pydantic_settings import BaseSettings


class DbSettings(BaseSettings):
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_pass: int

    @property
    def db_url(self):
        return f"""postgresql://{self.db_user}:{self.db_pass}@{self.db_host}:
                                               {self.db_port}/{self.db_name}"""


class AppSettings(BaseSettings):
    app_port: int


class JWTSettings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


db_settings = DbSettings()
jwt_settings = JWTSettings()
