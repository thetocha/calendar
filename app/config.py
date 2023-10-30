from pydantic_settings import BaseSettings, SettingsConfigDict


class DbSettings(BaseSettings):
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_pass: int

    model_config = SettingsConfigDict(env_file="../.env")


class AppSettings(BaseSettings):
    app_port: int

    model_config = SettingsConfigDict(env_file="../.env")


class PgAdminSettings(BaseSettings):
    pgadmin_email: str
    pgadmin_password: str
    pgadmin_port: int

    model_config = SettingsConfigDict(env_file="../.env")


db_settings = DbSettings()

SQLALCHEMY_DATABASE_URL = f"""postgresql://{db_settings.db_user}:{db_settings.db_pass}@{db_settings.db_host}:
                                           {db_settings.db_port}/{db_settings.db_name}"""
